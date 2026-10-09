# Test plan: Password reset with a single-use link that expires after 30 minutes

## 1. Request a reset link for a registered email

- **Category:** happy path
- **Priority:** high

### Preconditions

- A registered user has access to their email inbox.

### Steps

1. Open the password reset page.
2. Enter the registered email address.
3. Submit the request.
4. Open the received reset link within 30 minutes.
5. Enter and confirm a valid new password.
6. Submit the new password.

### Expected result

The password is changed and the user can sign in with the new password.

## 2. Do not reveal whether an email is registered

- **Category:** negative
- **Priority:** high

### Preconditions

- None

### Steps

1. Request a reset link using a registered email address and record the confirmation message.
2. Request a reset link using an unregistered email address.
3. Compare the visible responses.

### Expected result

Both requests display the same neutral confirmation and do not reveal account existence.

## 3. Reject a reset link after 30 minutes

- **Category:** edge case
- **Priority:** high

### Preconditions

- A password reset link was issued more than 30 minutes ago.

### Steps

1. Open the expired reset link.
2. Attempt to set a new password.

### Expected result

The password is not changed and the user is told that the link has expired.

## 4. Reject a reset link that has already been used

- **Category:** negative
- **Priority:** high

### Preconditions

- A password reset link has already been used successfully.

### Steps

1. Open the same reset link again.
2. Attempt to enter another new password.

### Expected result

The reused link is rejected and the password remains unchanged.

## 5. Submit an empty email address

- **Category:** negative
- **Priority:** medium

### Preconditions

- The password reset page is open.

### Steps

1. Leave the email field empty.
2. Submit the form.

### Expected result

The request is not submitted and a clear validation message is displayed.

## 6. Navigate the reset form using only a keyboard

- **Category:** accessibility
- **Priority:** medium

### Preconditions

- The password reset page is open.

### Steps

1. Navigate through the form using Tab and Shift+Tab.
2. Enter an email address.
3. Submit the form using the keyboard.

### Expected result

Every interactive element has a visible focus state and the form can be completed without a mouse.
