import json
import os
from datetime import datetime, timedelta
import random
import uuid
from typing import List, Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================================================
# CONFIGURACIÓN: Cantidad de registros a generar por tabla
# ============================================================================
NUM_LOCALES = 100           # 100 locales en diferentes distritos
NUM_USUARIOS = 5000         # 5000 usuarios (70% con tarjeta)
NUM_PRODUCTOS_POR_LOCAL = 50 # ~5000 productos total
NUM_EMPLEADOS = 500         # 5 empleados por local aprox
NUM_COMBOS_POR_LOCAL = 5    # ~500 combos total
NUM_PEDIDOS = 10000         # 10000 pedidos
NUM_OFERTAS_POR_LOCAL = 5   # ~500 ofertas total
NUM_RESENAS = 1000          # 1000 reseñas
#Nota. Estos valores son aproximados para generar un conjunto de datos masivo para pruebas.
# ============================================================================

# Crear carpeta de salida
output_dir = "dynamodb_data"
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# DATOS DE EJEMPLO EXPANDIDOS - China Wok
# ============================================================================

# Nombres (150 nombres únicos)
nombres = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Laura", "Miguel", "Sofia",
    "Jorge", "Isabel", "Diego", "Valentina", "Fernando", "Gabriela", "Ricardo", "Daniela", "Alberto", "Camila",
    "Roberto", "Andrea", "Andrés", "Natalia", "Manuel", "Paula", "Francisco", "Lucía", "José", "Victoria",
    "Antonio", "Martina", "Javier", "Elena", "Rafael", "Adriana", "Sergio", "Claudia", "Ramón", "Silvia",
    "Gustavo", "Mónica", "Héctor", "Patricia", "Raúl", "Rosa", "Eduardo", "Sandra", "Arturo", "Teresa",
    "Enrique", "Beatriz", "Víctor", "Diana", "Oscar", "Verónica", "Felipe", "Rocío", "Julio", "Gloria",
    "Tomás", "Pilar", "Ignacio", "Cristina", "Rodrigo", "Alejandra", "Mauricio", "Cecilia", "César", "Irene",
    "Pablo", "Marta", "Rubén", "Julia", "Emilio", "Angela", "Lorenzo", "Alicia", "Marcos", "Raquel",
    "Leonardo", "Susana", "Gonzalo", "Eva", "Esteban", "Lorena", "Alfredo", "Nuria", "Nicolás", "Carolina",
    "Santiago", "Leticia", "Mateo", "Yolanda", "Sebastián", "Amparo", "Alejandro", "Dolores", "Daniel", "Inés",
    "Gabriel", "Mercedes", "Samuel", "Concepción", "Adrián", "Rosario", "Ángel", "Remedios", "Hugo", "Josefa",
    "Iván", "Manuela", "Cristian", "Francisca", "Omar", "Antonia", "Óscar", "Encarnación", "Bruno", "Soledad",
    "Matías", "Consuelo", "Lucas", "Milagros", "Simón", "Esperanza", "Benjamín", "Asunción", "Fabián", "Purificación",
    "Damián", "Trinidad", "Agustín", "Luz", "Félix", "Visitación", "Ezequiel", "Inmaculada", "Ismael", "Virtudes",
    "Joel", "Sagrario", "Abel", "Angustias", "Elías", "Dolores", "Gael", "Piedad", "Axel", "Caridad"
]

