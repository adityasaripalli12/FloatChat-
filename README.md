# FloatChat 🚀

> **FloatChat** – A modern, real‑time chat application built with **FastAPI**, **React**, and **TypeScript**. Designed for researchers and administrators to collaborate on datasets, visualize results, and manage security events.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **User Management** – Role‑based authentication for Admin and Researcher users.
- **Dataset Handling** – Upload, store, and query large research datasets.
- **Chat History** – Persisted chat sessions with searchable history.
- **Visualization** – Interactive data visualizations for research insights.
- **Security Auditing** – Detailed logs for security events and audit trails.
- **CORS & Security Headers** – Ready for deployment behind modern front‑ends.

---

## Tech Stack
| Layer | Technology |
|-------|-------------|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | SQLite (default) – can be swapped for PostgreSQL |
| Frontend | Vite + React (TypeScript) |
| Styling | Tailwind CSS |
| Auth | JWT + Password hashing |
| Dev Tools | Docker, pytest |

---

## Installation
```bash
# Clone the repository
git clone https://github.com/adityasaripalli12/FloatChat.git
cd FloatChat

# Set up a virtual environment (recommended)
python -m venv .venv
# Activate the environment (Windows)
.venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install
```
> **Tip:** The project ships with a `.venv` directory for isolation. Ensure you activate it before running backend commands.

---

## Running the Application
```bash
# Start the backend (FastAPI)
uvicorn backend.main:app --reload

# In another terminal, start the frontend (Vite)
npm run dev
```
The API will be available at `http://localhost:8000` and the UI at `http://localhost:5173`.

---

## API Documentation
FastAPI automatically generates interactive docs:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for your changes.
4. Ensure all tests pass (`pytest`).
5. Submit a pull request with a clear description.

---

## License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ by the FloatChat team.*
