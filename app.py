import streamlit as st
import datetime

# ==========================================
# 1. CONFIGURACIÓN VISUAL (LIMPIA Y CLARA)
# ==========================================
st.set_page_config(
    page_title="Kreación Kerkus | Finanzas",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (PARA QUE SE VEA BIEN SÍ O SÍ) ---
st.markdown("""
<style>
    /* Forzar colores claros y textos oscuros */
    .stApp {
        background-color: #fdfbf7; /* Crema muy suave */
        color: #1a1a1a; /* Casi negro */
    }
    
    /* Textos generales */
    p, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #1a1a1a !important;
    }
    
    /* Título Principal */
    h1 {
        font-family: 'Georgia', serif;
        color: #8b4513 !important; /* Marrón cuero */
        border-bottom: 2px solid #daa520;
    }
    
    /* Cajas de texto y números (BLANCAS y LIMPÍAS) */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ccc !important;
    }
    
    /* Botones Dorados */
    .stButton > button {
        background-color: #daa520 !important;
        color: #000000 !important;
        border: 1px solid #8b4513 !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background-color: #ffd700 !important;
    }
    
    /* Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #f0e6d2; /* Beige un poco más oscuro */
    }
    
    /* Tarjetas de Métricas (Cajas de dinero) */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Alertas legibles */
    .stAlert {
        background-color: #fff3cd;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# LOGO
try: st.image("logo_kerkus.jpg", width=200)
except: st.title("🌿 Kerkus Magikus")

# ==========================================
# 2. DATOS: COSTES Y RECETAS
# ==========================================
COSTES = {
    # Tensioactivos
    "SCI": 0.022, "Betaína de Coco": 0.012, "Coco Glucoside": 0.021, "SLSA": 0.069, "SCS": 0.016,
    # Mantecas y Ceras
    "Manteca de Karité": 0.023, "Manteca de Cacao": 0.025, "Manteca de Mango": 0.049,
    "Cera de Abejas": 0.035, "Cera Candelilla": 0.096, "BTMS-50": 0.030,
    "Ácido Esteárico": 0.015, "Alcohol Cetílico": 0.029,
    # Aceites
    "Aceite de Almendras": 0.012, "Oleato Almendras (Caléndula)": 0.015,
    "Aceite de Argán": 0.108, "Aceite de Coco": 0.022, "Aceite de Girasol AO": 0.010,
    "Oleato Girasol (Manzanilla)": 0.015, "Aceite de Pepita Uva": 0.020,
    "Oleato Pepita Uva (Romero)": 0.025, "Aceite de Jojoba": 0.080, "Aceite de Arroz": 0.024,
    "Aceite de Ricino": 0.038, "Aceite de Té Verde": 0.072,
    # Polvos y Arcillas
    "Polvo de Arroz": 0.041, "Caolín": 0.010, "Arcilla Verde": 0.020,
    "Avena Coloidal": 0.032, "Ortiga Verde": 0.060, "Aloe Vera 200x": 0.200,
    "Miel en Polvo": 0.085, "Semillas de Amapola": 0.057,
    # Activos
    "Pantenol (B5)": 0.116, "Hidroqueratina": 0.120, "Niacinamida (B3)": 0.200,
    "Glicerina": 0.041, "Vitamina E": 0.166, "Leucidal": 0.183, "Euxyl Eco": 0.196,
    # Aceites Esenciales
    "AAEE (Geranio/Ylang)": 0.550, "AAEE (Naranja/Cedro)": 0.150, 
    "AAEE (Menta/Romero/Limón)": 0.200, "AAEE (Lavanda/Geranio)": 0.400,
    "AAEE Salvia": 0.500, "AAEE Incienso": 1.00, "AAEE Sándalo": 0.66,
    # Otros
    "Ácido Láctico": 0.05, "Bicarbonato": 0.01, "Consuelda": 0.086
}

RECETAS = {
    "🧴 1. Champú Nutritivo (Pelo Seco)": {
        "minimo_stock": 4, "conservacion": "Lugar fresco.",
        "ingredientes": {
            "SCI": 44.0, "Polvo de Arroz": 7.0, "Caolín": 3.0,
            "Ácido Esteárico": 5.0, "Alcohol Cetílico": 4.0, "Manteca de Karité": 6.0, "Oleato Almendras (Caléndula)": 6.0, "Aceite de Argán": 1.5,
            "Betaína de Coco": 8.5, "Pantenol (B5)": 1.5, "Hidroqueratina": 1.7, "Vitamina E": 0.8, "AAEE (Geranio/Ylang)": 1.6
        },
        "instrucciones": "1. Mezclar polvos. 2. Fundir grasas. 3. Unir. 4. Activos en frío. 5. Prensar."
    },
    "🌿 2. Champú Equilibrante (Pelo Normal)": {
        "minimo_stock": 4, "conservacion": "Lugar fresco.",
        "ingredientes": {
            "SCI": 44.0, "Avena Coloidal": 6.5, "Caolín": 2.0, "Aloe Vera 200x": 0.8,
            "Ácido Esteárico": 5.0, "Alcohol Cetílico": 3.5, "Manteca de Karité": 4.5, "Manteca de Mango": 1.5, "Oleato Girasol (Manzanilla)": 6.0,
            "Betaína de Coco": 8.5, "Pantenol (B5)": 1.5, "Hidroqueratina": 1.7, "Vitamina E": 0.8, "AAEE (Naranja/Cedro)": 2.5
        },
        "instrucciones": "1. Mezclar polvos. 2. Fundir grasas. 3. Unir. 4. Activos en frío. 5. Prensar."
    },
    "🍏 3. Champú Purificante (Pelo Graso)": {
        "minimo_stock": 4, "conservacion": "Lugar fresco.",
        "ingredientes": {
            "SCI": 46.0, "Arcilla Verde": 8.0, "Ortiga Verde": 4.0,
            "Ácido Esteárico": 5.0, "Alcohol Cetílico": 3.5, "Manteca de Karité": 3.0, "Oleato Pepita Uva (Romero)": 4.0, "Aceite de Jojoba": 1.0,
            "Betaína de Coco": 8.5, "Pantenol (B5)": 1.5, "Hidroqueratina": 1.0, "Vitamina E": 0.8, "AAEE (Menta/Romero/Limón)": 3.5
        },
        "instrucciones": "1. Mezclar polvos. 2. Fundir grasas. 3. Unir. 4. Activos en frío. 5. Prensar."
    },
    "✨ 4. Acondicionador Seda (Todo tipo)": {
        "minimo_stock": 4, "conservacion": "❄️ RECOMENDADO: Nevera en verano.",
        "ingredientes": {
            "BTMS-50": 33.0, "Alcohol Cetílico": 9.0, "Manteca de Karité": 6.0, "Oleato Almendras (Caléndula)": 4.5, "Aceite de Argán": 1.5,
            "Hidroqueratina": 1.5, "Pantenol (B5)": 1.0, "Vitamina E": 0.6, "AAEE (Lavanda/Geranio)": 1.2
        },
        "instrucciones": "1. Fundir todo. 2. Templar y añadir activos. 3. Enmoldar rápido."
    },
    "☁️ 5. Limpiador Facial Nube de Arroz": {
        "minimo_stock": 5, "conservacion": "Secar bien tras uso.",
        "ingredientes": {
            "SCI": 18.0, "Caolín": 8.0, "Avena Coloidal": 4.0, "Polvo de Arroz": 4.0,
            "Ácido Esteárico": 3.0, "Alcohol Cetílico": 4.5, "Manteca de Mango": 4.0, "Aceite de Arroz": 4.0,
            "Coco Glucoside": 2.0, "Glicerina": 2.0, "Niacinamida (B3)": 1.5, "Vitamina E": 0.5
        },
        "instrucciones": "1. Mezclar polvos. 2. Fundir grasas. 3. Líquidos. 4. Unir y amasar."
    },
    "💋 6. Bálsamo Labial Beso de Kerkus": {
        "minimo_stock": 10, "conservacion": "Evitar sol.",
        "ingredientes": {
            "Cera de Abejas": 6.0, "Manteca de Karité": 7.0, "Oleato Almendras (Caléndula)": 7.5, "Miel en Polvo": 1.5, "Vitamina E": 0.2
        },
        "instrucciones": "1. Fundir Cera/Karité. 2. Oleato+Miel. 3. Envasar."
    }
}

# ==========================================
# 3. GESTIÓN DEL ESTADO (CON AUTOCORRECCIÓN DE ERRORES)
# ==========================================

# 1. CORRECCIÓN DE STOCK PT (Esto arregla el fallo que veías en pantalla)
if 'stock_pt' not in st.session_state:
    st.session_state.stock_pt = {k: 0 for k in RECETAS.keys()}
else:
    # Si hay productos antiguos que no coinciden con los nuevos nombres, reseteamos las claves
    claves_actuales = set(st.session_state.stock_pt.keys())
    claves_nuevas = set(RECETAS.keys())
    if claves_actuales != claves_nuevas:
        # Intentamos conservar cantidades si el nombre es parecido, si no, a cero
        nuevo_stock = {}
        for k in claves_nuevas:
            nuevo_stock[k] = st.session_state.stock_pt.get(k, 0)
        # Valores manuales que me dijiste en el audio:
        nuevo_stock["🧴 1. Champú Nutritivo (Pelo Seco)"] = 4
        nuevo_stock["🌿 2. Champú Equilibrante (Pelo Normal)"] = 2
        nuevo_stock["🍏 3. Champú Purificante (Pelo Graso)"] = 5
        nuevo_stock["☁️ 5. Limpiador Facial Nube de Arroz"] = 4
        st.session_state.stock_pt = nuevo_stock

# 2. STOCK DE MATERIALES (MP)
if 'stock_mp' not in st.session_state:
    st.session_state.stock_mp = {
        "SCI": 1400.0, "Betaína de Coco": 1000.0, "Coco Glucoside": 250.0,
        "Manteca de Karité": 100.0, "Manteca de Cacao": 500.0, "Manteca de Mango": 150.0,
        "Cera de Abejas": 306.0, "Cera Candelilla": 50.0, "BTMS-50": 500.0, 
        "Ácido Esteárico": 500.0, "Alcohol Cetílico": 80.0,
        "Aceite de Almendras": 1000.0, "Oleato Almendras (Caléndula)": 500.0,
        "Aceite de Argán": 100.0, "Aceite de Coco": 300.0, 
        "Aceite de Girasol AO": 1000.0, "Oleato Girasol (Manzanilla)": 500.0,
        "Aceite de Pepita Uva": 500.0, "Oleato Pepita Uva (Romero)": 500.0,
        "Aceite de Jojoba": 100.0, "Aceite de Arroz": 200.0, 
        "Aceite de Ricino": 125.0, "Aceite de Té Verde": 100.0,
        "Polvo de Arroz": 22.0, "Caolín": 450.0, "Arcilla Verde": 200.0,
        "Avena Coloidal": 110.0, "Ortiga Verde": 400.0, "Aloe Vera 200x": 180.0,
        "Miel en Polvo": 20.0, "Semillas de Amapola": 30.0,
        "Pantenol (B5)": 100.0, "Hidroqueratina": 20.0, "Niacinamida (B3)": 35.0,
        "Glicerina": 125.0, "Vitamina E": 50.0, "Leucidal": 30.0, "Euxyl Eco": 15.0,
        "AAEE (Geranio/Ylang)": 50.0, "AAEE (Naranja/Cedro)": 50.0, 
        "AAEE (Menta/Romero/Limón)": 90.0, "AAEE (Lavanda/Geranio)": 50.0,
        "AAEE Salvia": 15.0, "AAEE Incienso": 15.0, "AAEE Sándalo": 15.0,
        "Ácido Láctico": 50.0, "Bicarbonato": 500.0, "SLSA": 50.0, "SCS": 400.0
    }

if 'stock_extra' not in st.session_state:
    st.session_state.stock_extra = {
        "Consuelda (Raíz)": 80.0, "Caléndula Seca": 30.0, "Lavanda Seca": 50.0,
        "Romero Fresco": 100.0, "Flores de Hibisco": 20.0
    }

if 'finanzas' not in st.session_state:
    st.session_state.finanzas = {"ingresos_totales": 0.0, "beneficio_total": 0.0, "gastos_material": 0.0}

if 'agenda' not in st.session_state: st.session_state.agenda = []
if 'pedidos' not in st.session_state: st.session_state.pedidos = []
if 'cuaderno' not in st.session_state: st.session_state.cuaderno = []

# ==========================================
# 4. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuración")
    modo_prueba = st.toggle("🛠️ MODO PRUEBAS", value=False)
    if modo_prueba: st.warning("⚠️ SIMULACIÓN")
    else: st.success("✅ REAL")
    
    st.divider()
    st.header("💰 Hucha Kerkus")
    c_hucha1, c_hucha2 = st.columns(2)
    c_hucha1.metric("Caja", f"{st.session_state.finanzas['ingresos_totales']:.2f}€")
    c_hucha2.metric("Beneficio", f"{st.session_state.finanzas['beneficio_total']:.2f}€")
    
    st.divider()
    st.header("📝 Notas")
    nota = st.text_input("Apuntar algo:")
    if st.button("Guardar"):
        st.session_state.cuaderno.append(f"{datetime.date.today().strftime('%d/%m')} {nota}")
    
    with st.expander("Ver notas"):
        for n in st.session_state.cuaderno: st.write(f"- {n}")

# ==========================================
# 5. PESTAÑAS PRINCIPALES
# ==========================================
tabs = st.tabs(["🧪 FABRICACIÓN", "🤝 VENTAS", "⚗️ ALQUIMIA", "📅 AGENDA", "📦 ALMACÉN"])

# --- TAB 1: FABRICACIÓN ---
with tabs[0]:
    st.subheader("Laboratorio de Producción")
    c1, c2, c3 = st.columns(3)
    prod = c1.selectbox("Producto:", list(RECETAS.keys()))
    cant = c2.number_input("Cantidad (Uds):", 1, 100, 10)
    
    # Calcular costes
    receta = RECETAS[prod]
    coste = 0.0
    for i, q in receta["ingredientes"].items():
        coste += (q * COSTES.get(i, 0.02) * cant)
    venta = cant * 10.0
    beneficio = venta - coste
    margen = (beneficio / venta) * 100 if venta > 0 else 0
    
    with c3:
        st.info(f"💰 **Coste:** {coste:.2f}€ | **Beneficio:** {beneficio:.2f}€ ({margen:.0f}%)")

    if st.button("📜 Ver y Fabricar"):
        st.divider()
        c_ing, c_inst = st.columns([1, 2])
        
        falta_stock = False
        with c_ing:
            st.markdown("### Ingredientes")
            for i, q in receta["ingredientes"].items():
                nec = q * cant
                tengo = st.session_state.stock_mp.get(i, 0)
                if tengo < nec:
                    st.error(f"{i}: Falta {nec-tengo:.1f}g")
                    falta_stock = True
                else:
                    st.success(f"{i}: {nec:.1f}g")
        
        with c_inst:
            st.markdown(receta["instrucciones"])
            st.divider()
            
            st.markdown("#### 🩺 Doctor pH")
            ph = st.number_input("pH medido:", 0.0, 14.0, 5.5, step=0.1)
            if ph < 4.5: st.error("🚨 ÁCIDO -> Añade Bicarbonato")
            elif ph > 6.0: st.error("🚨 ALCALINO -> Añade Ác. Láctico")
            else: st.success("✅ pH Correcto")
            
            st.divider()
            if st.button("✅ Confirmar Lote"):
                if falta_stock: st.error("❌ No hay stock suficiente")
                else:
                    if not modo_prueba:
                        for i, q in receta["ingredientes"].items():
                            st.session_state.stock_mp[i] -= (q * cant)
                        st.session_state.stock_pt[prod] += cant
                        st.session_state.finanzas["gastos_material"] += coste
                        
                        hoy = datetime.date.today().strftime("%Y-%m-%d")
                        st.session_state.agenda.append({"fecha": hoy, "tipo": "Producción", "nota": f"Lote {cant}x {prod}"})
                        st.session_state.agenda.append({"fecha": hoy, "tipo": "Instagram", "nota": f"📸 FOTO: Nuevo {prod}"})
                        st.balloons()
                        st.success("¡Fabricado!")
                        st.rerun()
                    else: st.info("Simulación correcta.")

# --- TAB 2: VENTAS ---
with tabs[1]:
    c_ped, c_rap = st.columns([2, 1])
    
    with c_ped:
        st.subheader("📋 Encargos")
        with st.expander("➕ Nuevo"):
            cli = st.text_input("Cliente:")
            pp = st.selectbox("Prod:", list(RECETAS.keys()), key="p_enc")
            qq = st.number_input("Cant:", 1, 50, 1, key="q_enc")
            if st.button("Apuntar"):
                if not modo_prueba:
                    st.session_state.pedidos.append({"c": cli, "p": pp, "q": qq, "f": datetime.date.today().strftime("%d/%m")})
                    st.rerun()

        for k, p in enumerate(st.session_state.pedidos):
            st.write(f"**{p['c']}**: {p['q']}x {p['p']}")
            if st.button("✅ Cobrar", key=f"e_{k}"):
                if not modo_prueba:
                    if st.session_state.stock_pt[p['p']] >= p['q']:
                        st.session_state.stock_pt[p['p']] -= p['q']
                        ingreso = p['q'] * 10.0
                        coste_est = sum([q * COSTES.get(i, 0.02) for i, q in RECETAS[p['p']]["ingredientes"].items()]) * p['q']
                        st.session_state.finanzas["ingresos_totales"] += ingreso
                        st.session_state.finanzas["beneficio_total"] += (ingreso - coste_est)
                        st.session_state.agenda.append({"fecha": datetime.date.today().strftime("%Y-%m-%d"), "tipo": "Venta", "nota": f"ENTREGA: {p['c']}"})
                        st.session_state.pedidos.pop(k)
                        st.rerun()
                    else: st.error("Falta Stock")
            st.divider()

    with c_rap:
        st.subheader("⚡ Venta Rápida")
        vp = st.selectbox("Prod:", list(RECETAS.keys()), key="v_fast")
        vq = st.number_input("Cant:", 1, 20, 1, key="q_fast")
        if st.button("Cobrar Rápido"):
            if not modo_prueba:
                if st.session_state.stock_pt[vp] >= vq:
                    st.session_state.stock_pt[vp] -= vq
                    ingreso = vq * 10.0
                    coste_est = sum([q * COSTES.get(i, 0.02) for i, q in RECETAS[vp]["ingredientes"].items()]) * vq
                    st.session_state.finanzas["ingresos_totales"] += ingreso
                    st.session_state.finanzas["beneficio_total"] += (ingreso - coste_est)
                    st.session_state.agenda.append({"fecha": datetime.date.today().strftime("%Y-%m-%d"), "tipo": "Venta", "nota": f"Venta Rápida {vq}x {vp}"})
                    st.success("Vendido.")
                    st.rerun()
                else: st.error("Falta Stock")

# --- TAB 3: ALQUIMIA ---
with tabs[2]:
    st.subheader("⚗️ Macerados")
    pl = st.text_input("Planta:")
    ba = st.selectbox("Base:", ["Almendras", "Oliva", "Girasol", "Uva", "Jojoba"])
    mt = st.selectbox("Método:", ["Solar (40 días)", "Baño María", "Caliente"])
    if st.button("Crear Alerta"):
        if not modo_prueba:
            d = 40 if "Solar" in mt else 0
            fin = datetime.date.today() + datetime.timedelta(days=d)
            st.session_state.agenda.append({"fecha": fin.strftime("%Y-%m-%d"), "tipo": "Alerta", "nota": f"FILTRAR: {pl} en {ba}"})
            st.success(f"Alerta para {fin}")

# --- TAB 4: AGENDA ---
with tabs[3]:
    st.subheader("📅 Historial")
    for x in sorted(st.session_state.agenda, key=lambda i: i['fecha'], reverse=True):
        icon = "🧴" if x["tipo"] == "Producción" else "💰" if x["tipo"] == "Venta" else "📸" if x["tipo"] == "Instagram" else "⏰"
        st.write(f"**{x['fecha']}** {icon} {x['nota']}")
        st.divider()

# --- TAB 5: ALMACÉN ---
with tabs[4]:
    st.markdown("### 🏪 Inventario")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🛍️ PRODUCTO TERMINADO")
        # Aquí es donde fallaba antes: ahora usamos .get() para evitar el error
        for p, c in st.session_state.stock_pt.items():
            min_s = RECETAS.get(p, {}).get("minimo_stock", 0) # Protección contra errores
            if c < min_s: st.error(f"🔴 {p}: {c}")
            elif c > 20: st.warning(f"⚠️ {p}: {c}")
            else: st.success(f"🟢 {p}: {c}")

    with c2:
        st.warning("📦 MATERIA PRIMA")
        for i, g in sorted(st.session_state.stock_mp.items()):
            color = "red" if g < 50 else "black"
            st.markdown(f"<span style='color:{color}'>**{i}**: {g:.1f}g</span>", unsafe_allow_html=True)

    with c3:
        st.success("🌿 EXTRAS")
        with st.expander("➕ Añadir"):
            en = st.text_input("Nombre:")
            eq = st.number_input("Gramos:", 0, 5000)
            if st.button("Guardar Extra"):
                if not modo_prueba:
                    st.session_state.stock_extra[en] = eq
                    st.rerun()
        for k, v in st.session_state.stock_extra.items():
            st.write(f"🌾 {k}: {v}g")