# Apellidos (150 apellidos únicos)
apellidos = [
    "García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores",
    "Rivera", "Gómez", "Díaz", "Cruz", "Morales", "Reyes", "Gutiérrez", "Ortiz", "Jiménez", "Ruiz",
    "Hernández", "Mendoza", "Álvarez", "Castillo", "Romero", "Herrera", "Medina", "Aguilar", "Vargas", "Castro",
    "Ramos", "Vega", "Guerrero", "Muñoz", "Rojas", "Delgado", "Campos", "Contreras", "Vázquez", "Núñez",
    "Cabrera", "Navarro", "Cárdenas", "Mejía", "Salazar", "Estrada", "León", "Sandoval", "Mendez", "Domínguez",
    "Peña", "Guzmán", "Cortés", "Ibarra", "Velasco", "Ríos", "Ponce", "Alvarado", "Luna", "Silva",
    "Carrillo", "Maldonado", "Acosta", "Valdez", "Fuentes", "Cervantes", "Pacheco", "Lara", "Valencia", "Ochoa",
    "Rubio", "Soto", "Mora", "Espinoza", "Bravo", "Molina", "Salas", "Figueroa", "Gallegos", "Zamora",
    "Santiago", "Miranda", "Ayala", "Suárez", "Cordero", "Robles", "Márquez", "Barrera", "Santana", "Franco",
    "Rosales", "Ávila", "Zavala", "Carrasco", "Montoya", "Serrano", "Corona", "Villarreal", "Hinojosa", "Solís",
    "Cisneros", "Trujillo", "Montes", "Huerta", "Lugo", "Cortez", "Villa", "Padilla", "Cardona", "Tapia",
    "Vega", "Ibáñez", "Camacho", "Paredes", "Parra", "Orozco", "Duarte", "Escobar", "Galván", "Quintero",
    "Bautista", "Carbajal", "Esquivel", "Villegas", "Gallardo", "Terán", "Cabral", "Rangel", "Bonilla", "Vidal",
    "Cano", "Arellano", "Bernal", "Villalobos", "Coronado", "Castellanos", "Beltrán", "Meza", "Cantu", "Santillán"
]

# Categorías de productos (30 categorías)
categorias = [
    "Arroces", "Tallarines", "Chaufas", "Wantanes", "Sopas",
    "Pollo", "Cerdo", "Res", "Mariscos", "Pescado",
    "Entradas Frías", "Entradas Calientes", "Rolls", "Dim Sum", "Dumplings",
    "Bebidas Frías", "Bebidas Calientes", "Jugos", "Tés", "Postres",
    "Salsas", "Guarniciones", "Ensaladas", "Especiales", "Vegetarianos",
    "Veganos", "Kids Menu", "Combos Familiares", "Promos", "Snacks"
]

