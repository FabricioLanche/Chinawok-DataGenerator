"""
Datos de ejemplo para el generador
"""


class SampleData:
    """Catálogos de datos de ejemplo"""
    
    # Nombres (150 nombres únicos)
    NOMBRES = [
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
    APELLIDOS = [
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
    CATEGORIAS = [
        "Arroces", "Tallarines", "Chaufas", "Wantanes", "Sopas",
        "Pollo", "Cerdo", "Res", "Mariscos", "Pescado",
        "Entradas Frías", "Entradas Calientes", "Rolls", "Dim Sum", "Dumplings",
        "Bebidas Frías", "Bebidas Calientes", "Jugos", "Tés", "Postres",
        "Salsas", "Guarniciones", "Ensaladas", "Especiales", "Vegetarianos",
        "Veganos", "Kids Menu", "Combos Familiares", "Promos", "Snacks"
    ]
    
    # Nombres de productos (200 productos únicos)
    PRODUCTOS_NOMBRES = [
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
        
       