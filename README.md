# TechBlog - Django Blog Application

A modern Django-based blog application with REST API functionality, user authentication, and comprehensive content management features.

## Features

- **User Authentication**: JWT-based authentication system with registration, login, logout, and profile management
- **Blog Posts**: Create, read, update, and delete blog posts with rich content
- **Categories & Tags**: Organize posts using categories and tags for better content management
- **REST API**: Full-featured API endpoints for all application functionality
- **Search & Filtering**: Advanced search and filtering capabilities for posts
- **Responsive Design**: Mobile-friendly interface (template-based frontend)

## Tech Stack

- **Backend**: Django 5.2.9
- **API Framework**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (default), with support for other databases
- **Filtering**: Django Filters
- **Frontend**: Django Templates (with potential for API consumption by frontend frameworks)

## Project Structure

```
techBlog/
├── accounts/           # User authentication and management
├── posts/             # Blog post functionality
├── categories/        # Post categories
├── tags/              # Post tags
├── authentication/    # Authentication components
├── techBlog/          # Main project settings
└── templates/         # HTML templates
```

## Installation

1. **Clone the repository** (if applicable) or navigate to your project directory

2. **Set up a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies** (if requirements.txt exists):
   ```bash
   pip install -r requirements.txt
   ```
   
   If no requirements file exists, install the necessary packages:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-filter
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get/update user profile

### Posts
- `GET /api/posts/` - List all posts (with search, filtering, and pagination)
- `POST /api/posts/` - Create a new post (authenticated users)
- `GET /api/posts/{id}/` - Get a specific post
- `PUT /api/posts/{id}/` - Update a specific post (authors only)
- `DELETE /api/posts/{id}/` - Delete a specific post (authors only)

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category (TBD)
- `GET /api/categories/{id}/` - Get a specific category

### Tags
- `GET /api/tags/` - List all tags
- `POST /api/tags/` - Create a new tag (TBD)
- `GET /api/tags/{id}/` - Get a specific tag

## Custom User Model

The application uses a custom user model (`accounts.CustomUser`) that extends Django's AbstractUser:
- Email-based authentication (email as username)
- IP address tracking
- Account creation and last login timestamps

## Filtering and Search

The posts API supports:
- **Filtering** by category and author
- **Searching** in title, summary, and body
- **Ordering** by creation date, update date, or title

## Frontend

The application includes:
- Homepage at root URL (`/`) displaying all posts
- API documentation page at `/api/`
- Admin interface at `/admin/`

## Configuration

Key settings in `techBlog/settings.py`:
- JWT token configuration (60 minutes access, 7 days refresh)
- REST Framework settings with pagination
- Custom user model reference
- Third-party app integrations

## Development

To run tests:
```bash
python manage.py test
```

To create new migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Security

- JWT tokens with refresh token rotation
- Password validation
- CSRF protection
- SQL injection prevention through ORM

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.