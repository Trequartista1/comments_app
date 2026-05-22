# Comments App

A full-stack SPA for threaded commenting with real-time updates.

**Live Demo:** https://perpetual-curiosity-production.up.railway.app

## Tech Stack

**Backend**
- Python 3.12 / Django 6.0
- Django REST Framework
- Django Channels + Daphne (WebSocket / ASGI)
- PostgreSQL
- Pillow (image processing)
- Bleach (XSS protection)
- PyJWT (CAPTCHA token validation)

**Frontend**
- Vue 3 (Composition API)
- Vite 8

**Infrastructure**
- Docker + Docker Compose
- Railway (hosting)

## Features

- Add comments with Username, Email, Homepage, and text
- Allowed HTML tags in text: `<strong>`, `<i>`, `<code>`, `<a>`
- Toolbar buttons for quick tag insertion (B, i, code, link)
- Live preview before submitting
- CAPTCHA validation (JWT-based, works cross-domain)
- Attach image (JPG, PNG, GIF — auto-resized to 320×240 if larger)
- Attach text file (TXT, max 100KB)
- Lightbox for image preview with animation
- Threaded replies (unlimited nesting)
- Top-level comments displayed as a sortable table
- Sort by Username, E-mail, or Date (ascending / descending)
- Pagination (25 comments per page)
- Real-time updates via WebSocket — new comments appear instantly without page reload
- XSS protection (Bleach sanitization on backend)
- Client-side and server-side validation
- HTML tag closure validation

## Project Structure

```
comments_app/
├── backend/
│   ├── comments/
│   │   ├── models.py        # Comment model
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # API views
│   │   ├── consumers.py     # WebSocket consumer
│   │   ├── routing.py       # WebSocket URL routing
│   │   └── urls.py          # HTTP URL routing
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── asgi.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CommentForm.vue
│   │   │   └── CommentItem.vue
│   │   ├── App.vue
│   │   └── style.css
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── schema.sql
```

## Database Schema

| Field       | Type         | Description                        |
|-------------|--------------|------------------------------------|
| id          | INTEGER (PK) | Auto increment                     |
| username    | VARCHAR(100) | Letters and digits only            |
| email       | VARCHAR      | Valid email format                 |
| homepage    | VARCHAR      | Optional URL                       |
| text        | TEXT         | Comment body (sanitized HTML)      |
| image       | VARCHAR      | Path to uploaded image (optional)  |
| text_file   | VARCHAR      | Path to uploaded TXT (optional)    |
| parent_id   | INTEGER (FK) | Self-reference for nested replies  |
| created_at  | DATETIME     | Auto timestamp                     |

## API Endpoints

| Method | Endpoint      | Description                              |
|--------|---------------|------------------------------------------|
| GET    | /comments/    | List top-level comments (paginated)      |
| POST   | /comments/    | Create a new comment                     |
| GET    | /captcha/     | Get CAPTCHA image + JWT token            |
| WS     | /ws/comments/ | WebSocket for real-time comment updates  |

### Query Parameters for GET /comments/

| Parameter | Values                                      |
|-----------|---------------------------------------------|
| page      | Page number (default: 1)                    |
| ordering  | username, -username, email, -email, created_at, -created_at |

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Run the project

```bash
git clone https://github.com/Trequartista1/comments_app.git
cd comments_app
docker compose build
docker compose up
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Apply migrations (first run)

In a separate terminal:

```bash
docker compose exec backend python manage.py migrate
```

### Stop the project

```bash
docker compose down
```
