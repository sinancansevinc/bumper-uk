
# Django Guest Entry API

A Django-based API for managing guest entries and user information, backed by PostgreSQL and Redis. The application is containerized using Docker, enabling a quick and consistent setup across environments.

## Features

- Create and retrieve guest entries linked to specific users.
- Annotate users with entry count and last entry details.
- Caching implemented with Redis for efficient data retrieval.
- PostgreSQL as the main database.
  
## API Endpoints

- **Users Endpoint**: Retrieve a list of users with entry data.
  - URL: `http://localhost:8000/api/users`
- **Guest Entries Endpoint**: Create and retrieve guest entries.
  - URL: `http://localhost:8000/api/guest-entries/`

## Prerequisites

- Docker and Docker Compose installed on your machine.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <bumper-uk>
```

### 2. Create the `.env` File

Create a `.env` file in the project root to store environment variables:

```plaintext
# .env

# Django settings
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True

# PostgreSQL settings
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DATABASE_URL=postgres://your_db_user:your_db_password@db:5432/your_db_name

# Redis settings
REDIS_URL=redis://redis:6379/1
```

Replace `your_secret_key`, `your_db_name`, `your_db_user`, and `your_db_password` with your own values.

### 3. Build and Start the Containers

Run the following command to build the images and start the containers:

```bash
docker-compose up --build
```

This command will:
- Set up the Django app and install dependencies.
- Launch PostgreSQL and Redis services.
- Run the Django development server on port 8000.

### 4. Run Database Migrations

In a separate terminal, apply database migrations to set up the PostgreSQL database:

```bash
docker-compose exec web python manage.py migrate
```

### 5. (Optional) Create a Superuser

To access the Django admin interface or create initial users:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Access the API

The application should now be running. You can access the API endpoints:

- **Users**: [http://localhost:8000/api/users](http://localhost:8000/api/users)
- **Guest Entries**: [http://localhost:8000/api/guest-entries/](http://localhost:8000/api/guest-entries/)

### 7. Run Tests

To ensure everything is working as expected, you can run the test suite:

```bash
docker-compose exec web python manage.py test
```

## Caching with Redis

- **Caching**: The project uses Redis to cache frequently accessed data to improve performance.
- **Cache Invalidation**: When guest entries are created or deleted, related cache entries are automatically invalidated to ensure data accuracy.


## Troubleshooting

- If containers fail to start, check `.env` for correct database and Redis credentials.
- Run `docker-compose down` to stop all containers, and then `docker-compose up --build` to rebuild and start fresh.
