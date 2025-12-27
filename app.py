import streamlit as st
import datetime

# ==========================================
# 1. CONFIGURACIÓN Y ESTÉTICA
# ==========================================
st.set_page_config(
    page_title="Kreación Kerkus | Laboratorio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carga del Logo con manejo de errores silencioso
try:
    st.image("logo_kerkus.jpg", width=180)
except:
    st.markdown("<h1>🌿 Kerkus Magikus</h1>", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS DE CONOCIMIENTO
# ==========================================
DICCIONARIO = {
    "SCI": "Tensioactivo aniónico derivado del coco. pH 5-7. Limpia y espuma.",
    "Manteca de Karité": "Nutrición profunda, regenerador. Ideal pieles secas.",
    "Aceite de Almendras": "Emoliente, calma picores y suaviza.",
    "Polvo de Arroz": "Suavidad, toque seco y efecto seda.",
    "Proteína de Seda": "Aporta brillo, soltura y manejabilidad.",
    "Glicerina": "Humectante (retiene agua en la piel/pelo).",
    "Arcilla Blanca": "Caolín. Purificante suave, regula sebo sin irritar.",
    "Vitamina E": "Tocoferol. Antioxidante (evita enranciamiento).",
    "Flores de Caléndula": "Calmante y antiinflamatorio.",
    "Ácido Láctico": "Corrector de pH (Baja el pH / Acidifica).",
    "Bicarbonato": "Corrector de pH (Sube el pH / Alcaliniza)."
}

# ==========================================
# 3. RECETARIO MAESTRO (Tratamientos y Fórmulas)
# ==========================================
RECETAS = {
    "Champú Nutritivo (Pelo Seco)": {
        "minimo_stock": 4, 
        "conservacion": "Lugar fresco y seco.",
        "ingredientes": {
            "SCI": 44.0, 
            "Oleato de Almendras": 10.0, 
            "Manteca de Karité": 5.0, 
            "Polvo de Plantas": 8.0, 
            "Agua/Hidrolato": 3.0
        },
        "instrucciones": """
        1. **Fase Polvo:** Pesa y mezcla el SCI con el polvo de plantas (Usa mascarilla).
        2. **Fase Fusión:** Al baño maría, funde el Karité junto con el Oleato.
        3. **Unión:** Vierte la fase grasa sobre los polvos y amasa bien.
        4. **Fase Acuosa:** Añade el agua poco a poco hasta lograr consistencia.
        5. **Enmoldado:** Prensa en moldes de 70g.
        """
    },
    "Champú Nube de Arroz": {
        "minimo_stock": 4, 
        "conservacion": "Lugar fresco y seco.",
        "ingredientes": {
            "SCI": 45.0, 
            "Polvo de Arroz": 15.0, 
            "Aceite de Coco": 7.0, 
            "Proteína de Seda": 3.0
        },
        "instrucciones": """
        1. **Preparación:** Tamiza el polvo de arroz (muy fino).
        2. **Mezcla:** Une el SCI con el arroz.
        3. **Aglutinante:** Añade el aceite de coco fundido y la proteína.
        4. **Forma:** Amasa hasta textura de 'arena mojada' y prensa fuerte.
        """
    },
    "Acondicionador Sólido": {
        "minimo_stock": 4, 
        "conservacion": "❄️ RECOMENDADO: Nevera en verano (se derrite fácil).",
        "ingredientes": {
            "BTMS (Cera)": 30.0, 
            "Manteca de Cacao": 20.0, 
            "Aceite de Argán": 10.0
        },
        "instrucciones": """
        1. **Fusión:** Funde todo junto al baño maría suave.
        2. **Enmoldado:** Trabaja rápido, solidifica enseguida al enfriar.
        """
    },
    "Bálsamo Labial (Cacao)": {
        "minimo_stock": 10, 
        "conservacion": "Evitar sol directo.",
        "ingredientes": {
            "Cera de Abejas": 2.0, 
            "Manteca de Cacao": 2.0, 
            "Oleato de Caléndula": 4.0
        },
        "instrucciones": """
        1. Fundir cera y manteca.
        2. Añadir oleato fuera del fuego (para no quemarlo).
        3. Envasar en tubos o latas antes de que enfríe.
        """
    }
}

# ==========================================
# 4. GESTIÓN DEL ESTADO (MEMORIA TEMPORAL)
# ==========================================
# Inicializamos las variables si no existen
if 'stock_mp' not in st.session_state:
    st.session_state.stock_mp = {
        "SCI": 2000.0, "Oleato de Almendras": 500.0, "Oleato de Caléndula": 300.0,
        "Polvo de Arroz": 200.0, "Manteca de Karité": 300.0, "Aceite de Coco": 400.0, 
        "Proteína de Seda": 50.0, "Polvo de Plantas": 150.0, "Agua/Hidrolato": 1000.0,
        "BTMS (Cera)": 500.0, "Manteca de Cacao": 500.0, "Aceite de Argán": 200.0, "Cera de Abejas": 200.0
    }

if 'stock_extra' not in st.session_state:
    st.session_state.stock_extra = {"Lavanda Seca (Huerta)": 50.0, "Romero Fresco": 100.0}

if 'stock_pt' not in st.session_state:
    st.session_state.stock_pt = {k: 0 for k in RECETAS.keys()}

if 'agenda' not in st.session_state: st.session_state.agenda = []
if 'pedidos' not in st.session_state: st.session_state.pedidos = []
if 'cuaderno' not in st.session_state: st.session_state.cuaderno = []

# ==========================================
# 5. BARRA LATERAL (CONFIGURACIÓN Y EXTRAS)
# ==========================================
with st.sidebar:
    st.header("⚙️ Panel de Control")
    
    # --- INTERRUPTOR DE SEGURIDAD (SANDBOX) ---
    modo_prueba = st.toggle("🛠️ MODO PRUEBAS / SIMULACIÓN", value=False)
    if modo_prueba:
        st.warning("⚠️ SIMULACIÓN ACTIVADA\nPuedes tocar todo. Nada se guardará.")
    else:
        st.success("✅ MODO REAL\nLos cambios afectan al stock.")

    st.divider()
    
    # --- CUADERNO DE NOTAS ---
    st.header("📝 Cuaderno de Campo")
    nota_input = st.text_input("Nueva nota rápida:")
    if st.button("Guardar Nota"):
        if nota_input:
            if not modo_prueba:
                fecha = datetime.date.today().strftime("%d/%m")
                st.session_state.cuaderno.append(f"[{fecha}] {nota_input}")
                st.success("Nota guardada.")
            else:
                st.info("Nota simulada (no guardada).")

    with st.expander("📖 Ver mis notas"):
        if not st.session_state.cuaderno:
            st.caption("No hay notas aún.")
        for n in st.session_state.cuaderno:
            st.write(f"- {n}")

    st.divider()
    
    # --- DICCIONARIO RÁPIDO ---
    ing_consulta = st.selectbox("📚 Diccionario de Ingredientes:", list(DICCIONARIO.keys()))
    st.info(DICCIONARIO[ing_consulta])

# ==========================================
# 6. ESTRUCTURA PRINCIPAL (PESTAÑAS)
# ==========================================
tab_prod, tab_ventas, tab_alquimia, tab_agenda, tab_stock = st.tabs([
    "🧪 FABRICACIÓN", "🤝 PEDIDOS & VENTAS", "⚗️ ALQUIMIA", "📅 AGENDA", "📦 ALMACÉN"
])

# ------------------------------------------
# PESTAÑA 1: FABRICACIÓN & DOCTOR pH
# ------------------------------------------
with tab_prod:
    st.subheader("Laboratorio de Producción")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        producto_seleccionado = st.selectbox("¿Qué vamos a fabricar?", list(RECETAS.keys()))
    with col_sel2:
        cantidad_fabricar = st.number_input("Nº Pastillas:", min_value=1, value=10)

    # Alerta de conservación preventiva
    aviso_conservacion = RECETAS[producto_seleccionado].get("conservacion", "")
    if "❄️" in aviso_conservacion:
        st.warning(f"⚠️ ATENCIÓN: {aviso_conservacion}")

    if st.button("📜 Cargar Ficha Técnica"):
        st.divider()
        col_ing, col_pasos = st.columns([1, 2])
        receta_actual = RECETAS[producto_seleccionado]
        
        # Verificación de Stock
        faltan_ingredientes = False
        with col_ing:
            st.markdown("### ⚖️ Ingredientes")
            for ing, gramos_u in receta_actual["ingredientes"].items():
                total_necesario = gramos_u * cantidad_fabricar
                stock_disponible = st.session_state.stock_mp.get(ing, 0)
                
                if stock_disponible < total_necesario:
                    st.error(f"{ing}: Faltan {total_necesario - stock_disponible:.1f}g")
                    faltan_ingredientes = True
                else:
                    st.success(f"{ing}: {total_necesario:.1f}g")

        with col_pasos:
            st.markdown("### 📝 Instrucciones")
            st.markdown(receta_actual["instrucciones"])
            
            st.divider()
            
            # --- SECCIÓN DOCTOR pH ---
            st.markdown("#### 🩺 Doctor pH (Control de Calidad)")
            st.caption("ℹ️ Mide el pH diluyendo 1g de pasta en 9g de agua.")
            ph_input = st.number_input("pH detectado:", 0.0, 14.0, 5.5, step=0.1)
            
            check_calidad = False
            if 4.5 <= ph_input <= 6.0:
                st.success(f"✅ pH {ph_input}: Rango Óptimo. Proceder al prensado.")
                check_calidad = True
            elif ph_input < 4.5:
                st.error(f"🚨 pH {ph_input}: DEMASIADO ÁCIDO.")
                st.info("💡 Solución: Añade solución de **Bicarbonato** o Arginina gota a gota.")
            else:
                st.error(f"🚨 pH {ph_input}: DEMASIADO ALCALINO.")
                st.info("💡 Solución: Añade unas gotas de **Ácido Láctico**.")

            st.divider()
            
            # BOTÓN FINAL DE FABRICACIÓN
            btn_fabricar = st.button("✅ Confirmar Lote y Restar Stock", use_container_width=True)
            
            if btn_fabricar:
                if faltan_ingredientes:
                    st.error("❌ No puedes fabricar: Falta materia prima.")
                else:
                    if not check_calidad:
                        st.warning("⚠️ Estás fabricando con el pH fuera de rango.")
                    
                    if modo_prueba:
                        st.balloons()
                        st.info("🧪 [MODO PRUEBA] Simulación exitosa. No se ha tocado el stock.")
                    else:
                        # 1. Restar MP
                        for ing, gr in receta_actual["ingredientes"].items():
                            st.session_state.stock_mp[ing] -= (gr * cantidad_fabricar)
                        # 2. Sumar PT
                        st.session_state.stock_pt[producto_seleccionado] += cantidad_fabricar
                        # 3. Anotar Agenda
                        hoy = datetime.date.today().strftime("%Y-%m-%d")
                        st.session_state.agenda.append({
                            "fecha": hoy, "tipo": "Producción", 
                            "nota": f"Lote {cantidad_fabricar}x {producto_seleccionado} (pH: {ph_input})"
                        })
                        # 4. Alerta Instagram
                        st.session_state.agenda.append({
                            "fecha": hoy, "tipo": "Instagram", 
                            "nota": f"📸 SUBIR FOTO: Nuevo {producto_seleccionado} recién hecho!"
                        })
                        
                        st.balloons()
                        st.success("¡Fabricación registrada con éxito!")
                        st.rerun()

# ------------------------------------------
# PESTAÑA 2: PEDIDOS Y VENTAS
# ------------------------------------------
with tab_ventas:
    c_pedidos, c_rapida = st.columns([2, 1])
    
    # GESTIÓN DE ENCARGOS
    with c_pedidos:
        st.subheader("📋 Lista de Encargos")
        with st.expander("➕ Apuntar Nuevo Encargo"):
            new_cli = st.text_input("Cliente / Nota:")
            new_prod = st.selectbox("Producto:", list(RECETAS.keys()), key="new_p_encargo")
            new_cant = st.number_input("Cantidad:", 1, 50, 1, key="new_c_encargo")
            
            if st.button("Guardar Encargo"):
                if modo_prueba: st.info("Simulado.")
                else:
                    st.session_state.pedidos.append({
                        "c": new_cli, "p": new_prod, "q": new_cant, 
                        "f": datetime.date.today().strftime("%Y-%m-%d")
                    })
                    st.success("Apuntado.")
                    st.rerun()

        if not st.session_state.pedidos:
            st.info("No hay encargos pendientes.")
        else:
            for i, p in enumerate(st.session_state.pedidos):
                col_info, col_btn = st.columns([3, 1])
                with col_info:
                    st.markdown(f"**{p['c']}** ({p['f']}) -> {p['q']}x {p['p']}")
                with col_btn:
                    if st.button("✅ Entregar", key=f"ent_{i}"):
                        if modo_prueba: st.info("Simulado.")
                        else:
                            # Verificar Stock
                            if st.session_state.stock_pt[p['p']] >= p['q']:
                                st.session_state.stock_pt[p['p']] -= p['q']
                                st.session_state.agenda.append({
                                    "fecha": datetime.date.today().strftime("%Y-%m-%d"),
                                    "tipo": "Venta",
                                    "nota": f"ENTREGA: {p['c']} ({p['q']}x {p['p']})"
                                })
                                st.session_state.pedidos.pop(i)
                                st.rerun()
                            else:
                                st.error("Sin Stock.")

    # VENTA RÁPIDA (MERCADILLO)
    with c_rapida:
        st.subheader("⚡ Venta Directa")
        st.caption("Para ventas al momento sin reserva.")
        vp = st.selectbox("Prod:", list(RECETAS.keys()), key="v_directa")
        vq = st.number_input("Cant:", 1, 20, 1, key="c_directa")
        
        if st.button("Cobrar y Restar"):
            if modo_prueba:
                st.balloons()
                st.info("Simulado.")
            else:
                if st.session_state.stock_pt[vp] >= vq:
                    st.session_state.stock_pt[vp] -= vq
                    hoy = datetime.date.today().strftime("%Y-%m-%d")
                    st.session_state.agenda.append({
                        "fecha": hoy, "tipo": "Venta", 
                        "nota": f"Venta Rápida: {vq}x {vp}"
                    })
                    st.success("Vendido.")
                    st.rerun()
                else:
                    st.error("No hay stock suficiente.")

# ------------------------------------------
# PESTAÑA 3: ALQUIMIA
# ------------------------------------------
with tab_alquimia:
    st.subheader("⚗️ Gestión de Macerados y Oleatos")
    
    c_alq1, c_alq2 = st.columns(2)
    with c_alq1:
        planta = st.text_input("Planta (ej. Hipérico):")
        base = st.selectbox("Aceite Base:", ["Almendras", "Oliva", "Girasol", "Jojoba"])
    with c_alq2:
        metodo = st.selectbox("Método:", ["Solar (40 días)", "Baño María (2h)", "En caliente (Rápido)"])
    
    if st.button("⏳ Crear Alerta de Filtrado"):
        if modo_prueba: st.info("Alerta simulada.")
        else:
            dias = 40 if "Solar" in metodo else 0
            fecha_fin = datetime.date.today() + datetime.timedelta(days=dias)
            
            nota_agenda = f"FILTRAR Oleato: {planta} en {base} ({metodo})"
            st.session_state.agenda.append({
                "fecha": fecha_fin.strftime("%Y-%m-%d"),
                "tipo": "Alerta",
                "nota": nota_agenda
            })
            st.success(f"Alerta creada para el {fecha_fin}")

# ------------------------------------------
# PESTAÑA 4: AGENDA
# ------------------------------------------
with tab_agenda:
    st.subheader("📅 Historial de Movimientos")
    
    # Ordenar cronológicamente inverso
    agenda_sorted = sorted(st.session_state.agenda, key=lambda x: x['fecha'], reverse=True)
    
    for item in agenda_sorted:
        # Iconos dinámicos
        if item["tipo"] == "Producción": icon = "🧴"
        elif item["tipo"] == "Venta": icon = "💰"
        elif item["tipo"] == "Instagram": icon = "📸"
        elif item["tipo"] == "Alerta": icon = "⏰"
        else: icon = "📌"
        
        st.markdown(f"**{item['fecha']}** {icon} {item['nota']}")
        st.divider()

# ------------------------------------------
# PESTAÑA 5: ALMACÉN (STOCK)
# ------------------------------------------
with tab_stock:
    st.markdown("### 🏪 Estado del Inventario")
    
    col_pt, col_mp, col_extra = st.columns(3)
    
    # 1. Producto Terminado
    with col_pt:
        st.info("🛍️ PRODUCTO TERMINADO")
        for prod, cant in st.session_state.stock_pt.items():
            minimo = RECETAS[prod]["minimo_stock"]
            
            if cant < minimo:
                st.error(f"🔴 **{prod}**: {cant} (BAJO)")
            elif cant > 20:
                st.warning(f"⚠️ **{prod}**: {cant} (EXCESO)")
            else:
                st.success(f"🟢 **{prod}**: {cant}")

    # 2. Materia Prima
    with col_mp:
        st.warning("📦 MATERIA PRIMA (Gramos)")
        for ing, gr in st.session_state.stock_mp.items():
            if gr < 100:
                st.error(f"{ing}: {gr:.1f}g")
            else:
                st.write(f"**{ing}**: {gr:.1f}g")

    # 3. Extras / Huerta
    with col_extra:
        st.success("🌿 HUERTA & EXTRAS")
        
        # Añadir nuevo extra
        with st.expander("➕ Añadir Ingrediente Extra"):
            ex_nombre = st.text_input("Nombre:")
            ex_cant = st.number_input("Gramos:", 0, 5000, 0)
            if st.button("Guardar Extra"):
                if not modo_prueba:
                    st.session_state.stock_extra[ex_nombre] = ex_cant
                    st.rerun()
        
        # Listado y Copiar para el Chat
        texto_chat = "Hola! Mira mi stock extra: "
        for item, c in st.session_state.stock_extra.items():
            st.write(f"🌾 {item}: {c}g")
            texto_chat += f"{item} ({c}g), "
        
        st.divider()
        st.caption("Copia esto para pedirme nuevas recetas:")
        st.code(texto_chat + "¿Qué puedo inventar?")
