"""
Generador de Combos
"""
import random
from ..config import Config


class CombosGenerator:
    """Generador de datos para la tabla Combos"""
    
    COMBOS_BASE = [
        {"nombre": "Combo Personal", "descripcion": "Plato principal + bebida", "num_productos": 2},
        {"nombre": "Combo Pareja", "descripcion": "2 platos principales + 2 bebidas", "num_productos": 4},
        {"nombre": "Combo Familiar", "descripcion": "3 platos + entrada + 3 bebidas", "num_productos": 7},
        {"nombre": "Combo Ejecutivo", "descripcion": "Plato principal + sopa + bebida", "num_productos": 3},
        {"nombre": "Combo Premium", "descripcion": "2 platos especiales + entrada + 2 bebidas + postre", "num_productos": 6}
    ]
    
    @classmethod
    def generar_combos(cls, locales_ids, productos_por_local, productos):
        """Genera combos para cada local"""
        combos = []
        combos_por_local = {}
        combo_counter = 1
        
        for local_id in locales_ids:
            combos_local = []
            productos_local = productos_por_local.get(local_id, [])
            
            if not productos_local:
                continue
            
            for combo_base in cls.COMBOS_BASE:
                num_productos = min(combo_base["num_productos"], len(productos_local))
                productos_seleccionados = random.sample(productos_local, num_productos)
                
                combo = {
                    "local_id": local_id,
                    "combo_id": f"COMBO-{combo_counter:05d}",
                    "nombre": combo_base["nombre"],
                    "productos_nombres": productos_seleccionados,
                    "descripcion": combo_base["descripcion"]
                }
                
                combos.append(combo)
                combos_local.append(combo["combo_id"])
                combo_counter += 1
            
            combos_por_local[local_id] = combos_local
        
        return combos, combos_por_local
