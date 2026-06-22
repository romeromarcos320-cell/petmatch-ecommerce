# 🐾 PetMatch - E-Commerce para Mascotas

**PetMatch** Es una plataforma web orientada a la venta de productos, accesorios y servicios para todo tipo de mascotas. El sistema permite la navegación por un catálogo categorizado, la gestión de un carrito de compras interactivo y el registro seguro de clientes.

###  Enlaces del Proyecto
* **Aplicación Web:** [Ingresar a PetMatch](https://mromero.pythonanywhere.com/)
* **Explicacion de la logica de registro:** Esta documentacion fue creada enteramente por la IA no se le pidio en ningun momento pero es interesante asi que lo adjunto tambien.
* **Repositorio GitHub:** 

---

##  Estructura de Datos (Unidad 2)

A continuación se presenta el diagrama de relaciones entre registros correspondientes al diseño planteado para la aplicacion.
![Diagrama de Estructura de Datos](Diagrama_Ecommerce.png)

Para gestionar la información de los usuarios del e-commerce, se definió la siguiente estructura de datos principal.

### Diseño del Registro Principal: `CLIENTE`
El sistema utiliza un registro compuesto por los siguientes campos para modelar la entidad del usuario:

| Campo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| **id_cliente** | Entero (`int`) | **[CLAVE PRIMARIA]** Identificador único autogenerado. |
| **nombre** | Cadena (`str`) | Nombre de pila del cliente. |
| **apellido** | Cadena (`str`) | Apellido del cliente. |
| **email** | Cadena (`str`) | Correo electrónico de contacto. |
| **telefono** | Cadena (`str`) | Número telefónico de contacto. |
| **direccion** | Cadena (`str`) | Dirección física para envíos. |
| **usuario** | Cadena (`str`) | Nombre de usuario para el login. |
| **clave** | Cadena (`str`) | Contraseña de acceso al sistema. |
| **fecha_registro**| Cadena (`str`) | Fecha en formato ISO (AAAA-MM-DD). |

### Identificación y Justificación de la Clave
Se seleccionó el campo **`id_cliente`** como la clave principal (Primary Key) del registro. 

**Justificación técnica:** Se optó por un campo autonumérico e interno en lugar de utilizar datos naturales (como el `email` o el `usuario`). Esta decisión garantiza que, si el usuario necesita actualizar su correo electrónico o su dirección en el futuro, el identificador único no se ve alterado. Esto permite mantener la integridad referencial intacta cuando el `id_cliente` se vincula como clave foránea en la estructura de los `PEDIDOS` y las `MASCOTAS`.

### Ejemplo de intercomunicacion con el Registro "CLIENTE" y "PEDIDO":
Se detalla la estructura que gestiona los carritos de compra:

Clave Primaria (Primary Key): Se seleccionó el campo `id_pedido` como identificador de este registro, asegurando que cada transacción en el e-commerce sea irrepetible.

Clave Foránea (Foreign Key): Para vincular la compra con su dueño, el registro incorpora el campo `id_cliente`. Esta relación entre registros es la que le permite al sistema (a través de la lógica de Python) saber a quién pertenece cada carrito, procesar los ítems y actualizar el stock del catálogo.
---

##  Desarrollo Asistido por Inteligencia Artificial

### Prompts Utilizados
*(Añadir aquí capturas de pantalla de los prompts o transcribir los más importantes)*
* **Prompt 1:** "Tengo la lógica de un e-commerce en Python, ¿cómo conecto esto a una interfaz HTML usando Flask?"
* **Prompt 2:** "Necesito diseñar una paleta de colores cálida y hogareña para el frontend utilizando CSS."
* **Prompt 3:** "Cómo estructurar la vista del carrito de compras leyendo datos de listas en memoria desde Flask."

### Reflexión sobre el uso de la IA
El uso de la Inteligencia Artificial fue fundamental como un "copiloto" técnico durante la integración del backend con el frontend. Si bien la lógica central, los módulos y los registros fueron definidos manualmente aplicando los conceptos de la cátedra, la IA agilizó drásticamente la integracion de los conceptos en un codigo funcional, el proceso de maquetado en HTML/CSS y la configuración de las rutas y sesiones con el framework Flask. Esto me permitió enfocarme en la integracion de las unidades trabajadas en la materia, dejando las tareas repetitivas de sintaxis y diseño a la herramienta, resultando en un prototipo mucho más completo y estético.