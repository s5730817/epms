from flask import Flask
from epms.config import BaseConfig as config
from epms.extensions import db, login_manager

from epms.routes.auth import auth as auth_blueprint
from epms.routes.main import main_bp as main_blueprint

def register_extensions(app):
    db.init_app(app)
    login_manager.login_view = "auth.login"
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint, url_prefix="/")
    login_manager.init_app(app)    

def create_app(config_file=config):
    app =  Flask(__name__)
    app.config.from_object(config_file)
    register_extensions(app)
    
    
    ### Webdev is an absolute from of a headscrather
    ### Doesn't want to work bc "extensions doesn't exist"
    ### TO FIX
    
    @app.cli.command("seed")
    def seed_command():
        with app.app_context():
            from .models import seed_db
            seed_db(db=db)   
    return app


if __name__ == "__main__":
    app = create_app(config_file=config)
    app.run(debug=True)
