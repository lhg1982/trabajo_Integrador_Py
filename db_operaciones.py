import sqlite3
from colorama import Fore, Style
from datetime import datetime
import csv
import os

# Crear la base de datos y la tabla de productos
def crear_bd():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria INTEGER NOT NULL
        )
    ''')

    # Verificar si la columna umbral_stock_bajo existe y agregarla si es necesario
    cursor.execute("PRAGMA table_info(productos)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    if 'umbral_stock_bajo' not in column_names:
        cursor.execute('''
            ALTER TABLE productos ADD COLUMN umbral_stock_bajo INTEGER DEFAULT 5
        ''')
        print(f"{Fore.YELLOW}Columna 'umbral_stock_bajo' añadida a la tabla 'productos'.{Style.RESET_ALL}")

    conn.commit()
    conn.close()

# Agregar un nuevo producto a la base de datos
def agregar_producto(nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo):
    if producto_existe(nombre):
        print(f"{Fore.RED}El producto con el nombre '{nombre}' ya existe o es similar a uno existente.{Style.RESET_ALL}")
        return

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo))  # Umbral personalizado
    conn.commit()
    conn.close()

    mostrar_detalles_producto(nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo)

# Verificar si un producto ya existe en la base de datos
def producto_existe(nombre):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nombre FROM productos WHERE LOWER(nombre) = LOWER(?)
    ''', (nombre,))
    productos = cursor.fetchall()
    conn.close()
    return len(productos) > 0

# Mostrar detalles de un producto
def mostrar_detalles_producto(nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo):
    print(f"{Fore.GREEN}Producto:{Style.RESET_ALL}")
    print(f"Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}, Umbral de Stock Bajo: {umbral_stock_bajo}")
    if cantidad == 0:
        print(f"{Fore.YELLOW}Advertencia: La cantidad del producto es cero, no está apto para la venta.{Style.RESET_ALL}")
    if precio == 0:
        print(f"{Fore.YELLOW}Advertencia: El precio del producto es cero, no está apto para la venta.{Style.RESET_ALL}")

# Actualizar la cantidad de un producto
def actualizar_producto(id, cantidad):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nombre, descripcion, precio, categoria, umbral_stock_bajo FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()

    if producto:
        nombre, descripcion, precio, categoria, umbral_stock_bajo = producto
        cursor.execute('''
            UPDATE productos
            SET cantidad = ?
            WHERE id = ?
        ''', (cantidad, id))
        conn.commit()
        mostrar_detalles_producto(nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo)
    else:
        print(f"{Fore.RED}El producto con ID {id} no existe.{Style.RESET_ALL}")

    conn.close()

# Eliminar un producto de la base de datos
def eliminar_producto(id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nombre FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()

    if producto:
        nombre = producto[0]
        cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        print(f"{Fore.GREEN}El producto '{nombre}' ha sido eliminado exitosamente.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}El producto con ID {id} no existe.{Style.RESET_ALL}")

    conn.close()

# Mostrar todos los productos de la base de datos
def mostrar_productos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Buscar productos por ID
def buscar_producto_por_id(id_producto):
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        print(f"Buscando producto con ID: {id_producto}")  # Mensaje de depuración
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        productos = cursor.fetchall()
        print(f"Productos encontrados: {productos}")  # Mensaje de depuración
        conn.close()
        return productos
    except sqlite3.Error as e:
        print(f"Error al buscar producto por ID: {e}")
        return []

# Buscar productos por nombre
def buscar_producto_por_nombre(nombre):
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE LOWER(nombre) LIKE LOWER(?)', ('%' + nombre + '%',))
        productos = cursor.fetchall()
        conn.close()
        return productos
    except sqlite3.Error as e:
        print(f"Error al buscar producto por nombre: {e}")
        return []

# Buscar productos por categoría
def buscar_producto_por_categoria(categoria):
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        print(f"Buscando producto con ID: {categoria}")  # Mensaje de depuración
        cursor.execute('SELECT * FROM productos WHERE categoria = ?', (categoria,))
        productos = cursor.fetchall()
        print(f"Productos encontrados: {productos}")  # Mensaje de depuración
        conn.close()
        return productos
    except sqlite3.Error as e:
        print(f"Error al buscar producto por categoría: {e}")
        return []

# Generar un reporte de productos con bajo stock
def reporte_stock_bajo():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= umbral_stock_bajo')
    productos = cursor.fetchall()
    conn.close()

    if len(productos) == 0:
        print(f"{Fore.YELLOW}No hay productos con bajo stock.{Style.RESET_ALL}")
    else:
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.RED}Reporte de Productos con Bajo Stock (Generado el {fecha_hora}):{Style.RESET_ALL}")
        mostrar_reporte(productos)
        # Opción para exportar el reporte a un archivo CSV
        exportar_reporte_csv(productos, fecha_hora)

