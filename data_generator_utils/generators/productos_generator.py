"""
Generador de Productos
"""
import random
from ..config import Config
from ..helpers import Helpers

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
        """Genera productos únicos para cada local (multi-tenancy)"""
        productos = []
        productos_por_local = {}
        
        for local_id in locales_ids:
            # Cada local tiene su propia lista de productos
            productos_por_local[local_id] = []
            
            # Cada local tiene entre 30-50 productos
            num_productos_local = random.randint(30, 50)
            
            for i in range(num_productos_local):
                producto = cls._crear_producto(local_id)
                productos.append(producto)
                # Guardar el NOMBRE del producto para este local
                productos_por_local[local_id].append(producto["nombre"])
        
        print(f"  ✅ {len(productos)} productos generados")
        print(f"  ℹ️  Distribuidos en {len(locales_ids)} locales")
        return productos, productos_por_local
    
    @classmethod
    def _crear_producto(cls, local_id):
        """Crea un producto individual con datos aleatorios"""
        nombre_categoria = random.choice(list(cls.PRODUCTOS_BASE.keys()))
        nombre_producto = random.choice(cls.PRODUCTOS_BASE[nombre_categoria])
        
        # Solo campos permitidos por el schema de validación
        return {
            "local_id": local_id,
            "nombre": nombre_producto,
            "precio": round(random.uniform(Config.PRECIO_MIN_PRODUCTO, Config.PRECIO_MAX_PRODUCTO), 2),
            "descripcion": f"{nombre_producto} preparado al estilo China Wok",
            "categoria": nombre_categoria,
            "stock": random.randint(10, 100)
        }
