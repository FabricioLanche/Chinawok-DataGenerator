"""
Generador de pedidos
"""
import random
from datetime import datetime, timedelta
from ..helpers import Helpers
from ..sample_data import SampleData
from ..config import Config


class PedidosGenerator:
    """Generador de pedidos"""
    
    @staticmethod
    def generar_pedidos(locales_ids, usuarios, productos, productos_por_local, empleados_por_local):
        """Genera pedidos con lógica de negocio"""
        pedidos = []
        pedidos_ids = []
        
        # Filtrar usuarios válidos (con tarjeta y clientes)
        usuarios_con_pago = [
            u for u in usuarios 
            if "informacion_bancaria" in u and u.get("role") == "cliente"
        ]
        
        if not usuarios_con_pago:
            print("  ⚠️  No hay usuarios con información bancaria. No se pueden generar pedidos.")
            return pedidos, pedidos_ids
        
        usuarios_validos_ids = [u["usuario_id"] for u in usuarios_con_pago]
        
        for i in range(Config.NUM_PEDIDOS):
            pedido_id = Helpers.generar_uuid()
            pedidos_ids.append(pedido_id)
            local_id = random.choice(locales_ids)
            usuario_id = random.choice(usuarios_validos_ids)
            status = random.choice(Config.ESTADOS_PEDIDO)
            
            # Seleccionar productos
            productos_ids_pedido = []
            if productos_por_local[local_id]:
                num_productos = random.randint(1, 4)
                productos_ids_pedido = random.sample(
                    productos_por_local[local_id],
                    min(num_productos, len(productos_por_local[local_id]))
                )
            
            # Calcular costo
            costo = sum([
                p["precio"] for p in productos 
                if p["producto_id"] in productos_ids_pedido
            ])
            costo += round(random.uniform(Config.PRECIO_MIN_DELIVERY, Config.PRECIO_MAX_DELIVERY), 2)
            costo = round(costo, 2)
            
            pedido = {
                "PK": f"LOCAL#{local_id}",
                "SK": f"PEDIDO#{pedido_id}",
                "local_id": local_id,
                "pedido_id": pedido_id,
                "usuario_id": usuario_id,
                "productos_ids": productos_ids_pedido,
                "cocinero_dni": "",
                "despachador_dni": "",
                "repartidor_dni": "",
                "costo": costo,
                "fecha_entrega": None,
                "direccion": "",
                "status": status
            }
            
            # Asignar empleados según status
            if status in ["cocinando", "empacando", "enviando", "recibido"]:
                if empleados_por_local[local_id]["cocinero"]:
                    pedido["cocinero_dni"] = random.choice(empleados_por_local[local_id]["cocinero"])
            
            if status in ["empacando", "enviando", "recibido"]:
                if empleados_por_local[local_id]["despachador"]:
                    pedido["despachador_dni"] = random.choice(empleados_por_local[local_id]["despachador"])
            
            if status in ["enviando", "recibido"]:
                if empleados_por_local[local_id]["repartidor"]:
                    pedido["repartidor_dni"] = random.choice(empleados_por_local[local_id]["repartidor"])
                
                pedido["direccion"] = Helpers.generar_direccion_string(
                    SampleData.CALLES,
                    SampleData.DISTRITOS_LIMA
                )
                fecha_entrega = datetime.now() + timedelta(minutes=random.randint(30, 90))
                pedido["fecha_entrega"] = fecha_entrega.isoformat()
            
            pedidos.append(pedido)
            
            if (i + 1) % 1000 == 0:
                print(f"  📊 Progreso: {i + 1}/{Config.NUM_PEDIDOS} pedidos generados")
        
        return pedidos, pedidos_ids
