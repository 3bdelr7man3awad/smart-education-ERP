from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    students,
    teachers,
    courses,
    assignments,
    grades,
    attendance,
    notifications
)
from app.api.endpoints import study_assistant

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
api_router.include_router(grades.router, prefix="/grades", tags=["Grades"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(study_assistant.router, prefix="/study-assistant", tags=["AI Study Assistant"]) 