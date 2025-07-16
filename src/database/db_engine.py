from sqlalchemy import create_engine
import platform

# Configuración de conexión a SQL Server
CONNECTION_STRING = (
    "mssql+pyodbc://@FANNY/Riccos_pollos"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(CONNECTION_STRING)