# Nombres de productos (200 productos únicos)
productos_nombres = [
    # Arroces y Chaufas (25)
    "Arroz Chaufa de Pollo", "Arroz Chaufa Especial", "Arroz Chaufa de Mariscos", "Arroz Chaufa de Cerdo",
    "Arroz Chaufa Vegetariano", "Arroz Chaufa de Res", "Arroz Chaufa Triple", "Arroz con Mariscos",
    "Arroz con Pollo al Jengibre", "Arroz Frito Cantonés", "Arroz con Camarones", "Arroz Thai",
    "Arroz Yangzhou", "Arroz con Pato", "Arroz con Langostinos", "Arroz Imperial",
    "Arroz con Vegetales", "Arroz Tres Delicias", "Arroz con Champiñones", "Arroz con Piña",
    "Arroz con Curry", "Arroz con Tamarindo", "Arroz Huancaína", "Arroz Oriental", "Arroz Mixto",
    
    # Tallarines (25)
    "Tallarin Saltado de Pollo", "Tallarin Saltado de Carne", "Tallarin con Verduras", "Tallarin Saltado Triple",
    "Tallarin con Mariscos", "Tallarin al Wok", "Tallarin con Camarones", "Tallarin Lo Mein",
    "Tallarin Pad Thai", "Tallarin con Salsa de Ostras", "Tallarin Singapur", "Tallarin con Cerdo",
    "Tallarin Yakisoba", "Tallarin Udon", "Tallarin Soba", "Tallarin con Pollo Teriyaki",
    "Tallarin con Res Mongoliana", "Tallarin Vegetariano", "Tallarin con Setas", "Tallarin Picante",
    "Tallarin con Salsa Negra", "Tallarin Chijaukay", "Tallarin con Langostinos", "Tallarin Curry", "Tallarin Oriental",
    
    # Aeropuertos y Especiales (20)
    "Aeropuerto Especial", "Aeropuerto de Pollo", "Aeropuerto de Carne", "Aeropuerto de Mariscos",
    "Aeropuerto Triple", "Aeropuerto Vegetariano", "Tipakay Especial", "Tipakay de Pollo",
    "Tipakay de Res", "Chi Jau Kay", "Kam Lu Wantan", "Taypá de Pollo",
    "Taypá de Carne", "Taypá de Mariscos", "Wantan Frito", "Chijaukay de Pollo",
    "Chijaukay de Res", "Combinado Oriental", "Especial de la Casa", "Plato Ejecutivo",
    
    # Pollos (20)
    "Pollo al Sillao", "Pollo Chi Jau Kay", "Pollo Mongoliano", "Pollo al Tamarindo",
    "Pollo Agridulce", "Pollo con Almendras", "Pollo al Limón", "Pollo Teriyaki",
    "Pollo con Champiñones", "Pollo con Piña", "Pollo Kung Pao", "Pollo al Curry",
    "Pollo con Vegetales", "Pollo con Maní", "Pollo Szechuan", "Pollo Orange",
    "Pollo General Tso", "Pollo con Brócoli", "Pollo al Jengibre", "Pollo Satay",
    
    # Carnes (20)
    "Lomo Saltado", "Carne Mongoliana", "Res con Brócoli", "Res al Sillao",
    "Res con Champiñones", "Res con Vegetales", "Carne Agridulce", "Res Teriyaki",
    "Res Szechuan", "Carne con Ostras", "Lomo al Tamarindo", "Carne con Piña",
    "Res al Jengibre", "Carne con Pimientos", "Res Hunan", "Carne con Curry",
    "Lomo Fino", "Res con Ajíes", "Carne Oriental", "Lomo Special",
    
    # Cerdos (15)
    "Chancho al Tamarindo", "Cerdo Agridulce", "Cerdo con Piña", "Cerdo al Sillao",
    "Cerdo con Champiñones", "Cerdo Teriyaki", "Cerdo con Vegetales", "Cerdo Mongoliano",
    "Cerdo Szechuan", "Cerdo con Maní", "Cerdo al Curry", "Cerdo BBQ",
    "Cerdo con Brócoli", "Cerdo al Jengibre", "Cerdo Agripicante",
    
    # Mariscos (20)
    "Camarones al Tamarindo", "Camarones Agridulces", "Camarones al Ajo", "Camarones Salteados",
    "Langostinos al Tamarindo", "Langostinos con Vegetales", "Pescado Agridulce", "Pescado al Tamarindo",
    "Pescado Frito", "Chicharrón de Pescado", "Mariscos Saltados", "Conchas Negras",
    "Pulpo al Olivo", "Calamar Frito", "Jalea Mixta", "Chicharrón de Mariscos",
    "Pescado al Vapor", "Camarones con Brócoli", "Langostinos al Curry", "Mix de Mariscos",
    
    # Entradas y Aperitivos (20)
    "Chicharrón de Pollo", "Sopa Wantan", "Wantan Frito", "Rollitos Primavera",
    "Empanaditas Chinas", "Gyozas", "Shumai", "Pan Bao",
    "Alitas Chinas", "Tequeños", "Calamares Fritos", "Deditos de Queso",
    "Croquetas de Pollo", "Ensalada China", "Brochetas de Pollo", "Nems Vietnamitas",
    "Dumplings al Vapor", "Har Gow", "Baozi", "Spring Rolls",
    
    # Sopas (15)
    "Sopa Wantan Especial", "Sopa de Mariscos", "Sopa de Pollo", "Sopa de Res",
    "Sopa Agripicante", "Sopa de Vegetales", "Sopa Miso", "Sopa Tom Yum",
    "Sopa de Wantan con Pollo", "Sopa de Fideos", "Sopa de Maní", "Sopa de Camarones",
    "Sopa de Pato", "Caldo de Gallina", "Sopa del Día",
    
    # Bebidas (20)
    "Inca Kola", "Inca Kola Zero", "Coca Cola", "Sprite", "Fanta",
    "Chicha Morada", "Limonada Frozen", "Limonada Natural", "Maracuyá Frozen", "Maracuyá Natural",
    "Agua Mineral", "Agua de Mesa", "Té Verde", "Té Jazmín", "Té Oolong",
    "Jugo de Naranja", "Jugo de Piña", "Jugo de Papaya", "Jugo de Mango", "Cerveza Cristal"
]

