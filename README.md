# Knowledge Transfer Platform API

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker + Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rajnishm990/KT_Sessions_API
cd backend
```

2. **Start the services**
```bash
docker-compose up --build
```

3. **Run migrations**
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

4. **Create a superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application**
- API: http://localhost:8000/
- Swagger Documentation: http://localhost:8000/swagger/
- Admin Panel: http://localhost:8000/admin/

## API Documentation

### Authentication Endpoints

#### Register 
I haven't made a Register endpoint so for registering a user use django's admin panel or user super user's credentials

```bash
docker-compose exec web python manage.py createsuperuser
```

#### Login
```http
POST /api/token/
Content-Type: application/json

{
    "username": "user123",
    "password": "securepassword123"
}
```

### KT Sessions Endpoints

#### Create Session
```http
POST /api/sessions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "React Hooks Knowledge Transfer",
    "description": "Session covering useState, useEffect, and custom hooks"
}
```

#### List User Sessions
```http
GET /api/kt/
Authorization: Bearer <access_token>
```

#### Get Session Details
```http
GET /api/kt/{session_id}/
Authorization: Bearer <access_token>
```

#### Add Attachment to Session
```http
POST /api/kt/{session_id}/add_attachment/
Authorization: Bearer <access_token>

file_type: audio
```

#### View Shared Session (Public)
```http
GET /api/sessions/shared/{share_token}/
```

### Attachment Endpoints

#### Get Attachment Details
```http
GET /api/attachments/{attachment_id}/
Authorization: Bearer <access_token>
```


## Mock User Credentials

For testing purposes, you can create users via  the Django admin.

**Sample Test User:**
- username: `testuser123`
- Email: `test@example.com`
- Password: `testpassword123`


### Shareable Links

Each KT session has a unique `share_token` that allows public access:
- Private URL: `/api/kt/{session_id}/` (requires authentication)
- Public URL: `/api/sessions/shared/{share_token}/` (no authentication)


## Environment Variables

Create a `.env` file for custom configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@db:5432/kt_platform
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS = 'localhost'
```

## Development

### Running Without Docker

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Start Redis**
```bash
redis-server
```

4. **Start Celery worker**
```bash
celery -A core worker --loglevel=info
```

5. **Start Django server**
```bash
python manage.py runserver
```


## API Usage Examples

### Complete Workflow Example

1. **Register a new user**
2. **Login and get access token**
3. **Create a KT session**
4. **add attachments to the session**
5. **Monitor processing status**
6. **Share the session using the public link**



## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 8000, 5432, and 6379 are available
2. **Database connection**: Ensure PostgreSQL is running before starting the web service

