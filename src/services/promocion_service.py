import pandas as pd
import numpy as np
from sqlalchemy import text
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from src.database.db_engine import engine
from src.repository.promocion_repository import obtener_productos
from src.processes.promocion_ia import *



def productos_mayor_ganancia(cantidad: int):
    df = obtener_productos()
    productos_seleccionados = calcular_descuentos(df, cantidad)
    return productos_seleccionados


def productos_mayor_ganancia_categoria(id_categoria: int):
    df = obtener_productos()
    df_categoria = df[df['IdCategoria'] == int(id_categoria)]
    productos_seleccionados = calcular_descuentos(df_categoria, 1)

    return productos_seleccionados
