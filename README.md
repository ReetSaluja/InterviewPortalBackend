# Interview Backend API

A FastAPI-based backend application for managing interviews, candidates, and interviewers. This RESTful API provides endpoints for user authentication, candidate management, and interviewer operations.

## Features

- 🔐 **User Authentication**: Register, login, password management
- 👥 **User Management**: Role-based access (Admin/Interviewer)
- 📋 **Candidate Management**: Create, read, update candidates with resume upload
- 👨‍💼 **Interviewer Management**: Fetch all interviewers
- 📄 **Pagination**: Paginated candidate listings
- 🔍 **Email Verification**: Check if email exists in the system
- 🌐 **CORS Enabled**: Configured for frontend integration

## Tech Stack

- **Framework**: FastAPI 0.115.5
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Python Version**: 3.11+
- **Server**: Uvicorn
- **Validation**: Pydantic 2.10.3

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd Back
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

1. **Create a `.env` file** in the root directory:
   ```bash
   touch .env
   ```

2. **Add your database URL** to the `.env` file:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```
   
   Example:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/interview_db
   ```

## Running the Application

1. **Make sure your virtual environment is activated**

2. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

   The `--reload` flag enables auto-reload on code changes.

3. **Access the API**:
   - **API Base URL**: http://127.0.0.1:8000
   - **Interactive API Docs (Swagger UI)**: http://127.0.0.1:8000/docs
   - **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc

   The root endpoint (`/`) automatically redirects to `/docs`.

## API Endpoints

### Authentication (`/auth`)

#### Register User
- **POST** `/auth/register`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "role": "admin"  // or "interviewer"
  }
  ```
- **Response**: User details (id, email, role)

#### Login
- **POST** `/auth/login`
- **Description**: Authenticate user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**: User details (id, email, role)

#### Get Users by Role
- **GET** `/auth/users?role=admin`
- **Description**: Get all users filtered by role
- **Query Parameters**:
  - `role` (required): "admin" or "interviewer"
- **Response**: Array of user objects

#### Check Email Exists
- **GET** `/auth/check-email?email=user@example.com`
- **Description**: Check if an email exists in the database
- **Query Parameters**:
  - `email` (required): Email address to check
- **Response**:
  ```json
  {
    "exists": true  // or false
  }
  ```

#### Update Password
- **PUT** `/auth/update-password`
- **Description**: Update user password
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "new_password": "newpassword123"
  }
  ```
- **Response**: Updated user details (id, email, role)

### Candidates (`/candidates`)

#### Create Candidate
- **POST** `/candidates/`
- **Description**: Create a new candidate with optional resume upload
- **Request**: Form data (multipart/form-data)
  - `CandidateName` (required)
  - `TotalExperience` (required)
  - `SkillSet` (required)
  - `CurrentOrganization` (required)
  - `NoticePeriod` (required)
  - `Feedback` (optional)
  - `Remarks` (optional)
  - `ClientName` (optional)
  - `ClientManagerName` (optional)
  - `InterviewerId` (optional)
  - `resume` (optional): File upload
- **Response**: Created candidate object

#### Get All Candidates
- **GET** `/candidates/`
- **Description**: Get all candidates
- **Response**: Array of candidate objects

#### Get Candidates (Paginated)
- **GET** `/candidates/paginated?skip=0&limit=10`
- **Description**: Get candidates with pagination
- **Query Parameters**:
  - `skip` (optional, default: 0): Number of records to skip
  - `limit` (optional, default: 10): Number of records to return
- **Response**: Paginated candidate data

#### Update Candidate
- **PUT** `/candidates/{candidate_id}`
- **Description**: Update candidate information
- **Path Parameters**:
  - `candidate_id` (required): ID of the candidate
- **Request Body**:
  ```json
  {
    "CandidateName": "John Doe",  // optional
    "TotalExperience": "5 years",  // optional
    "SkillSet": "Python, FastAPI",  // optional
    "CurrentOrganization": "Tech Corp",  // optional
    "NoticePeriod": "30 days",  // optional
    "Feedback": "Good candidate",  // optional
    "Remarks": "Technical round passed"  // optional
  }
  ```
- **Response**: Updated candidate object

### Interviewers (`/interviewers`)

#### Get All Interviewers
- **GET** `/interviewers/`
- **Description**: Get all interviewers
- **Response**: Array of interviewer objects
  ```json
  [
    {
      "id": 1,
      "InterviewerName": "Jane Smith",
      "PrimarySkill": "Python",
      "Proficiency": 8
    }
  ]
  ```

## Project Structure

```
Back/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── db/
│   └── database.py        # Database configuration and session management
├── models/
│   └── models.py          # SQLAlchemy models (User, Candidate, Interviewer)
├── schemas/
│   └── schemas.py         # Pydantic schemas for request/response validation
├── routers/
│   ├── auth_router.py     # Authentication endpoints
│   ├── candidate_router.py # Candidate management endpoints
│   └── interviewer_router.py # Interviewer endpoints
├── services/
│   ├── auth_service.py    # Authentication business logic
│   ├── candidate_service.py # Candidate business logic
│   └── Interviewer_service.py # Interviewer business logic
└── repository/
    ├── user_repository.py # User data access layer
    ├── candidate_repository.py # Candidate data access layer
    └── interview_repository.py # Interview data access layer
```

## Database Models

### User
- `id`: Integer (Primary Key)
- `email`: String (Unique, Indexed)
- `password`: String
- `role`: Enum (admin, interviewer)

### Candidate
- `id`: Integer (Primary Key)
- `CandidateName`: String
- `TotalExperience`: String
- `SkillSet`: String
- `CurrentOrganization`: String
- `NoticePeriod`: String
- `Feedback`: String (Optional)
- `Remarks`: String (Optional)
- `ClientName`: String (Optional)
- `ClientManagerName`: String (Optional)
- `InterviewerId`: Integer (Optional)
- `ResumePath`: String (Optional)

### Interviewer
- `id`: Integer (Primary Key)
- `InterviewerName`: String
- `PrimarySkill`: String
- `Proficiency`: Integer

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (Vite default port)
- `http://127.0.0.1:3000` (React default port)

To add more origins, modify the `origins` list in `main.py`.

## Error Handling

The API returns standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors, invalid input)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default:
```bash
uvicorn main:app --reload
```

### Code Structure

The project follows a layered architecture:
1. **Routers**: Handle HTTP requests and responses
2. **Services**: Contain business logic
3. **Repository**: Handle database operations
4. **Models**: Define database schema
5. **Schemas**: Define request/response validation

## Notes

- Database tables are automatically created on application startup
- Passwords are stored in plain text (consider implementing password hashing for production)
- The API uses Pydantic V2 with `from_attributes = True` for ORM mode
- File uploads are supported for candidate resumes

## License

This project is part of an interview management system.

## Support

For issues or questions, please refer to the API documentation at `/docs` endpoint.

