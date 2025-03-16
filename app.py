from flask import Flask, render_template,session
from config import Config
from extensions import db, migrate, login_manager,csrf
from models import User
from utils import create_search_form

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Enable session timeout globally
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Setup login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    #set pagination for products
    app.config['PRODUCTS_PER_PAGE'] = 20

    # Initialize CSRF protection
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.cart import cart_bp
    from routes.product import product_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(product_bp, url_prefix='/products')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        search_form = create_search_form()
        return render_template('errors/404.html', search_form = search_form), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        search_form = create_search_form()
        return render_template('errors/500.html', search_form = search_form), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
