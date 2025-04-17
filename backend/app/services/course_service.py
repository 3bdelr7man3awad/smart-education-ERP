from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def get_course(self, course_id: int) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        return self.db.query(Course).offset(skip).limit(limit).all()

    def create_course(self, course: CourseCreate) -> Course:
        db_course = Course(
            title=course.title,
            description=course.description,
            teacher_id=course.teacher_id
        )
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def update_course(self, course_id: int, course: CourseUpdate) -> Optional[Course]:
        db_course = self.get_course(course_id)
        if not db_course:
            return None
        update_data = course.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_course, field, value)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def delete_course(self, course_id: int) -> bool:
        db_course = self.get_course(course_id)
        if not db_course:
            return False
        self.db.delete(db_course)
        self.db.commit()
        return True 