"""
pedido.py
---------
Módulo de pedidos de PetMatch.

Opera sobre los registros PEDIDO y DETALLE_PEDIDO definidos en
datos.py. Un pedido nace en estado "Pendiente" y funciona como
carrito: se le pueden agregar o quitar items. Al confirmarlo se
descuenta el stock real del catálogo.
"""

import datetime
import datos
import catalogo


# ------------------------------------------------------------------
# CREACIÓN Y CONSULTA DE PEDIDOS
# ------------------------------------------------------------------

def crear_pedido(id_cliente):
    """
    Crea un nuevo registro PEDIDO en estado 'Pendiente' (actúa como
    carrito) y lo agrega a datos.pedidos. Devuelve el diccionario
    creado.
    """
    nuevo_pedido = {
        "id_pedido": datos.generar_id_pedido(),
        "id_cliente": id_cliente,
        "fecha_pedido": datetime.date.today().isoformat(),
        "estado": "Pendiente",
        "total": 0.0,
        "metodo_pago": None,
    }
    datos.pedidos.append(nuevo_pedido)
    return nuevo_pedido


def buscar_pedido_por_id(id_pedido):
    """Devuelve el registro PEDIDO con ese id, o None si no existe."""
    for pedido in datos.pedidos:
        if pedido["id_pedido"] == id_pedido:
            return pedido
    return None


def listar_pedidos_cliente(id_cliente):
    """Devuelve el historial de pedidos (todos los estados) de un cliente."""
    return [p for p in datos.pedidos if p["id_cliente"] == id_cliente]


# ------------------------------------------------------------------
# ITEMS DEL PEDIDO (DETALLE_PEDIDO)
# ------------------------------------------------------------------

def agregar_item_pedido(id_pedido, id_producto, cantidad, id_mascota=None):
    """
    Agrega un producto/servicio al pedido (debe estar 'Pendiente').
    Valida existencia del producto y stock disponible. id_mascota es
    opcional, por si el item no es para una mascota en particular.
    Devuelve el registro DETALLE_PEDIDO creado, o None si algo falló.
    """
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None or pedido["estado"] != "Pendiente":
        print("El pedido no existe o ya no admite cambios.")
        return None

    producto = catalogo.buscar_producto_por_id(id_producto)
    if producto is None or not producto["estado"]:
        print("El producto/servicio no existe o está inactivo.")
        return None

    if producto["stock"] is not None and producto["stock"] < cantidad:
        print(f"Stock insuficiente. Disponible: {producto['stock']}.")
        return None

    nuevo_detalle = {
        "id_detalle": datos.generar_id_detalle(),
        "id_pedido": id_pedido,
        "id_producto": id_producto,
        "id_mascota": id_mascota,
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
    }
    datos.detalle_pedido.append(nuevo_detalle)
    calcular_total(id_pedido)
    return nuevo_detalle


def quitar_item_pedido(id_detalle):
    """
    Quita un ítem del pedido (solo si el pedido sigue 'Pendiente').
    Devuelve True si se quitó, False en caso contrario.
    """
    for detalle in datos.detalle_pedido:
        if detalle["id_detalle"] == id_detalle:
            pedido = buscar_pedido_por_id(detalle["id_pedido"])
            if pedido is None or pedido["estado"] != "Pendiente":
                return False
            datos.detalle_pedido.remove(detalle)
            calcular_total(detalle["id_pedido"])
            return True
    return False


def listar_items_pedido(id_pedido):
    """Devuelve la lista de registros DETALLE_PEDIDO de un pedido dado."""
    return [d for d in datos.detalle_pedido if d["id_pedido"] == id_pedido]


# ------------------------------------------------------------------
# TOTALES Y CONFIRMACIÓN
# ------------------------------------------------------------------

def calcular_total(id_pedido):
    """Recalcula y guarda el total del pedido en base a sus items."""
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None:
        return 0.0

    total = sum(d["cantidad"] * d["precio_unitario"] for d in listar_items_pedido(id_pedido))
    pedido["total"] = total
    return total


def confirmar_pedido(id_pedido, metodo_pago):
    """
    Confirma el pedido: valida el método de pago, descuenta stock real
    de cada producto y pasa el estado a 'Confirmado'. Devuelve True si
    se confirmó, False si el pedido no existe, ya fue procesado, no
    tiene items o el método de pago no es válido.
    """
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None or pedido["estado"] != "Pendiente":
        return False

    if metodo_pago not in datos.METODOS_PAGO_VALIDOS:
        print(f"Método de pago inválido. Opciones: {', '.join(datos.METODOS_PAGO_VALIDOS)}")
        return False

    items = listar_items_pedido(id_pedido)
    if not items:
        print("El pedido no tiene items.")
        return False

    for item in items:
        catalogo.actualizar_stock(item["id_producto"], -item["cantidad"])

    pedido["metodo_pago"] = metodo_pago
    pedido["estado"] = "Confirmado"
    calcular_total(id_pedido)
    return True


def cancelar_pedido(id_pedido):
    """
    Cancela un pedido. Si ya estaba 'Confirmado', restituye el stock
    descontado. Devuelve True si se canceló, False si no corresponde
    (por ejemplo, si ya fue entregado).
    """
    pedido = buscar_pedido_por_id(id_pedido)
    if pedido is None or pedido["estado"] in ("Entregado", "Cancelado"):
        return False

    if pedido["estado"] == "Confirmado":
        for item in listar_items_pedido(id_pedido):
            catalogo.actualizar_stock(item["id_producto"], item["cantidad"])

    pedido["estado"] = "Cancelado"
    return True