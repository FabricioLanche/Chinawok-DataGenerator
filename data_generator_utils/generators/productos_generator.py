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

        """
Generador de Productos
"""
import random
from ..config import Config

class ProductosGenerator:
    """Generador de datos para la tabla Productos"""
    
    PRODUCTOS_BASE = {
        "Arroces": [
            "Arroz Chaufa de Pollo", "Arroz Chaufa de Carne", "Arroz Chaufa Mixto",
            "Arroz Chaufa de Mariscos", "Arroz Chaufa Especial"
        ],
        "Tallarines": [
            "Tallarín Saltado de Pollo", "Tallarín Saltado de Carne",
            "Tallarín Saltado Mixto", "Tallarín con Mariscos"
        ],
        "Pollo al wok": [
            "Pollo con Tamarindo", "Pollo Chi Jau Kay", "Pollo Tipakay",
            "Pollo con Verduras"
        ],
        "Carne de res": [
            "Carne Mongoliana", "Lomo Saltado", "Carne con Ostión",
            "Carne con Verduras al Wok"
        ],
        "Cerdo": [
            "Cerdo Agridulce", "Chancho con Tamarindo", "Cerdo al Sillao"
        ],
        "Mariscos": [
            "Chicharrón de Calamar", "Camarones al Tamarindo",
            "Arroz con Mariscos", "Chijaukai de Mariscos"
        ],
        "Entradas": [
            "Wantán Frito", "Empanaditas Chinas", "Siu Mai",
            "Rollitos Primavera"
        ],
        "Guarniciones": [
            "Arroz Blanco", "Wantanes Fritos", "Chapsui de Verduras"
        ],
        "Sopas": [
            "Sopa Wantán", "Sopa de Gallina China", "Sopa Min"
        ],
        "Bebidas": [
            "Chicha Morada 1L", "Inca Kola 1.5L", "Agua Mineral 625ml",
            "Té Helado 500ml"
        ],
        "Postres": [
            "Helado de Lúcuma", "Picarones", "Mazamorra Morada"
        ]
    }
    
    @classmethod
    def generar_productos(cls, locales_ids):
        """Genera productos para todos los locales"""
        productos = []
        productos_por_local = {}
        
        for local_id in locales_ids:
            productos_local = []
            
            for categoria, items in cls.PRODUCTOS_BASE.items():
                for nombre in items:
                    producto = {
                        "local_id": local_id,
                        "nombre": nombre,
                        "precio": round(random.uniform(
                            Config.PRECIO_MIN_PRODUCTO,
                            Config.PRECIO_MAX_PRODUCTO
                        ), 2),
                        "descripcion": f"{nombre} preparado al estilo China Wok",
                        "categoria": categoria,
                        "stock": random.randint(10, 100)
                    }
                    productos.append(producto)
                    productos_local.append(nombre)
            
            productos_por_local[local_id] = productos_local
        
        return productos, productos_por_local
