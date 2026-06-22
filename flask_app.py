from flask import Flask, render_template, request, redirect, url_for, session, flash
import datos
import catalogo
import auth_sistema as autenticacion
import pedido
import cliente

app = Flask(__name__)
# MUY IMPORTANTE: Se necesita una clave secreta para poder usar sesiones en Flask
app.secret_key = 'petmatch_secret_key_123'


IMAGENES_PRODUCTOS = {
    "Alimento Royal Canin Perro Adulto (15kg)": "https://puppis.vtexassets.com/arquivos/ids/207121-1600-1600?v=639173174622530000&width=1600&height=1600&aspect=true",
    "Alimento Royal Canin Perro Cachorro (5kg)": "https://static.mispichos.com/mp_images/royal-canin-mini-puppy-mini-junior_18",
    "Alimento Purina Pro Plan Performance (20kg)": "https://vetdirect.purina.com.ar/cdn/shop/products/7613287031051_4_1200x1200.png?v=1634324495",
    "Alimento Hill's Science Diet Light (10kg)": "https://www.supermascotas.com.co/cdn/shop/files/ComidaParaPerroHillsSbAdultoLightRazasPequenasPollo5LB-1_49d68820-2820-4339-904f-2924784e0fc6.png?v=1757514379&width=840",
    "Alimento Eukanuba Adult Large Breed (15kg)": "https://www.eukanuba.com/arg/sites/g/files/fnmzdf6531/files/2025-04/ar-l-eukanuba-packshot-adult-large-breed.jpeg",
    "Alimento Pedigree Adulto Carne y Vegetales (20kg)": "https://animalworld.com.ar/wp-content/uploads/2024/02/Pedigree-Adultos-Carne-y-Vegetales.png",
    "Alimento Whiskas Gatitos Mix (10kg)": "https://www.whiskas.com.ar/cdn-cgi/image/format=auto,q=90/sites/g/files/fnmzdf4921/files/2022-12/7797453972277-product-image-1.png",
    "Alimento Whiskas Adulto Salmón (10kg)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-I8NH65s9mt4WwyOGbq5MGPnBHBfit1vFp9nuY-G1NofH6KbcWYB5MMOM&s=10",
    "Alimento Iams Proactive Health Gatos (10kg)": "https://www.iams.com.ar/cdn-cgi/image/format=auto,q=90/sites/g/files/fnmzdf2196/files/2022-12/IAMS-Healthy-Adult.png",
    "Alimento Mazuri Rodent Pellets (2kg)": "https://www.labodeguitaonline.cl/wp-content/uploads/2018/04/mazuri-rata.jpg",
    "Alimento Vitakraft Emotion Beauty (1kg)": "https://shop.vitakraft.com/media/catalog/product/cache/cb5cd77e61e5ef2e9e3f680271398f0d/0/4/04008239314642_C1L1_s04_2_3.png",
    "Alimento Kaytee Fiesta Gourmet (2.5kg)": "https://valuepetsglobal.com/uploads/products/8120-kaytee-fiesta-guinea-pig-625lb/main.png",
    "Capita de Abrigo Impermeable": "https://http2.mlstatic.com/D_956991-MLA112388812009_052026-O.webp",
    "Buzo Polar Mascotas": "https://http2.mlstatic.com/D_NQ_NP_906584-MLA75636192481_042024-O.webp",
    "Chaleco Temático Mini": "https://s.alicdn.com/@sc04/kf/Hb2fa9381441a433590749954d248f275K.jpg",
    "Collar Regulable de Nylon Premium": "https://acdn-us.mitiendanube.com/stores/680/557/products/b-14-6c9e6252ddeedd6ff317794767558010-480-0.webp",
    "Collar Reflectivo con Cascabel": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVZ6HDas7SOCk82GjEm9fa-eMaHVrw3ZpWj_V_T3t37w&s",
    "Hueso de Goma Maciza": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFW60m-IRbP2l7uKmx3fSivwgii35XD7qULdC89tvtnA&s=10",
    "Pelota de Tenis Reforzada (Pack x3)": "https://acdn-us.mitiendanube.com/stores/006/471/210/products/d_919402-mla43951869855_102020-b-59d314effdc02bf46917523642191622-1024-1024.webp",
    "Torre Rascador de 3 Niveles": "https://http2.mlstatic.com/D_NQ_NP_635554-MLA99451650170_112025-O.webp",
    "Ratón de Peluche con Catnip": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHRTr43dxZfikga37RaEZJ_8ERNit4Wb1PjfFg9VaXAlq9FVX6uOADWrw&s=10",
    "Rueda de Ejercicios Silenciosa": "https://i5.walmartimages.com/asr/b9ac63bd-bda3-4a7e-b5a1-946a1d02768e.11ff153444c3473fa8e925731865361c.jpeg?odnHeight=612&odnWidth=612&odnBg=FFFFFF",
    "Consulta Veterinaria General": "https://agendapro.com/mp/_next/image?url=https%3A%2F%2Fdcx13p9dsx90t.cloudfront.net%2Fuploads%2Fattachment_images%2F322731%2Fattachment_dea91ce165231db3.png&w=1920&q=75",
    "Plan de Vacunación Anual": "https://media.diariopopular.com.ar/p/55907caf0b870c3300288bd9c0fda445/adjuntos/143/imagenes/007/988/0007988720/1140x0/smart/vacunas-para-perrosjpg.jpg",
    "Baño y Peluquería Canina": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOJ5nEoXAVSJP2ZVsI4oymkw_9JWmHx5CsS--6efDZNw&s=10",
}



