"""
cliente.py
----------
Módulo de gestión de clientes y mascotas en PetMatch.

Opera sobre los registros CLIENTE y MASCOTA definidos en datos.py:
permite dar de alta, modificar y eliminar mascotas, así como editar
los datos de perfil de un cliente ya registrado. El alta de cliente
y la validación de usuario/clave viven en autenticacion.py.
"""

import datos


# ------------------------------------------------------------------
# GESTIÓN DE MASCOTAS
# ------------------------------------------------------------------

def alta_mascota(id_cliente, nombre_mascota, especie, raza, edad, peso, notas_especiales=""):
    """
    Crea un nuevo registro MASCOTA vinculado a un cliente existente
    (id_cliente como FK). Devuelve el diccionario de la mascota creada,
    o None si la especie indicada no es válida.
    """
    if especie not in datos.ESPECIES_VALIDAS:
        print(f"Especie inválida. Opciones: {', '.join(datos.ESPECIES_VALIDAS)}")
        return None

    nueva_mascota = {
        "id_mascota": datos.generar_id_mascota(),
        "id_cliente": id_cliente,
        "nombre_mascota": nombre_mascota,
        "especie": especie,
        "raza": raza,
        "edad": edad,
        "peso": peso,
        "notas_especiales": notas_especiales,
    }
    datos.mascotas.append(nueva_mascota)
    return nueva_mascota


def listar_mascotas_cliente(id_cliente):
    """Devuelve la lista de registros MASCOTA cuyo id_cliente (FK) coincide."""
    return [m for m in datos.mascotas if m["id_cliente"] == id_cliente]


def buscar_mascota_por_id(id_mascota):
    """Devuelve el registro MASCOTA con ese id, o None si no existe."""
    for mascota in datos.mascotas:
        if mascota["id_mascota"] == id_mascota:
            return mascota
    return None


def modificar_mascota(id_mascota, **campos_nuevos):
    """
    Actualiza los campos indicados (ej: raza="Labrador", peso=12.5) del
    registro MASCOTA con ese id. No permite modificar id_mascota ni
    id_cliente (claves). Devuelve True si se actualizó, False si la
    mascota no existe.
    """
    mascota = buscar_mascota_por_id(id_mascota)
    if mascota is None:
        return False

    for campo, valor in campos_nuevos.items():
        if campo in mascota and campo not in ("id_mascota", "id_cliente"):
            mascota[campo] = valor
    return True


def eliminar_mascota(id_mascota):
    """Elimina el registro MASCOTA con ese id. Devuelve True si se eliminó."""
    mascota = buscar_mascota_por_id(id_mascota)
    if mascota is None:
        return False
    datos.mascotas.remove(mascota)
    return True


# ------------------------------------------------------------------
# GESTIÓN DE PERFIL DE CLIENTE
# ------------------------------------------------------------------

def modificar_datos_cliente(id_cliente, **campos_nuevos):
    """
    Actualiza datos de perfil del cliente (nombre, apellido, email,
    telefono, direccion). El usuario y la clave NO se modifican acá;
    eso es responsabilidad de autenticacion.py.
    Devuelve True si se actualizó, False si el cliente no existe.
    """
    campos_permitidos = {"nombre", "apellido", "email", "telefono", "direccion"}

    for cliente in datos.clientes:
        if cliente["id_cliente"] == id_cliente:
            for campo, valor in campos_nuevos.items():
                if campo in campos_permitidos:
                    cliente[campo] = valor
            return True
    return False