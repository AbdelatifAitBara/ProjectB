
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configure the app and register blueprints, if any
    # Configuration settings (if any)
    app.config['DEBUG'] = True

    # Register routes and views
    from . import routes  # Import the module containing your routes
    app.register_blueprint(routes.bp)
    
    return app
