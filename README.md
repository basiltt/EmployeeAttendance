# Employee Attendance API

A minimal yet powerful FastAPI application for managing employee records, addresses, and attendance. This backend-only service uses SQLModel for data modeling and validation and an asynchronous SQLite database for storage.

The application automatically creates the necessary database schema on startup, making setup quick and easy.

***

## ✨ Features

- **Employee Management**: Create and retrieve employee records.
- **Address Management**: Add, update, or delete an address for each employee.
- **Attendance Tracking**: Clock-in and clock-out functionality.
- **Business Logic**: Prevents an employee from clocking in if they do not have an address on file.
- **Automatic Setup**: Database and tables are created automatically when the server starts.
- **Interactive Docs**: Built-in Swagger UI for easy API testing and documentation.

***

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Data Modeling / ORM**: SQLModel (combining Pydantic and SQLAlchemy)
- **Database**: SQLite (with async support via `aiosqlite`)
- **Server**: Uvicorn

***

## 🚀 Getting Started

Follow these instructions to get the API server up and running on your local machine.

### Prerequisites

- Python 3.9+

### Setup and Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone [https://your-repository-url.git](https://your-repository-url.git)
    cd your-project-directory
    ```

2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

3.  **Create and activate a virtual environment**:
    -   On **Windows**:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    -   On **macOS & Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

4.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

Once the setup is complete, run the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will start and be available at `http://127.0.0.1:8000`. The `--reload` flag enables hot-reloading for development.

***

## API

This project includes automatically generated interactive API documentation (via Swagger UI). Once the server is running, you can access and test all the endpoints directly in your browser.

- **API Docs URL**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

***

## 📂 Project Structure

```plaintext
backend/
├── app/
│   ├── __init__.py
│   ├── crud.py         # Contains all database interaction logic
│   ├── database.py     # Database engine and session setup
│   ├── main.py         # Main FastAPI app, endpoints, and startup logic
│   └── models.py       # SQLModel data models and schemas
├── requirements.txt    # Project dependencies
└── attendance.db       # SQLite database file (auto-generated)
```