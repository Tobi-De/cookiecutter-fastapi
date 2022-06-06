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
  - `templates`: Html templates directory, only include if you enter **y** to the **render_html** option.
    - `base.html`: Base html for all your html templates.
    - `index.html`: Example html for the index page.
  - `tests`: Your application tests.
    - `conftest.py`: Module to store pytest [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html). 
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
- `.env.template`: A template to create your **.env** file.
- `.gitignore`: List common files and directories of python projects to keep out of git, read [here](https://git-scm.com/docs/gitignore) for more details.
- `.pre-commit-config.yaml`: [pre-commit](https://pre-commit.com/) configuration file for auto formatting of your code on each commit.
- `manage.py`: Cli app to simplify project management, run `python manage.py --help` for all available commands.
- `pyproject.toml`: Application dependencies, packaging data and metadata, for more details read [this](https://peps.python.org/pep-0621/).
- `README.md`: Details and setup guide for your application.
- `setup.cfg`: A python configuration file for external tools like flake8, mypy etc., but I strongly recommend to put them in the `pyproject.toml` file if the tool supports it. This file will probably be removed in future versions when all tools used here add support for the `pyproject.toml` file.

Most of the ideas and patterns that this template follows were inspired by OSS (open source software) projects and tools.
I took the most interesting (from my point of view) patterns and applied them when creating this cookiecutter, and you are by no 
means obliged to follow 100% of the structure described here. I'm always learning new things and will improve this project over time. 
If you think something doesn't make sense in the files and folder structures, the code base, or if you have suggestions or improvements or
anything else really, please feel free to open an [issue](https://github.com/Tobi-De/cookiecutter-fastapi/issues/new) or a [discussion](https://github.com/Tobi-De/cookiecutter-fastapi/discussions/new), I will be glad to discuss with you.
This cookiecutter can't cover every use case, so here are some alternatives if this template doesn't fit your needs:

- [fastapi-template](https://github.com/99sbr/fastapi-template)
- [manage-fastapi](https://github.com/ycd/manage-fastapi)
- [fastapi-nano](https://github.com/rednafi/fastapi-nano)

## Why... ???

This section addresses questions you may have about some of my design decisions.

### Why the apps/components thing anyway ?

I am a [django](https://www.djangoproject.com/) user, and I like its [concept of apps](https://docs.djangoproject.com/en/4.0/ref/applications/). 
This cookiecutter tries to emulate that idea. I really like the idea of separating functionality into clear and distinct (and sometimes reusable) applications, 
and I've been wanting to emulate this idea with fastapi for a while now. This is one of the main reasons why I created this cookiecutter. Fastapi does not impose 
any kind of structure on you, and that's great but sometimes (for other things than test projects and tutorials) I need a well-structured and organized base to work on projects.
If you search for [fastapi projects on github](https://github.com/search?q=fastapi) you will get a lot of different styles and structures,
most people work on the basis of their experience and the structure of this template represents mine, which is basically being a django developer,
and it's probably the same for many python developers out there. The idea is the following: features bound to the same domain in the business logic are encapsulated in an application. 
Applications should be small, simple and focus on a single task. E.g. the **users** app for users management.


### Why aren't all tests in the same folders? Why do apps have their own test folder?

For a while, I hesitated between putting all the tests in the same folder or separating them as I did.  
I'm still not 100% sure I chose the best approach, and that may change in a future iteration of this project. Bottom line,
applications are where you will spend most of your development time, they encapsulate your business logic and if you practice
[TDD](https://en.wikipedia.org/wiki/Test-driven_development) and you should, it might be really more practical if 
the tests for these applications are very close to the code of these applications. It may even motivate you to apply TDD if 
you don't have to go too far away from the location of the code to be tested to write the tests. That's what I told myself when I chose this approach. 
You can do whatever you prefer here and not follow this approach. If the `startapp` command bothers you by always creating a `tests` folder, 
you can easily change the behavior of the command in the `manage.py` file. 

### Why put all the frontend files in a specific directory?

Here too I hesitated a lot. When I use fastapi, it's usually for small backend services and not for full fledge SSR 
projects (think of an e-commerce site with django or laravel for example). I mainly use fastapi for 
relatively simple backend APIs and I rarely need to serve html and when I do it's for very few pages. If I needed to build
a big monolith that serves html, I would probably choose django. The idea here is that the `frontend` directory is
an application in your project, it will serve the few html pages you need. If you build
a public weather API for example, but you need a few html pages to present the project, a home page, a contact page and maybe some user 
account pages, you can use the frontend app for that instead of creating a separate html/css/js or
<**place your favorite js framework here**> project for that. Spreading the routes for those pages in your API routes is not a good idea
in my opinion. The `frontend` application is a bit special in that it is a full Fastapi application [that is mounted](https://fastapi.tiangolo.com/advanced/sub-applications/) on top of your main application.
I don't think this approach can scale to hundreds of html pages, so think twice before you consider using it for a huge project (frankly I don't know, I haven't tried it, I could be wrong).

**Note**: This page is a work in progress, new content will be added with new release of `cookiecutter-fastapi`.
