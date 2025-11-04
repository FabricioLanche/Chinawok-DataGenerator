"""
Generador de Pedidos con máquina de estados
"""
import random
from datetime import datetime, timedelta
from ..config import Config
from ..sample_data import SampleData


class PedidosGenerator:
    """Generador de datos para la tabla Pedidos con máquina de estados"""
    
    ESTADOS = ["procesando", "cocinando", "empacando", "enviando", "recibido"]
    
    @classmethod
    def generar_pedidos(cls, locales_ids, usuarios, productos, productos_por_local, empleados_por_local):
        """Genera pedidos con estados progresivos"""
        pedidos = []
        
        usuarios_validos = [u for u in usuarios if u.get("informacion_bancaria") and u.get("role") == "cliente"]
        
        if not usuarios_validos:
            print("  ⚠️  No hay usuarios con información bancaria")
            return pedidos, []
        
        print(f"  ℹ️  Usuarios válidos: {len(usuarios_validos)}")
        
        # Crear diccionario de productos por nombre para búsqueda rápida
        productos_dict = {p["nombre"]: p for p in productos}
        
        for i in range(Config.NUM_PEDIDOS):
            local_id = random.choice(locales_ids)
            usuario = random.choice(usuarios_validos)
            
            pedido = cls._crear_pedido_con_estados(
                i + 1, local_id, usuario, productos_dict, productos_por_local, empleados_por_local
            )
            
            pedidos.append(pedido)
            
            if (i + 1) % 1000 == 0:
                print(f"  📊 Progreso: {i + 1}/{Config.NUM_PEDIDOS}")
        
        pedidos_ids = [p["pedido_id"] for p in pedidos]
        print(f"  ✅ {len(pedidos)} pedidos generados")
        
        return pedidos, pedidos_ids
    
    @classmethod
    def _crear_pedido_con_estados(cls, counter, local_id, usuario, productos_dict, productos_por_local, empleados_por_local):
        """Crea un pedido con transición de estados"""
        pedido_id = f"PED-{counter:06d}"
        
        # Seleccionar productos
        productos_disponibles = productos_por_local.get(local_id, [])
        
        if not productos_disponibles:
            productos_nombres = []
            costo = 0
        else:
            num_productos = min(random.randint(1, 4), len(productos_disponibles))
            productos_nombres = random.sample(productos_disponibles, num_productos)
            
            costo = sum([
                productos_dict[nombre]["precio"] 
                for nombre in productos_nombres 
                if nombre in productos_dict
            ])
            costo += random.uniform(3.0, 8.0)
        
        estado_actual = random.choices(
            cls.ESTADOS,
            weights=[10, 20, 15, 25, 30],
            k=1
        )[0]
        
        fecha_base = datetime.now() - timedelta(hours=random.randint(0, 72))
        
        # Calcular fecha de entrega aproximada
        fecha_entrega_aproximada = cls._calcular_fecha_entrega(fecha_base, len(productos_nombres))
        
        estados = cls._generar_estados_progresivos(
            estado_actual, fecha_base, local_id, empleados_por_local
        )
        
        pedido = {
            "local_id": local_id,
            "pedido_id": pedido_id,
            "usuario_correo": usuario["correo"],
            "productos_nombres": productos_nombres,
            "costo": round(costo, 2),
            "fecha_entrega_aproximada": fecha_entrega_aproximada,
            "direccion": random.choice(SampleData.DIRECCIONES_LIMA) if estado_actual in ["enviando", "recibido"] else "",
            "status": estado_actual,
            "procesando": estados["procesando"]
        }
        
        # Solo agregar estados que ya se han alcanzado
        if estados["cocinando"] is not None:
            pedido["cocinando"] = estados["cocinando"]
        if estados["empacando"] is not None:
            pedido["empacando"] = estados["empacando"]
        if estados["enviando"] is not None:
            pedido["enviando"] = estados["enviando"]
        if estados["recibido"] is not None:
            pedido["recibido"] = estados["recibido"]
        
        return pedido
    
    @classmethod
    def _calcular_fecha_entrega(cls, fecha_base, num_productos):
        """Calcula fecha de entrega aproximada basada en número de productos"""
        tiempo_preparacion = 30 + max(0, (num_productos - 1) * 5)
        tiempo_delivery = random.randint(20, 30)
        tiempo_total = tiempo_preparacion + tiempo_delivery
        
        fecha_entrega = fecha_base + timedelta(minutes=tiempo_total)
        return fecha_entrega.isoformat()
    
    @classmethod
    def _generar_estados_progresivos(cls, estado_actual, fecha_base, local_id, empleados_por_local):
        """Genera los estados con TODOS sus campos completos (hora_fin siempre presente)"""
        estados = {
            "procesando": {},
            "cocinando": None,
            "empacando": None,
            "enviando": None,
            "recibido": None
        }
        
        tiempo_acumulado = 0
        estado_actual_index = cls.ESTADOS.index(estado_actual)
        
        for idx, estado in enumerate(cls.ESTADOS):
            if idx <= estado_actual_index:
                es_estado_actual = (idx == estado_actual_index)
                
                hora_inicio = fecha_base + timedelta(minutes=tiempo_acumulado)
                duracion = cls._obtener_duracion_estado(estado)
                hora_fin = hora_inicio + timedelta(minutes=duracion)
                
                if estado == "procesando":
                    estados[estado] = {
                        "activo": es_estado_actual,
                        "hora_inicio": hora_inicio.isoformat(),
                        "hora_fin": hora_fin.isoformat()
                    }
                
                elif estado == "cocinando":
                    empleado_dni = random.choice(empleados_por_local[local_id]["cocinero"]) if empleados_por_local[local_id]["cocinero"] else ""
                    empleado_info = empleados_por_local[local_id]["info_empleados"].get(empleado_dni, {})
                    
                    estados[estado] = {
                        "activo": es_estado_actual,
                        "cocinero_dni": empleado_dni,
                        "cocinero_nombre": empleado_info.get("nombre", ""),
                        "cocinero_apellido": empleado_info.get("apellido", ""),
                        "cocinero_calificacion_prom": empleado_info.get("calificacion_prom", round(random.uniform(3.5, 5.0), 2)),
                        "hora_inicio": hora_inicio.isoformat(),
                        "hora_fin": hora_fin.isoformat()
                    }
                
                elif estado == "empacando":
                    empleado_dni = random.choice(empleados_por_local[local_id]["despachador"]) if empleados_por_local[local_id]["despachador"] else ""
                    empleado_info = empleados_por_local[local_id]["info_empleados"].get(empleado_dni, {})
                    
                    estados[estado] = {
                        "activo": es_estado_actual,
                        "despachador_dni": empleado_dni,
                        "despachador_nombre": empleado_info.get("nombre", ""),
                        "despachador_apellido": empleado_info.get("apellido", ""),
                        "despachador_calificacion_prom": empleado_info.get("calificacion_prom", round(random.uniform(3.5, 5.0), 2)),
                        "hora_inicio": hora_inicio.isoformat(),
                        "hora_fin": hora_fin.isoformat()
                    }
                
                elif estado == "enviando":
                    empleado_dni = random.choice(empleados_por_local[local_id]["repartidor"]) if empleados_por_local[local_id]["repartidor"] else ""
                    empleado_info = empleados_por_local[local_id]["info_empleados"].get(empleado_dni, {})
                    
                    estados[estado] = {
                        "activo": es_estado_actual,
                        "repartidor_dni": empleado_dni,
                        "repartidor_nombre": empleado_info.get("nombre", ""),
                        "repartidor_apellido": empleado_info.get("apellido", ""),
                        "repartidor_calificacion_prom": empleado_info.get("calificacion_prom", round(random.uniform(3.5, 5.0), 2)),
                        "hora_inicio": hora_inicio.isoformat(),
                        "hora_fin": hora_fin.isoformat()
                    }
                
                elif estado == "recibido":
                    estados[estado] = {
                        "activo": es_estado_actual,
                        "hora_inicio": hora_inicio.isoformat(),
                        "hora_fin": hora_fin.isoformat()
                    }
                
                tiempo_acumulado += duracion
        
        return estados
    
    @classmethod
    def _obtener_duracion_estado(cls, estado):
        """Retorna la duración típica de cada estado en minutos"""
        duraciones = {
            "procesando": random.randint(2, 5),
            "cocinando": random.randint(15, 30),
            "empacando": random.randint(3, 8),
            "enviando": random.randint(20, 45),
            "recibido": 0
        }
        return duraciones.get(estado, 5)
