## Draft 1
**Customer:** I don't want purchase ORD-87590

**Sentences:**
1. Hello!
2. You can cancel an order at any time before it is dispatched [2].
3. To cancel online, sign in to the ShopEase customer portal, open **My Orders**, select the order, click **Cancel Order**, choose a reason, and confirm [2].
4. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number [4].

**Passages shown to the model:**
[1] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.
[2] (cancel-order) Cancelling an order. You can cancel an order at any time before it is dispatched.

**How to cancel**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Cancel Order**.
3. Choose a reason and confirm.
[3] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.
[4] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.

---

## Draft 2
**Customer:** want help canceling purchase ORD-20607

**Sentences:**
1. Hello!
2. You can cancel your order at any time before it is dispatched [2].
3. To cancel, sign in to the ShopEase customer portal and open **My Orders**, select your order, click **Cancel Order**, choose a reason, and confirm [2].
4. If you cannot cancel online, you can contact customer support at +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number [1].
5. If the order is already dispatched, cancellation is no longer possible, but you can refuse the delivery or return the items within 30 days under the refund policy [3].

**Passages shown to the model:**
[1] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[2] (cancel-order) Cancelling an order. You can cancel an order at any time before it is dispatched.

**How to cancel**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Cancel Order**.
3. Choose a reason and confirm.
[3] (cancel-order) Cancelling an order. **If the order is already dispatched**
Cancellation is no longer possible, and **Cancel Order** is not shown. You can refuse the delivery or return the items within 30 days under the refund policy.
[4] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.

---

## Draft 3
**Customer:** modifying purchase ORD-76074

**Sentences:**
1. You can change an order until it is dispatched [4].
2. Once the order status shows **Dispatched**, it can no longer be changed [4].
3. You can change the item size or colour, quantity, delivery address, or delivery option where the new option is available [4].
4. If **Change Order** is not shown for your order, or the change you need is not listed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number [3].
5. Customer support can help with the rest of your request.

**Passages shown to the model:**
[1] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[2] (change-order) Changing an order. **Timing:** orders placed before 12 PM on a business day are dispatched the same day, so make changes as soon as possible after ordering.

**If the order is already dispatched**
You cannot change it. Once it is delivered, you can return items within 30 days under the refund policy.
[3] (change-order) Changing an order. If **Change Order** is not shown for your order, or the change you need is not listed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[4] (change-order) Changing an order. You can change an order until it is dispatched. Once the order status shows **Dispatched**, it can no longer be changed.

**What you can change**
- Item size or colour
- Quantity
- Delivery address
- Delivery option, where the new option is available

---

## Draft 4
**Customer:** i cant correct purchase ORD-49437

**Sentences:**
1. Hello!
2. If the change you need is not listed, or if the option is not shown for your order, please contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number [2].
3. Customer support can help with the rest of your request.

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Corrections**
If the name or address on an invoice is wrong, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with the invoice number. A corrected invoice is issued within 3 business days.
[2] (change-order) Changing an order. If **Change Order** is not shown for your order, or the change you need is not listed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[3] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[4] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.

---

## Draft 5
**Customer:** is it possible to locate the bill #37777?

**Sentences:**
1. To find your bill, open Account Settings and select Billing History, then choose a date range to list all invoices in that period [1].
2. You can click an invoice to see its details or download it [1].
3. An invoice is also emailed to your registered address when the order is dispatched [2].
4. If the invoice is missing after dispatch, check your spam folder and then contact customer support [3].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.
[2] (invoices) Checking and downloading invoices. An invoice is created for every order when it is dispatched. Invoice numbers look like INV-12345. We also email the invoice to your registered address.
[3] (invoices) Checking and downloading invoices. **If an invoice is missing**
The invoice appears after dispatch. If your order has been dispatched and there is still no invoice, check your spam folder, then contact customer support.
[4] (invoices) Checking and downloading invoices. **Corrections**
If the name or address on an invoice is wrong, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with the invoice number. A corrected invoice is issued within 3 business days.

---

## Draft 6
**Customer:** how to list your allowed payment methods?

**Sentences:**
1. ShopEase accepts credit and debit cards (Visa, Mastercard, and RuPay), UPI, net banking, and cash on delivery for standard delivery orders up to ₹5,000 [1].
2. The specific payment methods available for your order will be shown at checkout before you place the order [2][3].

**Passages shown to the model:**
[1] (payment-methods) Accepted payment methods. ShopEase accepts the following payment methods. All prices are in rupees (₹).

- **Credit and debit cards:** Visa, Mastercard and RuPay.
- **UPI:** pay from any UPI app using your UPI ID or a QR code.
- **Net banking:** supported for major Indian banks.
- **Cash on delivery:** available for standard delivery orders up to ₹5,000.
[2] (payment-methods) Accepted payment methods. The methods you can use are shown at checkout, before you place the order.

**Saved payment methods**
You can save a card for faster checkout. Go to **Account Settings**, then **Payment Methods**, to view or remove saved cards. We never store your full card number or security code.
[3] (payment-methods) Accepted payment methods. If a payment method is not shown at checkout, it may not be available for your order. Try another method, or contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (payment-methods) Accepted payment methods. **Security**
Payments are encrypted. ShopEase will never ask you for your card PIN, a one-time password or your full card number by phone, email or chat.

---

## Draft 7
**Customer:** can uhelp me check the bloody allowed paymentmethods

**Sentences:**
1. ShopEase accepts the following payment methods: credit and debit cards (Visa, Mastercard, and RuPay), UPI (using any UPI app or QR code), net banking for major Indian banks, and cash on delivery for standard delivery orders up to ₹5,000 [1].
2. All prices are in rupees (₹) [1].
3. If a payment method is not shown at checkout, it may not be available for your order, and you can try another method or contact customer support [4].

**Passages shown to the model:**
[1] (payment-methods) Accepted payment methods. ShopEase accepts the following payment methods. All prices are in rupees (₹).

- **Credit and debit cards:** Visa, Mastercard and RuPay.
- **UPI:** pay from any UPI app using your UPI ID or a QR code.
- **Net banking:** supported for major Indian banks.
- **Cash on delivery:** available for standard delivery orders up to ₹5,000.
[2] (payment-methods) Accepted payment methods. **Security**
Payments are encrypted. ShopEase will never ask you for your card PIN, a one-time password or your full card number by phone, email or chat.
[3] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.
[4] (payment-methods) Accepted payment methods. If a payment method is not shown at checkout, it may not be available for your order. Try another method, or contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 8
**Customer:** I try to check in what cases can I request my money back

**Sentences:**
1. You can request a refund for duplicate or unauthorized charges, damaged or defective items, and orders that did not arrive [4].
2. To request a refund, sign in to the ShopEase customer portal and open **My Orders**, select the order, and click **Return or Refund** [2].
3. Then, choose the item and the reason, and submit the request [2].
4. Customer support can help with the rest.

