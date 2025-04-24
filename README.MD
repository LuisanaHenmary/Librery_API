# Librery_API

A REST API built with **FastAPI** and **PostgreSQL** for managing a fictional public library. It allows you to register users, manage books, manage loans, and apply roles with JWT authentication.

---

## 🚀 Technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL
- asyncpg
- Pydantic
- JWT (Json Web Tokens)
- Uvicorn

---

## ⚙️ Installation

python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt

Defive .env values

uvicorn app.main:app --reload
