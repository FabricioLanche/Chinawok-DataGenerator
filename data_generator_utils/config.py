"""
Configuración del generador de datos
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración centralizada para el generador de datos"""
    
    # Cantidades de registros
    NUM_LOCALES = 100
    NUM_USUARIOS = 5000
    NUM_PRODUCTOS_POR_LOCAL = 50
    NUM_EMPLEADOS = 500
    NUM_COMBOS_POR_LOCAL = 5
    NUM_PEDIDOS = 10000
    NUM_OFERTAS_POR_LOCAL = 5
    NUM_RESENAS = 1000
    
    # Directorio de salida
    OUTPUT_DIR = "dynamodb_data"
    
    # Porcentajes
    PORCENTAJE_USUARIOS_CON_TARJETA = 0.7
    PORCENTAJE_PRODUCTOS_VEGETARIANOS = 0.3
    PORCENTAJE_PRODUCTOS_PICANTES = 0.3
    PORCENTAJE_RESENAS_CON_EMPLEADO = 0.6
    
    # Rangos de precios
    PRECIO_MIN_PRODUCTO = 10.0
    PRECIO_MAX_PRODUCTO = 50.0
    PRECIO_MIN_DELIVERY = 3.0
    PRECIO_MAX_DELIVERY = 8.0
    
    # Rangos de salarios
    SALARIO_MIN = 1200.0
    SALARIO_MAX = 3000.0
    
    # Admin credentials
    ADMIN_NOMBRE = os.getenv('ADMIN_NOMBRE', 'Administrador')
    ADMIN_APELLIDO = os.getenv('ADMIN_APELLIDO', 'Sistema')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@chinawok.pe')
    ADMIN_TELEFONO = os.getenv('ADMIN_TELEFONO', '+51-999999999')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Admin123!')
    
    # Estados de pedidos
    ESTADOS_PEDIDO = ["eligiendo", "cocinando", "empacando", "enviando", "recibido"]
    
    # Roles de empleados (DEBEN coincidir con schema: Primera letra mayúscula)
    ROLES_EMPLEADO = ["Repartidor", "Cocinero", "Despachador"]
    
    # Categorías de productos (DEBEN coincidir con schema exactamente)
    CATEGORIAS_PRODUCTO = [
        "Arroces",
        "Tallarines",
        "Pollo al wok",
        "Carne de res",
        "Cerdo",
        "Mariscos",
        "Entradas",
        "Guarniciones",
        "Sopas",
        "Combos",
        "Bebidas",
        "Postres"
    ]
    
    # Roles de usuarios (DEBEN coincidir con schema: Primera letra mayúscula)
    ROLES_USUARIO = ["Cliente", "Admin"]

    @classmethod
    def crear_directorio_salida(cls):
        """Crea el directorio de salida si no existe"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
