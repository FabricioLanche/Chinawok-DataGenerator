import json
import os
from datetime import datetime, timedelta
import random
import string

# Crear carpeta de salida
output_dir = "dynamodb_data"
os.makedirs(output_dir, exist_ok=True)

# Datos de ejemplo - China Wok
nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Laura", "Miguel", "Sofia"]
apellidos = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores"]
categorias = ["Arroces", "Tallarines", "Chaufas", "Pollo", "Cerdo", "Res", "Mariscos", "Entradas", "Bebidas", "Sopas"]
productos_nombres = [
    "Arroz Chaufa de Pollo", "Arroz Chaufa Especial", "Arroz Chaufa de Mariscos",
    "Tallarin Saltado de Pollo", "Tallarin Saltado de Carne", "Tallarin con Verduras",
    "Aeropuerto Especial", "Pollo al Sillao", "Pollo Chi Jau Kay",
    "Chancho al Tamarindo", "Cerdo Agridulce", "Lomo Saltado",
    "Carne Mongoliana", "Camarones al Tamarindo", "Chicharrón de Pollo",
    "Sopa Wantan", "Wantan Frito", "Rollitos Primavera",
    "Inca Kola", "Chicha Morada", "Limonada Frozen"
]

# IDs de locales
locales_ids = ["LOC001", "LOC002", "LOC003"]


def generar_email(nombre, apellido):
    return f"{nombre.lower()}.{apellido.lower()}@email.com"


def generar_tarjeta():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])


def generar_cvv():
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])


def generar_fecha_vencimiento():
    mes = random.randint(1, 12)
    año = random.randint(25, 30)
    return f"{mes:02d}/{año:02d}"


def generar_dni():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])


def generar_id(prefijo):
    return f"{prefijo}{random.randint(1000, 9999)}"


# 1. Generar Locales
locales = []
direcciones = ["Av. Principal 123", "Calle Comercio 456", "Jr. Los Olivos 789"]
telefonos = ["+51-1-2345678", "+51-1-8765432", "+51-1-5551234"]

for i, local_id in enumerate(locales_ids):
    locales.append({
        "local_id": local_id,
        "direccion": direcciones[i],
        "telefono": telefonos[i],
        "hora_apertura": "08:00",
        "hora_finalizacion": "22:00"
    })

with open(f"{output_dir}/locales.json", "w", encoding="utf-8") as f:
    json.dump(locales, f, indent=2, ensure_ascii=False)

# 2. Generar Usuarios (partition_key = usuario_id, sin local_id)
usuarios = []
usuarios_ids = []

for i in range(15):
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    usuario_id = generar_id("USR")
    usuarios_ids.append(usuario_id)

    usuario = {
        "usuario_id": usuario_id,
        "nombre": f"{nombre} {apellido}",
        "correo": generar_email(nombre, apellido) + str(i),
        "contrasena": "password123",
        "role": random.choice(["Cliente", "Admin"])
    }

    # 50% tienen información bancaria
    if random.random() > 0.5:
        usuario["informacion_bancaria"] = {
            "numero_tarjeta": generar_tarjeta(),
            "cvv": generar_cvv(),
            "fecha_vencimiento": generar_fecha_vencimiento(),
            "direccion_facturacion": f"Calle {random.randint(1, 100)} #{random.randint(1, 500)}"
        }

    usuarios.append(usuario)

with open(f"{output_dir}/usuarios.json", "w", encoding="utf-8") as f:
    json.dump(usuarios, f, indent=2, ensure_ascii=False)

# 3. Generar Productos (partition_key = local_id, sort_key = producto_id, incluye stock)
productos = []
productos_por_local = {local_id: [] for local_id in locales_ids}

