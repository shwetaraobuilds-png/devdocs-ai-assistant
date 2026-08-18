## API Authentication

Stripe API requests are authenticated using API keys.

Secret API keys must be kept on the server and should never be exposed
in browser code, mobile applications, public repositories, or other
client-side environments.

Stripe API keys are generally provided using Bearer authentication in
the Authorization request header.

Example:

Authorization: Bearer sk_test_example

Test secret keys begin with `sk_test_`.
Live secret keys begin with `sk_live_`.

A test key is used for development and testing. A live key is used for
real transactions.

Source:
https://docs.stripe.com/api/authentication


## Test Mode and Live Mode

Stripe provides separate environments for testing and production.

Test mode allows developers to simulate payment activity without moving
real money. Objects created in test mode are separate from objects
created in live mode.

Developers should use test API keys with test-mode data and live API
keys with live-mode data.

A test API key cannot access live-mode resources.

Source:
https://docs.stripe.com/test-mode


## PaymentIntents

A PaymentIntent represents Stripe's process for collecting a payment
from a customer.

A developer typically creates one PaymentIntent for each order or
checkout session.

The PaymentIntent tracks the payment throughout its lifecycle. Its
status can change depending on whether the payment requires customer
action, succeeds, or fails.

A PaymentIntent can have statuses such as:

- requires_payment_method
- requires_confirmation
- requires_action
- processing
- succeeded
- canceled

Source:
https://docs.stripe.com/payments/payment-intents


## Idempotency

Idempotency helps prevent duplicate API operations when a request is
retried.

A developer can send an idempotency key using the `Idempotency-Key`
request header.

Example:

Idempotency-Key: order_12345_payment

When retrying the same logical operation, the developer should reuse
the same idempotency key.

Stripe recommends using idempotency keys with POST requests. This can
prevent duplicate resources or payments when a network failure causes
an application to repeat a request.

Source:
https://docs.stripe.com/api/idempotent_requests


## API Errors

Stripe uses HTTP status codes to communicate whether an API request
succeeded or failed.

Status codes in the 2xx range generally indicate success.

Status codes in the 4xx range generally indicate a problem with the
request. Examples include:

- Missing required parameters
- Invalid API credentials
- A resource that does not exist
- A payment that was declined

Status codes in the 5xx range generally indicate a server-side problem.

A 401 response usually indicates an authentication problem, such as a
missing or invalid API key.

A 404 response indicates that the requested resource could not be
found.

A 429 response indicates that too many API requests were made in a
short period.

Source:
https://docs.stripe.com/api/errors


## Webhooks

Webhooks allow Stripe to notify an application when an event occurs.

For example, Stripe can send webhook events when:

- A payment succeeds
- A payment fails
- A refund is created
- A subscription is updated

Stripe includes a signature in the `Stripe-Signature` request header.

The application should verify the signature before trusting or
processing the webhook event.

Webhook signature verification uses the endpoint's signing secret.
Each webhook endpoint has its own signing secret.

Developers can use Stripe's official libraries to verify webhook
signatures.

Source:
https://docs.stripe.com/webhooks
