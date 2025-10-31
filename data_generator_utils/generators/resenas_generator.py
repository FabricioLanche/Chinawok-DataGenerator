"""
Generador de reseñas
"""
import random
from ..helpers import Helpers
from ..sample_data import SampleData
from ..config import Config


class ResenasGenerator:
    """Generador de reseñas"""
    
    @staticmethod
    def generar_resenas(pedidos):
        """Genera reseñas para pedidos recibidos"""
        resenas = []
        
        pedidos_recibidos = [p for p in pedidos if p["status"] == "recibido"]
        
        if not pedidos_recibidos:
            print("  ⚠️  No hay pedidos recibidos. No se pueden generar reseñas.")
            return resenas
        
        num_resenas_a_generar = min(Config.NUM_RESENAS, len(pedidos_recibidos))
        pedidos_a_reseñar = random.sample(pedidos_recibidos, num_resenas_a_generar)
        
        for pedido in pedidos_a_reseñar:
            resena_id = Helpers.generar_uuid()
            local_id = pedido["local_id"]
            calificacion = round(random.uniform(3.5, 5.0), 1)
            
            resena = {
                "PK": f"LOCAL#{local_id}",
                "SK": f"RESENA#{resena_id}",
                "resena_id": resena_id,
                "local_id": local_id,
                "pedido_id": pedido["pedido_id"],
                "usuario_id": pedido["usuario_id"],
                "calificacion": calificacion,
                "comentario": random.choice(
                    SampleData.COMENTARIOS_POSITIVOS if calificacion >= 4.0 
                    else SampleData.COMENTARIOS_NEUTRALES
                ),
                "calificacion_comida": round(random.uniform(3.0, 5.0), 1),
                "calificacion_servicio": round(random.uniform(3.0, 5.0), 1),
                "calificacion_entrega": round(random.uniform(3.0, 5.0), 1),
                "respuesta_local": None,
                "fecha_respuesta": None,
                "verificada": True,
                "reportada": False,
                "created_at": Helpers.generar_timestamp(),
                "updated_at": Helpers.generar_timestamp()
            }
            
            # 60% incluyen calificación de empleado
            if random.random() < Config.PORCENTAJE_RESENAS_CON_EMPLEADO:
                if "repartidor_dni" in pedido and pedido["repartidor_dni"]:
                    resena["empleado_dni"] = pedido["repartidor_dni"]
                    resena["calificacion_empleado"] = round(random.uniform(3.5, 5.0), 1)
            
            resenas.append(resena)
        
        return resenas