# Crear productos para cada local
for local_id in locales_ids:
    # Cada local tiene entre 8 y 12 productos
    num_productos = random.randint(8, 12)
    nombres_seleccionados = random.sample(productos_nombres, min(num_productos, len(productos_nombres)))

    for nombre_prod in nombres_seleccionados:
        producto_id = generar_id("PROD")

        producto = {
            "local_id": local_id,
            "producto_id": producto_id,
            "nombre": nombre_prod,
            "precio": round(random.uniform(5.0, 50.0), 2),
            "descripcion": f"Delicioso {nombre_prod.lower()} preparado con ingredientes frescos",
            "categoria": random.choice(categorias),
            "stock": random.randint(10, 100)
        }

        productos.append(producto)
        productos_por_local[local_id].append(producto_id)

with open(f"{output_dir}/productos.json", "w", encoding="utf-8") as f:
    json.dump(productos, f, indent=2, ensure_ascii=False)

# 4. Generar Empleados (por local)
empleados = []
empleados_por_local = {local_id: {"Repartidor": [], "Cocinero": [], "Despachador": []}
                       for local_id in locales_ids}

for i in range(20):
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    dni = generar_dni()
    local_id = random.choice(locales_ids)
    role = random.choice(["Repartidor", "Cocinero", "Despachador"])

    empleado = {
        "local_id": local_id,
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "role": role
    }

    # 70% tienen calificación y sueldo
    if random.random() > 0.3:
        empleado["calificacion_prom"] = round(random.uniform(3.0, 5.0), 2)
        empleado["sueldo"] = round(random.uniform(1000.0, 3000.0), 2)

    empleados.append(empleado)
    empleados_por_local[local_id][role].append(dni)

with open(f"{output_dir}/empleados.json", "w", encoding="utf-8") as f:
    json.dump(empleados, f, indent=2, ensure_ascii=False)

# 5. Generar Combos (por local)
combos = []
combos_por_local = {local_id: [] for local_id in locales_ids}

for local_id in locales_ids:
    # Cada local tiene entre 2 y 4 combos
    num_combos = random.randint(2, 4)

    for i in range(num_combos):
        combo_id = generar_id("COMBO")

        # Seleccionar productos de este local
        if productos_por_local[local_id]:
            num_productos = min(random.randint(2, 4), len(productos_por_local[local_id]))
            productos_combo = random.sample(productos_por_local[local_id], num_productos)
        else:
            continue

        combo = {
            "local_id": local_id,
            "combo_id": combo_id,
            "nombre": f"Combo Especial {i + 1}",
            "productos_ids": productos_combo,
            "descripcion": f"Combo con {len(productos_combo)} productos deliciosos"
        }

        combos.append(combo)
        combos_por_local[local_id].append(combo_id)

with open(f"{output_dir}/combos.json", "w", encoding="utf-8") as f:
    json.dump(combos, f, indent=2, ensure_ascii=False)

# 6. Generar Pedidos (por local)
pedidos = []
pedidos_ids = []
status_opciones = ["eligiendo", "cocinando", "empacando", "enviando", "recibido"]

for i in range(30):
    pedido_id = generar_id("PED")
    pedidos_ids.append(pedido_id)
    local_id = random.choice(locales_ids)
    usuario_id = random.choice(usuarios_ids)

    # Seleccionar productos de este local
    if productos_por_local[local_id]:
        num_productos = random.randint(1, 4)
        productos_pedido = random.sample(productos_por_local[local_id],
                                         min(num_productos, len(productos_por_local[local_id])))
    else:
        continue

    pedido = {
        "local_id": local_id,
        "pedido_id": pedido_id,
        "usuario_id": usuario_id,
        "productos_ids": productos_pedido,
        "costo": round(random.uniform(20.0, 150.0), 2),
        "status": random.choice(status_opciones)
    }

    # Agregar empleados del local según el status
    if pedido["status"] in ["cocinando", "empacando", "enviando", "recibido"]:
        if empleados_por_local[local_id]["Cocinero"]:
            pedido["cocinero_dni"] = random.choice(empleados_por_local[local_id]["Cocinero"])

    if pedido["status"] in ["empacando", "enviando", "recibido"]:
        if empleados_por_local[local_id]["Despachador"]:
            pedido["despachador_dni"] = random.choice(empleados_por_local[local_id]["Despachador"])

    if pedido["status"] in ["enviando", "recibido"]:
        if empleados_por_local[local_id]["Repartidor"]:
            pedido["repartidor_dni"] = random.choice(empleados_por_local[local_id]["Repartidor"])
        pedido["direccion"] = f"Av. Ejemplo {random.randint(100, 999)}, Lima"
        fecha_entrega = datetime.now() + timedelta(days=random.randint(0, 7))
        pedido["fecha_entrega"] = fecha_entrega.isoformat()

    pedidos.append(pedido)

