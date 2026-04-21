# API Documentation

## Authentication
All endpoints require a session cookie. Authenticate via the `/login` page or by sending a POST request with the password.

## Endpoints

### 1. `POST /attack`
Triggers a new attack in the background.

**Payload:**
```json
{
  "phone": "09123456789",
  "amount": 5,
  "services": ["EZLOAN", "LBC"]
}
```
*Note: If `services` is null or omitted, all services are used.*

**Response:**
```json
{
  "success": true
}
```
*Errors:* `400 Bad Request` (Invalid format), `429 Too Many Requests` (Attack in progress).

### 2. `GET /status`
Returns the current status of the background attack and recently generated logs.

**Response:**
```json
{
  "active": true,
  "success": 10,
  "failed": 2,
  "logs": [
    {"msg": "Batch 1/5 completed: 2 OK, 0 FAIL", "type": "info"}
  ]
}
```
*Note: `logs` are cleared after being read.*

### 3. `GET /logout`
Clears the session.
