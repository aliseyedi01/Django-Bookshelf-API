# Bookshelf API with Django & DRF

A Bookshelf API implemented with Django and FastAPI

## 📚 Contents

- [Bookshelf API with Django \& DRF](#bookshelf-api-with-django--drf)
  - [📚 Contents](#-contents)
  - [📚 Demo                                                     🔝](#-demo-----------------------------------------------------)
  - [✨ Features](#-features)
  - [🔧 Technologies Used](#-technologies-used)
  - [🚀 API Endpoints](#-api-endpoints)
  - [🗃️ Database](#️-database)
  - [🛠️ Installation](#️-installation)
  - [🖥️ Usage](#️-usage)
  - [🤝 Contributing](#-contributing)
  - [📝 License](#-license)


## 📚 Demo                                                     [🔝](#contents)

> **Tip:** The Render.com free plan may experience a short delay (approximately 1 minute) when starting up. Please be patient for the initial access.

- **Render.com**
	- [Swagger](https://library-api-t70g.onrender.com/swagger/)
		- [ReDoc](https://library-api-t70g.onrender.com/redoc/)
- **Online Code**
	- [Github1s](https://github1s.com/aliseyedi01/Library_Api)
- **Database**
	- [dbdiagram](https://dbdiagram.io/d/library-65e177d0cd45b569fb458e75)

## ✨ Features

- **Book Endpoints:**
	- Comprehensive CRUD operations for managing book details, covering creation, retrieval, updating, and deletion.
- **Category Management:**
	- Operations for managing book categories, allowing users to create, retrieve, update, and delete book categories.
- **User Authentication:**
	- Implementation of secure user authentication using JWT (JSON Web Token) for robust access control and identity verification.
- **Search and Filter:**
	- Implementation of advanced search and filter functionalities to elevate the book browsing experience, allowing users to find specific information efficiently.
- **Account Management:**
	- User-friendly operations for managing user accounts, enabling users to retrieve, update, or delete their account information.
- **Swagger:**
	- Seamless integration of Swagger UI or ReDoc for comprehensive API documentation. This ensures developers have clear and accessible documentation to understand and utilize the API effectively.

## 🔧 Technologies Used

- **Django:** 
	- A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **PostgreSQL:** 
	- A powerful open-source relational database management system used for data storage.
- **JWT Authentication:** 
	- Implementing JSON Web Token authentication for secure user authentication.
- **Pydantic:** 
	- A data validation and settings management library for Python, often used with FastAPI.
- **Gunicorn:** 
	- A Python WSGI HTTP server for UNIX, used for deploying Django applications in production.
- **Django ORM:** 
	- Django's built-in Object-Relational Mapping (ORM) library for database interactions, used for managing book data.
- **Django Rest Framework (DRF):** 
	- A powerful toolkit for building Web APIs in Django, used for creating RESTful endpoints for book management.

## 🚀 API Endpoints

![image](https://github.com/aliseyedi01/Library_Api/assets/118107025/52cb714a-2297-4eb6-973b-c66abc9a618d)

## 🗃️ Database

![image](https://github.com/aliseyedi01/Library_Api/assets/118107025/2719d623-8a2b-43d8-a743-aad32d5c5b7f)

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/aliseyedi01/Django-Bookshelf-API.git
```

2. **Navigate to the project directory:**

   ```bash
   Django-Bookshelf-API
   ```

3. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment:**

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

1. **Run Django migrations:**

   ```bash
   python manage.py migrate
   ```

   This will apply any pending database migrations.

2. **Run the Django development server:**

   ```bash
   python manage.py runserver
   ```

   The API will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

3. **Access the Swagger UI and ReDoc:**

   - Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
   - ReDoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## 🤝 Contributing

Feel free to contribute to the project. Fork the repository, make changes, and submit a pull request.

## 📝 License

This project is licensed under the [MIT License](LICENSE).
