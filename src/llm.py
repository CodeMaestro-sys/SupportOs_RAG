import hashlib
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from google.genai import types

CACHE_PATH = Path("data/llm_cache.db")


class LLM:
    """Gemini calls with a disk cache, rate limiting and retries."""

    def __init__(self, model=None, cache_path=CACHE_PATH, min_interval=6.0):
        self.model = model or os.environ["GEMINI_MODEL"]
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.min_interval = min_interval            # seconds between real calls; see note below
        self._last = 0.0
        self.calls = 0
        self.cache_hits = 0
        self.db = sqlite3.connect(cache_path)
        self.db.execute("CREATE TABLE IF NOT EXISTS llm_cache "
                        "(key TEXT PRIMARY KEY, model TEXT, prompt TEXT, response TEXT, created TEXT)")

    def _key(self, prompt, system):
        raw = "\x1f".join([self.model, system or "", prompt])
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def generate(self, prompt, system=None):
        key = self._key(prompt, system)
        row = self.db.execute("SELECT response FROM llm_cache WHERE key = ?", (key,)).fetchone()
        if row:
            self.cache_hits += 1
            return row[0]

        text = ""
        for attempt in range(6):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            try:
                resp = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, system_instruction=system),
                )
                text = resp.text or ""
                break
            except Exception as e:
                code = getattr(e, "code", None)
                if code in (429, 500, 503) and attempt < 5:      # busy or rate limited: wait and retry
                    time.sleep(min(60, 5 * 2 ** attempt))
                    continue
                raise

        self.calls += 1
        if text:                                                  # never cache an empty answer
            self.db.execute("INSERT OR REPLACE INTO llm_cache VALUES (?, ?, ?, ?, ?)",
                            (key, self.model, prompt, text, datetime.now(timezone.utc).isoformat()))
            self.db.commit()
        return text