# --- DATOS DE PRUEBA ---
# --- DATOS DE PRUEBA AMPLIADOS PARA LA PRESENTACIÓN ---
if not datos.productos:
    # --- ALIMENTOS PERROS ---
    catalogo.alta_producto("Alimento Royal Canin Perro Adulto (15kg)", "Nutrición a medida para perros adultos de tamaño mediano.", "Producto", "Alimento", "Perro", False, 45000, 12)
    catalogo.alta_producto("Alimento Royal Canin Perro Cachorro (5kg)", "Crecimiento óptimo y refuerzo del sistema inmunológico.", "Producto", "Alimento", "Perro", False, 18500, 8)
    catalogo.alta_producto("Alimento Purina Pro Plan Performance (20kg)", "Alta concentración de proteínas para perros de alta actividad.", "Producto", "Alimento", "Perro", False, 52000, 10)
    catalogo.alta_producto("Alimento Hill's Science Diet Light (10kg)", "Control de peso para perros adultos propensos al sobrepeso.", "Producto", "Alimento", "Perro", False, 31000, 6)
    catalogo.alta_producto("Alimento Eukanuba Adult Large Breed (15kg)", "Cuidado articular para perros de razas grandes.", "Producto", "Alimento", "Perro", False, 43500, 15)
    catalogo.alta_producto("Alimento Pedigree Adulto Carne y Vegetales (20kg)", "Nutrición completa y balanceada para el día a día.", "Producto", "Alimento", "Perro", False, 28000, 20)

    # --- ALIMENTOS GATOS ---
    catalogo.alta_producto("Alimento Whiskas Gatitos Mix (10kg)", "Deliciosas croquetas rellenas con los nutrientes que necesitan.", "Producto", "Alimento", "Gato", False, 12500, 14)
    catalogo.alta_producto("Alimento Whiskas Adulto Salmón (10kg)", "Sabor irresistible que ayuda al control de bolas de pelo.", "Producto", "Alimento", "Gato", False, 22000, 11)
    catalogo.alta_producto("Alimento Iams Proactive Health Gatos (10kg)", "Proteína de pollo premium para mantener la masa muscular.", "Producto", "Alimento", "Gato", False, 29500, 7)

    # --- ALIMENTOS ROEDORES ---
    catalogo.alta_producto("Alimento Mazuri Rodent Pellets (2kg)", "Dieta de alta calidad ideal para hámsters, ratas y ratones.", "Producto", "Alimento", "Roedor", False, 6800, 25)
    catalogo.alta_producto("Alimento Vitakraft Emotion Beauty (1kg)", "Mezcla premium con ácidos grasos para un pelaje brillante.", "Producto", "Alimento", "Roedor", False, 4200, 18)
    catalogo.alta_producto("Alimento Kaytee Fiesta Gourmet (2.5kg)", "Variedad de semillas, frutas y vegetales para una dieta divertida.", "Producto", "Alimento", "Roedor", False, 7500, 15)

    # --- INDUMENTARIA Y ACCESORIOS (ROPA / COLLARES) ---
    catalogo.alta_producto("Capita de Abrigo Impermeable", "Capa térmica con interior de corderito para días fríos.", "Producto", "Accesorio", "Perro", True, 8500, 10)
    catalogo.alta_producto("Buzo Polar Mascotas", "Prenda súper suave y elástica para mantenerlos abrigados en casa.", "Producto", "Accesorio", "Gato", True, 6200, 12)
    catalogo.alta_producto("Chaleco Temático Mini", "Mini chaleco ajustable con diseños divertidos.", "Producto", "Accesorio", "Roedor", False, 3400, 5)
    catalogo.alta_producto("Collar Regulable de Nylon Premium", "Collar reforzado con hebilla de seguridad y argolla soldada.", "Producto", "Accesorio", "Perro", True, 4500, 30)
    catalogo.alta_producto("Collar Reflectivo con Cascabel", "Mayor visibilidad nocturna y broche antiahogo.", "Producto", "Accesorio", "Gato", False, 2800, 25)

    # --- JUGUETES ---
    catalogo.alta_producto("Hueso de Goma Maciza", "Juguete mordillo ideal para limpiar los dientes y descargar ansiedad.", "Producto", "Juguete", "Perro", False, 3800, 15)
    catalogo.alta_producto("Pelota de Tenis Reforzada (Pack x3)", "Pelotas de alta durabilidad sin compuestos nocivos.", "Producto", "Juguete", "Perro", False, 2900, 40)
    catalogo.alta_producto("Torre Rascador de 3 Niveles", "Centro de juegos con plataformas colgantes y postes de sisal.", "Producto", "Juguete", "Gato", False, 26000, 4)
    catalogo.alta_producto("Ratón de Peluche con Catnip", "Despierta el instinto cazador de tu felino.", "Producto", "Juguete", "Gato", False, 1500, 50)
    catalogo.alta_producto("Rueda de Ejercicios Silenciosa", "Rueda plástica con rodamientos suaves para evitar ruidos molestos.", "Producto", "Juguete", "Roedor", False, 5200, 10)

    # --- SALUD Y ESTÉTICA (SERVICIOS Y PRODUCTOS) ---
    catalogo.alta_producto("Consulta Veterinaria General", "Chequeo preventivo de salud y control de peso profesional.", "Servicio", "Salud", "Todas", False, 7000)
    catalogo.alta_producto("Plan de Vacunación Anual", "Colocación de vacunas quíntuple/sextuple y antirrábica.", "Servicio", "Salud", "Todas", False, 14000)
    catalogo.alta_producto("Baño y Peluquería Canina", "Corte higiénico, vaciado de glándulas, baño estético y perfume.", "Servicio", "Estetica", "Perro", True, 9500)

