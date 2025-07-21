
# 🎯 Interview Coding Exercise – FastAPI CRUD Stack (45 min)

This repository contains a **dummy FastAPI application**. During the live session you will extend it by touching multiple layers (models → CRUD helpers → routes → schemas).  
Choose **one** of the tasks below (the interviewer will assign it) and complete as much as you can within the allotted 30 minutes of coding time.

---

## ⏰ Interview Agenda (45 min total)

| Segment | Activity | Lead | Time |
|---------|----------|------|------|
| 1 | Environment check & quick walkthrough of existing code | Interviewer | **5 min** |
| 2 | Coding task (implementation) | Candidate | **30 min** |
| 3 | Demo & technical discussion | Candidate / Interviewer | **8 min** |
| 4 | Wrap‑up & next steps | Interviewer | **2 min** |

---

## 📋 Task Options

### Task 1 – Add **Department** support (many‑to‑one)

| # | Sub‑task | File(s) to touch | Est. time |
|---|----------|------------------|-----------|
| 1 | Create `Department` model (`id`, `name`) and add `department_id` FK + relationship on `Employee` | `models.py` | 5 min |
| 2 | CRUD helpers: `create_department`, `get_departments`, `assign_employee_department` | `crud.py` | 8 min |
| 3 | Pydantic schemas: `DepartmentCreate`, `DepartmentRead`; extend employee read schema | *(schemas file)* | 4 min |
| 4 | Routes: `POST /departments/`, `GET /departments/`, `PUT /employees/{id}/department/{dept_id}` | `main.py` | 10 min |
| 5 | Smoke‑test with httpie/Postman | – | 3 min |
| **Total** | | | **30 min** |

---

### Task 2 – Implement **Attendance Summary** endpoint

| # | Sub‑task | File(s) to touch | Est. time |
|---|----------|------------------|-----------|
| 1 | Write helper `attendance_summary(employee_id, start, end)` to aggregate worked hours | `crud.py` | 8 min |
| 2 | Define response schema `AttendanceSummaryRead` | *(schemas file)* | 3 min |
| 3 | New route `GET /attendance/summary?employee_id=&start=&end=` | `main.py` | 10 min |
| 4 | Input validation & error handling (open clock‑ins, bad date range) | `main.py` | 6 min |
| 5 | Manual test & showcase result | – | 3 min |
| **Total** | | | **30 min** |

---

### Task 3 – Add **Soft‑Delete & Restore** for employees

| # | Sub‑task | File(s) to touch | Est. time |
|---|----------|------------------|-----------|
| 1 | Add column `is_active: bool = True` to `Employee` | `models.py` | 4 min |
| 2 | Refactor existing fetch helpers to filter `is_active=True` by default | `crud.py` | 6 min |
| 3 | Implement `deactivate_employee` & `restore_employee` helpers | `crud.py` | 5 min |
| 4 | Routes: `DELETE /employees/{id}` (soft delete) & `PUT /employees/{id}/restore` | `main.py` | 10 min |
| 5 | Verify attendances remain intact | – | 5 min |
| **Total** | | | **30 min** |

---

### Task 4 – Add **Search & Filtering** to `/employees/`

| # | Sub‑task | File(s) to touch | Est. time |
|---|----------|------------------|-----------|
| 1 | Extend list route with optional query params (`name`, `city`, `department_id`, `has_open_clockin`) | `main.py` | 10 min |
| 2 | Build dynamic filters in helper function | `crud.py` | 10 min |
| 3 | Update response schema if needed | *(schemas file)* | 3 min |
| 4 | Return paginated results with total count header | `main.py` | 5 min |
| 5 | Quick demo via curl/Postman | – | 2 min |
| **Total** | | | **30 min** |

---

## 📝 Evaluation Rubric

| Area | What we’re looking for |
|------|-----------------------|
| **Correctness** | End‑to‑end functionality; DB schema updates work; async session handling preserved |
| **API design** | RESTful verbs, status codes, clear request/response bodies, helpful error messages |
| **Code quality** | Consistent style with existing project, typing hints, concise naming, doc‑strings |
| **Testing / demo** | Manual or automated demonstration that new routes behave as intended |
| **Communication** | Ability to explain decisions, discuss edge‑cases & trade‑offs |

**Take‑home relevance:** If time permits, suggest how you would extend or harden your solution (tests, auth, caching).

Good luck 🚀
