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
    def generar_resenas(cls, pedidos, empleados_por_local):
        """Genera reseñas para pedidos completados con los 3 roles de empleados"""
        resenas = []
        
        pedidos_completados = [p for p in pedidos if p["estado"] == "recibido"]
        num_resenas = min(Config.NUM_RESENAS, len(pedidos_completados))
        pedidos_a_resenar = random.sample(pedidos_completados, num_resenas)
        
        for pedido in pedidos_a_resenar:
            resena = cls._crear_resena(pedido, empleados_por_local)
            if resena:  # Solo agregar si se pudo crear correctamente
                resenas.append(resena)
        
        print(f"  ✅ {len(resenas)} reseñas generadas")
        return resenas
    
    @classmethod
    def _crear_resena(cls, pedido, empleados_por_local):
        """Crea una reseña con los DNIs de cocinero, repartidor y despachador"""
        # Extraer empleados del historial_estados por rol (en minúsculas según schema de pedidos)
        cocinero_dni = None
        repartidor_dni = None
        despachador_dni = None
        
        for entrada in pedido.get("historial_estados", []):
            empleado = entrada.get("empleado")
            if empleado and empleado.get("dni") and empleado.get("rol"):
                rol = empleado["rol"].lower()  # Asegurar minúsculas
                if rol == "cocinero" and not cocinero_dni:
                    cocinero_dni = empleado["dni"]
                elif rol == "repartidor" and not repartidor_dni:
                    repartidor_dni = empleado["dni"]
                elif rol == "despachador" and not despachador_dni:
                    despachador_dni = empleado["dni"]
        
        # Si falta algún empleado, intentar obtenerlo del local
        local_id = pedido["local_id"]
        
        # Verificar si empleados_por_local es un dict con listas de objetos empleado
        if local_id not in empleados_por_local:
            print(f"  ⚠️  Local {local_id} no encontrado en empleados_por_local")
            return None
        
        empleados_data = empleados_por_local[local_id]
        
        # empleados_por_local[local_id] debería ser una lista de objetos empleado
        if not cocinero_dni:
            cocineros = [e for e in empleados_data if isinstance(e, dict) and e.get("role") == "Cocinero"]
            if cocineros:
                cocinero_dni = random.choice(cocineros)["dni"]
        
        if not repartidor_dni:
            repartidores = [e for e in empleados_data if isinstance(e, dict) and e.get("role") == "Repartidor"]
            if repartidores:
                repartidor_dni = random.choice(repartidores)["dni"]
        
        if not despachador_dni:
            despachadores = [e for e in empleados_data if isinstance(e, dict) and e.get("role") == "Despachador"]
            if despachadores:
                despachador_dni = random.choice(despachadores)["dni"]
        
        # Validar que tengamos los 3 empleados
        if not all([cocinero_dni, repartidor_dni, despachador_dni]):
            print(f"  ⚠️  No se pudo crear reseña para pedido {pedido['pedido_id']} - faltan empleados")
            return None
        
        resena_id = Helpers.generar_uuid()
        calificacion = random.uniform(1, 5)
        
        if calificacion >= 4:
            resena_texto = random.choice(SampleData.RESENAS_POSITIVAS)
        elif calificacion >= 3:
            resena_texto = random.choice(SampleData.RESENAS_NEUTRAS)
        else:
            resena_texto = random.choice(SampleData.RESENAS_NEGATIVAS)
        
        return {
            "local_id": local_id,
            "cocinero_dni": cocinero_dni,
            "repartidor_dni": repartidor_dni,
            "despachador_dni": despachador_dni,
            "resena_id": resena_id,
            "pedido_id": pedido["pedido_id"],
            "resena": resena_texto,
            "calificacion": round(calificacion, 2)
        }
