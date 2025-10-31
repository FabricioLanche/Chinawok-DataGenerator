"""
Generador de Usuarios
"""
import random
from ..config import Config
from ..sample_data import SampleData
from ..utils import generar_email, generar_password, generar_tarjeta

class UsuariosGenerator:
    """Generador de datos para la tabla Usuarios"""
    
    @classmethod
    def generar_usuarios(cls):
        """Genera la lista de usuarios y retorna (usuarios, correos)"""
        usuarios = []
        correos_generados = set()
        
        # 1. Crear usuario administrador
        admin = cls._crear_admin()
        usuarios.append(admin)
        correos_generados.add(admin["correo"])
        
        # 2. Crear usuarios clientes
        for i in range(Config.NUM_USUARIOS):
            usuario = cls._crear_cliente(correos_generados)
            usuarios.append(usuario)
            correos_generados.add(usuario["correo"])
        
        return usuarios, list(correos_generados)
    
    @classmethod
    def _crear_admin(cls):
        """Crea el usuario administrador desde variables de entorno"""
        admin = {
            "nombre": f"{Config.ADMIN_NOMBRE} {Config.ADMIN_APELLIDO}",
            "correo": Config.ADMIN_EMAIL,
            "contrasena": Config.ADMIN_PASSWORD,
            "role": "Admin"
        }
        return admin
    
    @classmethod
    def _crear_cliente(cls, correos_existentes):
        """Crea un usuario cliente"""
        nombre = random.choice(SampleData.NOMBRES)
        apellido = random.choice(SampleData.APELLIDOS)
        
        # Generar correo único
        correo = generar_email(nombre, apellido)
        while correo in correos_existentes:
            correo = generar_email(nombre, apellido)
        
        usuario = {
            "nombre": f"{nombre} {apellido}",
            "correo": correo,
            "contrasena": generar_password(),
            "role": "Cliente"
        }
        
        # Agregar información bancaria (70% de los usuarios)
        if random.random() < Config.PORCENTAJE_USUARIOS_CON_TARJETA:
            usuario["informacion_bancaria"] = generar_tarjeta()
        
        return usuario
