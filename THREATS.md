# TrustVault – Security Threat Model

## 1. Introduction

TrustVault is a secure document-sharing application developed using Django. This document identifies possible security threats and describes the security measures implemented or planned to protect user documents.

## 2. Assets to Protect

- User login credentials
- Uploaded documents
- Document ownership information
- Document sharing permissions
- Audit log records
- Application secret key

## 3. Security Threats and Mitigation

| Threat | Description | Mitigation |
|---|---|---|
| Unauthorized Access | Users may try to access documents belonging to others. | Login authentication and ownership checks. |
| Broken Access Control | A user may download a document without permission. | Read and edit permission verification. |
| Malicious File Upload | An attacker may upload an unwanted file. | Extension and file-size validation. Additional content validation is planned. |
| Cross-Site Request Forgery (CSRF) | An attacker may attempt unauthorized requests. | Django CSRF protection and CSRF tokens in forms. |
| Secret Key Exposure | Application secrets may be exposed in source code. | Environment variable-based secret key configuration. |
| Data Tampering | Unauthorized users may try to modify documents or permissions. | Ownership and edit permission checks. |
| Audit Log Tampering | Users may try to modify activity records. | Audit logs are read-only through Django Admin. |
| Brute Force Login | Attackers may repeatedly guess passwords. | Login rate limiting is planned. |

## 4. Implemented Security Controls

- Django authentication for protected views.
- Document ownership verification.
- Read and edit permission checks.
- File extension validation.
- Maximum upload size of 5 MB.
- CSRF tokens in upload, login, and sharing forms.
- Audit logging for important document activities.
- Secret key stored through an environment variable.
- Audit log records cannot be edited or deleted through Django Admin.

## 5. Planned Security Improvements

- Validate actual file content and MIME type.
- Add login rate limiting.
- Configure HTTPS for production.
- Set DEBUG to False in production.
- Configure secure cookies and allowed hosts.
- Add automated security tests.
- Use secure file storage and access controls.
- Review permissions and error handling.

## 6. Conclusion

TrustVault includes authentication, authorization, file validation, and audit logging to reduce common security risks. Further testing and production hardening are required before real-world deployment.