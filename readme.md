<h1 align="center">Hi 👋, I'm Luna!</h1>

The code that runs my personal website, [lunalux.io](https://lunalux.io). Feel free to inspect, use, or be inspired by the code, but keep in mind, it was made to fit my needs and may not be suitable for your use case.

## ToC
- [Overview](#overview)
    - [Bidirectional Linking](#bidirectional-linking)
    - [Trending Pages](#trending-pages)
    - [Interactive widgets](#interactive-widgets)
- [Installation](#installation)
- [Deployment](#deployment)


## Overview
The website is based on [Wagtail CMS](https://wagtail.io/), and is primarily structured as a blog. 

Each page is an instance of the `Page` model, and the content is created in the admin interface using predefined components that I have created in [home/templates/blocks](home/templates/blocks), but some special pages are defined as django view functions primarily located in [home/views.py](home/views.py).

The main content pages are `HomePage`, and `Article` which are located in [home/models.py](home/models.py). `HomePage` is meant to be flexible enough to create a wide range of pages whereas `Article` is constrained to be in a blog-post format. However, since most pages are `Article` instances, I have developed more components for that. The most notable use of `HomePage` is the index page. 

### Bidirectional linking
Whenever an `Article` is saved, the body is scanned for internal links (see `add_interpage_links` on `Article`) to other articles. If an internal link is found, a `InterPageLink` is created between the two articles. This is used to create a "Continue Reading" section at the bottom of each article.

### Trending pages
Whenever a page is rendered, we save a `PageHit` object to the database. We use these to find the trending pages on the site by counting the number of hits in the last 7 days (see `AbstractPage.get_trending_articles`). This is used to create the "Trending" section on the index page.

### Interactive widgets
In some articles, I include interactive widgets such as in [Gradient Descent](https://lunalux.io/gradient-descent-how-machines-learn/?series=14). These are one-off components located in [home/templates/oneoff_blocks](home/templates/oneoff_blocks).


## Installation

Make sure that you have one of the following Python versions `3.8, 3.9, 3.10, 3.11, 3.12`, if not, I recommend using [pyenv](https://github.com/pyenv/pyenv) to manage your Python versions.

1: Create a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Note if running in production mode, you should install `requirements_production.txt` in addition to `requirements.txt`.

2: Apply migrations:

```bash
python3 manage.py migrate
```

3: Create superuser

```bash
python3 manage.py createsuperuser
```

4: Run the development server:

```bash
python3 manage.py runserver
```

If you go to `localhost:8000` in your browser, you should see `Welcome to your new Wagtail site!` and be able to log in to the admin interface at `localhost:8000/admin/` with your username and passwords. 

You can now start to set up your website using my [components](home/templates/blocks). You can use the [Wagtail documentation](https://guide.wagtail.org/en-latest/) to learn more about how to use Wagtail.

## Deployment
To deploy to production, you can load the `application` in [wsgi_production.py](lunalux/wsgi_production.py) which loads the [production settings](lunalux/settings/production.py).

I use [gunicorn](https://gunicorn.org/) to run the application and [nginx](https://www.nginx.com/) as a reverse proxy.

`Note`: You will have to change the settings to be suitable for your production environment, primarily the hostname. 