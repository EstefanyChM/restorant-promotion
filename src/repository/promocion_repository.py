import pandas as pd
from sqlalchemy import text
from src.database.db_engine import engine

def obtener_productos():
    query = text("""
        SELECT p.Id, p.Nombre, p.IdCategoria, p.Precio, p.Stock, p.MargenGanancia,
               ISNULL(MAX(v.FechaVenta), '2000-01-01') AS UltimaVenta,
               ISNULL(dp.PorcentajeDescuentoPorUnidad, 0) AS DescuentoPrevio,
               COUNT(DISTINCT dp2.IdPedido) AS HistorialPedidosJuntos
        FROM producto.Producto p
        JOIN producto.Categoria c ON p.IdCategoria = c.Id
        LEFT JOIN venta.Venta v ON v.IdPedido IN (SELECT IdPedido FROM pedido.DetallePedido WHERE IdProducto = p.Id)
        LEFT JOIN pedido.DetallePedido dp ON dp.IdProducto = p.Id
        LEFT JOIN pedido.DetallePedido dp2 ON dp2.IdProducto = p.Id
        WHERE p.Estado = 1 AND p.Disponibilidad = 1 AND c.Estado = 1 AND c.Disponibilidad = 1
        GROUP BY p.Id, p.Nombre, p.IdCategoria, p.Precio, p.Stock, p.MargenGanancia, dp.PorcentajeDescuentoPorUnidad
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df