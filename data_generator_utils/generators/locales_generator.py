"""
Generador de Locales
"""
import random
from ..config import Config
from ..sample_data import SampleData

class LocalesGenerator:
    """Generador de datos para la tabla Locales"""
    
    @classmethod
    def generar_locales(cls):
        """Genera la lista de locales"""
        locales = []
        locales_ids = []
        
        for i in range(Config.NUM_LOCALES):
            local_id = f"LOCAL-{i+1:04d}"
            local = {
                "local_id": local_id,
                "direccion": random.choice(SampleData.DIRECCIONES_LIMA),
                "telefono": cls._generar_telefono(),
                "hora_apertura": "10:00",
                "hora_finalizacion": "22:00"
            }
            
            locales.append(local)
            locales_ids.append(local_id)
        
        return locales, locales_ids
    
    @staticmethod
    def _generar_telefono():
        """Genera un teléfono peruano válido"""
        return f"+51-{random.randint(900000000, 999999999)}"
