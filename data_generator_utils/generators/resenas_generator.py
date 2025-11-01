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
            # Generar reseñas para cada empleado que participó en el pedido
            empleados_en_pedido = []
            
            if pedido.get("cocinero_dni"):
                empleados_en_pedido.append(pedido["cocinero_dni"])
            if pedido.get("despachador_dni"):
                empleados_en_pedido.append(pedido["despachador_dni"])
            if pedido.get("repartidor_dni"):
                empleados_en_pedido.append(pedido["repartidor_dni"])
            
            # Crear una reseña por cada empleado
            for empleado_dni in empleados_en_pedido:
                resena = cls._crear_resena(resena_counter, pedido, empleado_dni)
                resenas.append(resena)
                resena_counter += 1
        
        return resenas
    
    @classmethod
    def _crear_resena(cls, counter, pedido, empleado_dni):
        """Crea una reseña individual para un empleado específico"""
        calificacion = random.uniform(1, 5)
        
        if calificacion >= 4:
            resena_texto = random.choice(SampleData.RESENAS_POSITIVAS)
        elif calificacion >= 3:
            resena_texto = random.choice(SampleData.RESENAS_NEUTRAS)
        else:
            resena_texto = random.choice(SampleData.RESENAS_NEGATIVAS)
        
        local_id = pedido["local_id"]
        
        # Crear partition key compuesta: LOCAL#<local_id>#EMP#<empleado_dni>
        pk = f"LOCAL#{local_id}#EMP#{empleado_dni}"
        
        return {
            "pk": pk,
            "local_id": local_id,
            "empleado_dni": empleado_dni,
            "resena_id": f"RES-{counter:05d}",
            "pedido_id": pedido["pedido_id"],
            "resena": resena_texto,
            "calificacion": round(calificacion, 2)
        }
