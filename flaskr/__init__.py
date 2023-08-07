import os
from flask import Flask, render_template
from flaskr.auth import login_required

def create_app(test_config = None):
    #This is the application factory where the app is created and configuration is done
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'devs',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route('/')
    @login_required
    def hello():
        result = "name"
        return render_template("index.html", result = result)
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import books
    app.register_blueprint(books.bp)
    return app
