from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    from app.config import Config
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from app.views import init_routes
        init_routes(app)
    
    return app

app = create_app()

csrf = CSRFProtect(app)



from app import models