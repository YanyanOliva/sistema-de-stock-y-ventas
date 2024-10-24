import sqlite3

# Conexión a la base de datos 
conn = sqlite3.connect('gestion_ventas_compras.db')

# Crear un cursor para ejecutar comados SQL
cursor = conn.cursor()

# Crear las tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    codigo TEXT NOT NULL,
                    precio_compra REAL NOT NULL,
                    precio_venta REAL NOT NULL,
                    stock INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    fecha_venta TEXT NOT NULL,
                    FOREIGN KEY(producto_id) REFERENCES productos(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    fecha_compra TEXT NOT NULL,
                    FOREIGN KEY(producto_id) REFERENCES productos(id))''')

# Confirmar los cambios
conn.commit()


