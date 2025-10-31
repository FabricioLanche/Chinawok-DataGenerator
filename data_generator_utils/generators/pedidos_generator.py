"""
Generador de Pedidos
"""
import random
from datetime import datetime, timedelta
from ..config import Config
from ..sample_data import SampleData


class PedidosGenerator:
    """Generador de datos para la tabla Pedidos"""
    
    @classmethod
    def generar_pedidos(cls, locales_ids, usuarios, productos, productos_por_local, empleados_por_local):
        """Genera pedidos distribuidos entre locales"""
        pedidos = []
        pedido_counter = 1
        
        usuarios_correos = [u["correo"] for u in usuarios if u["role"] == "Cliente"]
        
        for _ in range(Config.NUM_PEDIDOS):
            local_id = random.choice(locales_ids)
            productos_local = productos_por_local.get(local_id, [])
            empleados_local = empleados_por_local.get(local_id, {})
            
            if not productos_local or not all(empleados_local.values()):
                continue
            
            pedido = cls._crear_pedido(
                pedido_counter,
                local_id,
                usuarios_correos,
                productos_local,
                empleados_local
            )
            
            pedidos.append(pedido)
            pedido_counter += 1
        
        return pedidos, [p["pedido_id"] for p in pedidos]
    
    @classmethod
    def _crear_pedido(cls, counter, local_id, usuarios_correos, productos_local, empleados_local):
        """Crea un pedido individual"""
        status = random.choice(Config.ESTADOS_PEDIDO)
        num_productos = random.randint(1, 5)
        productos_nombres = random.sample(productos_local, min(num_productos, len(productos_local)))
        
        pedido = {
            "local_id": local_id,
            "pedido_id": f"PED-{counter:06d}",
            "usuario_correo": random.choice(usuarios_correos),
            "productos_nombres": productos_nombres,
            "cocinero_dni": random.choice(empleados_local.get("Cocinero", ["00000000"])),
            "despachador_dni": random.choice(empleados_local.get("Despachador", ["00000000"])),
            "repartidor_dni": random.choice(empleados_local.get("Repartidor", ["00000000"])),
            "costo": round(random.uniform(20.0, 150.0), 2),
            "status": status
        }
        
        if status in ["enviando", "recibido"]:
            pedido["direccion"] = random.choice(SampleData.DIRECCIONES_LIMA)
            pedido["fecha_entrega"] = (datetime.now() + timedelta(minutes=random.randint(30, 90))).isoformat()
        
        return pedido