# Distritos de Lima (50 distritos)
distritos_lima = [
    "Miraflores", "San Isidro", "Surco", "La Molina", "San Borja",
    "Barranco", "Chorrillos", "San Miguel", "Pueblo Libre", "Magdalena",
    "Jesús María", "Lince", "Breña", "Lima Cercado", "Rímac",
    "Los Olivos", "Independencia", "San Martín de Porres", "Comas", "Carabayllo",
    "Puente Piedra", "Ancón", "Santa Rosa", "La Victoria", "El Agustino",
    "San Luis", "Ate", "Santa Anita", "San Juan de Lurigancho", "Lurigancho",
    "Chaclacayo", "Cieneguilla", "Villa El Salvador", "Villa María del Triunfo", "San Juan de Miraflores",
    "Lurín", "Pachacámac", "Punta Hermosa", "Punta Negra", "San Bartolo",
    "Santa María del Mar", "Pucusana", "Callao", "Bellavista", "Carmen de la Legua",
    "La Perla", "La Punta", "Ventanilla", "Mi Perú", "Surquillo"
]

# Calles comunes (100 calles)
calles = [
    "Av. Larco", "Av. Arequipa", "Av. Javier Prado", "Av. Benavides", "Av. Angamos",
    "Av. La Marina", "Av. Universitaria", "Av. Túpac Amaru", "Av. Colonial", "Av. Brasil",
    "Av. Venezuela", "Av. Abancay", "Av. Grau", "Av. Wilson", "Av. Aviación",
    "Jr. de la Unión", "Jr. Lampa", "Jr. Carabaya", "Jr. Áncash", "Jr. Huallaga",
    "Calle Los Pinos", "Calle Las Flores", "Calle Los Rosales", "Calle San Martín", "Calle Bolívar",
    "Calle Grau", "Calle Comercio", "Calle Lima", "Calle Arequipa", "Calle Cusco",
    "Av. El Sol", "Av. La Paz", "Av. Primavera", "Av. Encalada", "Av. Caminos del Inca",
    "Av. Tomás Marsano", "Av. República de Panamá", "Av. Paseo de la República", "Av. 28 de Julio", "Av. Arenales",
    "Av. Salaverry", "Av. Alfonso Ugarte", "Av. Nicolás de Piérola", "Av. Tacna", "Av. Emancipación",
    "Calle Schell", "Calle Porta", "Calle Colina", "Calle Alcanfores", "Calle Martir Olaya",
    "Av. José Pardo", "Av. Oscar R. Benavides", "Av. Petit Thouars", "Av. Dos de Mayo", "Av. Progreso",
    "Av. Los Héroes", "Av. Pershing", "Av. Separadora Industrial", "Av. Carlos Izaguirre", "Av. Naranjal",
    "Av. Los Alisos", "Av. Santa Rosa", "Av. El Ejército", "Av. Del Parque", "Av. Defensores del Morro",
    "Calle Las Begonias", "Calle Las Camelias", "Calle Las Palmeras", "Calle Los Eucaliptos", "Calle Los Sauces",
    "Calle Los Álamos", "Calle Los Cedros", "Calle Las Acacias", "Calle Las Magnolias", "Calle Las Orquídeas",
    "Jr. Moquegua", "Jr. Cuzco", "Jr. Ica", "Jr. Ayacucho", "Jr. Junín",
    "Jr. Puno", "Jr. Callao", "Jr. Huánuco", "Jr. Chancay", "Jr. Miró Quesada",
    "Av. Canadá", "Av. San Luis", "Av. Óscar R. Benavides", "Av. Prolongación Iquitos", "Av. Honorio Delgado",
    "Av. Próceres de la Independencia", "Av. La Molina", "Av. Raúl Ferrero", "Av. Flora Tristán", "Av. Las Torres",
    "Calle Conquistadores", "Calle Shell", "Calle Talara", "Calle Berlín", "Calle Madrid"
]

# Helpers
def generar_uuid():
    """Genera un UUID único"""
    return str(uuid.uuid4())

def generar_timestamp():
    """Genera timestamp ISO 8601"""
    return datetime.now().isoformat()

