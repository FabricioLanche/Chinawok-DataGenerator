"""
Generador de usuarios
"""
import random
from ..helpers import Helpers
from ..sample_data import SampleData
from ..config import Config


class UsuariosGenerator:
    """Generador de usuarios (admin y clientes)"""
    
    @staticmethod
    def generar_usuarios():
        """Genera usuarios con admin y clientes"""
        usuarios = []
        usuarios_ids = []
        
        # ADMIN
        admin_id = Helpers.generar_uuid()
        usuarios_ids.append(admin_id)
        
        admin = {
            "PK": f"USER#{admin_id}",
            "SK": f"USER#{admin_id}",
            "usuario_id": admin_id,
            "nombre": Config.ADMIN_NOMBRE,
            "apellido": Config.ADMIN_APELLIDO,
            "email": Config.ADMIN_EMAIL,
            "telefono": Config.ADMIN_TELEFONO,
            "password_hash": f"hashed_{Config.ADMIN_PASSWORD}",
            "role": "admin",
            "activo": True,
            "created_at": Helpers.generar_timestamp(),
            "updated_at": Helpers.generar_timestamp()
        }
        
        usuarios.append(admin)
        
        # CLIENTES
        for i in range(Config.NUM_USUARIOS):
            nombre = random.choice(SampleData.NOMBRES)
            apellido = random.choice(SampleData.APELLIDOS)
            usuario_id = Helpers.generar_uuid()
            usuarios_ids.append(usuario_id)
            
            usuario = {
                "PK": f"USER#{usuario_id}",
                "SK": f"USER#{usuario_id}",
                "usuario_id": usuario_id,
                "nombre": nombre,
                "apellido": apellido,
                "email": Helpers.generar_email(nombre, apellido, str(i)),
                "telefono": Helpers.generar_telefono(),
                "password_hash": f"hashed_password_{random.randint(1000, 9999)}",
                "role": "cliente",
                "activo": True,
                "created_at": Helpers.generar_timestamp(),
                "updated_at": Helpers.generar_timestamp()
            }
            
            # 70% tienen información bancaria
            if random.random() < Config.PORCENTAJE_USUARIOS_CON_TARJETA:
                usuario["informacion_bancaria"] = {
                    "numero_tarjeta_encriptado": Helpers.generar_tarjeta(),
                    "cvv_encriptado": Helpers.generar_cvv(),
                    "fecha_vencimiento": Helpers.generar_fecha_vencimiento(),
                    "nombre_titular": f"{nombre} {apellido}",
                    "tipo_tarjeta": random.choice(Config.TIPOS_TARJETA)
                }
            
            usuario["direccion_facturacion"] = Helpers.generar_direccion(
                SampleData.CALLES,
                SampleData.DISTRITOS_LIMA
            )
            
            usuarios.append(usuario)
        
        return usuarios, usuarios_ids