with open(f"{output_dir}/pedidos.json", "w", encoding="utf-8") as f:
    json.dump(pedidos, f, indent=2, ensure_ascii=False)

# 7. Generar Ofertas (por local)
ofertas = []

for local_id in locales_ids:
    # Cada local tiene entre 3 y 5 ofertas
    num_ofertas = random.randint(3, 5)

    for i in range(num_ofertas):
        oferta_id = generar_id("OFE")

        fecha_inicio = datetime.now() - timedelta(days=random.randint(0, 30))
        fecha_limite = fecha_inicio + timedelta(days=random.randint(7, 60))

        oferta = {
            "local_id": local_id,
            "oferta_id": oferta_id,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_limite": fecha_limite.isoformat(),
            "porcentaje_descuento": random.randint(10, 50)
        }

        # 60% para productos, 40% para combos
        if random.random() > 0.4 and productos_por_local[local_id]:
            oferta["producto_id"] = random.choice(productos_por_local[local_id])
        elif combos_por_local[local_id]:
            oferta["combo_id"] = random.choice(combos_por_local[local_id])

        ofertas.append(oferta)

with open(f"{output_dir}/ofertas.json", "w", encoding="utf-8") as f:
    json.dump(ofertas, f, indent=2, ensure_ascii=False)

# 8. Generar Reseñas (por local/pedido)
resenas = []

for i in range(20):
    resena_id = generar_id("RES")
    # Seleccionar pedidos completados
    pedidos_completados = [p for p in pedidos if p["status"] == "recibido"]

    if pedidos_completados:
        pedido = random.choice(pedidos_completados)
        local_id = pedido["local_id"]

        resena = {
            "local_id": local_id,
            "resena_id": resena_id,
            "pedido_id": pedido["pedido_id"],
            "calificacion": round(random.uniform(3.0, 5.0), 1),
            "resena": random.choice([
                "Excelente servicio y comida deliciosa",
                "Muy buena atención, volveré pronto",
                "Entrega rápida y producto fresco",
                "Calidad excepcional, totalmente recomendado",
                "Buen sabor y presentación"
            ])
        }

        # 60% incluyen empleado_dni del local
        if random.random() > 0.4:
            empleados_local = [e["dni"] for e in empleados if e["local_id"] == local_id]
            if empleados_local:
                resena["empleado_dni"] = random.choice(empleados_local)

        resenas.append(resena)

with open(f"{output_dir}/resenas.json", "w", encoding="utf-8") as f:
    json.dump(resenas, f, indent=2, ensure_ascii=False)

print(f"✅ Datos generados exitosamente en la carpeta '{output_dir}/'")
print(f"\n📁 Archivos creados:")
print(f"  - locales.json ({len(locales)} registros)")
print(f"  - usuarios.json ({len(usuarios)} registros) [PK: usuario_id]")
print(f"  - productos.json ({len(productos)} registros) [PK: local_id, SK: producto_id, incluye stock]")
print(f"  - empleados.json ({len(empleados)} registros)")
print(f"  - combos.json ({len(combos)} registros)")
print(f"  - pedidos.json ({len(pedidos)} registros)")
print(f"  - ofertas.json ({len(ofertas)} registros)")
print(f"  - resenas.json ({len(resenas)} registros)")