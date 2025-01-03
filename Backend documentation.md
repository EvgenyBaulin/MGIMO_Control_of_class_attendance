# **API Overview**

1. **Authentication**:
    - Uses **JWT** (JSON Web Tokens).
    - Obtain tokens via `POST /api/login/`.
    - Include `"Authorization: Bearer <ACCESS_TOKEN>"` in request headers to access protected resources.

2. **Roles**:
    - **Student**: Can register themselves, log in, and scan NFC tags to record attendance.
    - **Instructor**: Needs a secret key to register. Has additional privileges (managing groups, auditoriums, lectures, and viewing attendance reports).

3. **Data Entities**:
    - **Group**: Student grouping (e.g., by year or class).
    - **User**: Custom user model with `role` field (`student` or `instructor`) and optional `group`.
    - **Auditorium**: Physical location with an NFC code and a corresponding NFC link.
    - **Lecture**: Session with `title`, `date`, `start_time`, `end_time`, and associated auditorium.
    - **Attendance**: Records a student’s presence at a lecture, along with a timestamp.

---

# **Authentication and Tokens**

## **1. Obtain JWT Token**
**Endpoint**: `POST /api/login/`  
**Description**: Logs in a user (student or instructor) and returns a JWT pair (access & refresh tokens).

- **Request Body** (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "somepassword"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "refresh": "<REFRESH_TOKEN>",
    "access": "<ACCESS_TOKEN>"
  }
  ```
- **Possible Status Codes**:
    - **200 OK**: Login successful.
    - **401 Unauthorized**: Invalid credentials.

## **2. Refresh JWT Token**
**Endpoint**: `POST /api/token/refresh/`  
**Description**: Exchanges a **refresh** token for a new **access** token.

- **Request Body** (JSON):
  ```json
  {
    "refresh": "<REFRESH_TOKEN>"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "access": "<NEW_ACCESS_TOKEN>"
  }
  ```
- **Possible Status Codes**:
    - **200 OK**: Token refreshed successfully.
    - **401 Unauthorized**: Invalid or expired refresh token.

---

# **User Management**

## **1. Student Registration**
**Endpoint**: `POST /api/register/student/`  
**Description**: Registers a new student user. Students **do not** need a secret key.

- **Request Body** (JSON):
  ```json
  {
    "email": "student@example.com",
    "username": "studentUser",
    "password": "strongpassword",
    "group": 1
  }
  ```
- **Response** (JSON):
  ```json
  {
    "message": "Student registered successfully!"
  }
  ```
- **Possible Status Codes**:
    - **201 Created**: Registration successful.
    - **400 Bad Request**: Invalid data (e.g., missing fields, email already in use).

## **2. Instructor Registration**
**Endpoint**: `POST /api/register/instructor/`  
**Description**: Registers a new instructor. Requires a **secret key**.

- **Request Body** (JSON):
  ```json
  {
    "email": "instructor@example.com",
    "username": "instructorUser",
    "password": "secretpassword",
    "secret_key": "MY_SECRET_KEY"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "message": "Instructor registered successfully!"
  }
  ```
- **Possible Status Codes**:
    - **201 Created**: Registration successful.
    - **403 Forbidden**: Incorrect secret key.
    - **400 Bad Request**: Invalid data.

---

# **Group Management**

## **1. Create Group**
**Endpoint**: `POST /api/groups/`  
**Headers**:
- `Authorization: Bearer <ACCESS_TOKEN>` (**Instructor** token)

- **Request Body** (JSON):
  ```json
  {
    "name": "Group 101"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "id": 1,
    "name": "Group 101"
  }
  ```
- **Possible Status Codes**:
    - **201 Created**: Group created.
    - **403 Forbidden** or **401 Unauthorized**: If request is not made by an instructor.

## **2. List Groups**
**Endpoint**: `GET /api/groups/`  
**Headers**:
- `Authorization: Bearer <ACCESS_TOKEN>` (**Instructor** token)

- **Response** (JSON array):
  ```json
  [
    {
      "id": 1,
      "name": "Group 101"
    },
    {
      "id": 2,
      "name": "Group 102"
    }
  ]
  ```
- **Possible Status Codes**:
    - **200 OK**: Returns all groups.
    - **401 Unauthorized**: Missing or invalid JWT token.
    - **403 Forbidden**: User is not an instructor.

---

# **Auditorium and NFC Management**

## **1. Create Auditorium**
**Endpoint**: `POST /api/auditoriums/`  
**Headers**:
- `Authorization: Bearer <ACCESS_TOKEN>` (**Instructor** token)

- **Request Body** (JSON):
  ```json
  {
    "name": "Auditorium 101"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "id": 1,
    "name": "Auditorium 101",
    "nfc_code": "some_auto_generated_code",
    "nfc_link": "http://example.com/attendance?code=some_auto_generated_code"
  }
  ```
- **Possible Status Codes**:
    - **201 Created**: Auditorium created with an auto-generated NFC code.
    - **403 Forbidden** or **401 Unauthorized**: If request is not made by an instructor.

## **2. List Auditoriums**
**Endpoint**: `GET /api/auditoriums/`  
**Headers**:
- `Authorization: Bearer <ACCESS_TOKEN>`

- **Response** (JSON array):
  ```json
  [
    {
      "id": 1,
      "name": "Auditorium 101",
      "nfc_code": "some_auto_generated_code",
      "nfc_link": "http://example.com/attendance?code=some_auto_generated_code"
    },
    {
      "id": 2,
      "name": "Auditorium 202",
      "nfc_code": "abc123xyz",
      "nfc_link": "http://example.com/attendance?code=abc123xyz"
    }
  ]
  ```
- **Possible Status Codes**:
    - **200 OK**
    - **401 Unauthorized**: Missing or invalid token.

---

# **Lecture Management**

## **1. Create Lecture**
**Endpoint**: `POST /api/lectures/`  
**Headers**:
- `Authorization: Bearer <ACCESS_TOKEN>` (**Instructor** token)

- **Request Body** (JSON):
  ```json
  {
    "title": "Mathematics 101",
    "date": "2025-01-31",
    "start_time": "10:00",
    "end_time": "11:30",
    "auditorium": 1
  }
  ```
- **Response** (JSON):
  ```json
  {
    "id": 10,
    "title": "Mathematics 101",
    "date": "2025-01-31",
    "start_time": "10:00:00",
    "end_time": "11:30:00",
    "auditorium": 1
  }
  ```
- **Possible Status Codes**:
    - **201 Created**: Lecture created.
    - **400 Bad Request**: Missing or invalid fields.
    - **403 Forbidden** or **401 Unauthorized**: If not an instructor.

---

# **Attendance Tracking**

## **1. Record Attendance via NFC**
**Endpoint**: `POST /api/attendance/`  
**Headers**:
- `Authorization: Bearer <ACCESS_TOKEN>` (**Student** token)

- **Request Body** (JSON):
  ```json
  {
    "code": "abc123xyz"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "message": "Attendance recorded"
  }
  ```
- **Possible Status Codes**:
    - **201 Created**: Attendance recorded.
    - **200 OK**: Attendance already recorded.
    - **404 Not Found**: NFC code not valid.

---

# **Error Handling**

- **400 Bad Request**: Missing or invalid input data.
- **401 Unauthorized**: The request lacks a valid JWT token or credentials.
- **403 Forbidden**: The user does not have permission (e.g., a student trying an instructor-only endpoint).
- **404 Not Found**: Resource doesn’t exist.
- **500 Internal Server Error**: Unexpected server error.