def generar_email(nombre, apellido, suffix=""):
    """Genera email único"""
    return f"{nombre.lower()}.{apellido.lower()}{suffix}@email.com"

def generar_telefono():
    """Genera número de teléfono peruano"""
    return f"+51-{random.randint(900000000, 999999999)}"

def generar_dni():
    """Genera DNI de 8 dígitos"""
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

# 1. Generar Locales
print("📍 Generando Locales...")
locales = []
locales_ids = []

# Generar direcciones dinámicamente
for i in range(NUM_LOCALES):
    local_id = generar_uuid()
    locales_ids.append(local_id)
    
    # Seleccionar distrito y calle aleatoriamente
    distrito = random.choice(distritos_lima)
    calle = random.choice(calles)
    numero = str(random.randint(100, 9999))
    codigo_postal = f"150{random.randint(10, 99)}"
    
    local = {
        "PK": f"LOCAL#{local_id}",
        "SK": f"LOCAL#{local_id}",
        "local_id": local_id,
        "nombre": f"China Wok {distrito}",
        "direccion": {
            "calle": calle,
            "numero": numero,
            "distrito": distrito,
            "ciudad": "Lima",
            "codigo_postal": codigo_postal
        },
        "telefono": generar_telefono(),
        "email": f"local{i+1}@chinawok.pe",
        "horario": {
            "apertura": "08:00",
            "cierre": "22:00",
            "dias_atencion": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        },
        "capacidad_maxima": random.randint(50, 200),
        "activo": True,
        "created_at": generar_timestamp(),
        "updated_at": generar_timestamp()
    }
    
    locales.append(local)

with open(f"{output_dir}/locales.json", "w", encoding="utf-8") as f:
    json.dump(locales, f, indent=2, ensure_ascii=False)

# 2. Generar Usuarios (1 Admin + N Clientes)
print("👥 Generando Usuarios...")
usuarios = []
usuarios_ids = []

# PRIMERO: Crear el administrador único desde variables de entorno
admin_id = generar_uuid()
usuarios_ids.append(admin_id)

admin = {
    "PK": f"USER#{admin_id}",
    "SK": f"USER#{admin_id}",
    "usuario_id": admin_id,
    "nombre": os.getenv('ADMIN_NOMBRE', 'Administrador'),
    "apellido": os.getenv('ADMIN_APELLIDO', 'Sistema'),
    "email": os.getenv('ADMIN_EMAIL', 'admin@chinawok.pe'),
    "telefono": os.getenv('ADMIN_TELEFONO', '+51-999999999'),
    "password_hash": f"hashed_{os.getenv('ADMIN_PASSWORD', 'Admin123!')}",
    "role": "admin",
    "activo": True,
    "created_at": generar_timestamp(),
    "updated_at": generar_timestamp()
}

usuarios.append(admin)

# SEGUNDO: Crear usuarios clientes
for i in range(NUM_USUARIOS):
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    usuario_id = generar_uuid()
    usuarios_ids.append(usuario_id)

    usuario = {
        "PK": f"USER#{usuario_id}",
        "SK": f"USER#{usuario_id}",
        "usuario_id": usuario_id,
        "nombre": nombre,
        "apellido": apellido,
        "email": generar_email(nombre, apellido, str(i)),
        "telefono": generar_telefono(),
        "password_hash": f"hashed_password_{random.randint(1000, 9999)}",
        "role": "cliente",
        "activo": True,
        "created_at": generar_timestamp(),
        "updated_at": generar_timestamp()
    }

    # 70% tienen información bancaria (pueden hacer pedidos)
    if random.random() > 0.3:
        usuario["informacion_bancaria"] = {
            "numero_tarjeta_encriptado": ''.join([str(random.randint(0, 9)) for _ in range(16)]),
            "cvv_encriptado": ''.join([str(random.randint(0, 9)) for _ in range(3)]),
            "fecha_vencimiento": f"{random.randint(1, 12):02d}/{random.randint(25, 30):02d}",
            "nombre_titular": f"{nombre} {apellido}",
            "tipo_tarjeta": random.choice(["Visa", "Mastercard", "American Express"])
        }
    
    # Dirección de facturación
    usuario["direccion_facturacion"] = {
        "calle": random.choice(calles),
        "numero": str(random.randint(100, 999)),
        "distrito": random.choice(distritos_lima),
        "ciudad": "Lima",
        "codigo_postal": f"150{random.randint(10, 99)}"
    }

    usuarios.append(usuario)

