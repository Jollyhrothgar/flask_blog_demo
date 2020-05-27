# How to deploy / access (developement)

# How to deplot / access (production)

# [Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/static/)

I'm following the flask.palletsprojects.com tutorial for creating a blog. This
repo is basically a copy/paste of it, where I've added more documentation /
comments to the code as I slowly folow the tutorial.

I will follow up this tutorial by building other web-app projects.



## Tutorial Notes

A micro-framework glues together other tools that get the job done. For example,
flask doesn't choose the database, the interface, or the structure of your
framework for you, but it glues it all together.

Note that I've already made apps following the model in the
[basic](https://flask.palletsprojects.com/en/1.1.x/quickstart/) Flask
template, but for a larget project (like battleshark), I'll need to factor the
application into blueprints.

## [Bookmark](https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/#the-blueprint)


### Environment

Set the following bash environment variables:

```bash
export FLASK_APP=flaskr # the name of the folder containing the app factory
export FLASK_ENV=development # deployment specific configuration..?
```

Run with

```bash
# From project root:
flask run
```

# Concepts With One-Liner Explainations

## [click](https://click.palletsprojects.com/en/7.x/)

Click is a python package for creating command line interfaces, it stands for:
"Command Line Interface Creation Kit".

Click defines some basic command-line tool functions, such as:

*   A prompt, for gathering user input
*   flags, for processing command line keyword flags (e.g. `--key value`).

Its like argparse or optparse, but different (easier..?)

## Flask

Flask applications are instances of the Flask class - configurations, urls, etc
are all registered with an instance of the Flask class.

Flask instances can be created globally - for example, when you just want a
one-script flask web-application.

Another way to create Flask instances is through a factory-method. This means
that flask instances are created by a function, initialized in the function, and
returned.

In this tutorial, we package the flask application factory in the `__init__.py`
module file to expose it at the module level.

### Concepts

#### Factory

#### Blueprints

Blueprints are a way to register functionality with an app without directly
passing instances of the app around to everywhere that needs to deal with it.
This is useful for adding modules to the code to incrementally expand functions
of the app and to add functions to the app when the context requires it.

### Flask Libraries

#### Flask app functions

Assuming we have an instance of Flask, called `app`.

##### `app.instance_path`

`instance_path` is a deployment-specific path that points to the instance
folder. The instance folder is not under version control and contains stuff
that is runtime / deployment specific, such as runtime or configuration files.

##### `app.config.from_mapping`

`from_mapping` sets the default mapped configurations, such as `SECRET_KEY` or
`DATABASE`.

`SECRET_KEY` should be randomly generated when deployed for encryption. 

`DATABASE` is the path for storing the SQLite database.

Flask doesn't make the instance path by default, so we specify the structure to
dump the database.

#### `current_app` and `g`

When using the app-factory pattern supported by Flask, there is generally not a
global app instance. This means we need a means to push data and instructions
to an app-context, accessible by `current_app` and `g`.

Without going into deep details, I will think of `current_app` and `g` as
proxies for passing in an actual app instance.

App contexts can also be pushed via the `flask.cli` method.

`current_app` can interact with resources via `current_app.open_resource` to,
for example, read files defined at the package level (e.g. schema in this
case).

Any functions we might define that need to be used by the broader application
need to be registered to that application.

#### `app.teardown_appcontext`

This registers functions used to deallocate resources when the app-context
goes out of scope (e.g. the app shuts off), or, the app issues a response to
a request.

#### `app.cli.add_command`

This adds command that can be passed to the app from the command line.

#### `flask.Blueprint`

Blueprints organize a group of related views and other code - instead of
registering these views with the app directly, they are registered with a
blueprint. The blueprint is then registered with the app when it becomes
available in the app factory.

#### `flask.flash`

A simple way to flash messages to users.

#### `flask.redirect`

Use to redirect a request to a different endpoint from the one triggered.

#### `flask.render_template`

A response that renders a template as a webpage. Can directly insert code here,
and the response will be turned into an appropriate response to show on a
webpage.

Templates are rendered using the jinja template, and, user input will be
properly escaped to not break the webpage.

*   `{{stuff}}` - something that we output into the final doc
*   `{% %}` - control flow (if, elif, else, for)
		*    Control flows use start/end tags, but jinja templating language uses
				 python-like syntax.

*   `{%block val%}` will be overridden in child pages

#### `flask.request`

A library to make HTTP requests.

#### `flask.session`

Allows storage of info associated with a user from one session to the next.
This is implemented using cookies - users can view cookies but not modify,
because they are cryptographically signed.

#### `flask.url_for`

Building URLs for specific function, without requiring that URLs are
hard-coded.

`url_for` points to the name of the endpoint, which is defined by the app.route
name.

## Werkzeug

### `werkzeug.security.check_password_hash`

### `werkzeug.security.generate_password_hash`

## SQL Lite

### `sqlite3`

Python has built-in support for SQLite. SQLite has some
advantages/disadvantages:

*   No requirement for separate SQL server software
*   Multiple write requests are processed sequentially. This is a problem for
		large apps, but not so noticable for small apps.
