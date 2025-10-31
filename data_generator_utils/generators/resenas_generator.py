"""
Generador de Reseñas
"""
import random
from ..config import Config
from ..sample_data import SampleData

class ResenasGenerator:
    """Generador de datos para la tabla Reseñas"""
    
    @classmethod
    def generar_resenas(cls, pedidos):
        """Genera reseñas solo para pedidos completados"""
        resenas = []
        resena_counter = 1
        
        pedidos_completados = [p for p in pedidos if p["status"] == "recibido"]
        num_resenas = min(Config.NUM_RESENAS, len(pedidos_completados))
        pedidos_a_resenar = random.sample(pedidos_completados, num_resenas)
        
        for pedido in pedidos_a_resenar:
            resena = cls._crear_resena(resena_counter, pedido)
            resenas.append(resena)
            resena_counter += 1
        
        return resenas
    
    @classmethod
    def _crear_resena(cls, counter, pedido):
        """Crea una reseña individual"""
        calificacion = random.uniform(1, 5)
        
        if calificacion >= 4:
            resena_texto = random.choice(SampleData.RESENAS_POSITIVAS)
        elif calificacion >= 3:
            resena_texto = random.choice(SampleData.RESENAS_NEUTRAS)
        else:
            resena_texto = random.choice(SampleData.RESENAS_NEGATIVAS)
        
        empleados_disponibles = [
            pedido["cocinero_dni"],
            pedido["despachador_dni"],
            pedido["repartidor_dni"]
        ]
        
        num_empleados = random.randint(0, 3)
        empleados_dni = random.sample(empleados_disponibles, num_empleados) if num_empleados > 0 else []
        
        return {
            "local_id": pedido["local_id"],
            "resena_id": f"RES-{counter:05d}",
            "pedido_id": pedido["pedido_id"],
            "resena": resena_texto,
            "calificacion": round(calificacion, 2),
            "empleados_dni": empleados_dni
        }
