#  Sistema de Gestión de Productos - CRUD

Trabajo Práctico Final - Técnicas Avanzadas de Programación

##  Descripción

Sistema CRUD (Crear, Leer, Actualizar, Eliminar) desarrollado en Python para gestionar productos con base de datos SQLite. Permite realizar operaciones básicas sobre una tabla de productos con interfaz de línea de comandos.

##  Estructura del Proyecto
```
tp-final/
│
├── src/
│   └── crud.py          # Código fuente principal del CRUD
│
├── dbf/
│   ├── estructura.sql   # Script de creación de la base de datos
│   └── productos.db     # Base de datos SQLite (se genera automáticamente)
│
├── dist/                # Carpeta para distribución (vacía)
│
└── README.md            # Este archivo
```

##  Base de Datos

### Tabla: productos

| Campo  | Tipo    | Descripción                    |
|--------|---------|--------------------------------|
| id     | INTEGER | Identificador único (autoincremental) |
| nombre | TEXT    | Nombre del producto            |
| precio | REAL    | Precio del producto (≥ 0)      |
| stock  | INTEGER | Cantidad en stock (≥ 0)        |



### Pasos para Ejecutar

1. **Clonar o descargar el repositorio**
```bash
git clone <URL-del-repositorio>
cd tp-final
```

2. **Ejecutar el programa**
```bash
# Desde la carpeta tp-final:
python src/crud.py

# O desde la carpeta src:
cd src
python crud.py
```

3. **Primera ejecución**: El sistema creará automáticamente la base de datos con datos de ejemplo.

##  Funcionalidades

### Menú Principal

El sistema ofrece 6 opciones:

1. **Crear producto**: Agregar un nuevo producto a la base de datos
2. **Ver todos los productos**: Listar todos los productos registrados
3. **Buscar producto por ID**: Consultar información de un producto específico
4. **Actualizar producto**: Modificar datos de un producto existente
5. **Eliminar producto**: Borrar un producto de la base de datos
6. **Salir**: Cerrar el sistema

### Validaciones Implementadas

-  Nombres no pueden estar vacíos
-  Precios deben ser números positivos
-  Stock debe ser un número entero positivo
-  IDs deben ser números enteros válidos
-  Confirmación antes de eliminar productos

##  Pruebas

Para verificar el funcionamiento correcto:

1. **Listar productos**: Verificar que aparecen los datos de ejemplo
2. **Crear producto**: Agregar un producto nuevo y verificar su creación
3. **Buscar por ID**: Consultar un producto específico
4. **Actualizar**: Modificar un producto y verificar los cambios
5. **Eliminar**: Borrar un producto y verificar su eliminación
6. **Validaciones**: Intentar ingresar datos inválidos (negativos, vacíos, etc.)

##  Tecnologías Utilizadas

- **Lenguaje**: Python 3
- **Base de Datos**: SQLite 3
- **Librería de BD**: sqlite3 (nativa de Python)

## 👤 Alumno: 

Alejandra Cortés


##  Notas Adicionales

- La base de datos se crea automáticamente en `dbf/productos.db` en la primera ejecución
- Los datos de ejemplo se cargan desde `dbf/estructura.sql`
- El sistema incluye manejo básico de errores y validaciones
- La interfaz es de línea de comandos con menú interactivo



