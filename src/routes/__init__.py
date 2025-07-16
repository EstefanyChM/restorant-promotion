from .promocion_routes import promocion_bp, PromocionController
from src.services.promocion_service import PromocionService

def register_blueprints(app, engine):
    servicio = PromocionService(engine)
    PromocionController(promocion_bp, servicio)
    app.register_blueprint(promocion_bp)