**Passages shown to the model:**
[1] (refund-tracking) Tracking a refund. **Refund statuses**
- **Requested:** we have received your request.
- **Approved:** the refund has been approved. You receive an email with your refund reference (it starts with REF).
- **Processing:** the money is being sent to your original payment method.
- **Completed:** the refund has been sent.
[2] (refund-policy) Refund policy. **How to request a refund**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Return or Refund**.
3. Choose the item and the reason, and submit the request.
[3] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[4] (refund-policy) Refund policy. We email you once the request is approved. For returns, approval happens after we receive and check the item.

**Refund time**
Refunds go back to your original payment method within 5 to 7 business days. For returns, this starts when the refund is approved. For cancelled orders, it starts on the day of cancellation. The same timeline applies to refunds for duplicate or unauthorized charges, damaged or defective items, and orders that did not arrive.

---

## Draft 9
**Customer:** I have got to file a bloody reclamation, will you help me?

**Sentences:**
1. To request a refund, sign in to the ShopEase customer portal and open **My Orders**, select the order and click **Return or Refund**, then choose the item and the reason to submit the request [3].
2. For other complaints, if you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent [1].
3. Customer support can help with the rest.

**Passages shown to the model:**
[1] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[2] (refund-policy) Refund policy. For questions about a refund, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (refund-policy) Refund policy. **How to request a refund**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Return or Refund**.
3. Choose the item and the reason, and submit the request.
[4] (payment-problems) Payment problems. **Duplicate or unauthorized charges**
If you see the same payment twice, or a payment you did not make, contact customer support immediately on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Tell us the order number, the date and amount of the payment, and the last four digits of the card or the UPI transaction ID. Once confirmed, the amount is refunded within 5 to 7 business days.

---

## Draft 10
**Customer:** i have got to file a customer claim

**Sentences:**
1. To file a complaint, you can sign in to the ShopEase customer portal, go to **My Orders**, select the order, and choose **Report a problem** [3].
2. Alternatively, you can contact customer support by calling +91 00000 00000, emailing support@shopease.example, or using the live chat on www.shopease.example (Monday to Friday, 9 AM to 6 PM) [3].
3. Please include your order number, a short description of what happened, and photos if an item was damaged or wrong [2].

**Passages shown to the model:**
[1] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[2] (complaints) Making a complaint. Please include your order number, a short description of what happened, and photos if an item was damaged or wrong.

**What happens next**
- We confirm that we have received your complaint within 1 business day.
- A support agent looks into the issue and contacts you with an outcome within 3 business days.
- Depending on the problem, the outcome can be a replacement, a refund, or a correction to your order. Refunds follow the timelines in the refund policy (5 to 7 business days).
[3] (complaints) Making a complaint. If something went wrong with your order, delivery, payment or support experience, you can make a complaint at any time.

**How to complain**
1. Sign in to the ShopEase customer portal, go to **My Orders**, select the order and choose **Report a problem**.
2. Or contact customer support: +91 00000 00000, support@shopease.example, or live chat on www.shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (payment-problems) Payment problems. **Duplicate or unauthorized charges**
If you see the same payment twice, or a payment you did not make, contact customer support immediately on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Tell us the order number, the date and amount of the payment, and the last four digits of the card or the UPI transaction ID. Once confirmed, the amount is refunded within 5 to 7 business days.

---

## Draft 11
**Customer:** I have to speak with customer assistance

**Sentences:**
1. If you prefer to speak to a human agent instead of using the automated help, you can use the phone line at +91 00000 00000 or select the "Talk to an agent" option in live chat on www.shopease.example [1][2].
2. Support hours are Monday to Friday, 9 AM to 6 PM [3].

**Passages shown to the model:**
[1] (contact-support) Contacting ShopEase customer support. If you prefer to speak to a human agent instead of using the automated help, use the phone line or the "Talk to an agent" option in live chat. The ShopEase customer portal also has a Help Center with answers to common questions, available at any time.
[2] (contact-support) Contacting ShopEase customer support. ShopEase customer support can be reached in three ways:

- **Phone:** +91 00000 00000. Your call goes directly to a support agent.
- **Email:** support@shopease.example. We reply within 1 business day.
- **Live chat:** available on www.shopease.example. Choose "Talk to an agent" to be connected to a person.
[3] (contact-support) Contacting ShopEase customer support. Support hours are Monday to Friday, 9 AM to 6 PM. Messages sent outside these hours are answered on the next business day.

To help us find your case quickly, have your order number (for example ORD-12345) or your registered email address ready. If your question is about an invoice, also include the invoice number.
[4] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.

---

## Draft 12
**Customer:** I need to see what hours I can call customer service

**Sentences:**
1. Support hours are Monday to Friday, 9 AM to 6 PM [1][2][3][4].

**Passages shown to the model:**
[1] (contact-support) Contacting ShopEase customer support. Support hours are Monday to Friday, 9 AM to 6 PM. Messages sent outside these hours are answered on the next business day.

To help us find your case quickly, have your order number (for example ORD-12345) or your registered email address ready. If your question is about an invoice, also include the invoice number.
[2] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[3] (change-order) Changing an order. If **Change Order** is not shown for your order, or the change you need is not listed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[4] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 13
**Customer:** I need assistance to contact somebody

**Sentences:**
1. Hello!
2. You can reach ShopEase customer support in three ways: by phone at +91 00000 00000, by email at support@shopease.example, or via live chat on www.shopease.example by choosing the "Talk to an agent" option [1][2].
3. Support hours are Monday to Friday, 9 AM to 6 PM, and messages sent outside these hours are answered on the next business day [4].
4. To help us find your case quickly, please have your order number or registered email address ready [4].
5. Let us know if you need help with anything else!

**Passages shown to the model:**
[1] (contact-support) Contacting ShopEase customer support. If you prefer to speak to a human agent instead of using the automated help, use the phone line or the "Talk to an agent" option in live chat. The ShopEase customer portal also has a Help Center with answers to common questions, available at any time.
[2] (contact-support) Contacting ShopEase customer support. ShopEase customer support can be reached in three ways:

- **Phone:** +91 00000 00000. Your call goes directly to a support agent.
- **Email:** support@shopease.example. We reply within 1 business day.
- **Live chat:** available on www.shopease.example. Choose "Talk to an agent" to be connected to a person.
[3] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[4] (contact-support) Contacting ShopEase customer support. Support hours are Monday to Friday, 9 AM to 6 PM. Messages sent outside these hours are answered on the next business day.

To help us find your case quickly, have your order number (for example ORD-12345) or your registered email address ready. If your question is about an invoice, also include the invoice number.

---

## Draft 14
**Customer:** I have to contact an assistant

**Sentences:**
1. If you prefer to speak to a human agent instead of using the automated help, you can use the phone line or select the "Talk to an agent" option in live chat [2].
2. Support hours are Monday to Friday, from 9 AM to 6 PM [3].
3. To help us find your case quickly, please have your order number or registered email address ready, and include the invoice number if your question is about an invoice [3].

