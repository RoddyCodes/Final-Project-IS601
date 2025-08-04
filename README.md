# 🧮 Calculator App – Overview

This is a Calculator web application with JWT-based authentication.

## 🔐 JWT Login & Registration Routes

- **/register**

  - Receives user info (username/email, password).
  - Validates input (checks for duplicates, hashes password, stores in DB).
  - Returns a JWT or a success response.

- **/login**
  - Valid credentials → returns JWT.
  - Invalid credentials → 401 Unauthorized.

## 🌐 Front-End Pages

- **register.html**

  - Fields for email, password,
  - Client-side checks (email format, minimum password length).
  - On success (200/201), displays a success message or stores the JWT.

- **login.html**
  - Fields for email, password.
  - Minimal client-side checks.
  - On success, stores the JWT or displays a success message.

## 🧪 Playwright E2E Tests

- **Positive Tests:**

  - Register with valid data (correct email format, password length), confirm success message.
  - Login with correct credentials, confirm success or token stored.

- **Negative Tests:**
  - Register with short password → front-end error or 400 from server, verify UI shows error.
  - Login with wrong password → server returns 401, UI shows invalid credentials message.

Tests locate form fields, enter invalid/valid data, submit, and check resulting UI states or server responses.

---

# 🚀 Running the Project

- **Without Docker**:

```bash
python main.py
```

- **With Docker**:

```bash
docker run -it --rm roddycodes/is601_module13
```

---

# 🌐 Running the Front-End

The front-end is served by FastAPI and is available at:  
[http://localhost:8000/](http://localhost:8000/)

---

# 🗄️ Accessing pgAdmin

pgAdmin (for managing your PostgreSQL database) is available at:  
[http://localhost:5050/](http://localhost:5050/)

---

# 🧪 Running Playwright Tests

Playwright is used for end-to-end testing.

1. Install Playwright (if not already installed):
   ```bash
   pip install playwright
   playwright install
   ```
2. Run Playwright tests:
   ```bash
   pytest tests/e2e/
   ```
   Or, if you use npm-based Playwright tests:
   ```bash
   npx playwright test
   ```

---

# 🐳 Docker Hub Repository

You can find the published Docker image for this project on Docker Hub:

- [Docker Hub Repository Link](https://hub.docker.com/repository/docker/roddycodes/is601_module13/general)

---

# 💻 GitHub Repository

- [GitHub Repository Link](https://github.com/RoddyCodes/module13_is601)

---

# 📋 Notes

- README file contains instructions on how to run the front-end, execute Playwright tests, and links to the Docker Hub repository.
- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and \*\*virtual