with open(f"{output_dir}/usuarios.json", "w", encoding="utf-8") as f:
    json.dump(usuarios, f, indent=2, ensure_ascii=False)

print(f"  ✅ Creado 1 administrador y {NUM_USUARIOS} clientes")

# 3. Generar Productos
print("🍜 Generando Productos...")
productos = []
productos_por_local = {local_id: [] for local_id in locales_ids}

for local_id in locales_ids:
    num_productos = NUM_PRODUCTOS_POR_LOCAL + random.randint(-2, 2)  # Variación de ±2
    nombres_seleccionados = random.sample(productos_nombres, min(num_productos, len(productos_nombres)))

    for nombre_prod in nombres_seleccionados:
        producto_id = generar_uuid()
        categoria = random.choice(categorias)
        
        producto = {
            "PK": f"LOCAL#{local_id}",
            "SK": f"PRODUCTO#{producto_id}",
            "producto_id": producto_id,
            "local_id": local_id,
            "nombre": nombre_prod,
            "descripcion": f"Delicioso {nombre_prod.lower()} preparado con ingredientes frescos",
            "categoria": categoria,
            "precio": round(random.uniform(10.0, 50.0), 2),
            "precio_descuento": None,
            "stock": random.randint(10, 100),
            "stock_minimo": 5,
            "imagen_url": f"https://chinawok.pe/images/productos/{producto_id}.jpg",
            "disponible": True,
            "es_vegetariano": categoria in ["Tallarines", "Arroces"] and random.random() > 0.7,
            "es_picante": random.random() > 0.7,
            "calorias": random.randint(200, 800),
            "tiempo_preparacion": random.randint(10, 30),
            "ingredientes": ["Ingrediente 1", "Ingrediente 2", "Ingrediente 3"],
            "alergenos": random.sample(["Gluten", "Soya", "Mariscos", "Ninguno"], k=1),
            "created_at": generar_timestamp(),
            "updated_at": generar_timestamp()
        }

        productos.append(producto)
        productos_por_local[local_id].append(producto_id)

with open(f"{output_dir}/productos.json", "w", encoding="utf-8") as f:
    json.dump(productos, f, indent=2, ensure_ascii=False)

# 4. Generar Empleados
print("👨‍🍳 Generando Empleados...")
empleados = []
empleados_por_local = {local_id: {"repartidor": [], "cocinero": [], "despachador": []}
                       for local_id in locales_ids}

for i in range(NUM_EMPLEADOS):
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    dni = generar_dni()
    local_id = random.choice(locales_ids)
    role = random.choice(["repartidor", "cocinero", "despachador"])

    empleado = {
        "PK": f"LOCAL#{local_id}",
        "SK": f"EMPLEADO#{dni}",
        "empleado_id": dni,
        "local_id": local_id,
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "email": generar_email(nombre, apellido, f"_{i}"),
        "telefono": generar_telefono(),
        "role": role,
        "fecha_contratacion": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
        "salario": round(random.uniform(1200.0, 3000.0), 2),
        "calificacion_promedio": round(random.uniform(3.5, 5.0), 2),
        "total_calificaciones": random.randint(10, 100),
        "activo": True,
        "turno": random.choice(["mañana", "tarde", "noche"]),
        "created_at": generar_timestamp(),
        "updated_at": generar_timestamp()
    }

    empleados.append(empleado)
    empleados_por_local[local_id][role].append(dni)

with open(f"{output_dir}/empleados.json", "w", encoding="utf-8") as f:
    json.dump(empleados, f, indent=2, ensure_ascii=False)

# 5. Generar Combos
print("🎁 Generando Combos...")
combos = []
combos_por_local = {local_id: [] for local_id in locales_ids}

