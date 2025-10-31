"""
Generador de combos
"""
import random
from datetime import datetime, timedelta
from ..helpers import Helpers
from ..config import Config


class CombosGenerator:
    """Generador de combos por local"""
    
    @staticmethod
    def generar_combos(locales_ids, productos_por_local, productos):
        """Genera combos para cada local"""
        combos = []
        combos_por_local = {local_id: [] for local_id in locales_ids}
        
        for local_id in locales_ids:
            num_combos = Config.NUM_COMBOS_POR_LOCAL + random.randint(-1, 2)
            
            for i in range(num_combos):
                combo_id = Helpers.generar_uuid()
                
                if not productos_por_local[local_id]:
                    continue
                
                num_productos = min(random.randint(2, 4), len(productos_por_local[local_id]))
                productos_combo = random.sample(productos_por_local[local_id], num_productos)
                
                precio_total = sum([
                    p["precio"] for p in productos 
                    if p["producto_id"] in productos_combo
                ])
                precio_combo = round(precio_total * random.uniform(0.7, 0.85), 2)
                
                combo = {
                    "PK": f"LOCAL#{local_id}",
                    "SK": f"COMBO#{combo_id}",
                    "combo_id": combo_id,
                    "local_id": local_id,
                    "nombre": f"Combo Especial {i + 1}",
                    "descripcion": f"Combo incluye {len(productos_combo)} productos deliciosos",
                    "productos_ids": productos_combo,
                    "precio": precio_combo,
                    "precio_original": precio_total,
                    "descuento_porcentaje": round(((precio_total - precio_combo) / precio_total) * 100, 0),
                    "disponible": True,
                    "imagen_url": f"https://chinawok.pe/images/combos/{combo_id}.jpg",
                    "valido_desde": Helpers.generar_timestamp(),
                    "valido_hasta": (datetime.now() + timedelta(days=random.randint(30, 90))).isoformat(),
                    "created_at": Helpers.generar_timestamp(),
                    "updated_at": Helpers.generar_timestamp()
                }
                
                combos.append(combo)
                combos_por_local[local_id].append(combo_id)
        
        return combos, combos_por_local
