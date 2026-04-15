# Civic Intelligence System – Complaint Service

Microservice for complaint registration, and comment handling.

---
## Overview

This service provides APIs for:

- Complaint creation and updates  
- Complaint listing and retrieval  
- Comment creation and discussion tracking  

---

## Services

| Service | Base URL | Description |
|--------|--------|------------|
| Complaints Service | (domain or in case of local http://localhost) | Complaint and comment management |

---

## Complaint APIs


### 1. Register Complaint

POST /register_complaint  
URL: Base URL  

Request Body:
{
  "category": 1, // Category text mapping can be managed using json
  "subcategory": 2, // Category text mapping can be managed using json
  "location": "Indore Madhya Pradesh",
  "location_url": "https://www.google.com/maps/search/Indore+Madhya+Pradesh/",
  "complaint": "Drainage Blocked in my locality",
  "file": "file_path",
  "status": 1, // Status text mapping can be managed using json
  "complainer": 1,
  "officer": 1
}

---

### 2. Update Complaint

POST /update_complaint  
URL: Base URL  

Request Body:
{
  "id": 101,
  "status": 3,
  "complainer": 1
}

---

### 3. Get Complaints

GET /complaints/{user_id}  
URL: Base URL  

Request Body (User-based):
{}

Use Cases:
- Fetch all complaints for a user  
- Fetch specific complaint details  
- Filter complaints  

### 4. Get Complaint

GET /get_complaint/{complaint_id}
URL: Base URL  

Request Body (Complaint-based):
{}

Use Cases:
- Fetch specific complaint details  

---

## Comment APIs

---

### 5. Add Comment

POST /comment  
URL: Base URL  

Request Body:
{
  "complaint_id": 101,
  "user_id": 1,
  "comment": "We are reviewing this complaint."
}

---

### 6. Get Comments

GET /comments/{complaint_id}  
URL: Base URL  

Request Body:
{}

Note: This endpoint is reused for comments. Consider separating into a dedicated /comments endpoint.

---

## Example Workflow

Complaint Flow:
1. Register complaint  
2. Fetch complaints  
3. Update complaint  
4. Fetch a complaint
5. Add comment  
6. Fetch comments  

---
## Collection

Postman Collection Name: Complaints  

Main Requests:
- Register Complaint  
- Update Complaint  
- Complaints  
- Add Comment  
- Comments  