# Test Specification: Login (UI demo)

> Neutral. UI/web level. Illustrates the locator-binding flow that the `qa`
> extension resolves. No framework, no selectors here.

## Requirements

### REQ-001 - successful login

- **Precondition:** a registered user exists; the login page is reachable.
- **Input:** valid email + password, submit.
- **Object under test:** the login form and its submit action.
- **Expected output:** the user lands on the dashboard; a greeting with their
  name is visible.
- **Acceptance:** Given a registered user, when they submit valid credentials,
  then the dashboard greeting is shown.

### REQ-002 - rejected login

- **Precondition:** the login page is reachable.
- **Input:** valid email + wrong password, submit.
- **Object under test:** the login form error path.
- **Expected output:** an error message is shown; the user stays on login.
- **Acceptance:** Given a wrong password, when submitted, then an inline error
  is shown and the URL is still the login page.