# Mostrar reporte en formato tabulado
def mostrar_reporte(productos):
    print(f"{Fore.YELLOW}{'-'*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<10}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*5} {'-'*20} {'-'*30} {'-'*10} {'-'*10} {'-'*10}{Style.RESET_ALL}")
    for producto in productos:
        print(f"{Fore.GREEN}{producto[0]:<5} {producto[1]:<20} {producto[2]:<30} {producto[3]:<10} {producto[4]:<10} {producto[5]:<10}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*80}{Style.RESET_ALL}")

# Exportar el reporte de stock bajo a un archivo CSV
def exportar_reporte_csv(productos, fecha_hora):
    nombre_archivo = f'reporte_stock_bajo_{fecha_hora.replace(":", "-").replace(" ", "_")}.csv'
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nombre', 'Descripción', 'Cantidad', 'Precio', 'Categoría'])
        for producto in productos:
            writer.writerow(producto)
    print(f"{Fore.GREEN}Reporte exportado exitosamente a {nombre_archivo}.{Style.RESET_ALL}")



# Generar un reporte de productos con bajo stock
def reporte_stock_bajo():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= umbral_stock_bajo')
    productos = cursor.fetchall()
    conn.close()

    if len(productos) == 0:
        print(f"{Fore.YELLOW}No hay productos con bajo stock.{Style.RESET_ALL}")
    else:
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.RED}Reporte de Productos con Bajo Stock (Generado el {fecha_hora}):{Style.RESET_ALL}")
        mostrar_reporte(productos)
        # Opción para exportar el reporte a un archivo CSV
        exportar_reporte_csv(productos, fecha_hora)

# Mostrar reporte en formato tabulado
def mostrar_reporte(productos):
    print(f"{Fore.YELLOW}{'-'*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<10}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*5} {'-'*20} {'-'*30} {'-'*10} {'-'*10} {'-'*10}{Style.RESET_ALL}")
    for producto in productos:
        print(f"{Fore.GREEN}{producto[0]:<5} {producto[1]:<20} {producto[2]:<30} {producto[3]:<10} {producto[4]:<10} {producto[5]:<10}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*80}{Style.RESET_ALL}")

# Exportar el reporte de stock bajo a un archivo CSV
def exportar_reporte_csv(productos, fecha_hora):
    nombre_archivo = f'reporte_stock_bajo_{fecha_hora.replace(":", "-").replace(" ", "_")}.csv'
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nombre', 'Descripción', 'Cantidad', 'Precio', 'Categoría'])
        for producto in productos:
            writer.writerow(producto)
    print(f"{Fore.GREEN}Reporte exportado exitosamente a '{nombre_archivo}'.{Style.RESET_ALL}")

    # Generar un reporte de todos los productos en stock
def reporte_todos_los_productos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

    if len(productos) == 0:
        print(f"{Fore.YELLOW}No hay productos en el inventario.{Style.RESET_ALL}")
    else:
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.CYAN}Reporte de Todos los Productos en Stock (Generado el {fecha_hora}):{Style.RESET_ALL}")
        mostrar_reporte(productos)
        # Opción para exportar el reporte a un archivo CSV
        exportar_reporte_csv(productos, fecha_hora)

# Borrar los reportes generados
def borrar_reportes():
    files_deleted = 0
    for file in os.listdir():
        if file.startswith("reporte_stock_bajo_") or file.startswith("reporte_todos_los_productos_"):
            os.remove(file)
            files_deleted += 1
            print(f"{Fore.GREEN}Reporte '{file}' eliminado exitosamente.{Style.RESET_ALL}")
    if files_deleted == 0:
        print(f"{Fore.YELLOW}No se encontraron reportes para eliminar.{Style.RESET_ALL}")