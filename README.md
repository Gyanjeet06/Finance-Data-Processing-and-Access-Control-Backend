# **Finance Data Processing and Access Control Backend**

A robust, logically structured RESTful API backend for a finance dashboard system. This project implements role-based access control (RBAC), financial record management, and dashboard analytics aggregation using FastAPI, SQLAlchemy, and SQLite.

This project was built to demonstrate clean backend architecture, strict access control, and efficient data aggregation.

## **🏗️ Architecture & Design Choices**

The project follows a layered architectural pattern to ensure separation of concerns, maintainability, and scalability.

* **app/api/**: Contains the route controllers and dependencies. Separated by domain (auth, users, records, stats).  
* **app/crud/**: Houses all database interactions and business logic. Keeps the API layer thin and routes testable.  
* **app/models/**: SQLAlchemy ORM models defining the database schema.  
* **app/schemas/**: Pydantic models for strict request/response data validation and serialization.  
* **app/core/**: Configuration management and security utilities (JWT, password hashing).  
* **app/db/**: Database session management and base classes.

## **✨ Core Features & Assignment Mapping**

### **1\. User and Role Management**

* **Implementation**: JWT-based authentication via OAuth2 with hashed passwords (bcrypt).  
* **Roles Enforced**:  
  * viewer: Can access dashboard summaries and trends.  
  * analyst: Can view financial records and access dashboard summaries/trends.  
  * admin: Full CRUD access to all users and financial records.  
* **Open Registration**: By default, new users register with the viewer role to ensure safe defaults.

### **2\. Financial Records Management**

* **Implementation**: Full CRUD endpoints for managing financial entries (income / expense).  
* **Filtering**: Records can be filtered natively via query parameters (category, entry\_type, start\_date, end\_date).

### **3\. Dashboard Summary APIs**

* **Implementation**: Aggregation logic handled at the CRUD layer to minimize memory overhead.  
* **Endpoints**:  
  * /api/v1/stats/summary: Returns total income, total expenses, net balance, category-wise totals, and recent activity.  
  * /api/v1/stats/trends: Returns a grouped monthly trend analysis.

### **4\. Access Control Logic**

* **Implementation**: Enforced via FastAPI Dependency Injection (require\_roles guard in app/api/deps.py).  
* **Benefit**: This acts as a centralized middleware policy check. If a user's role is not in the allowed list, a 403 Forbidden is immediately raised before the route logic ever executes.

### **5\. Validation and Error Handling**

* **Implementation**: Leveraging Pydantic for strict input validation (e.g., ensuring entry\_type is only "income" or "expense" via Literal).  
* Custom HTTP exceptions are raised for business logic errors (e.g., 404 Not Found for missing records, 400 Bad Request for duplicate emails).

### **6\. Data Persistence & Data Modeling**

* **Database**: SQLite (via SQLAlchemy). Chosen for simplicity and zero-configuration setup for evaluation purposes.  
* **Relationships**: A one-to-many relationship is established between User and Record (cascading deletes ensure orphan records are removed if an admin deletes a user).

## **🚀 Setup & Installation**

### **Prerequisites**

* Python 3.10+

### **1\. Create a Virtual Environment**

python \-m venv .venv  
source .venv/bin/activate  \# On Windows: .venv\\Scripts\\activate

### **2\. Install Dependencies**

pip install \-r requirements.txt

### **3\. Environment Configuration**

Create a .env file in the root directory:

DATABASE\_URL=sqlite:///./finance.db  
SECRET\_KEY=your\_super\_secret\_key\_here  
ACCESS\_TOKEN\_EXPIRE\_MINUTES=60

### **4\. Run the Application**

uvicorn app.main:app \--reload \--port 8000

The API documentation will be available at: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

### **5\. Run Tests**

pytest

## **📖 API Endpoints Overview**

| Method | Endpoint | Role Required | Description |
| :---- | :---- | :---- | :---- |
| **POST** | /api/v1/auth/token | *Public* | Authenticate and receive JWT |
| **POST** | /api/v1/users/ | *Public* | Register a new user (defaults to viewer) |
| **GET** | /api/v1/users/me | *Any* | Get current authenticated user |
| **GET** | /api/v1/users/ | admin | List all system users |
| **PATCH** | /api/v1/users/{id} | admin | Update a user's role or active status |
| **POST** | /api/v1/records/ | admin | Create a financial record |
| **GET** | /api/v1/records/ | analyst, admin | List/filter financial records |
| **PUT** | /api/v1/records/{id} | admin | Update a specific record |
| **DELETE** | /api/v1/records/{id} | admin | Delete a specific record |
| **GET** | /api/v1/stats/summary | viewer, analyst, admin | Get dashboard KPIs and recent activity |
| **GET** | /api/v1/stats/trends | analyst, admin | Get monthly income/expense trends |

## **🧠 Assumptions & Trade-offs**

1. **Database Choice**: SQLite is used for immediate evaluability. Thanks to SQLAlchemy, transitioning to PostgreSQL (which would be used in a real production environment) only requires updating the DATABASE\_URL and installing asyncpg or psycopg2.  
2. **Dashboard Logic**: The dashboard aggregations currently fetch records and aggregate in Python memory. For a highly scaled production application, these aggregations would be pushed down to the database level using GROUP BY SQL queries to reduce memory footprint.  
3. **Soft Deletes**: To keep the implementation clean and focused on the core assignment requirements, physical deletes were implemented. In a real-world financial system, a soft-delete mechanism (e.g., an is\_deleted boolean) would be utilized for compliance.

## **🛠️ Potential Future Enhancements**

* **Dockerization**: Wrapping the application and a PostgreSQL database in a docker-compose.yml for isolated deployment.  
* **Pagination**: Adding limit and offset pagination to the GET /records/ endpoint.  
* **Caching**: Implementing Redis caching for the /stats/summary and /stats/trends endpoints since dashboard data is read-heavy.