**Passages shown to the model:**
[1] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[2] (contact-support) Contacting ShopEase customer support. If you prefer to speak to a human agent instead of using the automated help, use the phone line or the "Talk to an agent" option in live chat. The ShopEase customer portal also has a Help Center with answers to common questions, available at any time.
[3] (contact-support) Contacting ShopEase customer support. Support hours are Monday to Friday, 9 AM to 6 PM. Messages sent outside these hours are answered on the next business day.

To help us find your case quickly, have your order number (for example ORD-12345) or your registered email address ready. If your question is about an invoice, also include the invoice number.
[4] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 15
**Customer:** i need assistance to create a standard account

**Sentences:**
1. Creating a ShopEase account is free and takes about two minutes [2].
2. Here are the steps to create an account:
3. Go to www.shopease.example and click **Sign up** [2].
4. Enter your full name, email address, mobile number and a password [2]. (Your password must be at least 8 characters and include a letter and a number [1].)
5. Click **Create account**, and we will send a verification email [2].
6. Open the email and click the verification link, which is valid for 24 hours [2].
7. If you need any further assistance, customer support can help [3].

**Passages shown to the model:**
[1] (create-account) Creating a ShopEase account and fixing sign-up problems. Your password must be at least 8 characters and include a letter and a number.

**Sign-up problems**
- **No verification email:** check your spam folder and wait 10 minutes, then choose **Resend email** on the login page.
- **Link expired:** the link works for 24 hours. Request a new one from the login page.
- **"Email already registered":** you already have an account. Use **Forgot Password** on the login page to get back in.
- **Still stuck:** contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used.
[2] (create-account) Creating a ShopEase account and fixing sign-up problems. Creating a ShopEase account is free and takes about two minutes.

**How to create an account**
1. Go to www.shopease.example and click **Sign up**.
2. Enter your full name, email address, mobile number and a password.
3. Click **Create account**. We send a verification email.
4. Open the email and click the verification link. The link is valid for 24 hours.
[3] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.
[4] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 16
**Customer:** I need assistance to delete the standard account

**Sentences:**
1. Hello!
2. You can ask to delete your ShopEase account at any time [4].
3. To delete your account, sign in to the ShopEase customer portal, open Account Settings, and choose Delete Account [2].
4. Select a reason (optional) and enter your password to confirm [2].
5. Please note that orders still being processed or delivered must be completed or cancelled first, and you should download any invoices you need beforehand [4].
6. Your account is closed within 7 days, during which you can cancel the request by signing in again [3].
7. If you cannot sign in, you can contact customer support on +91 00000 00000 or support@shopease.example from Monday to Friday, 9 AM to 6 PM [1].

**Passages shown to the model:**
[1] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.
[2] (delete-account) Deleting your account. **How to delete your account**
1. Sign in to the ShopEase customer portal.
2. Open **Account Settings** and choose **Delete Account**.
3. Select a reason (optional) and enter your password to confirm.
[3] (delete-account) Deleting your account. **What happens next**
Your account is closed within 7 days. During these 7 days you can change your mind: sign in again and your deletion request is cancelled. After 7 days, your profile, saved addresses and saved payment methods are permanently removed.
[4] (delete-account) Deleting your account. You can ask to delete your ShopEase account at any time.

**Before you delete**
- Orders that are still being processed or delivered must be completed or cancelled first.
- Download any invoices you need. After deletion, your order history and invoices cannot be recovered.

---

## Draft 17
**Customer:** I want help to check what options for delivery you offer

**Sentences:**
1. To see what delivery options are available for you, enter your PIN code at checkout [1].
2. Customer support can help with the rest.

**Passages shown to the model:**
[1] (delivery-options) Delivery options. Which options you see depends on your delivery address and the items in your cart. Enter your PIN code at checkout to see what is available for you.
[2] (delivery-options) Delivery options. Delivery times are counted from the day your order is dispatched. See the delivery times guide for details.

To change the delivery option of an order that is not yet dispatched, open **My Orders**, select the order and click **Change Order**. For help, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (change-order) Changing an order. You can change an order until it is dispatched. Once the order status shows **Dispatched**, it can no longer be changed.

**What you can change**
- Item size or colour
- Quantity
- Delivery address
- Delivery option, where the new option is available
[4] (payment-methods) Accepted payment methods. If a payment method is not shown at checkout, it may not be available for your order. Try another method, or contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 18
**Customer:** is it possible to place an order from Delhi

**Sentences:**
1. Yes, you can place an order from Delhi [1][3].
2. ShopEase delivers within India [1], and same-day delivery is available in Delhi for orders placed before 12 PM on a business day [2].
3. To place an order, you need a ShopEase account, which you can create for free on www.shopease.example [3].

**Passages shown to the model:**
[1] (shipping-address) Setting up and changing delivery addresses. You can save several addresses and choose between them when you place an order. We deliver within India.

**Change the address on an existing order**
- If the order has not been dispatched, open **My Orders**, select the order and click **Change Order**, then update the delivery address.
- If the order is already dispatched, the address cannot be changed online. Contact customer support straight away on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number. We will ask the delivery partner to redirect the parcel, but we cannot guarantee that this is possible.
[2] (delivery-options) Delivery options. ShopEase offers four ways to receive your order. Available options and their prices are shown at checkout, before you pay.

- **Standard delivery:** 4 to 6 business days.
- **Express delivery:** 1 to 2 business days.
- **Same-day delivery:** available in Delhi, Mumbai, Pune and Chennai for orders placed before 12 PM on a business day.
- **Store pickup:** collect your order from our store at 12 MG Road, Pune. Your order is ready for collection within 2 hours of confirmation, and we email you when it is ready. Bring your order number and a photo ID.
[3] (place-order) Placing an order. To place an order you need a ShopEase account. You can create one for free on www.shopease.example.

**Steps**
1. Add items to your cart and click **Checkout**.
2. Confirm or choose your delivery address.
3. Select a delivery option: standard, express, same-day (where available) or store pickup.
4. Choose a payment method and click **Place Order**.
[4] (change-order) Changing an order. You can change an order until it is dispatched. Once the order status shows **Dispatched**, it can no longer be changed.

**What you can change**
- Item size or colour
- Quantity
- Delivery address
- Delivery option, where the new option is available

---

## Draft 19
**Customer:** I want help to check how soon can I expect my package

**Sentences:**
1. Hello!
2. The estimated delivery date for your order is shown on the order page and in your dispatch email [1].
3. If your order has not arrived by the estimated date, check Track Order first [2].

**Passages shown to the model:**
[1] (track-order) Tracking an order. The estimated delivery date is shown on the order page and in your dispatch email.

If there is no update for 48 hours, or the order has not arrived by the estimated date, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number.
[2] (delivery-times) How long delivery takes. **If your order is late**
If your order has not arrived by the estimated delivery date, check **Track Order** first. If there is no update, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[3] (track-order) Tracking an order. When the order is dispatched, we email you a tracking number (it starts with TRK). It can take up to 24 hours after dispatch for tracking updates to appear.
[4] (invoices) Checking and downloading invoices. **If an invoice is missing**
The invoice appears after dispatch. If your order has been dispatched and there is still no invoice, check your spam folder, then contact customer support.

---

