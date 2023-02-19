# User Guide
 
## Introduction: Structuring of API

- `app`: Contains all the API related code base. 
  - `core`: Contains core modules of your application.
    - `auth.py`: Contains authentication configuration based on [fastapi-users](https://fastapi-users.github.io/fastapi-users/10.0/).
    - `config.py`: Contains main global settings of your application.
    - `logger.py`: Logging module for application.
    - `pagination.py`: Contains simple helpers to apply limit-offset based pagination on your api routes.
  - `db`: Main package for your database / orm configuration.
    - `config.py`: Main module for your database configuration.
    - `models.py`: Contains some common abstract base models for your **apps** database models. Read the *WHY* section bellow to understand what **apps** are.
  - `emails`: Contains html templates for your emails.
    - `base.html`: Base html template from which all your other email templates must inherit.
    - `welcome.html`: Welcome email template, sent when a new user registers.
  - `frontend`: Contains all the python code for your frontend. This directory is only present when you enter **y** with the **render_html** option. More details about this directory are available in the *WHY* section.
    - `routers`: All your frontend API routers.
      - `home.py`: This is an example, containing a single route to render the html of the home page.
    - `app.py`: The frontend is in fact a separate fastapi application defined in this module and mounted on the main application in the `main.py` file.
    - `utils.py`: Contains python utilities specific to frontend stuff.
  - `services`: Contains classes and functions intended to connect to external resources that your application could use.
    - `email`: Contains helper modules to connect to an email provider to send emails. 
      - `errors.py`: Errors related to sending an email.
      - `null.py`: A dummy email provider when you don't want to send real emails. 
      - `ses.py`: Email provider class to send email with [amazon ses](https://aws.amazon.com/fr/ses/) using [aioaws](https://github.com/samuelcolvin/aioaws). This file is only included if you choose **AMAZON SES** as **mail_service**.
      - `smtp.py`: Email provider class to send email via [smtp](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) using [aiosmtplib](https://aiosmtplib.readthedocs.io/en/stable/usage.html#authentication). This file is only included if you choose **SMTP** as **mail_service**.
  - `static`: Folder to store static files, only included if you enter **y** in the **render_html** option.
    - `style.css`: Your project css.
  - `templates`: Html templates directory, only include if you enter **y** to the **render_html** option.
    - `base.html`: Base html for all your html templates.
    - `index.html`: Example html for the index page.
  - `users`: Users management app.
     - `tests`: Tests for your users' app.
       - `factories.py`: Test factories for the users models.
     - `manager.py`: User manager class, used by the [fastapi-users](https://fastapi-users.github.io/fastapi-users/10.0/configuration/user-manager/) package. You can use this concept for your other apps if you like it.
     - `models.py`: Users database models.
     - `routes.py`: Users API router and routes.
     - `schemas.py`: Users pydantic schemas.
     - `tasks.py`: Task queues tasks specific to the user's app.
     - `utils.py`: Utilities specific to the user's app.
  - `health.py`: Health API route.
  - `initial_data.py`: Contains functions that create some initial data for your application.
  - `lifetime.py`: In this module are defined the start and shutdown event handlers for your application.
  - `main.py`: Entry point of your application, the main **FastAPI** application is defined here.
  - `utils.py`: Global application utilities, which can be turned into a module later if there are too many.
  - `worker.py`: Task queue worker configuration file.
- `tests`: Your application tests.
- `.env.template`: A template to create your **.env** file.
- `.gitignore`: List common files and directories of python projects to keep out of git, read [here](https://git-scm.com/docs/gitignore) for more details.
- `Dockerfile`: Production [dockerfile](https://www.docker.com/) if you enter **y** to the **use_docker** option.
- `.pre-commit-config.yaml`: [pre-commit](https://pre-commit.com/) configuration file for auto formatting of your code on each commit.
- `manage.py`: Cli app to simplify project management, run `python manage.py --help` for all available commands.
- `Procfile`: [Heroku Procfile](https://devcenter.heroku.com/articles/procfile) configuration file, only present when you choose **y** to the **user_heroku** option.
- `pyproject.toml`: Application dependencies, packaging data and metadata, for more details read [this](https://peps.python.org/pep-0621/).
- `README.md`: Details and setup guide for your application.
- `runtime.txt`: [Heroku runtime](https://devcenter.heroku.com/articles/python-runtimes) configuration file, only present when you choose **y** to the **user_heroku** option.
- `setup.cfg`: A python configuration file for external tools like flake8, mypy etc., but I strongly recommend to put them in the `pyproject.toml` file if the tool supports it. This file will probably be removed in future versions when all tools used here add support for the `pyproject.toml` file.
- `gunicorn.conf.py`: [gunicorn](https://docs.gunicorn.org/en/stable/index.html) configuration file for deployment.

Most of the ideas and patterns that this template follows were inspired by OSS (open source software) projects and tools.
I took the most interesting (from my point of view) patterns and applied them when creating this cookiecutter, and you are by no 
means obliged to follow 100% of the structure described here. I'm always learning new things and will improve this project over time. 
If you think something doesn't make sense in the files and folder structures, the code base, or if you have suggestions or improvements or
anything else really, please feel free to open an [issue](https://github.com/Tobi-De/cookiecutter-fastapi/issues/new) or a [discussion](https://github.com/Tobi-De/cookiecutter-fastapi/discussions/new), I will be glad to discuss with you.
This cookiecutter can't cover every use case, so here are some alternatives if this template doesn't fit your needs:

- [fastapi-template](https://github.com/99sbr/fastapi-template)
- [manage-fastapi](https://github.com/ycd/manage-fastapi)
- [fastapi-nano](https://github.com/rednafi/fastapi-nano)


## Design Decisions

n this section, we'll explore some of the design decisions made in the creation of the cookicutter-fastapi project template. 
We'll discuss the reasoning behind the choices made in terms of project structure, code organization, and other key aspects of the template. 
This section is intended to provide insight into the thought process behind the template, as well as to help users understand why certain design decisions were made.

### Use of Django-style "apps" in the Template

> **TL;DR**: Features bound to the same domain in the business logic are encapsulated in an application. 
Applications should be small, simple and focus on a single task. E.g. the **users** app for users management.

One of the core design decisions of the `cookicutter-fastapi` project template is the use of the Django-style "apps" structure. 
As a [Django](https://www.djangoproject.com/)  user, I appreciate the [concept of applications](https://docs.djangoproject.com/en/4.0/ref/applications/) which is basically the clear and distinct separation of functionality into reusable packages. 
With this in mind, I set out to emulate this idea with FastAPI.

FastAPI does not impose any kind of structure on users, which is great for simple projects, but for more complex projects, a well-structured 
and organized base is necessary. If you search for [FastAPI projects on GitHub](https://github.com/search?q=fastapi), you will find a wide variety of styles and structures, 
each reflecting the experience and preferences of the individual developer. In the `cookicutter-fastapi` template, I have implemented a 
structure that represents my own experience as a Django developer, and I believe it will be familiar and intuitive to many other django developers.

The idea behind the `apps` structure is to encapsulate features that are bound to the same domain in the business logic within a single application. 
Each application should be small, simple, and focused on a single task. For example in the context on an ecommerce web app, a `users` application 
would be responsible for managing users, while an `orders` application would be responsible for managing orders. In my opinion, this structure allows 
a better organization and a better maintainability of the project as it grows and becomes more complex.

### The frontend application

When I use fastapi, it's usually for small backend services and not for full fledge server side rendered (SSR) 
projects (think of an e-commerce site with django or laravel for example). I mainly use fastapi for relatively simple backend 
APIs and I rarely need to serve html and when I do it's for very few pages. If I needed to build
a big monolith that serves html, I would probably choose django. The idea here is that the `frontend` directory is
an application in your project, it will serve the few html pages you need. If you build
a public weather API for example, but you need a few html pages to present the project, a home page, a contact page and maybe some user 
account pages, you can use the frontend app for that instead of creating a separate html/css/js or
<**place your favorite js framework here**> project for that. Spreading the routes for those pages in your API routes is not a good idea
in my opinion. The `frontend` application is a bit special in that it is a full Fastapi application [that is mounted](https://fastapi.tiangolo.com/advanced/sub-applications/) on top of your main application.
I don't think this approach can scale to hundreds of html pages, so think twice before you consider using it for a huge project (frankly I don't know, I haven't tried it, I could be wrong).

> **Note**: Checkout [htmx](https://htmx.org/) if you to improve your frontend development and user experience without relying on a complex SPA javascript framework.

# Deployment

For deployment the official fastapi documentation has an excellent guide on the subject [here](https://fastapi.tiangolo.com/deployment/).
If you want some platform recommendation check this [page](https://tobi-de.github.io/fuzzy-couscous/deployment/).

**Note**: This page is a work in progress, new content will be added with new release of `cookiecutter-fastapi`.
