import sqlite3

conn = sqlite3.connect('gestion_ventas_compras.db')
cursor = conn.cursor()
#registrar producto


def registrar_producto(nombre, codigo, precio_compra, precio_venta, stock):
    cursor.execute('''INSERT INTO productos (nombre, codigo, precio_compra, precio_venta, stock)
                      VALUES (?, ?, ?, ?, ?)''', (nombre, codigo, precio_compra, precio_venta, stock))
    conn.commit()
    print(f'Producto "{nombre}" registrado exitosamente.')

#realizar compra1

def realizar_compra(producto_id, cantidad, fecha_compra):
    # Actualizar el stock del producto
    cursor.execute('''UPDATE productos SET stock = stock + ? WHERE id = ?''', (cantidad, producto_id))
    
    # Registrar la compra
    cursor.execute('''INSERT INTO compras (producto_id, cantidad, fecha_compra)
                      VALUES (?, ?, ?)''', (producto_id, cantidad, fecha_compra))
    
    conn.commit()
    print(f'Compra de {cantidad} unidades del producto ID {producto_id} registrada.')

#realizar ventas 

def realizar_venta(producto_id, cantidad, fecha_venta):
    # Comprobar si hay suficiente stock
    cursor.execute('SELECT stock FROM productos WHERE id = ?', (producto_id,))
    stock_actual = cursor.fetchone()[0]
    
    if stock_actual >= cantidad:
        # Reducir el stock
        cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, producto_id))
        
        # Registrar la venta
        cursor.execute('''INSERT INTO ventas (producto_id, cantidad, fecha_venta)
                          VALUES (?, ?, ?)''', (producto_id, cantidad, fecha_venta))
        
        conn.commit()
        print(f'Venta de {cantidad} unidades del producto ID {producto_id} registrada.')
    else:
        print("No hay suficiente stock disponible.")

#consulta de stock

def consultar_stock():
    cursor.execute('SELECT nombre, stock FROM productos')
    productos = cursor.fetchall()
    
    print("Estado actual del stock:")
    for producto in productos:
        print(f'Producto: {producto[0]}, Stock: {producto[1]}')

#cantidades vendidas

def generar_reporte_ventas(fecha_inicio, fecha_fin):
    cursor.execute('''SELECT p.nombre, v.cantidad, v.fecha_venta
                      FROM ventas v
                      JOIN productos p ON v.producto_id = p.id
                      WHERE v.fecha_venta BETWEEN ? AND ?''', (fecha_inicio, fecha_fin))
    ventas = cursor.fetchall()
    
    print(f'Reporte de ventas entre {fecha_inicio} y {fecha_fin}:')
    for venta in ventas:
        print(f'Producto: {venta[0]}, Cantidad: {venta[1]}, Fecha: {venta[2]}')


#borrar producto

def borrar_producto(producto_id):
   
    cursor.execute('SELECT nombre FROM productos WHERE id = ?', (producto_id,))
    producto = cursor.fetchone()

    if producto:
        confirmacion = input(f'¿Está seguro de que desea eliminar el producto "{producto[0]}" (ID: {producto_id})? (s/n): ')
        if confirmacion.lower() == 's':
            
            cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
            conn.commit()
            print(f'Producto "{producto[0]}" (ID: {producto_id}) eliminado exitosamente.')
        else:
            print("Operación cancelada.")
    else:
        print(f"No se encontró un producto con el ID {producto_id}.")
      

def mostrar_menu():
    print("\n--- Sistema de Gestión de Ventas y Compras ---")
    print("1. Registrar Producto")
    print("2. Realizar Compra")
    print("3. Realizar Venta")
    print("4. Consultar Stock")
    print("5. Generar Reporte de Ventas")
    print("6. Borrar Producto") 
    print("7. Salir")

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ")
            codigo = input("Código del producto: ")
            precio_compra = float(input("Precio de compra: "))
            precio_venta = float(input("Precio de venta: "))
            stock = int(input("Cantidad inicial en stock: "))
            registrar_producto(nombre, codigo, precio_compra, precio_venta, stock)
        
        elif opcion == '2':
            producto_id = int(input("ID del producto: "))
            cantidad = int(input("Cantidad a comprar: "))
            fecha_compra = input("Fecha de compra (YYYY-MM-DD): ")
            realizar_compra(producto_id, cantidad, fecha_compra)
        
        elif opcion == '3':
            producto_id = int(input("ID del producto: "))
            cantidad = int(input("Cantidad a vender: "))
            fecha_venta = input("Fecha de venta (YYYY-MM-DD): ")
            realizar_venta(producto_id, cantidad, fecha_venta)
        
        elif opcion == '4':
            consultar_stock()
        
        elif opcion == '5':
            fecha_inicio = input("Fecha de inicio del reporte (YYYY-MM-DD): ")
            fecha_fin = input("Fecha de fin del reporte (YYYY-MM-DD): ")
            generar_reporte_ventas(fecha_inicio, fecha_fin)

        elif opcion == '6': 
            producto_id = int(input("ID del producto a eliminar: "))
            borrar_producto(producto_id) 

        elif opcion == '7':
            print("Saliendo del sistema...")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")

# Ejecutar el menú
ejecutar_menu()