## Draft 20
**Customer:** I don't know how to see how soon ca I expect my article

**Sentences:**
1. The estimated delivery date is shown on the order page and in your dispatch email [1].
2. When your order is dispatched, we email you a tracking number starting with TRK [2].
3. It can take up to 24 hours after dispatch for tracking updates to appear [2].

**Passages shown to the model:**
[1] (track-order) Tracking an order. The estimated delivery date is shown on the order page and in your dispatch email.

If there is no update for 48 hours, or the order has not arrived by the estimated date, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number.
[2] (track-order) Tracking an order. When the order is dispatched, we email you a tracking number (it starts with TRK). It can take up to 24 hours after dispatch for tracking updates to appear.
[3] (track-order) Tracking an order. **Order statuses**
- **Order Placed:** we have received your order.
- **Packed:** your items are ready to go.
- **Dispatched:** the order has been handed to our delivery partner, SwiftShip.
- **Out for Delivery:** the delivery agent is on the way.
- **Delivered:** the order has arrived.
[4] (delivery-times) How long delivery takes. **If your order is late**
If your order has not arrived by the estimated delivery date, check **Track Order** first. If there is no update, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.

---

## Draft 21
**Customer:** correct information on Basic account

**Sentences:**
1. If the name or address on an invoice is wrong, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with the invoice number [3].
2. A corrected invoice is issued within 3 business days [3].
3. If you need to edit other account details that cannot be edited online, you can also reach customer support using the same contact details [2].
4. Customer support can help with the rest of your request.

**Passages shown to the model:**
[1] (edit-account) Editing your account details. **Changing your email address:** we send a 6-digit verification code to the new address. Your email only changes after you enter the code. Order updates and invoices go to the new address from then on.
[2] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (invoices) Checking and downloading invoices. **Corrections**
If the name or address on an invoice is wrong, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with the invoice number. A corrected invoice is issued within 3 business days.
[4] (create-account) Creating a ShopEase account and fixing sign-up problems. Your password must be at least 8 characters and include a letter and a number.

**Sign-up problems**
- **No verification email:** check your spam folder and wait 10 minutes, then choose **Resend email** on the login page.
- **Link expired:** the link works for 24 hours. Request a new one from the login page.
- **"Email already registered":** you already have an account. Use **Forgot Password** on the login page to get back in.
- **Still stuck:** contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used.

---

## Draft 22
**Customer:** edit information on standard account

**Sentences:**
1. Hello!
2. You can update your personal details at any time in the ShopEase customer portal [2].
3. Here are the steps to edit your details:
4. Sign in to the ShopEase customer portal [2].
5. Open **Account Settings** and select **Profile** [2].
6. Change your name, mobile number or email address [2].
7. Click **Save** [2].
8. Changes apply immediately [2].
9. If you are changing your email address, a 6-digit verification code will be sent to the new address, and the email only changes after you enter this code [3].
10. If a detail cannot be edited online, please contact customer support [1].

**Passages shown to the model:**
[1] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[2] (edit-account) Editing your account details. You can update your personal details at any time in the ShopEase customer portal.

**How to edit your details**
1. Sign in to the ShopEase customer portal.
2. Open **Account Settings** and select **Profile**.
3. Change your name, mobile number or email address.
4. Click **Save**. Changes apply immediately.
[3] (edit-account) Editing your account details. **Changing your email address:** we send a 6-digit verification code to the new address. Your email only changes after you enter the code. Order updates and invoices go to the new address from then on.
[4] (edit-account) Editing your account details. **Changing your password:** go to **Account Settings**, then **Password and Security**.

**Delivery addresses:** these are managed separately under **Saved Addresses** in Account Settings (see the shipping address guide).

---

## Draft 23
**Customer:** i cannot find bill #85632 can usendit to me

**Sentences:**
1. To check or find invoices over a specific period, open **Account Settings** and select **Billing History** [1].
2. Then, choose a date range to see all listed invoices with their invoice number, order number, date, and amount in ₹, and click an invoice to view its details or download it [1].
3. Customer support can help with the rest.

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.
[2] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.
[3] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[4] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.

---

## Draft 24
**Customer:** I don't know what to do to download the invoice #85632

**Sentences:**
1. To download the invoice for your order, sign in to the ShopEase customer portal and open **My Orders** [2].
2. Select the order and click **Download Invoice** to save it as a PDF [2].
3. Invoices appear after dispatch [1].
4. If your order has been dispatched and the invoice is missing, please check your spam folder and then contact customer support [1].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **If an invoice is missing**
The invoice appears after dispatch. If your order has been dispatched and there is still no invoice, check your spam folder, then contact customer support.
[2] (invoices) Checking and downloading invoices. **Download an invoice for one order**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Download Invoice**. The invoice is saved as a PDF.
[3] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.
[4] (invoices) Checking and downloading invoices. An invoice is created for every order when it is dispatched. Invoice numbers look like INV-12345. We also email the invoice to your registered address.

---

## Draft 25
**Customer:** can you help me to request a reimbursement of money?

**Sentences:**
1. To request a refund, sign in to the ShopEase customer portal and open **My Orders** [2].
2. Select the order and click **Return or Refund**, then choose the item and the reason, and submit the request [2].
3. For questions about a refund, you can contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [3].
4. Customer support can help with the rest.

**Passages shown to the model:**
[1] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[2] (refund-policy) Refund policy. **How to request a refund**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Return or Refund**.
3. Choose the item and the reason, and submit the request.
[3] (refund-policy) Refund policy. For questions about a refund, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (payment-problems) Payment problems. **Duplicate or unauthorized charges**
If you see the same payment twice, or a payment you did not make, contact customer support immediately on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Tell us the order number, the date and amount of the payment, and the last four digits of the card or the UPI transaction ID. Once confirmed, the amount is refunded within 5 to 7 business days.

---

## Draft 26
**Customer:** want assistance to obtain a restitution of money

**Sentences:**
1. To request a refund, sign in to the ShopEase customer portal and open **My Orders**, select the order and click **Return or Refund**, then choose the item and the reason, and submit the request [4].
2. For questions about a refund, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [2].

**Passages shown to the model:**
[1] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[2] (refund-policy) Refund policy. For questions about a refund, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (refund-tracking) Tracking a refund. **If you have not received your refund**
If it has been more than 7 business days, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Please share your order number and refund reference.
[4] (refund-policy) Refund policy. **How to request a refund**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Return or Refund**.
3. Choose the item and the reason, and submit the request.

---

## Draft 27
**Customer:** i try to report an payment error

**Sentences:**
1. To report a payment error or make a complaint, you can sign in to the ShopEase customer portal, go to **My Orders**, select the order, and choose **Report a problem** [3].
2. Alternatively, you can contact customer support via phone at +91 00000 00000, email at support@shopease.example, or live chat on www.shopease.example, available Monday to Friday from 9 AM to 6 PM [3].
3. If your payment failed, please check your card details, balance or limit, and your internet connection, or try another payment method like UPI or net banking [1].
4. You can also wait a few minutes before trying again, as a processing payment can sometimes look like a failure [1].

