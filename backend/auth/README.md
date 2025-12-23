# OctoVision Authentication Module

FastAPI-based authentication system with JWT and MongoDB, supporting User/Admin roles.

## Features

- **User Registration** (`POST /register`) — Create new user accounts with hashed passwords
- **User Login** (`POST /login`) — Authenticate and receive JWT tokens
- **Role-Based Access Control (RBAC)** — Support for `user` and `admin` roles
- **JWT Token Management** — Secure token generation and validation
- **Protected Endpoints** — Dependencies to enforce authentication and authorization
- **Password Hashing** — bcrypt for secure password storage

## Setup

### 1. Install Dependencies

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r backend/auth/requirements.txt
```

### 2. Configure Environment Variables

Copy the example file and update with your settings:

```bash
cp backend/auth/.env.example backend/auth/.env
```

Edit `backend/auth/.env`:
- `MONGO_URI` — MongoDB connection string (default: `mongodb://localhost:27017`)
- `JWT_SECRET` — Secret key for signing JWT tokens (⚠️ change in production)
- `JWT_EXPIRE_MINUTES` — Token expiration time in minutes (default: 10080 = 7 days)

### 3. Ensure MongoDB is Running

Start MongoDB via Docker Compose:

```bash
docker-compose -f data_infra/docker-compose.yml up -d mongodb
```

Verify connection:

```bash
mongo --host 127.0.0.1 --port 27017 --eval 'db.runCommand({ ping: 1 })'
```

### 4. Run the Server

From the root directory:

```bash
cd backend/auth
export $(cat .env | xargs)  # Load env vars (Linux/Mac)
uvicorn main:app --reload --port 8001
```

Server will be available at `http://localhost:8001`

**API Documentation:**
- OpenAPI Docs: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## API Endpoints

### Register

```bash
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "role": "user"
}
```

### Login

```bash
curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```bash
curl -X GET http://localhost:8001/me \
  -H "Authorization: Bearer <your-token-here>"
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "role": "user"
}
```

### Admin-Only Route (Example)

```bash
curl -X GET http://localhost:8001/admin-only \
  -H "Authorization: Bearer <admin-token-here>"
```

## Testing

Run the test suite:

```bash
pytest backend/auth/test_auth.py -v
```

Test coverage includes:
- User registration (success and duplicate email)
- User login (valid and invalid credentials)
- Token validation
- Role-based access control (user vs admin)
- Protected endpoints

## Database Schema

### Users Collection

```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "hashed_password": "$2b$12$...",
  "role": "user" | "admin"
}
```

## JWT Token Claims

```json
{
  "sub": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "role": "user",
  "exp": 1703448000
}
```

## Integrating with Other Routes

Import the `get_current_user` or `admin_required` dependencies to protect routes:

```python
from backend.auth.main import get_current_user, admin_required

@app.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['email']}"}

@app.delete("/delete-user")
async def delete_user(current_user: dict = Depends(admin_required)):
    # Only admins can delete users
    return {"deleted": True}
```

## Security Notes

- **Always use HTTPS in production** to protect tokens in transit
- **Rotate JWT_SECRET regularly** and never commit it to version control
- **Use strong passwords** — enforce minimum length and complexity on the frontend
- **Monitor failed login attempts** and implement rate limiting if needed
- **Set appropriate token expiration** based on security requirements

## Troubleshooting

**"ModuleNotFoundError: No module named 'email_validator'"**
```bash
pip install email-validator
```

**"pymongo.errors.ServerSelectionTimeoutError"**
- Ensure MongoDB is running: `docker-compose -f data_infra/docker-compose.yml ps`
- Check `MONGO_URI` in `.env`

**"Invalid token" error**
- Token may have expired (default 7 days)
- Verify `JWT_SECRET` matches between token generation and validation
- Ensure token is passed correctly in `Authorization: Bearer <token>` header
