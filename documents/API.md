
# TrustVault - API and Application Endpoint Documentation

## 1. Project Overview

TrustVault is a Django-based secure document-sharing web application. It allows authenticated users to upload, view, download, and share documents with other users.

Note: This project currently uses Django web views and HTML forms. It does not currently provide a REST API.

## 2. Base URL

Local development URL:

http://127.0.0.1:8000/

## 3. Authentication

Users must log in to access protected document operations.

Login URL:
- Method: GET, POST
- Endpoint: /login/
- Purpose: Displays the login form and authenticates users.

## 4. Application Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | / | Displays TrustVault welcome message | No |
| GET, POST | /login/ | User login | No |
| GET, POST | /upload/ | Upload a document | Required |
| GET | /my-documents/ | View documents owned by the user | Required |
| GET | /download/<document_id>/ | Download an authorized document | Required |
| GET, POST | /share/<document_id>/ | Share a document with another user | Required |
| GET | /admin/ | Django administration panel | Admin login |

## 5. Upload Document

Endpoint: /upload/

Method: GET, POST

Required form fields:
- title: Document title
- category: Document category (optional)
- file: Document file

Security validations:
- Title is required.
- Allowed extensions: PDF, DOCX, TXT.
- Maximum file size: 5 MB.
- User must be authenticated.

## 6. Download Document

Endpoint: /download/<document_id>/

Method: GET

Purpose:
Downloads a document after checking user permissions.

Access rules:
- Document owner can download.
- Superuser can download.
- Users with read permission can download.
- Users with edit permission can also download.
- Unauthorized users receive HTTP 403 Forbidden.

## 7. Share Document

Endpoint: /share/<document_id>/

Method: GET, POST

Required form fields:
- username: Recipient username
- permission: read or edit

Access rules:
- Only the document owner can share it.
- Users cannot share documents with themselves.
- Only read and edit permissions are accepted.

## 8. My Documents

Endpoint: /my-documents/

Method: GET

Purpose:
Displays documents uploaded by the logged-in user.

## 9. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 302 | Redirect, such as login required |
| 403 | Access forbidden |
| 404 | Resource not found |

## 10. Security Measures

- Django authentication
- Login protection for document operations
- Document ownership verification
- Read and edit permission checks
- CSRF tokens in HTML forms
- File extension validation
- File size validation
- Audit logging for document activities

## 11. Future Improvements

- REST API using Django REST Framework
- Token-based API authentication
- File content and MIME-type validation
- API schema documentation using OpenAPI
- Login rate limiting