@app.route('/')
def index():
    productos = catalogo.listar_productos()
     # CLAVE : categorias=datos.CATEGORIAS_VALIDAS
    return render_template('index.html', productos=productos, categorias=datos.CATEGORIAS_VALIDAS, imagenes=IMAGENES_PRODUCTOS)

@app.route('/categoria/<nombre_cat>')
def por_categoria(nombre_cat):
    productos = catalogo.buscar_por_categoria(nombre_cat)
    print(session)
    return render_template('index.html', productos=productos, categorias=datos.CATEGORIAS_VALIDAS, imagenes=IMAGENES_PRODUCTOS)


# --- RESTRISTRO Y AUTENTICACIÓN ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Capturamos los datos del formulario HTML
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        usuario = request.form['usuario']
        clave = request.form['clave']
        # Llamamos a tu función nativa
        
        nuevo_cliente = autenticacion.registrar_cliente(nombre, apellido, email, telefono, direccion, usuario, clave)
        session['id_cliente'] = nuevo_cliente['id_cliente']
        return redirect(url_for('login'))
        
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        # Validamos con tu función
        user_validado = autenticacion.validar_credenciales(usuario, clave)
        session['id_cliente'] = user_validado['id_cliente']
        if user_validado:
            session['id_cliente'] = user_validado['id_cliente']
            session['nombre_cliente'] = user_validado['nombre']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Usuario o clave incorrectos.")
       
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- COMPRAS Y CARRITO ---

@app.route('/agregar_al_carrito/<int:id_producto>', methods=['POST'])
def agregar_al_carrito(id_producto):
    print(f"\n--- 🛒 INTENTANDO AGREGAR PRODUCTO {id_producto} ---")
    
    if 'id_cliente' not in session:
        print("❌ FALLO: No hay 'id_cliente' en sesión. Redirigiendo a login.")
        return redirect(url_for('login'))
        
    id_cliente = session['id_cliente']
    print(f"✅ Usuario logueado con ID: {id_cliente}")
    
    cantidad = int(request.form.get('cantidad', 1))
    
    # 1. Buscamos pedido pendiente
    pedido_actual = None
    for p in datos.pedidos:
        if p['id_cliente'] == id_cliente and p['estado'] == 'Pendiente':
            pedido_actual = p
            break
            
    if pedido_actual is None:
        print("✅ No había pedido pendiente. Creando uno nuevo...")
        pedido_actual = pedido.crear_pedido(id_cliente)
    else:
        print(f"✅ Pedido pendiente encontrado: ID {pedido_actual['id_pedido']}")
        
    # 2. Intentamos agregar el ítem
    print(f"⏳ Ejecutando pedido.agregar_item_pedido({pedido_actual['id_pedido']}, {id_producto}, {cantidad})...")
    resultado = pedido.agregar_item_pedido(pedido_actual['id_pedido'], id_producto, cantidad)
    
    print(f"👉 Resultado de la función interna: {resultado}")
    
    # 3. Verificamos la "Base de Datos" (Memoria)
    # ¡OJO! Si tu lista se llama distinto en datos.py (ej: detalles_pedido en vez de detalle_pedido), 
    # Python te dará error en la siguiente línea. Si es así, corrigelo.
    if hasattr(datos, 'detalle_pedido'):
        print(f"📦 Estado de datos.detalle_pedido: {datos.detalle_pedido}")
    else:
        print("⚠️ ALERTA CRÍTICA: No existe 'datos.detalle_pedido'. Revisa el nombre de la lista en datos.py")
        
    print("--- FIN DEL INTENTO ---\n")
    return redirect(url_for('carrito'))


