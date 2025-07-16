from flask import Blueprint, request, jsonify
from src.services.promocion_service import *
from src.repository.promocion_repository import obtener_productos
import json

promocion_bp = Blueprint('promocion', __name__)

@promocion_bp.route('/lista-productos', methods=['GET'])
def obtener_promociones():
    try:
        n = int(request.args.get('cantidad', 5))
        productos_seleccionados = productos_mayor_ganancia(n)
        return jsonify({'productosSeleccionados': productos_seleccionados})
    except Exception as e:
        return jsonify({'error': str(e)})


@promocion_bp.route('/producto-descuento', methods=['GET'])
def obtener_producto_descuento():
    try:
        id_categoria = request.args.get('idCategoria')
        if not id_categoria:
            return jsonify({'error': 'Se requiere el parámetro idCategoria'}), 400

        productos_seleccionados = productos_mayor_ganancia_categoria(id_categoria)

        return jsonify({'productosSeleccionados': [productos_seleccionados[0]]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500   