for local_id in locales_ids:
    num_combos = NUM_COMBOS_POR_LOCAL + random.randint(-1, 2)  # Variación de -1 a +2

    for i in range(num_combos):
        combo_id = generar_uuid()

        if productos_por_local[local_id]:
            num_productos = min(random.randint(2, 4), len(productos_por_local[local_id]))
            productos_combo = random.sample(productos_por_local[local_id], num_productos)
        else:
            continue

        # Calcular precio total de productos individuales
        precio_total = sum([p["precio"] for p in productos if p["producto_id"] in productos_combo])
        precio_combo = round(precio_total * random.uniform(0.7, 0.85), 2) # 15-30% descuento

        combo = {
            "PK": f"LOCAL#{local_id}",
            "SK": f"COMBO#{combo_id}",
            "combo_id": combo_id,
            "local_id": local_id,
            "nombre": f"Combo Especial {i + 1}",
            "descripcion": f"Combo incluye {len(productos_combo)} productos deliciosos",
            "productos_ids": productos_combo,
            "precio": precio_combo,
            "precio_original": precio_total,
            "descuento_porcentaje": round(((precio_total - precio_combo) / precio_total) * 100, 0),
            "disponible": True,
            "imagen_url": f"https://chinawok.pe/images/combos/{combo_id}.jpg",
            "valido_desde": generar_timestamp(),
            "valido_hasta": (datetime.now() + timedelta(days=random.randint(30, 90))).isoformat(),
            "created_at": generar_timestamp(),
            "updated_at": generar_timestamp()
        }

        combos.append(combo)
        combos_por_local[local_id].append(combo_id)

with open(f"{output_dir}/combos.json", "w", encoding="utf-8") as f:
    json.dump(combos, f, indent=2, ensure_ascii=False)

# 6. Generar Pedidos (CIÑÉNDOSE AL SCHEMA)
print("📦 Generando Pedidos...")
pedidos = []
pedidos_ids = []
status_opciones = ["eligiendo", "cocinando", "empacando", "enviando", "recibido"]

# Filtrar usuarios que tienen información bancaria
usuarios_con_pago = [
    u["usuario_id"] for u in usuarios 
    if "informacion_bancaria" in u and u.get("role") == "cliente"
]

if not usuarios_con_pago:
    print("  ⚠️  No hay usuarios con información bancaria. No se pueden generar pedidos.")
else:
    for i in range(NUM_PEDIDOS):
        pedido_id = generar_uuid()
        pedidos_ids.append(pedido_id)
        local_id = random.choice(locales_ids)
        usuario_id = random.choice(usuarios_con_pago)
        status = random.choice(status_opciones)

        # Seleccionar productos (según schema: productos_ids array)
        productos_ids_pedido = []
        if productos_por_local[local_id]:
            num_productos = random.randint(1, 4)
            productos_ids_pedido = random.sample(
                productos_por_local[local_id],
                min(num_productos, len(productos_por_local[local_id]))
            )

        # Calcular costo total
        costo = 0
        for prod_id in productos_ids_pedido:
            prod = next((p for p in productos if p["producto_id"] == prod_id), None)
            if prod:
                costo += prod["precio"]
        
        # Agregar delivery fee
        costo += round(random.uniform(3.0, 8.0), 2)
        costo = round(costo, 2)

        # Crear pedido según schema exacto + PK/SK para DynamoDB
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
            
            pedido["direccion"] = f"Av. Ejemplo {random.randint(100, 999)}, {random.choice(['Miraflores', 'San Isidro', 'Surco'])}, Lima"
            
            fecha_entrega = datetime.now() + timedelta(minutes=random.randint(30, 90))
            pedido["fecha_entrega"] = fecha_entrega.isoformat()

        pedidos.append(pedido)

with open(f"{output_dir}/pedidos.json", "w", encoding="utf-8") as f:
    json.dump(pedidos, f, indent=2, ensure_ascii=False)

print(f"  ✅ {len(pedidos)} pedidos generados con PK/SK")

# 7. Generar Ofertas
print("🎉 Generando Ofertas...")
ofertas = []

