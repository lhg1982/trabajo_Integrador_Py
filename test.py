import sqlite3

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

# Script de prueba para verificar la función de búsqueda
productos = buscar_producto_por_id(2)  # Reemplaza con un ID válido que exista en tu base de datos
print(f"Resultado de la búsqueda: {productos}")  # Mensaje de depuración