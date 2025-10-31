"""
Generador de ofertas
"""
import random
from datetime import datetime, timedelta
from ..helpers import Helpers
from ..config import Config


class OfertasGenerator:
    """Generador de ofertas por local"""
    
    @staticmethod
    def generar_ofertas(locales_ids, productos_por_local, combos_por_local):
        """Genera ofertas para cada local"""
        ofertas = []
        
        for local_id in locales_ids:
            num_ofertas = Config.NUM_OFERTAS_POR_LOCAL + random.randint(-1, 1)
            
            for i in range(num_ofertas):
                oferta_id = Helpers.generar_uuid()
                tipo_oferta = random.choice(["producto", "combo", "descuento_general"])
                
                fecha_inicio = datetime.now() - timedelta(days=random.randint(0, 30))
                fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 60))
                
                oferta = {
                    "PK": f"LOCAL#{local_id}",
                    "SK": f"OFERTA#{oferta_id}",
                    "oferta_id": oferta_id,
                    "local_id": local_id,
                    "nombre": f"Oferta Especial {i+1}",
                    "descripcion": "Aprovecha esta increíble oferta por tiempo limitado",
                    "tipo": tipo_oferta,
                    "descuento_porcentaje": random.randint(10, 50),
                    "descuento_monto": None,
                    "fecha_inicio": fecha_inicio.isoformat(),
                    "fecha_fin": fecha_fin.isoformat(),
                    "activo": True,
                    "dias_aplicables": random.sample(Config.DIAS_SEMANA, k=random.randint(3, 7)),
                    "horario_inicio": "00:00",
                    "horario_fin": "23:59",
                    "cantidad_maxima_usos": random.randint(50, 200),
                    "cantidad_usos_actuales": random.randint(0, 50),
                    "created_at": Helpers.generar_timestamp(),
                    "updated_at": Helpers.generar_timestamp()
                }
                
                if tipo_oferta == "producto" and productos_por_local[local_id]:
                    oferta["producto_id"] = random.choice(productos_por_local[local_id])
                elif tipo_oferta == "combo" and combos_por_local[local_id]:
                    oferta["combo_id"] = random.choice(combos_por_local[local_id])
                
                ofertas.append(oferta)
        
        return ofertas
