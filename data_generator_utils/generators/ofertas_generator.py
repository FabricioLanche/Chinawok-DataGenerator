"""
Generador de Ofertas
"""
import random
from datetime import datetime, timedelta
from ..config import Config


class OfertasGenerator:
    """Generador de datos para la tabla Ofertas"""
    
    @classmethod
    def generar_ofertas(cls, locales_ids, productos_por_local, combos_por_local):
        """Genera ofertas para productos y combos"""
        ofertas = []
        oferta_counter = 1
        
        for local_id in locales_ids:
            productos = productos_por_local.get(local_id, [])
            combos = combos_por_local.get(local_id, [])
            
            # Ofertas para productos (70%)
            num_ofertas_productos = int(Config.NUM_OFERTAS_POR_LOCAL * 0.7)
            for _ in range(num_ofertas_productos):
                if productos:
                    oferta = cls._crear_oferta_producto(
                        oferta_counter,
                        local_id,
                        random.choice(productos)
                    )
                    ofertas.append(oferta)
                    oferta_counter += 1
            
            # Ofertas para combos (30%)
            num_ofertas_combos = Config.NUM_OFERTAS_POR_LOCAL - num_ofertas_productos
            for _ in range(num_ofertas_combos):
                if combos:
                    oferta = cls._crear_oferta_combo(
                        oferta_counter,
                        local_id,
                        random.choice(combos)
                    )
                    ofertas.append(oferta)
                    oferta_counter += 1
        
        return ofertas
    
    @classmethod
    def _crear_oferta_producto(cls, counter, local_id, producto_nombre):
        """Crea una oferta para un producto"""
        fecha_inicio = datetime.now()
        fecha_limite = fecha_inicio + timedelta(days=random.randint(7, 30))
        
        return {
            "local_id": local_id,
            "oferta_id": f"OFE-{counter:05d}",
            "producto_nombre": producto_nombre,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_limite": fecha_limite.isoformat(),
            "porcentaje_descuento": random.choice([10, 15, 20, 25, 30])
        }
    
    @classmethod
    def _crear_oferta_combo(cls, counter, local_id, combo_id):
        """Crea una oferta para un combo"""
        fecha_inicio = datetime.now()
        fecha_limite = fecha_inicio + timedelta(days=random.randint(7, 30))
        
        return {
            "local_id": local_id,
            "oferta_id": f"OFE-{counter:05d}",
            "combo_id": combo_id,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_limite": fecha_limite.isoformat(),
            "porcentaje_descuento": random.choice([15, 20, 25, 30])
        }
