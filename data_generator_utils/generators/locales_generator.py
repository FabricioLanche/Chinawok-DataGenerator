"""
Generador de Locales
"""
import random
from ..config import Config
from ..sample_data import SampleData
from ..helpers import Helpers

class LocalesGenerator:
    """Generador de datos para la tabla Locales"""
    
    @classmethod
    def generar_locales(cls):
        """Genera locales con administradores únicos"""
        locales = []
        locales_ids = []
        
        for i in range(Config.NUM_LOCALES):
            local = cls._crear_local(i)
            locales.append(local)
            locales_ids.append(local["local_id"])
        
        print(f"  ✅ {Config.NUM_LOCALES} locales generados (cada uno con su administrador)")
        return locales, locales_ids
    
    @classmethod
    def _crear_local(cls, index):
        """Crea un local individual con su administrador"""
        local_id = Helpers.generar_uuid()
        direccion = random.choice(SampleData.DIRECCIONES_LIMA)
        
        # Generar administrador único para este local
        nombre_admin = random.choice(SampleData.NOMBRES)
        apellido_admin = random.choice(SampleData.APELLIDOS)
        
        return {
            "local_id": local_id,
            "direccion": direccion,
            "telefono": f"+51{random.randint(900000000, 999999999)}",
            "hora_apertura": "08:00",
            "hora_finalizacion": "22:00",
            "administrador": {
                "nombre": f"{nombre_admin} {apellido_admin}",
                "correo": f"admin.{index + 1:03d}@chinawok.pe",
                "contrasena": f"Admin{index + 1:03d}!123"
            }
        }
