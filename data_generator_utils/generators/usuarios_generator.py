"""
Generador de Usuarios
"""
import random
from ..config import Config
from ..sample_data import SampleData

class UsuariosGenerator:
    """Generador de datos para la tabla Usuarios"""
    
    @classmethod
    def generar_usuarios(cls):
        """Genera administradores (proporcionales a locales) + clientes"""
        usuarios = []
        usuarios_ids = []
        
        # Crear administradores (1 por cada 10 clientes aproximadamente)
        num_admins = max(1, Config.NUM_USUARIOS // 10)
        
        for i in range(num_admins):
            admin = cls._crear_administrador(i)
            usuarios.append(admin)
            usuarios_ids.append(admin["correo"])
        
        # Crear clientes
        for i in range(Config.NUM_USUARIOS):
            usuario = cls._crear_cliente(i)
            usuarios.append(usuario)
            usuarios_ids.append(usuario["correo"])
        
        print(f"  ✅ {num_admins} administradores + {Config.NUM_USUARIOS} clientes generados")
        return usuarios, usuarios_ids
    
    @classmethod
    def _crear_administrador(cls, index):
        """Crea un usuario administrador"""
        nombre = random.choice(SampleData.NOMBRES)
        apellido = random.choice(SampleData.APELLIDOS)
        
        return {
            "nombre": nombre,
            "apellido": apellido,
            "correo": f"admin{index+1:03d}@chinawok.pe",
            "telefono": f"+51{random.randint(900000000, 999999999)}",
            "contrasena": f"Admin{index+1:03d}!",
            "role": "admin"
        }
    
    @classmethod
    def _crear_cliente(cls, index):
        """Crea un cliente individual"""
        nombre = random.choice(SampleData.NOMBRES)
        apellido = random.choice(SampleData.APELLIDOS)
        
        usuario = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": f"{nombre.lower()}.{apellido.lower()}{index}@email.com",
            "telefono": f"+51{random.randint(900000000, 999999999)}",
            "contrasena": f"cliente{index:04d}",
            "role": "cliente"
        }
        
        # 70% de los clientes tienen información bancaria COMPLETA
        if random.random() > 0.3:
            usuario["informacion_bancaria"] = {
                "numero_tarjeta": ''.join([str(random.randint(0, 9)) for _ in range(16)]),
                "cvv": ''.join([str(random.randint(0, 9)) for _ in range(3)]),
                "fecha_vencimiento": f"{random.randint(1, 12):02d}/{random.randint(25, 30):02d}",
                "direccion_delivery": random.choice(SampleData.DIRECCIONES_LIMA)
            }
        
        return usuario
