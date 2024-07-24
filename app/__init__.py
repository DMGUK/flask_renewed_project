from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__)

    from config import DevelopmentConfig, ProductionConfig, TestingConfig

    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.login'
    login_manager.login_message_category = 'info'


    with app.app_context():
        from .mainpage.views import portfolio
        from .accounts.views import accounts
        from .todo.views import todo
        from .posts.views import posts

        app.register_blueprint(accounts)
        app.register_blueprint(portfolio)
        app.register_blueprint(todo)
        app.register_blueprint(posts)
    return app

# postgresql://flask_renew_db_user:8i1EcgSdwYA0zrrkoNZji5GgpkrEan9W@dpg-cqggfmqju9rs73cdvg7g-a.frankfurt-postgres.render.com/flask_renew_db