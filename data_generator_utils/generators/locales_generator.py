"""
Generador de locales
"""
import random
from ..helpers import Helpers
from ..sample_data import SampleData
from ..config import Config


class LocalesGenerator:
    """Generador de locales de China Wok"""
    
    @staticmethod
    def generar_locales():
        """Genera locales con sus datos completos"""
        locales = []
        locales_ids = []
        
        for i in range(Config.NUM_LOCALES):
            local_id = Helpers.generar_uuid()
            locales_ids.append(local_id)
            
            distrito = random.choice(SampleData.DISTRITOS_LIMA)
            calle = random.choice(SampleData.CALLES)
            numero = str(random.randint(100, 9999))
            codigo_postal = f"150{random.randint(10, 99)}"
            
            local = {
                "PK": f"LOCAL#{local_id}",
                "SK": f"LOCAL#{local_id}",
                "local_id": local_id,
                "nombre": f"China Wok {distrito}",
                "direccion": {
                    "calle": calle,
                    "numero": numero,
                    "distrito": distrito,
                    "ciudad": "Lima",
                    "codigo_postal": codigo_postal
                },
                "telefono": Helpers.generar_telefono(),
                "email": f"local{i+1}@chinawok.pe",
                "horario": {
                    "apertura": "08:00",
                    "cierre": "22:00",
                    "dias_atencion": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
                },
                "capacidad_maxima": random.randint(50, 200),
                "activo": True,
                "created_at": Helpers.generar_timestamp(),
                "updated_at": Helpers.generar_timestamp()
            }
            
            locales.append(local)
        
        return locales, locales_ids
