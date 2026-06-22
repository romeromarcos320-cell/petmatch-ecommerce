"""
autenticacion.py
-----------------
Módulo de autenticación de PetMatch.

Opera sobre el registro CLIENTE definido en datos.py: permite dar de
alta nuevos clientes y validar el inicio de sesión (usuario y clave)
contra los registros ya guardados.
"""

import datetime
import datos


def registrar_cliente(nombre, apellido, email, telefono, direccion, usuario, clave):
    """
    Crea un nuevo registro CLIENTE y lo agrega a datos.clientes.
    Devuelve el diccionario del cliente creado.
    """
    nuevo_cliente = {
        "id_cliente": datos.generar_id_cliente(),
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
        "usuario": usuario,
        "clave": clave,
        "fecha_registro": datetime.date.today().isoformat(),
    }
    datos.clientes.append(nuevo_cliente)
    return nuevo_cliente


def buscar_cliente_por_usuario(usuario):
    """Devuelve el registro CLIENTE cuyo campo 'usuario' coincide, o None si no existe."""
    for cliente in datos.clientes:
        if cliente["usuario"] == usuario:
            return cliente
    return None


def validar_credenciales(usuario, clave):
    """Devuelve el registro CLIENTE si usuario y clave coinciden, o None en caso contrario."""
    cliente = buscar_cliente_por_usuario(usuario)
    if cliente is not None and cliente["clave"] == clave:
        return cliente
    return None


def iniciar_sesion():
    """
    Solicita usuario y clave por consola, hasta datos.MAX_INTENTOS_LOGIN veces.
    Devuelve el registro CLIENTE si el login es exitoso, o None si se
    agotan los intentos.
    """
    intentos = 0
    while intentos < datos.MAX_INTENTOS_LOGIN:
        usuario = input("Usuario: ")
        clave = input("Clave: ")
        cliente = validar_credenciales(usuario, clave)

        if cliente is not None:
            print(f"¡Bienvenido/a, {cliente['nombre']}!")
            return cliente

        intentos += 1
        intentos_restantes = datos.MAX_INTENTOS_LOGIN - intentos
        if intentos_restantes > 0:
            print(f"Usuario o clave incorrectos. Intentos restantes: {intentos_restantes}")
        else:
            print("Se agotaron los intentos. Acceso denegado.")

    return None