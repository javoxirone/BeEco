# BeEco: A Sustainable Living Platform

BeEco is a web application built with Django that encourages users to adopt eco-friendly habits by tracking their waste disposal and rewarding them for their efforts. This README provides a comprehensive guide on how to set up and run the BeEco project.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Static Files](#static-files)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Waste Tracking:** Users can log the waste they dispose of, categorizing it by type (e.g., paper, plastic, metal).
- **Venue Locator:** The application provides a list of venues for waste collection, with location details.
- **Points and Rewards:** Users earn points for logging waste, which can be used to unlock badges and achievements.
- **User Profiles:** Customizable user profiles with the ability to upload a profile picture.
- **Activity Logging:** Tracks user activities, providing a history of their contributions.
- **Educational Recommendations:** Provides users with recommendations and tips on reducing waste and living sustainably.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python:** Version 3.8 or higher. You can download it from [python.org](https://www.python.org/downloads/).
- **pip:** Python package installer (comes with Python installations).
- **Git:** For cloning the repository. You can download it from [git-scm.com](https://git-scm.com/downloads).

## Installation

Follow these steps to install the BeEco project:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/javoxirone/BeEco.git
    cd BeEco
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to isolate project dependencies.

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    -   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    -   On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    This command installs all the required Python packages listed in the `requirements.txt` file.

## Configuration

1.  **Database setup:**
    This project uses SQLite as its default database. The database file is `db.sqlite3`. No additional configuration is needed for SQLite unless you want to use a different database engine (PostgreSQL, MySQL, etc.).  If you wish to use another database, edit the `DATABASES` setting in `project/settings.py` accordingly.

2.  **Static files configuration:**

    The static files (CSS, JavaScript, images) are configured in `project/settings.py`. The `STATIC_URL`, `STATIC_ROOT`, and `STATICFILES_DIRS` settings determine how static files are served. In development, Django serves static files automatically. In production, you'll need to configure a static file server like Nginx or Apache.

3.  **Media files configuration:**
    The MEDIA_ROOT and MEDIA_URL settings defines the storage and URL structure for media files(user uploaded content).
    ```
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL =  '/media/'
    ```

## Running the Project

1.  **Apply migrations:**

    This command creates the database tables based on the Django models.

    ```bash
    python manage.py migrate
    ```

2.  **Create a superuser:**

    Create an admin user to access the Django admin panel.

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to enter a username, email address, and password.

3.  **Collect static files:**

    This command collects all static files into the `STATIC_ROOT` directory. This is required before deploying the application to production.

    ```bash
    python manage.py collectstatic
    ```

4.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    This starts the Django development server. You can access the application in your web browser at `http://127.0.0.1:8000/`.

## Environment Variables

While this project doesn't heavily rely on environment variables for core functionality in its current state (using SQLite and hardcoded settings), it's good practice to be aware of how to use them, especially when deploying to production:

- `DJANGO_SETTINGS_MODULE`:  This is already set in `manage.py` and `wsgi.py` to point to your settings file (`project.settings`).
- `SECRET_KEY`: In a production environment, you should set the SECRET_KEY as an environment variable for security reasons.
- `DEBUG`: Set this to `False` in production.
- `ALLOWED_HOSTS`: Configure this with your production domain(s).

**Example usage in a production environment:**

```bash
export DJANGO_SETTINGS_MODULE=project.settings
export SECRET_KEY="your_production_secret_key"
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com,*.yourdomain.com"
```

## Database Setup

The project is configured to use SQLite by default, which requires no additional setup. The database file `db.sqlite3` will be created in the project's root directory when you run `python manage.py migrate`.

If you want to use another database engine like PostgreSQL or MySQL, you'll need to:

1.  **Install the appropriate Python package:**

    ```bash
    pip install psycopg2  # For PostgreSQL
    pip install mysqlclient # For MySQL
    ```

2.  **Update the `DATABASES` setting in `project/settings.py`:**

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # or 'django.db.backends.mysql'
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',  # or your database host
            'PORT': '5432',       # or your database port
        }
    }
    ```

3.  **Run migrations:**

    ```bash
    python manage.py migrate
    ```

## Static Files

In development mode, Django automatically serves static files. However, in a production environment, it's recommended to use a dedicated static file server like Nginx or Apache. Here's how to configure static files for production:

1.  **Set `DEBUG = False` in `project/settings.py`.**

2.  **Run `python manage.py collectstatic` to collect all static files into the `STATIC_ROOT` directory.**

3.  **Configure your web server to serve the static files from the `STATIC_ROOT` directory.**

    -   **Nginx:**

        ```nginx
        server {
            location /static/ {
                alias /path/to/your/project/static/;
            }
        }
        ```

    -   **Apache:**

        ```apache
        <Directory /path/to/your/project/static>
            Require all granted
        </Directory>

        Alias /static /path/to/your/project/static
        ```
    Also configure to serve media files which is uploaded by user, such as profile images, etc.

## Contributing

We welcome contributions to the BeEco project! Here are the steps to contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Push your changes to your fork.
5.  Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).
