from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, courses, students, assignments, notifications, organizations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"]) 