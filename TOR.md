# AI Development Prompt: Student Attendance Tracking System

**Objective:**  
Develop a simple and quick web application using **Node.js**, **Express.js**, and **SQLite** for tracking student attendance with mandatory registration. Implement **JWT** for authentication and configure **Docker** with `docker-compose.yml`.

**NFC Link Format:**  
All NFC links should follow `{url}/scan/?code=code`.

## **1. Data Models**

### **Group**
- `id`: Auto-increment, Primary Key
- `name`: String, unique

### **Student**
- `id`: Auto-increment, Primary Key
- `full_name`: String (max 200 characters)
- `email`: String, unique
- `group_id`: Foreign Key to `Group`, on_delete=PROTECT

### **Auditorium**
- `id`: Auto-increment, Primary Key
- `name`: String (max 100 characters), unique

### **Tag**
- `id`: Auto-increment, Primary Key
- `tag_id`: String (max 255 characters), unique (16-hex identifier)
- `auditorium_id`: Foreign Key to `Auditorium`, on_delete=CASCADE

### **Lecture**
- `id`: Auto-increment, Primary Key
- `name`: String (max 200 characters)
- `date`: Date
- `start_time`: Time
- `end_time`: Time
- `auditorium_id`: Foreign Key to `Auditorium`, on_delete=CASCADE
- `groups`: Many-to-Many with `Group`

### **Attendance**
- `id`: Auto-increment, Primary Key
- `student_id`: Foreign Key to `Student`, on_delete=CASCADE
- `group_id`: Foreign Key to `Group`, on_delete=CASCADE
- `registration_time`: DateTime, auto_now_add
- `auditorium_id`: Foreign Key to `Auditorium`, on_delete=SET_NULL, nullable
- `tag_id`: Foreign Key to `Tag`, on_delete=SET_NULL, nullable
- `lecture_id`: Foreign Key to `Lecture`, on_delete=SET_NULL, nullable

**Constraints:**
- Unique `(student_id, lecture_id)` in `Attendance`
- Prevent deletion of `Group` if associated `Students` exist

### **Directory Structure**

```
project/
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   ├── app.js
│   ├── models.js
│   ├── routes/
│   ├── controllers/
│   ├── middleware/
│   ├── config/
│   └── database.sqlite
├── frontend/
│   ├── Dockerfile (optional)
│   ├── public/
│   └── views/
└── docker-compose.yml
```

## **5. Additional Requirements**

- **Teacher Registration:** Must provide a valid `secret_key`.
- **Password Security:** Use `bcrypt` for hashing.
- **NFC Link Format:** `{url}/scan/?code=code`.
- **Date & Time Validation:** Ensure `start_time` < `end_time` for lectures.
- **Access Control:** Only `TEACHER` role can manage lectures, tags, and view reports.
- **Error Handling:** Provide clear error messages for all failure cases.
- **Group Deletion Protection:** Prevent deleting a `Group` if it has associated `Students`.


## **7. Example NFC Link**

```
https://yourdomain.com/scan/?code=TAG123456
```

**Functionality:**  
When a student accesses this link, they are directed to the attendance registration page where the `code` identifies the auditorium and the current active lecture.

All extra text i need on russian