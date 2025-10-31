"""
Generador de Empleados
"""
import random
from ..config import Config
from ..sample_data import SampleData

class EmpleadosGenerator:
    """Generador de datos para la tabla Empleados"""
    
    @classmethod
    def generar_empleados(cls, locales_ids):
        """Genera empleados distribuidos por locales"""
        empleados = []
        empleados_por_local = {}
        dnis_generados = set()
        
        empleados_por_local_count = Config.NUM_EMPLEADOS // len(locales_ids)
        
        for local_id in locales_ids:
            empleados_local = {
                "Cocinero": [],
                "Despachador": [],
                "Repartidor": []
            }
            
            for _ in range(empleados_por_local_count):
                empleado = cls._crear_empleado(local_id, dnis_generados)
                empleados.append(empleado)
                empleados_local[empleado["role"]].append(empleado["dni"])
            
            empleados_por_local[local_id] = empleados_local
        
        return empleados, empleados_por_local
    
    @classmethod
    def _crear_empleado(cls, local_id, dnis_existentes):
        """Crea un empleado individual"""
        dni = cls._generar_dni()
        while dni in dnis_existentes:
            dni = cls._generar_dni()
        dnis_existentes.add(dni)
        
        empleado = {
            "local_id": local_id,
            "dni": dni,
            "nombre": random.choice(SampleData.NOMBRES),
            "apellido": random.choice(SampleData.APELLIDOS),
            "role": random.choice(Config.ROLES_EMPLEADO),
            "calificacion_prom": round(random.uniform(3.5, 5.0), 2),
            "sueldo": round(random.uniform(Config.SALARIO_MIN, Config.SALARIO_MAX), 2)
        }
        
        return empleado
    
    @staticmethod
    def _generar_dni():
        """Genera un DNI peruano válido (8 dígitos)"""
        return f"{random.randint(10000000, 99999999)}"
