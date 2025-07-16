from .promocion_routes import promocion_bp
from .descripcion_routes import descripcion_bp

def register_blueprints(app):
    app.register_blueprint(promocion_bp)
    app.register_blueprint(descripcion_bp)
