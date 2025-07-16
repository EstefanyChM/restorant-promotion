from flask import Blueprint, request, jsonify
from src.services.promocion_service import PromocionService
import json

promocion_bp = Blueprint('promocion', __name__)


# clase que registra las rutas
class PromocionController:
    def __init__(self, bp: Blueprint, service: PromocionService):
        self.bp = bp
        self.service = service
        self.register_routes()

    def register_routes(self):
        @self.bp.route('/lista-productos', methods=['GET'])
        def obtener_promociones():
            try:
                n = int(request.args.get('cantidad', 5))
                productos_seleccionados = self.service.productos_mayor_ganancia(n)
                return jsonify({'productosSeleccionados': productos_seleccionados})
            except Exception as e:
                return jsonify({'error': str(e)})
    

        @self.bp.route('/producto-descuento', methods=['GET'])
        def obtener_producto_descuento():
            try:
                id_categoria = request.args.get('idCategoria')
                if not id_categoria:
                    return jsonify({'error': 'Se requiere el parámetro idCategoria'}), 400

                productos_seleccionados = self.service.productos_mayor_ganancia_categoria(id_categoria)

                return jsonify({'productosSeleccionados': [productos_seleccionados[0]]})
            except Exception as e:
                return jsonify({'error': str(e)}), 500   

# exporta explcitamente
__all__ = ['promocion_bp', 'PromocionController']


