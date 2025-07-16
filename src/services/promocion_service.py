import pandas as pd
import numpy as np
from sqlalchemy import text
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
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

def entrenar_modelo(df):
    df['UltimaVenta'] = pd.to_datetime(df['UltimaVenta'])
    df['DiasSinVenta'] = (pd.Timestamp.today() - df['UltimaVenta']).dt.days
    X = df[['Stock', 'MargenGanancia', 'DiasSinVenta', 'HistorialPedidosJuntos']]
    y = df['DiasSinVenta']
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    df['PrediccionRotacion'] = model.predict(X)
    return df

def calcular_descuentos(df, n):
    df = entrenar_modelo(df)
    df['RangoStock'] = MinMaxScaler().fit_transform(df[['Stock']])
    df['MargenNormalizado'] = MinMaxScaler().fit_transform(df[['MargenGanancia']])
    df['Rotacion'] = MinMaxScaler().fit_transform(df[['PrediccionRotacion']])
    df['HistorialNormalizado'] = MinMaxScaler().fit_transform(df[['HistorialPedidosJuntos']])
    df['Puntaje'] = df['RangoStock'] * 0.2 + df['MargenNormalizado'] * 0.3 + df['Rotacion'] * 0.3 + df['HistorialNormalizado'] * 0.2
    df = df.sort_values(by='Puntaje', ascending=False)

    categorias_seleccionadas = set()
    seleccionados = []
    for _, row in df.iterrows():
        if row['IdCategoria'] not in categorias_seleccionadas and len(seleccionados) < n and row['DescuentoPrevio'] == 0:
            descuento = min(row['MargenGanancia'] * 0.5, 20)
            seleccionados.append({
                'idProducto': row['Id'],
                'nombreProducto': row['Nombre'],
                'precioUnitario': row['Precio'],
                'precioXCant': row['Precio'],
                'cantidad': 1,
                'idCategoria': row['IdCategoria'],
                'descuento': round(descuento, 2)
            })
            categorias_seleccionadas.add(row['IdCategoria'])

        if len(seleccionados) >= n:
            break

    return seleccionados

def generar_descripcion(productos):
    return 'descripcion generada por IA openAI que está comentado para no consumir limites'

def generar_imagen(descripcion):
    return 'url de imagen generada por IA'
