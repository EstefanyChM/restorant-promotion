from flask import Flask
from flask_cors import CORS
from src.database.db_engine import engine
from src.routes import register_blueprints

def create_app():
    app = Flask(__name__)
    CORS(app)
    register_blueprints(app, engine)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



