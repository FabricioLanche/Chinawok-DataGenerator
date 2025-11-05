"""
Generador de Reseñas
"""
import random
from ..config import Config
from ..sample_data import SampleData
from ..helpers import Helpers

class ResenasGenerator:
    """Generador de datos para la tabla Reseñas"""
    
    @classmethod
    def generar_resenas(cls, pedidos):
        """Genera reseñas solo para pedidos completados"""
        resenas = []
        
        pedidos_completados = [p for p in pedidos if p["estado"] == "recibido"]
        num_resenas = min(Config.NUM_RESENAS, len(pedidos_completados))
        pedidos_a_resenar = random.sample(pedidos_completados, num_resenas)
        
        for pedido in pedidos_a_resenar:
            # Extraer empleados del historial_estados
            empleados_en_pedido = []
            
            for entrada in pedido.get("historial_estados", []):
                empleado = entrada.get("empleado")
                if empleado and empleado.get("dni"):
                    # Evitar duplicados
                    if empleado["dni"] not in [e["dni"] for e in empleados_en_pedido]:
                        empleados_en_pedido.append(empleado)
            
            # Crear una reseña por cada empleado
            for empleado in empleados_en_pedido:
                resena = cls._crear_resena(pedido, empleado)
                resenas.append(resena)
        
        print(f"  ✅ {len(resenas)} reseñas generadas")
        return resenas
    
    @classmethod
    def _crear_resena(cls, pedido, empleado):
        """Crea una reseña individual para un empleado específico"""
        resena_id = Helpers.generar_uuid()
        calificacion = random.uniform(1, 5)
        
        if calificacion >= 4:
            resena_texto = random.choice(SampleData.RESENAS_POSITIVAS)
        elif calificacion >= 3:
            resena_texto = random.choice(SampleData.RESENAS_NEUTRAS)
        else:
            resena_texto = random.choice(SampleData.RESENAS_NEGATIVAS)
        
        local_id = pedido["local_id"]
        empleado_dni = empleado["dni"]
        pk = f"LOCAL#{local_id}#EMP#{empleado_dni}"
        
        return {
            "pk": pk,
            "local_id": local_id,
            "empleado_dni": empleado_dni,
            "resena_id": resena_id,
            "pedido_id": pedido["pedido_id"],
            "resena": resena_texto,
            "calificacion": round(calificacion, 2)
        }
