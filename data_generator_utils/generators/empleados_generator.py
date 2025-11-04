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
        """Genera empleados para todos los locales"""
        empleados = []
        empleados_por_local = {
            local_id: {
                "repartidor": [],
                "cocinero": [],
                "despachador": [],
                "info_empleados": {}  # Nuevo: diccionario con info completa
            }
            for local_id in locales_ids
        }
        
        empleado_counter = 1
        
        for local_id in locales_ids:
            num_empleados_local = random.randint(3, 7)
            
            for _ in range(num_empleados_local):
                empleado = cls._crear_empleado(empleado_counter, local_id)
                empleados.append(empleado)
                
                # Guardar DNI en lista por rol
                empleados_por_local[local_id][empleado["role"].lower()].append(empleado["dni"])
                
                # Guardar información completa del empleado
                empleados_por_local[local_id]["info_empleados"][empleado["dni"]] = {
                    "nombre": empleado["nombre"],
                    "apellido": empleado["apellido"],
                    "calificacion_prom": empleado.get("calificacion_prom")
                }
                
                empleado_counter += 1
        
        return empleados, empleados_por_local
    
    @classmethod
    def _crear_empleado(cls, counter, local_id):
        """Crea un empleado individual"""
        nombre = random.choice(SampleData.NOMBRES)
        apellido = random.choice(SampleData.APELLIDOS)
        dni = cls._generar_dni(counter)
        role = random.choice(["Repartidor", "Cocinero", "Despachador"])
        
        return {
            "local_id": local_id,
            "dni": dni,
            "nombre": nombre,
            "apellido": apellido,
            "calificacion_prom": round(random.uniform(3.5, 5.0), 2),
            "sueldo": round(random.uniform(1200, 3000), 2),
            "role": role
        }
    
    @staticmethod
    def _generar_dni(counter):
        """Genera un DNI único de 8 dígitos"""
        return f"{10000000 + counter:08d}"