**Passages shown to the model:**
[1] (payment-problems) Payment problems. **Payment failed**
- Check your card details, balance or limit, and your internet connection.
- Try another payment method such as UPI or net banking.
- Wait a few minutes before trying again, because a payment that is still processing can look as if it failed.
[2] (payment-problems) Payment problems. **Duplicate or unauthorized charges**
If you see the same payment twice, or a payment you did not make, contact customer support immediately on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Tell us the order number, the date and amount of the payment, and the last four digits of the card or the UPI transaction ID. Once confirmed, the amount is refunded within 5 to 7 business days.
[3] (complaints) Making a complaint. If something went wrong with your order, delivery, payment or support experience, you can make a complaint at any time.

**How to complain**
1. Sign in to the ShopEase customer portal, go to **My Orders**, select the order and choose **Report a problem**.
2. Or contact customer support: +91 00000 00000, support@shopease.example, or live chat on www.shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.

---

## Draft 28
**Customer:** i have to retrieve the key of my user how do i do it

**Sentences:**
1. To recover your password, go to the login page on www.shopease.example and click **Forgot Password** [1].
2. Then, enter your registered email address [1].
3. Open the email we send you, click the reset link (valid for 30 minutes), and choose a new password with at least 8 characters, including a letter and a number [1].
4. If the email does not arrive, check your spam folder, wait a few minutes, and make sure you typed the same email address you registered with [3].
5. If you need further assistance, please contact customer support at +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [2].

**Passages shown to the model:**
[1] (password-recovery) Recovering or changing your password. If you cannot sign in, you can set a new password yourself.

**Recover a forgotten password**
1. Go to the login page on www.shopease.example and click **Forgot Password**.
2. Enter the email address registered to your account.
3. Open the email we send you and click the reset link. The link is valid for 30 minutes.
4. Choose a new password: at least 8 characters, with a letter and a number.
[2] (password-recovery) Recovering or changing your password. **Change your password while signed in**
Go to **Account Settings**, then **Password and Security**, and enter your current password followed by the new one.

If none of this works, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (password-recovery) Recovering or changing your password. **If the email does not arrive**
Check your spam folder and wait a few minutes before trying again. Make sure you typed the same email address you registered with.
[4] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 29
**Customer:** I need to report problems with a sign-up

**Sentences:**
1. Hello!
2. For sign-up problems, your password must be at least 8 characters and include a letter and a number [1].
3. If you did not receive a verification email, check your spam folder, wait 10 minutes, and choose **Resend email** on the login page [1].
4. If your link expired, remember it works for 24 hours, and you can request a new one from the login page [1].
5. If you see "Email already registered," use **Forgot Password** on the login page [1].
6. If you are still stuck, contact customer support at +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and provide the email address you used [1].

**Passages shown to the model:**
[1] (create-account) Creating a ShopEase account and fixing sign-up problems. Your password must be at least 8 characters and include a letter and a number.

**Sign-up problems**
- **No verification email:** check your spam folder and wait 10 minutes, then choose **Resend email** on the login page.
- **Link expired:** the link works for 24 hours. Request a new one from the login page.
- **"Email already registered":** you already have an account. Use **Forgot Password** on the login page to get back in.
- **Still stuck:** contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used.
[2] (complaints) Making a complaint. If something went wrong with your order, delivery, payment or support experience, you can make a complaint at any time.

**How to complain**
1. Sign in to the ShopEase customer portal, go to **My Orders**, select the order and choose **Report a problem**.
2. Or contact customer support: +91 00000 00000, support@shopease.example, or live chat on www.shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.
[4] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.

---

## Draft 30
**Customer:** i cant sign up want assistance to report sign-up problems

**Sentences:**
1. If you are experiencing sign-up problems, please check your spam folder and wait 10 minutes if you received no verification email, then choose **Resend email** on the login page [1].
2. If your link expired, remember it works for 24 hours and you can request a new one from the login page [1].
3. If you see "Email already registered," use **Forgot Password** on the login page [1].
4. If you are still stuck, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used [1].
5. Customer support can help with the rest.

**Passages shown to the model:**
[1] (create-account) Creating a ShopEase account and fixing sign-up problems. Your password must be at least 8 characters and include a letter and a number.

**Sign-up problems**
- **No verification email:** check your spam folder and wait 10 minutes, then choose **Resend email** on the login page.
- **Link expired:** the link works for 24 hours. Request a new one from the login page.
- **"Email already registered":** you already have an account. Use **Forgot Password** on the login page to get back in.
- **Still stuck:** contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used.
[2] (delete-account) Deleting your account. If you cannot sign in, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and we will help you with the request.
[3] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.
[4] (password-recovery) Recovering or changing your password. **If the email does not arrive**
Check your spam folder and wait a few minutes before trying again. Make sure you typed the same email address you registered with.

---

## Draft 31
**Customer:** is it possible to set up the secondary shipping address

**Sentences:**
1. Yes, you can save several addresses to your account [1][2].
2. To save a new address, sign in to the ShopEase customer portal and open **Account Settings** [2].
3. Select **Saved Addresses** and click **Add a New Address**, then enter the full address including the PIN code and a contact number [2].
4. You can also tick **Make default** if you want it used automatically at checkout [2].

**Passages shown to the model:**
[1] (shipping-address) Setting up and changing delivery addresses. You can save several addresses and choose between them when you place an order. We deliver within India.

**Change the address on an existing order**
- If the order has not been dispatched, open **My Orders**, select the order and click **Change Order**, then update the delivery address.
- If the order is already dispatched, the address cannot be changed online. Contact customer support straight away on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number. We will ask the delivery partner to redirect the parcel, but we cannot guarantee that this is possible.
[2] (shipping-address) Setting up and changing delivery addresses. **Save an address to your account**
1. Sign in to the ShopEase customer portal and open **Account Settings**.
2. Select **Saved Addresses** and click **Add a New Address**.
3. Enter the full address, including the PIN code and a contact number.
4. Tick **Make default** if you want it used automatically at checkout.
[3] (change-order) Changing an order. You can change an order until it is dispatched. Once the order status shows **Dispatched**, it can no longer be changed.

**What you can change**
- Item size or colour
- Quantity
- Delivery address
- Delivery option, where the new option is available
[4] (place-order) Placing an order. To place an order you need a ShopEase account. You can create one for free on www.shopease.example.

**Steps**
1. Add items to your cart and click **Checkout**.
2. Confirm or choose your delivery address.
3. Select a delivery option: standard, express, same-day (where available) or store pickup.
4. Choose a payment method and click **Place Order**.

---

## Draft 32
**Customer:** i have issues entering a delivery adrdess

**Sentences:**
1. To change or set up your delivery address, go to Saved Addresses in your Account Settings [1][2].
2. Make sure to enter the correct PIN code, as wrong PIN codes are the most common cause of late deliveries [1].

**Passages shown to the model:**
[1] (shipping-address) Setting up and changing delivery addresses. Make sure the PIN code is correct. Wrong PIN codes are the most common cause of late deliveries.
[2] (edit-account) Editing your account details. **Changing your password:** go to **Account Settings**, then **Password and Security**.