for local_id in locales_ids:
    num_ofertas = NUM_OFERTAS_POR_LOCAL + random.randint(-1, 1)  # Variación de ±1

    for i in range(num_ofertas):
        oferta_id = generar_uuid()
        tipo_oferta = random.choice(["producto", "combo", "descuento_general"])

        fecha_inicio = datetime.now() - timedelta(days=random.randint(0, 30))
        fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 60))

        oferta = {
            "PK": f"LOCAL#{local_id}",
            "SK": f"OFERTA#{oferta_id}",
            "oferta_id": oferta_id,
            "local_id": local_id,
            "nombre": f"Oferta Especial {i+1}",
            "descripcion": "Aprovecha esta increíble oferta por tiempo limitado",
            "tipo": tipo_oferta,
            "descuento_porcentaje": random.randint(10, 50),
            "descuento_monto": None,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "activo": True,
            "dias_aplicables": random.sample(["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"], k=random.randint(3, 7)),
            "horario_inicio": "00:00",
            "horario_fin": "23:59",
            "cantidad_maxima_usos": random.randint(50, 200),
            "cantidad_usos_actuales": random.randint(0, 50),
            "created_at": generar_timestamp(),
            "updated_at": generar_timestamp()
        }

        # Asignar a producto o combo
        if tipo_oferta == "producto" and productos_por_local[local_id]:
            oferta["producto_id"] = random.choice(productos_por_local[local_id])
        elif tipo_oferta == "combo" and combos_por_local[local_id]:
            oferta["combo_id"] = random.choice(combos_por_local[local_id])

        ofertas.append(oferta)

with open(f"{output_dir}/ofertas.json", "w", encoding="utf-8") as f:
    json.dump(ofertas, f, indent=2, ensure_ascii=False)

# 8. Generar Reseñas
print("⭐ Generando Reseñas...")
resenas = []

# Filtrar pedidos con status "recibido" (equivalente a "entregado")
pedidos_recibidos = [p for p in pedidos if p["status"] == "recibido"]

if not pedidos_recibidos:
    print("  ⚠️  No hay pedidos recibidos. No se pueden generar reseñas.")
else:
    # Limitar al número configurado o los pedidos recibidos disponibles
    num_resenas_a_generar = min(NUM_RESENAS, len(pedidos_recibidos))
    
    # Seleccionar aleatoriamente pedidos para reseñar
    pedidos_a_reseñar = random.sample(pedidos_recibidos, num_resenas_a_generar)

    for pedido in pedidos_a_reseñar:
        resena_id = generar_uuid()
        local_id = pedido["local_id"]
        calificacion = round(random.uniform(3.5, 5.0), 1)

        comentarios_positivos = [
            "Excelente servicio y comida deliciosa",
            "Muy buena atención, volveré pronto",
            "Entrega rápida y producto fresco",
            "Calidad excepcional, totalmente recomendado",
            "Buen sabor y presentación impecable"
        ]
        
        comentarios_neutrales = [
            "Bueno pero puede mejorar",
            "Cumple con lo esperado",
            "Servicio aceptable"
        ]

        resena = {
            "PK": f"LOCAL#{local_id}",
            "SK": f"RESENA#{resena_id}",
            "resena_id": resena_id,
            "local_id": local_id,
            "pedido_id": pedido["pedido_id"],
            "usuario_id": pedido["usuario_id"],
            "calificacion": calificacion,
            "comentario": random.choice(comentarios_positivos if calificacion >= 4.0 else comentarios_neutrales),
            "calificacion_comida": round(random.uniform(3.0, 5.0), 1),
            "calificacion_servicio": round(random.uniform(3.0, 5.0), 1),
            "calificacion_entrega": round(random.uniform(3.0, 5.0), 1),
            "respuesta_local": None,
            "fecha_respuesta": None,
            "verificada": True,
            "reportada": False,
            "created_at": generar_timestamp(),
            "updated_at": generar_timestamp()
        }

        # 60% incluyen calificación de empleado
        if random.random() > 0.4 and "repartidor_dni" in pedido and pedido["repartidor_dni"]:
            resena["empleado_dni"] = pedido["repartidor_dni"]
            resena["calificacion_empleado"] = round(random.uniform(3.5, 5.0), 1)

        resenas.append(resena)

with open(f"{output_dir}/resenas.json", "w", encoding="utf-8") as f:
    json.dump(resenas, f, indent=2, ensure_ascii=False)