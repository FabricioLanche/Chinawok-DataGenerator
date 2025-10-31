"""
Generador de empleados
"""
import random
from datetime import datetime, timedelta
from ..helpers import Helpers
from ..sample_data import SampleData
from ..config import Config


class EmpleadosGenerator:
    """Generador de empleados por local"""
    
    @staticmethod
    def generar_empleados(locales_ids):
        """Genera empleados para cada local"""
        empleados = []
        empleados_por_local = {
            local_id: {"repartidor": [], "cocinero": [], "despachador": []}
            for local_id in locales_ids
        }
        
        for i in range(Config.NUM_EMPLEADOS):
            nombre = random.choice(SampleData.NOMBRES)
            apellido = random.choice(SampleData.APELLIDOS)
            dni = Helpers.generar_dni()
            local_id = random.choice(locales_ids)
            role = random.choice(Config.ROLES_EMPLEADO)
            
            empleado = {
                "PK": f"LOCAL#{local_id}",
                "SK": f"EMPLEADO#{dni}",
                "empleado_id": dni,
                "local_id": local_id,
                "dni": dni,
                "nombre": nombre,
                "apellido": apellido,
                "email": Helpers.generar_email(nombre, apellido, f"_{i}"),
                "telefono": Helpers.generar_telefono(),
                "role": role,
                "fecha_contratacion": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
                "salario": round(random.uniform(Config.SALARIO_MIN, Config.SALARIO_MAX), 2),
                "calificacion_promedio": round(random.uniform(3.5, 5.0), 2),
                "total_calificaciones": random.randint(10, 100),
                "activo": True,
                "turno": random.choice(Config.TURNOS),
                "created_at": Helpers.generar_timestamp(),
                "updated_at": Helpers.generar_timestamp()
            }
            
            empleados.append(empleado)
            empleados_por_local[local_id][role].append(dni)
        
        return empleados, empleados_por_local
