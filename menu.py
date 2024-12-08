from db_operaciones import crear_bd, agregar_producto, mostrar_productos, actualizar_producto, eliminar_producto, buscar_producto_por_id, buscar_producto_por_nombre, buscar_producto_por_categoria, reporte_stock_bajo, reporte_todos_los_productos, borrar_reportes
from colorama import init, Fore, Style

# Inicializar colorama
init()

# Función para validar entradas numéricas
def input_num(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor, ingrese un número." + Style.RESET_ALL)

# Función para validar entradas de precios
def input_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor, ingrese un número decimal." + Style.RESET_ALL)

# Función para mostrar todos los productos con sus IDs y cantidades
def listar_productos():
    productos = mostrar_productos()
    if len(productos) == 0:
        print(f"{Fore.YELLOW}No hay productos en el inventario.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}{'-'*90}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Lista de Productos:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<10}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'-'*5} {'-'*20} {'-'*30} {'-'*10} {'-'*10} {'-'*10}{Style.RESET_ALL}")
        for producto in productos:
            print(f"{Fore.GREEN}{producto[0]:<5} {producto[1]:<20} {producto[2]:<30} {producto[3]:<10} {producto[4]:<10} {producto[5]:<10}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'-'*90}{Style.RESET_ALL}")

# Menú principal de la aplicación
def menu():
    try:
        while True:
            print(f"{Fore.CYAN}\nGestión de Inventario{Style.RESET_ALL}")
            print(f"{Fore.BLUE}1. Registrar producto{Style.RESET_ALL}")
            print(f"{Fore.BLUE}2. Actualizar cantidad de producto{Style.RESET_ALL}")
            print(f"{Fore.BLUE}3. Eliminar producto{Style.RESET_ALL}")
            print(f"{Fore.BLUE}4. Mostrar productos{Style.RESET_ALL}")
            print(f"{Fore.BLUE}5. Buscar producto{Style.RESET_ALL}")
            print(f"{Fore.BLUE}6. Generar reporte{Style.RESET_ALL}")
            print(f"{Fore.BLUE}7. Borrar reportes generados{Style.RESET_ALL}")
            print(f"{Fore.BLUE}8. Salir{Style.RESET_ALL}")
            
            opcion = input(f"{Fore.MAGENTA}Seleccione una opción: {Style.RESET_ALL}")
            
            if opcion == '1':
                while True:
                    nombre = input("Nombre del producto (o ingrese 'S' para salir): ")
                    if nombre.lower() == 's':
                        break
                    descripcion = input("Descripción del producto: ")
                    cantidad = input_num("Cantidad: ")
                    precio = input_float("Precio: ")
                    categoria = input("Categoría: ")
                    umbral_stock_bajo = input_num("Umbral de stock bajo: ")
                    agregar_producto(nombre, descripcion, cantidad, precio, categoria, umbral_stock_bajo)
                    repetir = input(f"{Fore.MAGENTA}¿Desea agregar otro producto? (s/n): {Style.RESET_ALL}").lower()
                    if repetir != 's':
                        break
            elif opcion == '2':
                while True:
                    productos = mostrar_productos()
                    if not productos:
                        print(f"{Fore.YELLOW}No hay productos en el inventario.{Style.RESET_ALL}")
                        break

                    listar_productos()
                    id = input("ID del producto que desea actualizar (o ingrese 'S' para salir): ")
                    if id.lower() == 's':
                        break
                    try:
                        id = int(id)
                        cantidad = input_num("Nueva cantidad: ")
                        actualizar_producto(id, cantidad)
                        repetir = input(f"{Fore.MAGENTA}¿Desea actualizar otro producto? (s/n): {Style.RESET_ALL}").lower()
                        if repetir != 's':
                            break
                    except ValueError:
                        print(Fore.RED + "ID no válido. Por favor, ingrese un número o 'S' para salir." + Style.RESET_ALL)
            elif opcion == '3':
                while True:
                    productos = mostrar_productos()
                    if not productos:
                        print(f"{Fore.YELLOW}No hay productos en el inventario.{Style.RESET_ALL}")
                        break

                    listar_productos()
                    id = input("ID del producto que desea eliminar (o ingrese 'S' para salir): ")
                    if id.lower() == 's':
                        break
                    try:
                        id = int(id)
                        eliminar_producto(id)
                        repetir = input(f"{Fore.MAGENTA}¿Desea eliminar otro producto? (s/n): {Style.RESET_ALL}").lower()
                        if repetir != 's':
                            break
                    except ValueError:
                        print(Fore.RED + "ID no válido. Por favor, ingrese un número o 'S' para salir." + Style.RESET_ALL)
            elif opcion == '4':
                listar_productos()
            elif opcion == "5":
            # Opción 5 para buscar productos
                while True:
                    criterio = input("Buscar por (id/nombre/categoría) o ingrese 'S' para salir: ").lower()
                    if criterio == 's':
                        break
                    if criterio == 'id':
                        id_producto = input_num("ID del producto: ")  # La función input_num debe permitir ingresar solo números
                        productos = buscar_producto_por_id(id_producto)
                        if len(productos) == 0:
                            print(f"{Fore.YELLOW}No se encontraron productos con ese ID.{Style.RESET_ALL}")
                        else:
                            for producto in productos:
                                print(f"{Fore.GREEN}{producto[0]:<5} {producto[1]:<20} {producto[2]:<30} {producto[3]:<10} {producto[4]:<10} {producto[5]:<10}{Style.RESET_ALL}")
                    elif criterio == 'nombre':
                        nombre = input("Nombre del producto: ").strip()
                        productos = buscar_producto_por_nombre(nombre)
                        if len(productos) == 0:
                            print(f"{Fore.YELLOW}No se encontraron productos con ese nombre.{Style.RESET_ALL}")
                        else:
                            for producto in productos:
                                print(f"{Fore.GREEN}{producto[0]:<5} {producto[1]:<20} {producto[2]:<30} {producto[3]:<10} {producto[4]:<10} {producto[5]:<10}{Style.RESET_ALL}")
                    elif criterio == 'categoria':
                        categoria = input("Categoría del producto: ").strip()
                        productos = buscar_producto_por_categoria(categoria)
                        if len(productos) == 0:
                            print(f"{Fore.YELLOW}No se encontraron productos con esa categoría.{Style.RESET_ALL}")
                        else:
                            for producto in productos:
                                print(f"{Fore.GREEN}{producto[0]:<5} {producto[1]:<20} {producto[2]:<30} {producto[3]:<10} {producto[4]:<10} {producto[5]:<10}{Style.RESET_ALL}")
                    else:
                        print(Fore.RED + "Criterio no válido. Por favor, elija id, nombre o categoría." + Style.RESET_ALL)
            elif opcion == '6':
                while True:
                    print(f"{Fore.CYAN}\nGenerar Reporte{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}1. Reporte de Bajo Stock{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}2. Reporte de Todos los Productos en Stock{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}3. Volver al menú principal{Style.RESET_ALL}")

                    sub_opcion = input(f"{Fore.MAGENTA}Seleccione una opción: {Style.RESET_ALL}")
                    
                    if sub_opcion == '1':
                        reporte_stock_bajo()
                    elif sub_opcion == '2':
                        reporte_todos_los_productos()
                    elif sub_opcion == '3':
                        break
                    else:
                        print(Fore.RED + "Opción no válida. Intente de nuevo." + Style.RESET_ALL)
            elif opcion == '7':
                borrar_reportes()
            elif opcion == '8':
                print(f"{Fore.CYAN}Saliendo del programa...{Style.RESET_ALL}")
                break
            else:
                print(Fore.RED + "Opción no válida. Intente de nuevo." + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Programa interrumpido por el usuario. Saliendo...{Style.RESET_ALL}")

# Ejecutar la función para crear la base de datos si no existe
crear_bd()

# Iniciar el menú principal
if __name__ == "__main__":
    menu()