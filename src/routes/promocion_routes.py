from flask import Blueprint, request, jsonify
from src.services.promocion_service import (
    obtener_productos, calcular_descuentos, generar_descripcion, generar_imagen
)
import json

promocion_bp = Blueprint('promocion', __name__)

@promocion_bp.route('/lista-productos', methods=['GET'])
def obtener_promociones():
    try:
        n = int(request.args.get('cantidad', 5))
        df = obtener_productos()
        productos_seleccionados = calcular_descuentos(df, n)
        return jsonify({'productosSeleccionados': productos_seleccionados})
    except Exception as e:
        return jsonify({'error': str(e)})

@promocion_bp.route('/obtener_descripcion', methods=['GET'])
def obtener_descripcion():
    try:
        productos_json = request.args.get('productos')
        if not productos_json:
            return jsonify({"error": "No se proporcionó la lista de productos"}), 400

        productos = json.loads(productos_json)
        descripcion = generar_descripcion(productos)
        url_imagen = generar_imagen(descripcion)

        return jsonify({
            "mensaje": "Promoción generada correctamente",
            "descripcion": descripcion,
            "imagen": url_imagen
        })
    except json.JSONDecodeError:
        return jsonify({"error": "Formato JSON inválido"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@promocion_bp.route('/producto-descuento', methods=['GET'])
def obtener_producto_descuento():
    try:
        id_categoria = request.args.get('idCategoria')
        if not id_categoria:
            return jsonify({'error': 'Se requiere el parámetro idCategoria'}), 400

        df = obtener_productos()
        df_categoria = df[df['IdCategoria'] == int(id_categoria)]

        if df_categoria.empty:
            return jsonify({'error': 'No hay productos disponibles para esta categoría'}), 404

        productos_seleccionados = calcular_descuentos(df_categoria, 1)
        if not productos_seleccionados:
            return jsonify({'error': 'No se pudo calcular el descuento para esta categoría'}), 404

        return jsonify({'productosSeleccionados': [productos_seleccionados[0]]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
