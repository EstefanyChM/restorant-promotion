from src.repository.promocion_repository import PromocionRepository
from src.processes.promocion_ia import PromocionIA

class PromocionService:

    def __init__(self, engine):
        self.repository = PromocionRepository(engine)
        self.ia = PromocionIA()

    def productos_mayor_ganancia(self, cantidad: int):
        df = self.repository.obtener_productos()
        productos_seleccionados = self.ia.calcular_descuentos(df, cantidad)
        return productos_seleccionados
    

    def productos_mayor_ganancia_categoria(self, id_categoria: int):
        df = self.repository.obtener_productos()
        df_categoria = df[df['IdCategoria'] == int(id_categoria)]
        productos_seleccionados = self.ia.calcular_descuentos(df_categoria, 1)
    
        return productos_seleccionados