**Delivery addresses:** these are managed separately under **Saved Addresses** in Account Settings (see the shipping address guide).
[3] (payment-problems) Payment problems. **Payment failed**
- Check your card details, balance or limit, and your internet connection.
- Try another payment method such as UPI or net banking.
- Wait a few minutes before trying again, because a payment that is still processing can look as if it failed.
[4] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.

---

## Draft 33
**Customer:** i try to track purchase ORD-40855

**Sentences:**
1. To track your purchase, please sign in to the ShopEase customer portal and open **My Orders**, then select your order and click **Track Order** [1].
2. Customer support can help with the rest.

**Passages shown to the model:**
[1] (track-order) Tracking an order. You can follow your order from placement to delivery.

**How to track an order**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Track Order**.
[2] (delivery-times) How long delivery takes. **If your order is late**
If your order has not arrived by the estimated delivery date, check **Track Order** first. If there is no update, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[3] (track-order) Tracking an order. **Order statuses**
- **Order Placed:** we have received your order.
- **Packed:** your items are ready to go.
- **Dispatched:** the order has been handed to our delivery partner, SwiftShip.
- **Out for Delivery:** the delivery agent is on the way.
- **Delivered:** the order has arrived.
[4] (track-order) Tracking an order. When the order is dispatched, we email you a tracking number (it starts with TRK). It can take up to 24 hours after dispatch for tracking updates to appear.

---

## Draft 34
**Customer:** help checking the ETA of the purchase ORD-73634

**Sentences:**
1. The estimated delivery date is shown on the order page and in your dispatch email [3].
2. If your order has not arrived by the estimated delivery date, check Track Order first [2].
3. If there is no update, customer support can help with the rest [3].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.
[2] (delivery-times) How long delivery takes. **If your order is late**
If your order has not arrived by the estimated delivery date, check **Track Order** first. If there is no update, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[3] (track-order) Tracking an order. The estimated delivery date is shown on the order page and in your dispatch email.

If there is no update for 48 hours, or the order has not arrived by the estimated date, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number.
[4] (refund-tracking) Tracking a refund. **If you have not received your refund**
If it has been more than 7 business days, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Please share your order number and refund reference.

---

## Draft 35
**Customer:** could I know if there are any updates on my rebate?

**Sentences:**
1. If it has been more than 7 business days, you can contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [4].
2. Please share your order number and refund reference [4].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **If an invoice is missing**
The invoice appears after dispatch. If your order has been dispatched and there is still no invoice, check your spam folder, then contact customer support.
[2] (refund-tracking) Tracking a refund. **Refund statuses**
- **Requested:** we have received your request.
- **Approved:** the refund has been approved. You receive an email with your refund reference (it starts with REF).
- **Processing:** the money is being sent to your original payment method.
- **Completed:** the refund has been sent.
[3] (payment-problems) Payment problems. **Duplicate or unauthorized charges**
If you see the same payment twice, or a payment you did not make, contact customer support immediately on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Tell us the order number, the date and amount of the payment, and the last four digits of the card or the UPI transaction ID. Once confirmed, the amount is refunded within 5 to 7 business days.
[4] (refund-tracking) Tracking a refund. **If you have not received your refund**
If it has been more than 7 business days, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Please share your order number and refund reference.

---

## Draft 36
**Customer:** i cant add an article to order ORD-60641

**Sentences:**
1. If an item is out of stock, it cannot be added to the cart [4].
2. For any other problem, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [4].

**Passages shown to the model:**
[1] (change-order) Changing an order. **How to change an order**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Change Order**.
3. Make your change and click **Save**. You receive an updated confirmation email.
[2] (change-order) Changing an order. You can change an order until it is dispatched. Once the order status shows **Dispatched**, it can no longer be changed.

**What you can change**
- Item size or colour
- Quantity
- Delivery address
- Delivery option, where the new option is available
[3] (place-order) Placing an order. To place an order you need a ShopEase account. You can create one for free on www.shopease.example.

**Steps**
1. Add items to your cart and click **Checkout**.
2. Confirm or choose your delivery address.
3. Select a delivery option: standard, express, same-day (where available) or store pickup.
4. Choose a payment method and click **Place Order**.
[4] (place-order) Placing an order. If an item is out of stock, it cannot be added to the cart. If your payment fails, see the payment problems guide. For any other problem, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 37
**Customer:** I want help to edit my address

**Sentences:**
1. To save a new delivery address to your account, sign in to the ShopEase customer portal and open **Account Settings** [1].
2. Next, select **Saved Addresses** and click **Add a New Address** [1].
3. Enter the full address, including the PIN code and a contact number, and tick **Make default** if you want it used automatically at checkout [1].
4. To change the address on an existing order that has not been dispatched, open **My Orders**, select the order and click **Change Order**, then update the delivery address [2].
5. If the order is already dispatched, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [2].

**Passages shown to the model:**
[1] (shipping-address) Setting up and changing delivery addresses. **Save an address to your account**
1. Sign in to the ShopEase customer portal and open **Account Settings**.
2. Select **Saved Addresses** and click **Add a New Address**.
3. Enter the full address, including the PIN code and a contact number.
4. Tick **Make default** if you want it used automatically at checkout.
[2] (shipping-address) Setting up and changing delivery addresses. You can save several addresses and choose between them when you place an order. We deliver within India.

**Change the address on an existing order**
- If the order has not been dispatched, open **My Orders**, select the order and click **Change Order**, then update the delivery address.
- If the order is already dispatched, the address cannot be changed online. Contact customer support straight away on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number. We will ask the delivery partner to redirect the parcel, but we cannot guarantee that this is possible.
[3] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (edit-account) Editing your account details. **Changing your password:** go to **Account Settings**, then **Password and Security**.

**Delivery addresses:** these are managed separately under **Saved Addresses** in Account Settings (see the shipping address guide).

---

## Draft 38
**Customer:** i dont know wwhat i need to do to check invoice #85632

**Sentences:**
1. To check the invoice for your order, sign in to the ShopEase customer portal and open **My Orders**, select your order, and click **Download Invoice** [4].
2. Alternatively, you can open **Account Settings**, select **Billing History**, choose the appropriate date range, and click the invoice to see its details or download it [1].
3. Please note that an invoice is created and emailed to your registered address only after the order has been dispatched [2][3].
4. If your order has been dispatched and the invoice is still missing, check your spam folder and then contact customer support [2].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.
[2] (invoices) Checking and downloading invoices. **If an invoice is missing**
The invoice appears after dispatch. If your order has been dispatched and there is still no invoice, check your spam folder, then contact customer support.
[3] (invoices) Checking and downloading invoices. An invoice is created for every order when it is dispatched. Invoice numbers look like INV-12345. We also email the invoice to your registered address.
[4] (invoices) Checking and downloading invoices. **Download an invoice for one order**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Download Invoice**. The invoice is saved as a PDF.

---

## Draft 39
**Customer:** I do not know how to list your payment methods