@app.route('/carrito')
def carrito():
    print("\n--- 🔍 LEYENDO EL CARRITO DESDE EL NAVEGADOR ---")
    if 'id_cliente' not in session:
        print("❌ LECTURA FALLIDA: No hay 'id_cliente' en la sesión.")
        return redirect(url_for('login'))
        
    id_cliente = session['id_cliente']
    print(f"👤 Cliente en sesión para la lectura: {id_cliente} (Tipo: {type(id_cliente)})")
    print(f"📋 Contenido total de datos.pedidos: {datos.pedidos}")
    print(f"📦 Contenido total de datos.detalle_pedido: {datos.detalle_pedido}")
    
    # 1. Buscamos el pedido del cliente
    pedido_actual = None
    for p in datos.pedidos:
        if p['id_cliente'] == id_cliente and p['estado'] == 'Pendiente':
            pedido_actual = p
            break
            
    print(f"👉 Pedido pendiente filtrado: {pedido_actual}")
            
    items_visibles = []
    
    if pedido_actual:
        pedido.calcular_total(pedido_actual['id_pedido'])
        lista_detalles = datos.detalle_pedido
        
        for d in lista_detalles:
            if d['id_pedido'] == pedido_actual['id_pedido']:
                prod = catalogo.buscar_producto_por_id(d['id_producto'])
                if prod:
                    items_visibles.append({
                        'nombre': prod['nombre_producto'],
                        'cantidad': d['cantidad'],
                        'subtotal': d['cantidad'] * d['precio_unitario']
                    })
                else:
                    print(f"⚠️ ALERTA: Producto ID {d['id_producto']} no se encontró en el catálogo.")
                    
    print(f"🛒 Items finales procesados para el HTML: {items_visibles}")
    print("--- FIN DE LA LECTURA ---\n")
                
    return render_template('carrito.html', pedido=pedido_actual, items=items_visibles, metodos=datos.METODOS_PAGO_VALIDOS)

@app.route('/confirmar_pedido/<int:id_pedido>', methods=['POST'])
def confirmar_pedido(id_pedido):
    if 'id_cliente' not in session:
        return redirect(url_for('login'))
        
    metodo_pago = request.form['metodo_pago']
    exito = pedido.confirmar_pedido(id_pedido, metodo_pago)
    
    if exito:
        # REDIRECCIÓN REAL: Enviamos al usuario a una nueva URL limpia de tipo GET
        return redirect(url_for('compra_exitosa', id_pedido=id_pedido))
    
    flash("No se pudo procesar la confirmación del pedido.")
    return redirect(url_for('carrito'))


@app.route('/compra-exitosa/<int:id_pedido>')
def compra_exitosa(id_pedido):
    if 'id_cliente' not in session:
        return redirect(url_for('login'))
        
    id_cliente = session['id_cliente']
    
    # Buscamos el pedido específico que se acaba de confirmar
    pedido_confirmado = None
    for p in datos.pedidos:
        # Validamos que el pedido pertenezca al cliente logueado por seguridad
        if p['id_pedido'] == id_pedido and p['id_cliente'] == id_cliente:
            pedido_confirmado = p
            break
            
    if not pedido_confirmado:
        # Si no existe o no es de este cliente, lo mandamos al inicio
        return redirect(url_for('index'))
        
    # Reconstruimos los items de ESTE pedido específico para mostrarlos en el resumen/recibo
    items_comprados = []
    for d in datos.detalle_pedido:
        if d['id_pedido'] == id_pedido:
            prod = catalogo.buscar_producto_por_id(d['id_producto'])
            if prod:
                items_comprados.append({
                    'nombre': prod['nombre_producto'],
                    'cantidad': d['cantidad'],
                    'subtotal': d['cantidad'] * d['precio_unitario']
                })
                
    # Renderizamos la plantilla de confirmación pasándole los datos históricos del pedido
    return render_template('conf_pedido.html', pedido=pedido_confirmado, items=items_comprados)
if __name__ == '__main__':
    app.run(debug=True)