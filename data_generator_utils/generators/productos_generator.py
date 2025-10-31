"""
Generador de productos
"""
import random
from ..helpers import Helpers
from ..sample_data import SampleData
from ..config import Config


class ProductosGenerator:
    """Generador de productos por local"""
    
    @staticmethod
    def generar_productos(locales_ids):
        """Genera productos para cada local"""
        productos = []
        productos_por_local = {local_id: [] for local_id in locales_ids}
        
        for local_id in locales_ids:
            num_productos = Config.NUM_PRODUCTOS_POR_LOCAL + random.randint(-2, 2)
            nombres_seleccionados = random.sample(
                SampleData.PRODUCTOS_NOMBRES,
                min(num_productos, len(SampleData.PRODUCTOS_NOMBRES))
            )
            
            for nombre_prod in nombres_seleccionados:
                producto_id = Helpers.generar_uuid()
                categoria = random.choice(SampleData.CATEGORIAS)
                
                producto = {
                    "PK": f"LOCAL#{local_id}",
                    "SK": f"PRODUCTO#{producto_id}",
                    "producto_id": producto_id,
                    "local_id": local_id,
                    "nombre": nombre_prod,
                    "descripcion": f"Delicioso {nombre_prod.lower()} preparado con ingredientes frescos",
                    "categoria": categoria,
                    "precio": round(random.uniform(Config.PRECIO_MIN_PRODUCTO, Config.PRECIO_MAX_PRODUCTO), 2),
                    "precio_descuento": None,
                    "stock": random.randint(10, 100),
                    "stock_minimo": 5,
                    "imagen_url": f"https://chinawok.pe/images/productos/{producto_id}.jpg",
                    "disponible": True,
                    "es_vegetariano": categoria in ["Tallarines", "Arroces"] and random.random() > Config.PORCENTAJE_PRODUCTOS_VEGETARIANOS,
                    "es_picante": random.random() < Config.PORCENTAJE_PRODUCTOS_PICANTES,
                    "calorias": random.randint(200, 800),
                    "tiempo_preparacion": random.randint(10, 30),
                    "ingredientes": ["Ingrediente 1", "Ingrediente 2", "Ingrediente 3"],
                    "alergenos": random.sample(["Gluten", "Soya", "Mariscos", "Ninguno"], k=1),
                    "created_at": Helpers.generar_timestamp(),
                    "updated_at": Helpers.generar_timestamp()
                }
                
                productos.append(producto)
                productos_por_local[local_id].append(producto_id)
        
        return productos, productos_por_local
