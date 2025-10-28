# Generador de Datos para DynamoDB - China Wok

Script Python que genera datos de prueba para las tablas de DynamoDB de la cadena de comidas China Wok.

## Descripción

Este generador crea archivos JSON con datos ficticios pero realistas para todas las tablas del sistema de gestión de China Wok. Los datos están relacionados entre sí manteniendo integridad referencial (por ejemplo, los pedidos referencian usuarios y productos existentes).

## Uso

```bash
python script.py
```

El script creará una carpeta `dynamodb_data/` con 8 archivos JSON listos para importar a DynamoDB.

## Estructura de Salida

```
dynamodb_data/
├── locales.json           # 3 locales de China Wok
├── usuarios.json          # 15 usuarios (clientes y admins)
├── productos.json         # ~30 productos con stock por local
├── empleados.json         # 20 empleados (cocineros, repartidores, despachadores)
├── combos.json            # ~8 combos de productos
├── pedidos.json           # 30 pedidos en diferentes estados
├── ofertas.json           # ~12 ofertas activas
└── resenas.json           # 20 reseñas de pedidos completados
```

## Schemas de Tablas

### 1. Usuarios
- **Partition Key:** `usuario_id`
- **Atributos:** nombre, correo, contraseña, role (Cliente/Admin), información_bancaria (opcional)
- **Nota:** Entidad global, independiente de locales

### 2. Productos
- **Partition Key:** `local_id`
- **Sort Key:** `producto_id`
- **Atributos:** nombre, precio, descripción, categoría, stock
- **Nota:** Cada local maneja sus propios productos y stock

### 3. Locales
- **Partition Key:** `local_id`
- **Atributos:** dirección, teléfono, hora_apertura, hora_finalizacion

### 4. Empleados
- **Partition Key:** `local_id`
- **Sort Key:** `dni`
- **Atributos:** nombre, apellido, role (Repartidor/Cocinero/Despachador), calificación_prom, sueldo

### 5. Combos
- **Partition Key:** `local_id`
- **Sort Key:** `combo_id`
- **Atributos:** nombre, productos_ids (array), descripción

### 6. Pedidos
- **Partition Key:** `local_id`
- **Sort Key:** `pedido_id`
- **Atributos:** usuario_id, productos_ids (array), costo, status, empleados asignados (DNIs), fecha_entrega, dirección
- **Status:** eligiendo, cocinando, empacando, enviando, recibido

### 7. Ofertas
- **Partition Key:** `local_id`
- **Sort Key:** `oferta_id`
- **Atributos:** producto_id o combo_id, fecha_inicio, fecha_limite, porcentaje_descuento

### 8. Reseñas
- **Partition Key:** `local_id`
- **Sort Key:** `resena_id`
- **Atributos:** pedido_id, reseña (texto), calificación (0-5), empleado_dni (opcional)

## Características

- ✅ Datos coherentes entre tablas con integridad referencial
- ✅ Validación de formatos (emails, tarjetas, fechas, teléfonos)
- ✅ Lógica de negocio (empleados según status del pedido)
- ✅ Productos y menú típico de China Wok
- ✅ Locales con direcciones reales de Lima, Perú

## Dependencias

- Python 3.6+
- Módulos estándar: json, os, datetime, random, string

No requiere instalación de paquetes externos.