**Sentences:**
1. To view the accepted payment methods, check the checkout screen before placing your order [2][3].
2. ShopEase accepts credit and debit cards (Visa, Mastercard, RuPay), UPI, net banking, and cash on delivery for standard delivery orders up to ₹5,000 [3].
3. If a payment method is not shown at checkout, it may not be available for your order, and you can try another method or contact customer support at +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [1].

**Passages shown to the model:**
[1] (payment-methods) Accepted payment methods. If a payment method is not shown at checkout, it may not be available for your order. Try another method, or contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[2] (payment-methods) Accepted payment methods. The methods you can use are shown at checkout, before you place the order.

**Saved payment methods**
You can save a card for faster checkout. Go to **Account Settings**, then **Payment Methods**, to view or remove saved cards. We never store your full card number or security code.
[3] (payment-methods) Accepted payment methods. ShopEase accepts the following payment methods. All prices are in rupees (₹).

- **Credit and debit cards:** Visa, Mastercard and RuPay.
- **UPI:** pay from any UPI app using your UPI ID or a QR code.
- **Net banking:** supported for major Indian banks.
- **Cash on delivery:** available for standard delivery orders up to ₹5,000.
[4] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.

---

## Draft 40
**Customer:** show me in which cases can I ask to be refunded

**Sentences:**
1. You can ask for a refund in cases of duplicate or unauthorized charges, damaged or defective items, orders that did not arrive [4], returns [1][4], and cancelled orders [4].
2. Customer support can help with the rest.

**Passages shown to the model:**
[1] (refund-policy) Refund policy. **How to request a refund**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Return or Refund**.
3. Choose the item and the reason, and submit the request.
[2] (refund-policy) Refund policy. For questions about a refund, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (refund-tracking) Tracking a refund. **If you have not received your refund**
If it has been more than 7 business days, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Please share your order number and refund reference.
[4] (refund-policy) Refund policy. We email you once the request is approved. For returns, approval happens after we receive and check the item.

**Refund time**
Refunds go back to your original payment method within 5 to 7 business days. For returns, this starts when the refund is approved. For cancelled orders, it starts on the day of cancellation. The same timeline applies to refunds for duplicate or unauthorized charges, damaged or defective items, and orders that did not arrive.

---

## Draft 41
**Customer:** need to file a bloody consumer reclamation how can i do it

**Sentences:**
1. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent [2].

**Passages shown to the model:**
[1] (refund-policy) Refund policy. **How to request a refund**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Return or Refund**.
3. Choose the item and the reason, and submit the request.
[2] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[3] (refund-policy) Refund policy. For questions about a refund, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (delete-account) Deleting your account. You can ask to delete your ShopEase account at any time.

**Before you delete**
- Orders that are still being processed or delivered must be completed or cancelled first.
- Download any invoices you need. After deletion, your order history and invoices cannot be recovered.

---

## Draft 42
**Customer:** where to see what hours i can reach customer service

**Sentences:**
1. Support hours are Monday to Friday, from 9 AM to 6 PM [1].
2. Messages sent outside these hours are answered on the next business day [1].

**Passages shown to the model:**
[1] (contact-support) Contacting ShopEase customer support. Support hours are Monday to Friday, 9 AM to 6 PM. Messages sent outside these hours are answered on the next business day.

To help us find your case quickly, have your order number (for example ORD-12345) or your registered email address ready. If your question is about an invoice, also include the invoice number.
[2] (cancel-order) Cancelling an order. If you cannot cancel online, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[3] (contact-support) Contacting ShopEase customer support. ShopEase customer support can be reached in three ways:

- **Phone:** +91 00000 00000. Your call goes directly to a support agent.
- **Email:** support@shopease.example. We reply within 1 business day.
- **Live chat:** available on www.shopease.example. Choose "Talk to an agent" to be connected to a person.
[4] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 43
**Customer:** could you help me to speak with a live agent?

**Sentences:**
1. To speak with a live human agent, you can call the phone line at +91 00000 00000 or use the "Talk to an agent" option in the live chat on www.shopease.example [1][2].

**Passages shown to the model:**
[1] (contact-support) Contacting ShopEase customer support. If you prefer to speak to a human agent instead of using the automated help, use the phone line or the "Talk to an agent" option in live chat. The ShopEase customer portal also has a Help Center with answers to common questions, available at any time.
[2] (contact-support) Contacting ShopEase customer support. ShopEase customer support can be reached in three ways:

- **Phone:** +91 00000 00000. Your call goes directly to a support agent.
- **Email:** support@shopease.example. We reply within 1 business day.
- **Live chat:** available on www.shopease.example. Choose "Talk to an agent" to be connected to a person.
[3] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[4] (create-account) Creating a ShopEase account and fixing sign-up problems. Your password must be at least 8 characters and include a letter and a number.

**Sign-up problems**
- **No verification email:** check your spam folder and wait 10 minutes, then choose **Resend email** on the login page.
- **Link expired:** the link works for 24 hours. Request a new one from the login page.
- **"Email already registered":** you already have an account. Use **Forgot Password** on the login page to get back in.
- **Still stuck:** contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used.

---

## Draft 44
**Customer:** want assistance to see the shipping options

**Sentences:**
1. To see the available delivery options, enter your PIN code at checkout, as the options depend on your delivery address and the items in your cart [1].
2. Customer support can help with the rest.

**Passages shown to the model:**
[1] (delivery-options) Delivery options. Which options you see depends on your delivery address and the items in your cart. Enter your PIN code at checkout to see what is available for you.
[2] (place-order) Placing an order. If an item is out of stock, it cannot be added to the cart. If your payment fails, see the payment problems guide. For any other problem, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[3] (delivery-options) Delivery options. Delivery times are counted from the day your order is dispatched. See the delivery times guide for details.

To change the delivery option of an order that is not yet dispatched, open **My Orders**, select the order and click **Change Order**. For help, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (change-order) Changing an order. You can change an order until it is dispatched. Once the order status shows **Dispatched**, it can no longer be changed.

**What you can change**
- Item size or colour
- Quantity
- Delivery address
- Delivery option, where the new option is available

---

## Draft 45
**Customer:** I want to see how long the shipping takes, how can I do it?

**Sentences:**
1. Delivery times depend on the option you choose at checkout, with Standard delivery taking 4 to 6 business days and Express delivery taking 1 to 2 business days [4].
2. The estimated delivery date is shown on the order page and in your dispatch email [3].

**Passages shown to the model:**
[1] (delivery-times) How long delivery takes. **If your order is late**
If your order has not arrived by the estimated delivery date, check **Track Order** first. If there is no update, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and quote your order number.
[2] (track-order) Tracking an order. When the order is dispatched, we email you a tracking number (it starts with TRK). It can take up to 24 hours after dispatch for tracking updates to appear.
[3] (track-order) Tracking an order. The estimated delivery date is shown on the order page and in your dispatch email.

If there is no update for 48 hours, or the order has not arrived by the estimated date, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) with your order number.
[4] (delivery-times) How long delivery takes. Delivery times depend on the option you choose at checkout.

