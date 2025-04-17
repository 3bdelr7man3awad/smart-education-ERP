# Smart Education ERP System API Documentation

## Overview
This document provides comprehensive documentation for the Smart Education ERP System API. The API follows RESTful principles and uses JSON for data exchange.

## Base URL
```
https://api.smartedu-erp.com/v1
```

## Authentication
All API requests require authentication using JWT (JSON Web Tokens). Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Rate Limiting
- Standard users: 100 requests per minute
- Admin users: 500 requests per minute
- System users: 1000 requests per minute

## Error Handling
All errors follow this format:
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {
            // Additional error details
        }
    }
}
```

## Common HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## API Endpoints

### Authentication
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout
- POST /auth/forgot-password
- POST /auth/reset-password

### User Management
- GET /users
- POST /users
- GET /users/{id}
- PUT /users/{id}
- DELETE /users/{id}
- GET /users/{id}/roles
- PUT /users/{id}/roles

### Academic Management
- GET /courses
- POST /courses
- GET /courses/{id}
- PUT /courses/{id}
- DELETE /courses/{id}
- GET /courses/{id}/students
- GET /courses/{id}/teachers

### Assessment
- GET /assessments
- POST /assessments
- GET /assessments/{id}
- PUT /assessments/{id}
- DELETE /assessments/{id}
- POST /assessments/{id}/submit
- GET /assessments/{id}/results

### AI Features
- POST /ai/grade
- POST /ai/predict
- POST /ai/recommend
- POST /ai/chat

### Analytics
- GET /analytics/performance
- GET /analytics/attendance
- GET /analytics/engagement
- GET /analytics/predictions

## Data Models

### User
```json
{
    "id": "string",
    "username": "string",
    "email": "string",
    "role": "string",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Course
```json
{
    "id": "string",
    "name": "string",
    "code": "string",
    "description": "string",
    "teacher_id": "string",
    "start_date": "date",
    "end_date": "date",
    "status": "string"
}
```

### Assessment
```json
{
    "id": "string",
    "course_id": "string",
    "title": "string",
    "type": "string",
    "due_date": "datetime",
    "total_marks": "number",
    "status": "string"
}
```

## Pagination
All list endpoints support pagination using query parameters:
- page: Page number (default: 1)
- limit: Items per page (default: 20)
- sort: Field to sort by
- order: Sort order (asc/desc)

## Versioning
API versioning is handled through the URL path. The current version is v1.

## Security
- All requests must use HTTPS
- JWT tokens expire after 24 hours
- Refresh tokens expire after 30 days
- Rate limiting is enforced per IP and user
- Input validation is performed on all endpoints
- SQL injection prevention is implemented
- XSS protection is enabled 