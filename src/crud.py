import sqlite3
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'dbf', 'productos.db')
SQL_PATH = os.path.join(BASE_DIR, 'dbf', 'estructura.sql')


def conectar_db():
    """Establece conexión con la base de datos"""
    try:
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except sqlite3.Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None


def inicializar_db():
    """Crea la base de datos y las tablas si no existen"""
    try:
        # Verifica si existe el archivo SQL
        if not os.path.exists(SQL_PATH):
            print(f"⚠️  Advertencia: No se encontró {SQL_PATH}")
            print("Creando tabla manualmente...")
            conexion = conectar_db()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        precio REAL NOT NULL CHECK(precio >= 0),
                        stock INTEGER NOT NULL CHECK(stock >= 0)
                    )
                ''')
                conexion.commit()
                conexion.close()
                print("✅ Base de datos creada exitosamente")
        else:
            # Lee y ejecuta el archivo SQL
            with open(SQL_PATH, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            conexion = conectar_db()
            if conexion:
                cursor = conexion.cursor()
                cursor.executescript(sql_script)
                conexion.commit()
                conexion.close()
                print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")


def crear_producto():
    """Crear un nuevo producto"""
    print("\n" + "="*50)
    print("➕  CREAR NUEVO PRODUCTO")
    print("="*50)
    
    try:
        # Solicitar datos
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return
        
        precio_str = input("Precio: $").strip()
        try:
            precio = float(precio_str)
            if precio < 0:
                print("❌ El precio no puede ser negativo")
                return
        except ValueError:
            print("❌ El precio debe ser un número válido")
            return
        
        stock_str = input("Stock: ").strip()
        try:
            stock = int(stock_str)
            if stock < 0:
                print("❌ El stock no puede ser negativo")
                return
        except ValueError:
            print("❌ El stock debe ser un número entero válido")
            return
        
        # Insertar en la base de datos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre, precio, stock)
            )
            conexion.commit()
            producto_id = cursor.lastrowid
            conexion.close()
            print(f"\n✅ Producto creado exitosamente con ID: {producto_id}")
        
    except sqlite3.Error as e:
        print(f"❌ Error al crear el producto: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def leer_productos():
    """Leer y mostrar todos los productos"""
    print("\n" + "="*50)
    print("📋  LISTA DE PRODUCTOS")
    print("="*50)
    
    try:
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id")
            productos = cursor.fetchall()
            conexion.close()
            
            if not productos:
                print("\n⚠️  No hay productos registrados")
            else:
                print(f"\n{'ID':<5} {'NOMBRE':<30} {'PRECIO':<12} {'STOCK':<8}")
                print("-" * 60)
                for producto in productos:
                    id_prod, nombre, precio, stock = producto
                    print(f"{id_prod:<5} {nombre:<30} ${precio:<11.2f} {stock:<8}")
                print(f"\n📊 Total de productos: {len(productos)}")
    
    except sqlite3.Error as e:
        print(f"❌ Error al leer los productos: {e}")


def leer_producto_por_id():
    """Buscar y mostrar un producto por su ID"""
    print("\n" + "="*50)
    print("🔍  BUSCAR PRODUCTO POR ID")
    print("="*50)
    
    try:
        id_str = input("Ingrese el ID del producto: ").strip()
        try:
            producto_id = int(id_str)
        except ValueError:
            print("❌ El ID debe ser un número entero")
            return
        
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
            producto = cursor.fetchone()
            conexion.close()
            
            if producto:
                print(f"\n{'Campo':<15} {'Valor'}")
                print("-" * 40)
                print(f"{'ID:':<15} {producto[0]}")
                print(f"{'Nombre:':<15} {producto[1]}")
                print(f"{'Precio:':<15} ${producto[2]:.2f}")
                print(f"{'Stock:':<15} {producto[3]}")
            else:
                print(f"\n❌ No se encontró ningún producto con ID {producto_id}")
    
    except sqlite3.Error as e:
        print(f"❌ Error al buscar el producto: {e}")


def actualizar_producto():
    """Actualizar un producto existente"""
    print("\n" + "="*50)
    print("✏️  ACTUALIZAR PRODUCTO")
    print("="*50)
    
    try:
        # Primero mostrar productos
        leer_productos()
        
        id_str = input("\nIngrese el ID del producto a actualizar: ").strip()
        try:
            producto_id = int(id_str)
        except ValueError:
            print("❌ El ID debe ser un número entero")
            return
        
        # Verificar que el producto existe
        conexion = conectar_db()
        if not conexion:
            return
        
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()
        
        if not producto:
            print(f"\n❌ No se encontró ningún producto con ID {producto_id}")
            conexion.close()
            return
        
        print(f"\nProducto actual: {producto[1]} - ${producto[2]:.2f} - Stock: {producto[3]}")
        print("\n📝 Ingrese los nuevos valores (presione Enter para mantener el valor actual):")
        
        # Solicitar nuevos datos
        nombre = input(f"Nuevo nombre [{producto[1]}]: ").strip()
        nombre = nombre if nombre else producto[1]
        
        precio_str = input(f"Nuevo precio [{producto[2]:.2f}]: ").strip()
        if precio_str:
            try:
                precio = float(precio_str)
                if precio < 0:
                    print("❌ El precio no puede ser negativo. Se mantendrá el valor actual.")
                    precio = producto[2]
            except ValueError:
                print("❌ Valor inválido. Se mantendrá el precio actual.")
                precio = producto[2]
        else:
            precio = producto[2]
        
        stock_str = input(f"Nuevo stock [{producto[3]}]: ").strip()
        if stock_str:
            try:
                stock = int(stock_str)
                if stock < 0:
                    print("❌ El stock no puede ser negativo. Se mantendrá el valor actual.")
                    stock = producto[3]
            except ValueError:
                print("❌ Valor inválido. Se mantendrá el stock actual.")
                stock = producto[3]
        else:
            stock = producto[3]
        
        # Actualizar en la base de datos
        cursor.execute(
            "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre, precio, stock, producto_id)
        )
        conexion.commit()
        conexion.close()
        
        print(f"\n✅ Producto actualizado exitosamente")
        print(f"Nuevos valores: {nombre} - ${precio:.2f} - Stock: {stock}")
    
    except sqlite3.Error as e:
        print(f"❌ Error al actualizar el producto: {e}")


def eliminar_producto():
    """Eliminar un producto"""
    print("\n" + "="*50)
    print("🗑️  ELIMINAR PRODUCTO")
    print("="*50)
    
    try:
        # Primero mostrar productos
        leer_productos()
        
        id_str = input("\nIngrese el ID del producto a eliminar: ").strip()
        try:
            producto_id = int(id_str)
        except ValueError:
            print("❌ El ID debe ser un número entero")
            return
        
        # Verificar que el producto existe
        conexion = conectar_db()
        if not conexion:
            return
        
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()
        
        if not producto:
            print(f"\n❌ No se encontró ningún producto con ID {producto_id}")
            conexion.close()
            return
        
        print(f"\n⚠️  Está por eliminar: {producto[1]} - ${producto[2]:.2f} - Stock: {producto[3]}")
        confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
        
        if confirmacion == 's' or confirmacion == 'si':
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conexion.commit()
            print(f"\n✅ Producto eliminado exitosamente")
        else:
            print("\n❌ Eliminación cancelada")
        
        conexion.close()
    
    except sqlite3.Error as e:
        print(f"❌ Error al eliminar el producto: {e}")


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("🛒  SISTEMA DE GESTIÓN DE PRODUCTOS")
    print("="*50)
    print("1. ➕  Crear producto")
    print("2. 📋  Ver todos los productos")
    print("3. 🔍  Buscar producto por ID")
    print("4. ✏️  Actualizar producto")
    print("5. 🗑️  Eliminar producto")
    print("6. 🚪  Salir")
    print("="*50)


def main():
    """Función principal"""
    print("\n" + "="*50)
    print("🚀  INICIANDO SISTEMA DE GESTIÓN DE PRODUCTOS")
    print("="*50)
    
    # Inicializar la base de datos
    inicializar_db()
    
    while True:
        mostrar_menu()
        opcion = ''.join(filter(str.isdigit, input("\n👉 Seleccione una opción (1-6): ")))
        
        if opcion == '1':
            crear_producto()
        elif opcion == '2':
            leer_productos()
        elif opcion == '3':
            leer_producto_por_id()
        elif opcion == '4':
            actualizar_producto()
        elif opcion == '5':
            eliminar_producto()
        elif opcion == '6':
            print("\n👋 ¡Gracias por usar el sistema! Hasta pronto.")
            break
        else:
            print("\n❌ Opción inválida. Por favor seleccione un número del 1 al 6.")
        
        input("\n⏸️  Presione Enter para continuar...")


if __name__ == "__main__":
    main()