| Option | Delivery time |
|---|---|
| Standard delivery | 4 to 6 business days |
| Express delivery | 1 to 2 business days |

---

## Draft 46
**Customer:** change info on Basic account

**Sentences:**
1. You can update your personal details at any time in the ShopEase customer portal [2].
2. To edit your details, sign in to the customer portal, open **Account Settings**, and select **Profile** [2].
3. From there, you can change your name, mobile number, or email address, and then click **Save** [2].
4. When changing your email address, we send a 6-digit verification code to the new address, and your email only changes after you enter the code [1].
5. If a detail cannot be edited online, please contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) [4].

**Passages shown to the model:**
[1] (edit-account) Editing your account details. **Changing your email address:** we send a 6-digit verification code to the new address. Your email only changes after you enter the code. Order updates and invoices go to the new address from then on.
[2] (edit-account) Editing your account details. You can update your personal details at any time in the ShopEase customer portal.

**How to edit your details**
1. Sign in to the ShopEase customer portal.
2. Open **Account Settings** and select **Profile**.
3. Change your name, mobile number or email address.
4. Click **Save**. Changes apply immediately.
[3] (edit-account) Editing your account details. **Changing your password:** go to **Account Settings**, then **Password and Security**.

**Delivery addresses:** these are managed separately under **Saved Addresses** in Account Settings (see the shipping address guide).
[4] (edit-account) Editing your account details. If a detail cannot be edited online, for example a name that is locked after an order has been placed, contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 47
**Customer:** what do i have to do to download the invoice #12588

**Sentences:**
1. To download the invoice for your order, sign in to the ShopEase customer portal and open **My Orders** [1].
2. Select the order and click **Download Invoice** to save it as a PDF [1].
3. An invoice is created for every order when it is dispatched and is also emailed to your registered address [2].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Download an invoice for one order**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Download Invoice**. The invoice is saved as a PDF.
[2] (invoices) Checking and downloading invoices. An invoice is created for every order when it is dispatched. Invoice numbers look like INV-12345. We also email the invoice to your registered address.
[3] (invoices) Checking and downloading invoices. **Check or find invoices over a period**
1. Open **Account Settings** and select **Billing History**.
2. Choose a date range. All invoices in that period are listed with their invoice number, order number, date and amount in ₹.
3. Click an invoice to see its details or download it.
[4] (invoices) Checking and downloading invoices. **If an invoice is missing**
The invoice appears after dispatch. If your order has been dispatched and there is still no invoice, check your spam folder, then contact customer support.

---

## Draft 48
**Customer:** the payment failed, I want assistance to notify of a problem

**Sentences:**
1. If your payment failed, please check your card details, balance or limit, and your internet connection [1].
2. You can also try another payment method such as UPI or net banking [1].
3. Since a payment that is still processing can look as if it failed, please wait a few minutes before trying again [1].

**Passages shown to the model:**
[1] (payment-problems) Payment problems. **Payment failed**
- Check your card details, balance or limit, and your internet connection.
- Try another payment method such as UPI or net banking.
- Wait a few minutes before trying again, because a payment that is still processing can look as if it failed.
[2] (payment-problems) Payment problems. **Duplicate or unauthorized charges**
If you see the same payment twice, or a payment you did not make, contact customer support immediately on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM). Tell us the order number, the date and amount of the payment, and the last four digits of the card or the UPI transaction ID. Once confirmed, the amount is refunded within 5 to 7 business days.
[3] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[4] (payment-methods) Accepted payment methods. If a payment method is not shown at checkout, it may not be available for your order. Try another method, or contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM).

---

## Draft 49
**Customer:** where do I purchase some articles?

**Sentences:**
1. To place an order, you need a ShopEase account, which you can create for free on www.shopease.example [2].
2. To purchase articles, follow these steps:
3. Add items to your cart and click **Checkout** [2].
4. Confirm or choose your delivery address [2].
5. Select a delivery option: standard, express, same-day (where available) or store pickup [2].
6. Choose a payment method and click **Place Order** [2].

**Passages shown to the model:**
[1] (invoices) Checking and downloading invoices. **Download an invoice for one order**
1. Sign in to the ShopEase customer portal and open **My Orders**.
2. Select the order and click **Download Invoice**. The invoice is saved as a PDF.
[2] (place-order) Placing an order. To place an order you need a ShopEase account. You can create one for free on www.shopease.example.

**Steps**
1. Add items to your cart and click **Checkout**.
2. Confirm or choose your delivery address.
3. Select a delivery option: standard, express, same-day (where available) or store pickup.
4. Choose a payment method and click **Place Order**.
[3] (payment-methods) Accepted payment methods. ShopEase accepts the following payment methods. All prices are in rupees (₹).

- **Credit and debit cards:** Visa, Mastercard and RuPay.
- **UPI:** pay from any UPI app using your UPI ID or a QR code.
- **Net banking:** supported for major Indian banks.
- **Cash on delivery:** available for standard delivery orders up to ₹5,000.
[4] (contact-support) Contacting ShopEase customer support. If you prefer to speak to a human agent instead of using the automated help, use the phone line or the "Talk to an agent" option in live chat. The ShopEase customer portal also has a Help Center with answers to common questions, available at any time.

---

## Draft 50
**Customer:** need to report issues with registrations

**Sentences:**
1. Hello!
2. If you are experiencing sign-up problems, passwords must be at least 8 characters and include a letter and a number [1].
3. Here are solutions for common sign-up issues:
4. **No verification email:** check your spam folder, wait 10 minutes, and choose **Resend email** on the login page [1].
5. **Link expired:** the link works for 24 hours, and you can request a new one from the login page [1].
6. **"Email already registered":** use **Forgot Password** on the login page [1].
7. If you are still stuck, customer support can help with the rest; contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used [1].

**Passages shown to the model:**
[1] (create-account) Creating a ShopEase account and fixing sign-up problems. Your password must be at least 8 characters and include a letter and a number.

**Sign-up problems**
- **No verification email:** check your spam folder and wait 10 minutes, then choose **Resend email** on the login page.
- **Link expired:** the link works for 24 hours. Request a new one from the login page.
- **"Email already registered":** you already have an account. Use **Forgot Password** on the login page to get back in.
- **Still stuck:** contact customer support on +91 00000 00000 or support@shopease.example (Monday to Friday, 9 AM to 6 PM) and tell us the email address you used.
[2] (complaints) Making a complaint. If you are not satisfied with the outcome, reply to the email we sent you and ask for your case to be passed to a senior support agent.
[3] (complaints) Making a complaint. If something went wrong with your order, delivery, payment or support experience, you can make a complaint at any time.

**How to complain**
1. Sign in to the ShopEase customer portal, go to **My Orders**, select the order and choose **Report a problem**.
2. Or contact customer support: +91 00000 00000, support@shopease.example, or live chat on www.shopease.example (Monday to Friday, 9 AM to 6 PM).
[4] (payment-problems) Payment problems. Never share your card PIN or a one-time password with anyone, including people who say they are from ShopEase.

---
