import json
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from decimal import Decimal

# Cargar variables de entorno
load_dotenv()

# Configuración de AWS
# Las credenciales se obtienen automáticamente de ~/.aws/credentials
# La región se puede configurar en .env o en ~/.aws/config (por defecto: us-east-1)

 = os.getenv('AWS_REGION', 'us-east-1')

# Nombres de las tablas DynamoDB
TABLE_LOCALES = os.getenv('TABLE_LOCALES')
TABLE_USUARIOS = os.getenv('TABLE_USUARIOS')
TABLE_PRODUCTOS = os.getenv('TABLE_PRODUCTOS')
TABLE_EMPLEADOS = os.getenv('TABLE_EMPLEADOS')
TABLE_COMBOS = os.getenv('TABLE_COMBOS')
TABLE_PEDIDOS = os.getenv('TABLE_PEDIDOS')
TABLE_OFERTAS = os.getenv('TABLE_OFERTAS')
TABLE_RESENAS = os.getenv('TABLE_RESENAS')

# Carpeta con los datos JSON
DATA_DIR = "dynamodb_data"

# Mapeo de archivos JSON a tablas DynamoDB
TABLE_MAPPING = {
    "locales.json": TABLE_LOCALES,
    "usuarios.json": TABLE_USUARIOS,
    "productos.json": TABLE_PRODUCTOS,
    "empleados.json": TABLE_EMPLEADOS,
    "combos.json": TABLE_COMBOS,
    "pedidos.json": TABLE_PEDIDOS,
    "ofertas.json": TABLE_OFERTAS,
    "resenas.json": TABLE_RESENAS
}


def convert_float_to_decimal(obj):
    """
    Convierte float a Decimal recursivamente para compatibilidad con DynamoDB
    """
    if isinstance(obj, list):
        return [convert_float_to_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_float_to_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj


def get_dynamodb_client():
    """
    Crea y retorna un cliente de DynamoDB usando credenciales de ~/.aws/credentials
    """
    try:
        # boto3 automáticamente busca credenciales en:
        # 1. Variables de entorno
        # 2. ~/.aws/credentials
        # 3. ~/.aws/config
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        
        # Verificar conexión intentando listar tablas
        client = boto3.client('dynamodb', region_name=AWS_REGION)
        client.list_tables(Limit=1)
        
        return dynamodb
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'UnrecognizedClientException':
            print(f"❌ Error de credenciales: Verifica tu archivo ~/.aws/credentials")
        else:
            print(f"❌ Error al conectar con DynamoDB: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"❌ Error al conectar con DynamoDB: {e}")
        print(f"💡 Verifica que el archivo ~/.aws/credentials esté configurado correctamente")
        return None


def load_json_file(filename):
    """
    Carga un archivo JSON y retorna su contenido
    """
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convertir floats a Decimal
            return convert_float_to_decimal(data)
    except FileNotFoundError:
        print(f"⚠️  Archivo no encontrado: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️  Error al decodificar JSON en {filename}: {e}")
        return None


def batch_write_items(table, items, batch_size=25):
    """
    Escribe items en lotes a DynamoDB (máximo 25 items por batch)
    """
    total_items = len(items)
    success_count = 0
    error_count = 0

    for i in range(0, total_items, batch_size):
        batch = items[i:i + batch_size]

        try:
            with table.batch_writer() as batch_writer:
                for item in batch:
                    batch_writer.put_item(Item=item)
                    success_count += 1

            print(f"  ✓ Procesados {min(i + batch_size, total_items)}/{total_items} items")

        except ClientError as e:
            error_count += len(batch)
            print(f"  ✗ Error en batch {i // batch_size + 1}: {e.response['Error']['Message']}")
        except Exception as e:
            error_count += len(batch)
            print(f"  ✗ Error inesperado en batch {i // batch_size + 1}: {e}")

    return success_count, error_count


def populate_table(dynamodb, filename, table_name):
    """
    Población de una tabla específica con datos del archivo JSON
    """
    print(f"\n📤 Poblando tabla: {table_name}")
    print(f"   Archivo: {filename}")

    # Validar nombre de tabla
    if not table_name:
        print(f"  ⚠️  Nombre de tabla no configurado en .env para {filename}")
        return False

    # Cargar datos del archivo
    items = load_json_file(filename)
    if items is None:
        return False

    if len(items) == 0:
        print(f"  ⚠️  El archivo {filename} está vacío")
        return False

    try:
        # Obtener referencia a la tabla
        table = dynamodb.Table(table_name)

        # Escribir items en lotes
        success, errors = batch_write_items(table, items)

        print(f"  ✅ Completado: {success} items insertados")
        if errors > 0:
            print(f"  ⚠️  {errors} items fallaron")

        return errors == 0

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"  ❌ La tabla '{table_name}' no existe en DynamoDB")
        else:
            print(f"  ❌ Error de DynamoDB: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False


def verify_credentials():
    """
    Verifica que las credenciales de AWS estén disponibles
    """
    try:
        # Intentar obtener credenciales de la sesión de boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            print("❌ ERROR: No se encontraron credenciales de AWS")
            print("   Configura el archivo ~/.aws/credentials con el formato:")
            print("   [default]")
            print("   aws_access_key_id=YOUR_ACCESS_KEY_ID")
            print("   aws_secret_access_key=YOUR_SECRET_ACCESS_KEY")
            print("   aws_session_token=YOUR_SESSION_TOKEN (opcional)")
            return False
        
        return True
    except Exception as e:
        print(f"❌ ERROR al verificar credenciales: {e}")
        return False


def verify_table_names():
    """
    Verifica que los nombres de las tablas estén configurados
    """
    missing_tables = []
    for filename, table_name in TABLE_MAPPING.items():
        if not table_name:
            missing_tables.append(filename)

    if missing_tables:
        print("⚠️  ADVERTENCIA: Algunas tablas no están configuradas en .env:")
        for filename in missing_tables:
            print(f"   - {filename}")
        print("\n   Estas tablas serán omitidas")
        return False
    return True


def main():
    """
    Función principal que ejecuta la población de todas las tablas
    """
    print("=" * 60)
    print("🚀 CHINA WOK - DATA POBLATOR")
    print("=" * 60)

    # Verificar credenciales
    if not verify_credentials():
        return

    # Verificar nombres de tablas
    verify_table_names()

    # Verificar que existe la carpeta de datos
    if not os.path.exists(DATA_DIR):
        print(f"\n❌ ERROR: La carpeta '{DATA_DIR}/' no existe")
        print("   Ejecuta primero el script DataGenerator.py")
        return

    # Conectar a DynamoDB
    print(f"\n🔌 Conectando a DynamoDB en región: {AWS_REGION}")
    dynamodb = get_dynamodb_client()

    if dynamodb is None:
        print("❌ No se pudo establecer conexión con DynamoDB")
        return

    print("✅ Conexión establecida exitosamente")

    # Poblar cada tabla
    print("\n" + "=" * 60)
    print("📊 INICIANDO POBLACIÓN DE TABLAS")
    print("=" * 60)

    results = {}
    for filename, table_name in TABLE_MAPPING.items():
        if table_name:  # Solo procesar si hay nombre de tabla configurado
            success = populate_table(dynamodb, filename, table_name)
            results[filename] = success

    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)

    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful

    print(f"\n✅ Tablas pobladas exitosamente: {successful}")
    if failed > 0:
        print(f"❌ Tablas con errores: {failed}")

    print("\n" + "=" * 60)
    print("🎉 PROCESO COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    main()