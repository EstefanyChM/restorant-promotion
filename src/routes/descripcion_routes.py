from flask import Blueprint, request, jsonify
from src.services.descipcion_service  import ( generar_descripcion, generar_imagen
)
import json

descripcion_bp = Blueprint('descripcion', __name__)


@descripcion_bp.route('/obtener_descripcion', methods=['GET'])
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
