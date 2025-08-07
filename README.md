# 🧮 Full-Stack Calculator & API

[![Build Status](https://img.shields.io/github/actions/workflow/status/RoddyCodes/Final-Project-IS601/main.yml?style=for-the-badge)](https://github.com/RoddyCodes/Final-Project-IS601/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A comprehensive, full-stack web application featuring a secure, multi-user calculator with a persistent history of operations. This project is built with a modern technology stack, including a robust **FastAPI** backend, a dynamic frontend, and a **PostgreSQL** database, all containerized with **Docker**.

The application provides a clean, responsive user interface and a well-documented RESTful API for all backend operations, including user authentication and calculation management.

---

## ✨ Key Features

- **Secure User Authentication**: Complete registration and login system using **JWT** for secure, stateless sessions.
- **Full CRUD Functionality**: Users can Create, Read, Update, and Delete their personal calculation history.
- **Standard Arithmetic Operations**: Addition, Subtraction, Multiplication, and Division.
- **Advanced Operations**: Includes **Modulus** and **Exponentiation** functionality.
- **Persistent User-Specific History**: All calculations are saved and associated with the logged-in user.
- **RESTful API**: A well-defined API for all backend services.
- **Interactive API Documentation**: Automatic, interactive API documentation via **Swagger UI** and **ReDoc**.
- **Comprehensive Test Suite**: Includes unit, integration, and end-to-end (E2E) tests to ensure reliability.
- **Modern UI/UX**: Responsive, user-friendly frontend with real-time result previews and error handling.
- **Role-Based Access**: Each user can only access and manage their own calculations.
- **Robust Error Handling**: Graceful error messages for invalid operations (e.g., division by zero, modulus by zero).
- **Extensible Architecture**: Easily add new operations or extend existing functionality.

---

## 🛠️ Technology Stack

| Category     | Technology                                                                                                                                                                                                                                                                                                                                                                                                                          |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**  | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)                                                                                                    |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)                                                                                                                                                                                                                                                                                                                   |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white) |
| **Testing**  | ![Pytest](https://img.shields.io/badge/Pytest-0A9B71?style=for-the-badge&logo=pytest&logoColor=white) ![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)                                                                                                                                                                                                             |
| **DevOps**   | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)                                                                                                                                                                                                  |

---

## 📚 Project Structure

```
Final-Project-IS601/
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── models/                # SQLAlchemy models (User, Calculation, etc.)
│   ├── operations/            # Arithmetic operation logic (add, subtract, etc.)
│   ├── api/                   # API route definitions
│   ├── auth/                  # Authentication logic (JWT, password hashing)
│   └── ...                    # Other backend modules
├── templates/                 # Jinja2 HTML templates for frontend
├── static/                    # Static files (CSS, JS, images)
├── tests/
│   ├── unit/                  # Unit tests for backend logic
│   ├── e2e/                   # End-to-end tests (API, UI)
│   └── ...                    # Additional test modules
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for FastAPI app
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

The entire application stack is containerized with Docker, making it easy to run with a single command.

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
- [Git](https://git-scm.com/)

### Installation & Running

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/RoddyCodes/Final-Project-IS601.git
    cd Final-Project-IS601
    ```

2.  **Build and run the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build the images, start the FastAPI server, PostgreSQL database, and pgAdmin services.

---

## 🌐 Accessing the Application

Once the containers are running, you can access the following services in your browser:

- **Web Application**: [http://localhost:8080/](http://localhost:8080/)
- **API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **pgAdmin (Database GUI)**: [http://localhost:5050/](http://localhost:5050/)

---

## 🧪 Running the Tests

The project includes a comprehensive test suite. To run the tests, first ensure the application containers are running.

1.  **Run Unit & Integration Tests (Pytest):**
    Open a new terminal and execute the following command to run all backend tests inside the container:

    ```bash
    docker-compose exec web pytest --cov=app
    ```

2.  **Run End-to-End Tests (Playwright):**
    These tests interact with a live browser to simulate user behavior.
    ```bash
    # Run the E2E tests against the live server
    pytest tests/e2e/
    ```

---

## 🧑‍💻 Example API Usage

**Create a Calculation (POST /calculations):**

```json
{
  "type": "modulus",
  "inputs": [10, 3]
}
```

**Response:**

```json
{
  "type": "modulus",
  "inputs": [10, 3],
  "result": 1
}
```

**Supported Calculation Types:**

- `addition`
- `subtraction`
- `multiplication`
- `division`
- `modulus`
- `exponentiate`

---

## 🗄️ Database Models Overview

The backend uses SQLAlchemy ORM with polymorphic inheritance for calculations. Each calculation type (addition, subtraction, multiplication, division, modulus, exponentiate) is a subclass of a base `Calculation` model. The `type` column is used for type discrimination, and each subclass implements its own `get_result()` method.

**User Model:**

- Stores authentication and profile information.
- Has a one-to-many relationship with calculations.

**Calculation Model:**

- Stores operation type, inputs, result, timestamps, and user association.
- Uses a factory method to instantiate the correct calculation subclass.

---

## 🖥️ Frontend Features

- **Dashboard**: View, edit, and delete your calculation history.
- **Edit Calculation**: Update inputs for any saved calculation with real-time result preview.
- **Responsive UI**: Built with modern CSS and JavaScript for a seamless experience.
- **How It Works**: Simple onboarding steps for new users.

---

## 🐳 Docker Hub & 💻 GitHub

- **Docker Hub Repository**: [https://hub.docker.com/r/roddycodes/is601_final](https://hub.docker.com/r/roddycodes/is601_final)
- **GitHub Repository**: [https://github.com/RoddyCodes/Final-Project-IS601](https://github.com/RoddyCodes/Final-Project-IS601)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙋 FAQ

**Q: Can I add more operations?**  
A: Yes! The backend is designed to be extensible. Add your operation logic in `app/operations/`, register it in the calculation factory, and update the frontend if needed.

**Q: How is user data secured?**  
A: Passwords are hashed using industry standards, and JWT is used for authentication. Users can only access their own calculations.

**Q: How do I reset the database?**  
A: Stop the containers, remove the volumes, and restart:

```bash
docker-compose down -v
docker-compose up --build
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

For questions or support, please open an issue on [GitHub](https://github.com/RoddyCodes/Final-Project-IS601/issues).

---

## 📝 Reflection: Implementing Modulus and Exponentiate

**Backend Implementation:**  
To support modulus and exponentiate operations, I extended both the operations logic and the database models. In the backend, I added `modulus` and `exponentiate` functions to the `app/operations/__init__.py` module, ensuring they handle edge cases (like modulus by zero). I then updated the calculation factory in the `Calculation` model to recognize these new types and created dedicated subclasses for each, implementing their `get_result()` methods with proper error handling.

**Frontend Integration:**  
On the frontend, I updated the JavaScript logic in the calculation forms (including edit and view pages) to recognize and correctly preview modulus (`%`) and exponentiate (`^`) operations. This included updating operator symbols, result preview logic, and error messages for invalid input (such as modulus by zero).

**Testing:**  
I wrote comprehensive unit tests for both new operations in the backend, covering normal cases and error conditions. I also added end-to-end API tests to ensure the FastAPI endpoints correctly handle requests for modulus and exponentiate calculations, including error responses for invalid input.

**Summary:**  
By following a modular and extensible approach, I was able to add new operations to both the backend and frontend with minimal friction, while maintaining robust error handling and test coverage. This demonstrates the flexibility and maintainability of the application's architecture.
