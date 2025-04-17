# Database Schema Specification

## User Management

### User
```sql
- id: UUID (Primary Key)
- email: String (Unique)
- password_hash: String
- role: Enum ['admin', 'teacher', 'student', 'parent', 'staff']
- first_name: String
- last_name: String
- phone: String
- status: Enum ['active', 'inactive', 'suspended']
- created_at: Timestamp
- updated_at: Timestamp
- last_login: Timestamp
```

### Student Profile
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key -> User)
- student_id: String (Unique)
- date_of_birth: Date
- gender: Enum ['male', 'female', 'other']
- address: Text
- enrollment_date: Date
- current_grade: String
- section: String
- academic_status: Enum ['enrolled', 'graduated', 'withdrawn']
- blood_group: String
- nationality: String
```

### Parent/Guardian
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key -> User)
- student_id: UUID (Foreign Key -> Student)
- relationship: String
- occupation: String
- work_phone: String
- emergency_contact: Boolean
```

### Teacher Profile
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key -> User)
- employee_id: String (Unique)
- department: String
- designation: String
- joining_date: Date
- qualifications: JSON
- specializations: Array<String>
```

## Academic Management

### Department
```sql
- id: UUID (Primary Key)
- name: String
- code: String (Unique)
- head_id: UUID (Foreign Key -> Teacher)
- description: Text
- created_at: Timestamp
```

### Course
```sql
- id: UUID (Primary Key)
- code: String (Unique)
- name: String
- department_id: UUID (Foreign Key -> Department)
- description: Text
- credits: Float
- level: String
- prerequisites: Array<UUID> (Foreign Keys -> Course)
- syllabus: Text
- learning_outcomes: JSON
- max_students: Integer
- status: Enum ['active', 'inactive', 'archived']
```

### Class Section
```sql
- id: UUID (Primary Key)
- course_id: UUID (Foreign Key -> Course)
- teacher_id: UUID (Foreign Key -> Teacher)
- academic_year: String
- semester: String
- room: String
- schedule: JSON
- max_capacity: Integer
```

### Enrollment
```sql
- id: UUID (Primary Key)
- student_id: UUID (Foreign Key -> Student)
- section_id: UUID (Foreign Key -> Class Section)
- enrollment_date: Date
- status: Enum ['enrolled', 'dropped', 'completed']
- grade: String
- attendance_percentage: Float
```

## Assessment Management

### Assignment
```sql
- id: UUID (Primary Key)
- section_id: UUID (Foreign Key -> Class Section)
- title: String
- description: Text
- type: Enum ['homework', 'quiz', 'project', 'exam']
- due_date: Timestamp
- total_points: Float
- weight_percentage: Float
- rubric: JSON
- allow_late_submission: Boolean
- late_penalty: Float
- auto_grade: Boolean
```

### Submission
```sql
- id: UUID (Primary Key)
- assignment_id: UUID (Foreign Key -> Assignment)
- student_id: UUID (Foreign Key -> Student)
- submitted_at: Timestamp
- content: Text
- attachments: Array<String>
- status: Enum ['draft', 'submitted', 'graded']
- grade: Float
- feedback: Text
- graded_by: UUID (Foreign Key -> User)
- graded_at: Timestamp
```

### Grade
```sql
- id: UUID (Primary Key)
- student_id: UUID (Foreign Key -> Student)
- course_id: UUID (Foreign Key -> Course)
- assignment_id: UUID (Foreign Key -> Assignment)
- score: Float
- max_score: Float
- weight: Float
- comments: Text
- graded_by: UUID (Foreign Key -> User)
- graded_at: Timestamp
```

## Attendance Management

### Attendance
```sql
- id: UUID (Primary Key)
- student_id: UUID (Foreign Key -> Student)
- section_id: UUID (Foreign Key -> Class Section)
- date: Date
- status: Enum ['present', 'absent', 'late', 'excused']
- remarks: Text
- recorded_by: UUID (Foreign Key -> User)
```

## Communication

### Notification
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key -> User)
- title: String
- message: Text
- type: Enum ['announcement', 'assignment', 'grade', 'attendance', 'system']
- priority: Enum ['low', 'medium', 'high']
- read: Boolean
- created_at: Timestamp
```

### Message
```sql
- id: UUID (Primary Key)
- sender_id: UUID (Foreign Key -> User)
- recipient_id: UUID (Foreign Key -> User)
- subject: String
- content: Text
- read: Boolean
- created_at: Timestamp
```

## AI and Analytics

### StudentPerformanceMetrics
```sql
- id: UUID (Primary Key)
- student_id: UUID (Foreign Key -> Student)
- course_id: UUID (Foreign Key -> Course)
- attendance_rate: Float
- assignment_completion_rate: Float
- average_grade: Float
- participation_score: Float
- risk_level: Enum ['low', 'medium', 'high']
- predictions: JSON
- last_updated: Timestamp
```

### LearningAnalytics
```sql
- id: UUID (Primary Key)
- student_id: UUID (Foreign Key -> Student)
- content_type: String
- interaction_type: String
- duration: Integer
- completion_status: Boolean
- difficulty_level: Float
- effectiveness_score: Float
- timestamp: Timestamp
```

### AIFeedback
```sql
- id: UUID (Primary Key)
- student_id: UUID (Foreign Key -> Student)
- assignment_id: UUID (Foreign Key -> Assignment)
- feedback_type: String
- content: Text
- confidence_score: Float
- generated_at: Timestamp
``` 