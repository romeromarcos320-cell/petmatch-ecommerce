"""
datos.py
--------
Módulo de datos de PetMatch.

Equivalencia con pseudocódigo:
- Cada REGISTRO ... FIN REGISTRO se modela aquí como un diccionario Python
  (un conjunto de campos de distinto tipo agrupados bajo un mismo nombre).
- Cada "tabla" de registros (el AMBIENTE persistente del programa) se modela
  como una lista de diccionarios.
- Las funciones generar_id_* cumplen el rol de los contadores autonuméricos
  que generan la clave primaria (PK) de cada nuevo registro.
"""

# ------------------------------------------------------------------
# CONSTANTES DEL SISTEMA
# ------------------------------------------------------------------

ESPECIES_VALIDAS = ["Perro", "Gato", "Ave", "Roedor", "Otro"]

CATEGORIAS_VALIDAS = ["Alimento", "Juguete", "Accesorio", "Salud", "Estetica", "Servicio"]

ESTADOS_PEDIDO = ["Pendiente", "Confirmado", "Enviado", "Entregado", "Cancelado"]

STOCK_MÍNIMO = 0

MAX_INTENTOS_LOGIN = 3

METODOS_PAGO_VALIDOS = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia", "Mercado Pago"]

# Lista de razas sugeridas para mascotas tipo "Perro", a modo de concepto
# de personalización. No se valida estrictamente: el campo "raza" del
# registro MASCOTA sigue aceptando cualquier texto.
RAZAS_PERRO_SUGERIDAS = ["Labrador", "Bulldog Francés", "Caniche", "Pastor Alemán", "Chihuahua", "Otro"]

METODOS_PAGO_VALIDOS = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia", "Mercado Pago"]

# Lista sugerida, no obligatoria: idea de "tienda personalizada" para mostrar
# opciones al dar de alta una mascota de especie "Perro". No se valida contra
# esta lista, queda como concepto a futuro.
RAZAS_PERRO_SUGERIDAS = ["Labrador", "Caniche", "Bulldog Francés", "Golden Retriever", "Chihuahua", "Salchicha", "Mestizo"]


# ------------------------------------------------------------------
# CONTADORES PARA CLAVES PRIMARIAS AUTONUMÉRICAS
# ------------------------------------------------------------------

_contador_id_cliente = 0
_contador_id_mascota = 0
_contador_id_producto = 0
_contador_id_pedido = 0
_contador_id_detalle = 0


def generar_id_cliente():
    """Genera y devuelve el siguiente id_cliente disponible (PK)."""
    global _contador_id_cliente
    _contador_id_cliente += 1
    return _contador_id_cliente


def generar_id_mascota():
    """Genera y devuelve el siguiente id_mascota disponible (PK)."""
    global _contador_id_mascota
    _contador_id_mascota += 1
    return _contador_id_mascota


def generar_id_producto():
    """Genera y devuelve el siguiente id_producto disponible (PK)."""
    global _contador_id_producto
    _contador_id_producto += 1
    return _contador_id_producto


def generar_id_pedido():
    """Genera y devuelve el siguiente id_pedido disponible (PK)."""
    global _contador_id_pedido
    _contador_id_pedido += 1
    return _contador_id_pedido


def generar_id_detalle():
    """Genera y devuelve el siguiente id_detalle disponible (PK)."""
    global _contador_id_detalle
    _contador_id_detalle += 1
    return _contador_id_detalle


# ------------------------------------------------------------------
# "BASES DE DATOS" SIMULADAS (listas de registros tipo diccionario)
# ------------------------------------------------------------------

# Registro CLIENTE:
#   id_cliente (PK, int) | nombre (str) | apellido (str) | email (str)
#   telefono (str) | direccion (str) | usuario (str) | clave (str)
#   fecha_registro (str, formato AAAA-MM-DD)
clientes = []

# Registro MASCOTA:
#   id_mascota (PK, int) | id_cliente (FK, int) | nombre_mascota (str)
#   especie (str) | raza (str) | edad (int) | peso (float)
#   notas_especiales (str)
mascotas = []

# Registro PRODUCTO (incluye también servicios):
#   id_producto (PK, int) | nombre_producto (str) | descripcion (str)
#   tipo (str: "Producto" / "Servicio") | categoria (str)
#   especie_mascota (str) | personalizable (bool) | precio (float)
#   stock (int o None si tipo == "Servicio") | fecha_alta (str)
#   estado (bool: True = activo)
productos = []

# Registro PEDIDO:
#   id_pedido (PK, int) | id_cliente (FK, int) | fecha_pedido (str)
#   estado (str) | total (float) | metodo_pago (str o None hasta confirmar)
pedidos = []

# Registro DETALLE_PEDIDO:
#   id_detalle (PK, int) | id_pedido (FK, int) | id_producto (FK, int)
#   id_mascota (FK, int) | cantidad (int) | precio_unitario (float)
detalle_pedido = []