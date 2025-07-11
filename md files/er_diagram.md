# ER Diagram: Online Learning Platform (Udemy Clone)

## Tables and Attributes

### User
- id (PK)
- username
- email
- password
- is_instructor

### Profile
- id (PK)
- user_id (FK) → User(id)
- profile_picture

### Course
- id (PK)
- title
- description
- category
- instructor_id (FK) → User(id)
- likes_count

### Enrollment
- id (PK)
- student_id (FK) → User(id)
- course_id (FK) → Course(id)
- enrolled_at

### Lesson
- id (PK)
- course_id (FK) → Course(id)
- title
- video_url
- order

### Like
- id (PK)
- student_id (FK) → User(id)
- course_id (FK) → Course(id)

### CourseProgress
- id (PK)
- student_id (FK) → User(id)
- course_id (FK) → Course(id)
- lesson_id (FK) → Lesson(id)
- completed
- last_updated

### Question
- id (PK)
- student_id (FK) → User(id)
- course_id (FK) → Course(id)
- content
- timestamp

### Answer
- id (PK)
- instructor_id (FK) → User(id)
- question_id (FK) → Question(id)
- content
- timestamp

### Follow
- id (PK)
- student_id (FK) → User(id)
- instructor_id (FK) → User(id)

### Certificate
- id (PK)
- student_id (FK) → User(id)
- course_id (FK) → Course(id)
- issued_at

## Relationships
- A **User** can have one **Profile**.
- A **User** can be a **student** or an **instructor**.
- A **User (instructor)** can create multiple **Courses**.
- A **User (student)** can **enroll** in many **Courses**.
- A **User (student)** can **like** multiple **Courses**.
- A **Course** can have many **Lessons**.
- A **Student** can have **CourseProgress** tracked per **Lesson**.
- **Students** can ask **Questions** in a course.
- **Instructors** can **Answer** questions.
- **Students** can **Follow** instructors.
- **Students** get **Certificates** for completed courses.

