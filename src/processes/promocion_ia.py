import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

class PromocionIA:

    def entrenar_modelo(self, df):
        df['UltimaVenta'] = pd.to_datetime(df['UltimaVenta'])
        df['DiasSinVenta'] = (pd.Timestamp.today() - df['UltimaVenta']).dt.days
        X = df[['Stock', 'MargenGanancia', 'DiasSinVenta', 'HistorialPedidosJuntos']]
        y = df['DiasSinVenta']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        df['PrediccionRotacion'] = model.predict(X)
        return df

    def calcular_descuentos(self, df, n):
        df = self.entrenar_modelo(df)
        df['RangoStock'] = MinMaxScaler().fit_transform(df[['Stock']])
        df['MargenNormalizado'] = MinMaxScaler().fit_transform(df[['MargenGanancia']])
        df['Rotacion'] = MinMaxScaler().fit_transform(df[['PrediccionRotacion']])
        df['HistorialNormalizado'] = MinMaxScaler().fit_transform(df[['HistorialPedidosJuntos']])
        df['Puntaje'] = (
            df['RangoStock'] * 0.2 +
            df['MargenNormalizado'] * 0.3 +
            df['Rotacion'] * 0.3 +
            df['HistorialNormalizado'] * 0.2
        )
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
