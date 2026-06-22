"""
main.py
-------
Punto de entrada de PetMatch.

Arma el menú principal de la aplicación, importando los módulos
datos, autenticacion, cliente, catalogo y pedido, y orquestando el
flujo completo: login/registro, gestión de mascotas, catálogo y
carrito de pedidos.
"""

import datos
import auth_sistema as autenticacion
import cliente
import catalogo
import pedido


def pedir_numero(mensaje):
    """Pide un número (float) por consola hasta que sea válido."""
    while True:
        texto = input(mensaje)
        try:
            return float(texto)
        except ValueError:
            print("Ingresá un número válido.")


def pedir_entero(mensaje):
    """Pide un número entero por consola hasta que sea válido."""
    while True:
        texto = input(mensaje)
        try:
            return int(texto)
        except ValueError:
            print("Ingresá un número entero válido.")


# ------------------------------------------------------------------
# MENÚ DE AUTENTICACIÓN
# ------------------------------------------------------------------

def menu_autenticacion():
    """
    Muestra el menú de ingreso/registro hasta que el usuario inicia
    sesión o decide salir. Devuelve el registro CLIENTE logueado, o
    None si elige salir.
    """
    while True:
        print("\n--- PETMATCH ---")
        print("1) Iniciar sesión")
        print("2) Registrarme")
        print("3) Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            cliente_actual = autenticacion.iniciar_sesion()
            if cliente_actual is not None:
                return cliente_actual
        elif opcion == "2":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            usuario = input("Elegí un usuario: ")
            clave = input("Elegí una clave: ")
            nuevo = autenticacion.registrar_cliente(
                nombre, apellido, email, telefono, direccion, usuario, clave
            )
            print(f"¡Listo, {nuevo['nombre']}! Ya podés iniciar sesión.")
        elif opcion == "3":
            return None
        else:
            print("Opción inválida.")


# ------------------------------------------------------------------
# MENÚ DE MASCOTAS
# ------------------------------------------------------------------

def menu_mascotas(cliente_actual):
    while True:
        print("\n--- MIS MASCOTAS ---")
        print("1) Ver mis mascotas")
        print("2) Agregar mascota")
        print("3) Volver")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            mascotas = cliente.listar_mascotas_cliente(cliente_actual["id_cliente"])
            if not mascotas:
                print("Todavía no tenés mascotas registradas.")
            for m in mascotas:
                print(f"#{m['id_mascota']} - {m['nombre_mascota']} ({m['especie']}, {m['raza']})")
        elif opcion == "2":
            nombre_mascota = input("Nombre de la mascota: ")
            print(f"Especies válidas: {', '.join(datos.ESPECIES_VALIDAS)}")
            especie = input("Especie: ")
            if especie.strip().lower() == "perro":
                print(f"Algunas razas sugeridas: {', '.join(datos.RAZAS_PERRO_SUGERIDAS)}")
            raza = input("Raza: ")
            edad = pedir_entero("Edad: ")
            peso = pedir_numero("Peso (kg): ")
            notas = input("Notas especiales (opcional): ")
            cliente.alta_mascota(cliente_actual["id_cliente"], nombre_mascota, especie, raza, edad, peso, notas)
        elif opcion == "3":
            return
        else:
            print("Opción inválida.")


# ------------------------------------------------------------------
# MENÚ DE CATÁLOGO
# ------------------------------------------------------------------

def mostrar_producto(p):
    extra = f"Stock: {p['stock']}" if p["stock"] is not None else "Servicio"
    print(f"#{p['id_producto']} - {p['nombre_producto']} | ${p['precio']} | {p['categoria']} | {extra}")


def menu_catalogo():
    while True:
        print("\n--- CATÁLOGO ---")
        print("1) Ver todo el catálogo")
        print("2) Buscar por categoría")
        print("3) Buscar por especie")
        print("4) Volver")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            for p in catalogo.listar_productos():
                mostrar_producto(p)
        elif opcion == "2":
            print(f"Categorías válidas: {', '.join(datos.CATEGORIAS_VALIDAS)}")
            categoria = input("Categoría: ")
            for p in catalogo.buscar_por_categoria(categoria):
                mostrar_producto(p)
        elif opcion == "3":
            print(f"Especies válidas: {', '.join(datos.ESPECIES_VALIDAS)}")
            especie = input("Especie: ")
            for p in catalogo.buscar_por_especie(especie):
                mostrar_producto(p)
        elif opcion == "4":
            return
        else:
            print("Opción inválida.")


# ------------------------------------------------------------------
# MENÚ DE PEDIDOS (CARRITO)
# ------------------------------------------------------------------

def obtener_o_crear_pedido_activo(cliente_actual):
    """Devuelve el pedido 'Pendiente' del cliente, o crea uno nuevo si no tiene."""
    for p in pedido.listar_pedidos_cliente(cliente_actual["id_cliente"]):
        if p["estado"] == "Pendiente":
            return p
    return pedido.crear_pedido(cliente_actual["id_cliente"])


def menu_pedido(cliente_actual):
    pedido_activo = obtener_o_crear_pedido_activo(cliente_actual)

    while True:
        print(f"\n--- CARRITO (Pedido #{pedido_activo['id_pedido']}) ---")
        print("1) Ver items del carrito")
        print("2) Agregar producto/servicio")
        print("3) Confirmar pedido")
        print("4) Cancelar pedido")
        print("5) Ver historial de pedidos")
        print("6) Volver")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            items = pedido.listar_items_pedido(pedido_activo["id_pedido"])
            if not items:
                print("El carrito está vacío.")
            for item in items:
                producto = catalogo.buscar_producto_por_id(item["id_producto"])
                nombre = producto["nombre_producto"] if producto else "Producto eliminado"
                subtotal = item["cantidad"] * item["precio_unitario"]
                print(f"#{item['id_detalle']} - {nombre} x{item['cantidad']} = ${subtotal}")
            print(f"Total: ${pedido.calcular_total(pedido_activo['id_pedido'])}")
        elif opcion == "2":
            for p in catalogo.listar_productos():
                mostrar_producto(p)
            id_producto = pedir_entero("ID del producto/servicio: ")
            cantidad = pedir_entero("Cantidad: ")

            id_mascota = None
            mascotas = cliente.listar_mascotas_cliente(cliente_actual["id_cliente"])
            if mascotas:
                for m in mascotas:
                    print(f"#{m['id_mascota']} - {m['nombre_mascota']}")
                texto = input("¿Para qué mascota es? (Enter para omitir): ")
                if texto.strip():
                    id_mascota = int(texto)

            pedido.agregar_item_pedido(pedido_activo["id_pedido"], id_producto, cantidad, id_mascota)
        elif opcion == "3":
            print(f"Métodos de pago válidos: {', '.join(datos.METODOS_PAGO_VALIDOS)}")
            metodo_pago = input("Método de pago: ")
            if pedido.confirmar_pedido(pedido_activo["id_pedido"], metodo_pago):
                print(f"¡Pedido confirmado! Total: ${pedido_activo['total']} ({metodo_pago})")
                pedido_activo = obtener_o_crear_pedido_activo(cliente_actual)
            else:
                print("No se pudo confirmar el pedido (revisá el método de pago o si está vacío).")
        elif opcion == "4":
            if pedido.cancelar_pedido(pedido_activo["id_pedido"]):
                print("Pedido cancelado.")
                pedido_activo = obtener_o_crear_pedido_activo(cliente_actual)
            else:
                print("No se pudo cancelar el pedido.")
        elif opcion == "5":
            for p in pedido.listar_pedidos_cliente(cliente_actual["id_cliente"]):
                pago = p["metodo_pago"] if p["metodo_pago"] else "—"
                print(f"#{p['id_pedido']} - {p['estado']} - ${p['total']} - {p['fecha_pedido']} - Pago: {pago}")
        elif opcion == "6":
            return
        else:
            print("Opción inválida.")


# ------------------------------------------------------------------
# MENÚ PRINCIPAL Y ARRANQUE
# ------------------------------------------------------------------

def menu_principal(cliente_actual):
    while True:
        print(f"\n--- HOLA, {cliente_actual['nombre'].upper()} ---")
        print("1) Mis mascotas")
        print("2) Catálogo")
        print("3) Carrito y pedidos")
        print("4) Cerrar sesión")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            menu_mascotas(cliente_actual)
        elif opcion == "2":
            menu_catalogo()
        elif opcion == "3":
            menu_pedido(cliente_actual)
        elif opcion == "4":
            return
        else:
            print("Opción inválida.")


def main():
    while True:
        cliente_actual = menu_autenticacion()
        if cliente_actual is None:
            print("¡Hasta la próxima!")
            break
        menu_principal(cliente_actual)


if __name__ == "__main__":
    main()