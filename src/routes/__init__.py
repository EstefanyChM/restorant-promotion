from .promocion_routes import promocion_bp

def register_blueprints(app):
    app.register_blueprint(promocion_bp)
