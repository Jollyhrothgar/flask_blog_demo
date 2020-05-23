import os

from flask import Flask

def create_app(test_config=None):
    """
    The default factory method we use to create apps for flaskr.

    Args:
        test_config - a configuration for tests that can be used instead of the
        instance configuration.
    Returns:
        A flask app.
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in 
        app.config.from_mapping(test_config)

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Debugging route - make sure app works.
    @app.route('/hello')
    def hello():
        return "<h1> Hello, World! </h1>"

    # Add database function context to the app
    from . import db
    db.init_app(app)

    # Add authentication blueprint to the app
    from . import auth
    app.register_blueprint(auth.bp)

    # Add the blog blueprint to the app
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
