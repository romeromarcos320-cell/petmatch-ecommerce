"""
catalogo.py
-----------
Módulo de catálogo de PetMatch.

Opera sobre el registro PRODUCTO definido en datos.py (que también
representa servicios): alta, búsqueda, modificación y control de
stock de los productos y servicios ofrecidos.
"""

import datetime
import datos


def alta_producto(nombre_producto, descripcion, tipo, categoria, especie_mascota, personalizable, precio, stock=None):
    """
    Crea un nuevo registro PRODUCTO (o servicio) y lo agrega a
    datos.productos. Devuelve el diccionario creado, o None si algún
    dato no es válido.
    """
    if tipo not in ("Producto", "Servicio"):
        print("Tipo inválido. Debe ser 'Producto' o 'Servicio'.")
        return None

    if categoria not in datos.CATEGORIAS_VALIDAS:
        print(f"Categoría inválida. Opciones: {', '.join(datos.CATEGORIAS_VALIDAS)}")
        return None

    if especie_mascota not in datos.ESPECIES_VALIDAS and especie_mascota != "Todas":
        print(f"Especie inválida. Opciones: {', '.join(datos.ESPECIES_VALIDAS)} o 'Todas'.")
        return None

    if tipo == "Servicio":
        stock = None  # los servicios no manejan stock

    nuevo_producto = {
        "id_producto": datos.generar_id_producto(),
        "nombre_producto": nombre_producto,
        "descripcion": descripcion,
        "tipo": tipo,
        "categoria": categoria,
        "especie_mascota": especie_mascota,
        "personalizable": personalizable,
        "precio": precio,
        "stock": stock,
        "fecha_alta": datetime.date.today().isoformat(),
        "estado": True,
    }
    datos.productos.append(nuevo_producto)
    return nuevo_producto


def listar_productos(solo_activos=True):
    """Devuelve la lista de productos/servicios, filtrando por activos si corresponde."""
    if solo_activos:
        return [p for p in datos.productos if p["estado"]]
    return list(datos.productos)


def buscar_producto_por_id(id_producto):
    """Devuelve el registro PRODUCTO con ese id, o None si no existe."""
    for producto in datos.productos:
        if producto["id_producto"] == id_producto:
            return producto
    return None


def buscar_por_categoria(categoria):
    """Devuelve los productos/servicios activos de una categoría dada."""
    return [p for p in listar_productos() if p["categoria"] == categoria]


def buscar_por_especie(especie):
    """Devuelve los productos/servicios activos para una especie (o los de 'Todas')."""
    return [p for p in listar_productos() if p["especie_mascota"] in (especie, "Todas")]


def modificar_producto(id_producto, **campos_nuevos):
    """
    Actualiza los campos indicados del registro PRODUCTO con ese id.
    No permite modificar id_producto (clave). Devuelve True si se
    actualizó, False si el producto no existe.
    """
    producto = buscar_producto_por_id(id_producto)
    if producto is None:
        return False

    for campo, valor in campos_nuevos.items():
        if campo in producto and campo != "id_producto":
            producto[campo] = valor
    return True


def dar_baja_producto(id_producto):
    """
    Da de baja lógica un producto/servicio (estado=False) en vez de
    eliminarlo, para no perder la referencia en pedidos ya realizados.
    Devuelve True si se dio de baja, False si no existe.
    """
    return modificar_producto(id_producto, estado=False)


def actualizar_stock(id_producto, cantidad):
    """
    Suma 'cantidad' al stock del producto (usar un valor negativo para
    descontar, por ejemplo al confirmar un pedido). No aplica a
    servicios, cuyo stock es None. Devuelve True si se pudo actualizar.
    """
    producto = buscar_producto_por_id(id_producto)
    if producto is None or producto["stock"] is None:
        return False
    producto["stock"] += cantidad
    return True