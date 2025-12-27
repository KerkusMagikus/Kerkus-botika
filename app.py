import streamlit as st
import datetime
import pandas as pd # Necesario para tablas bonitas

# ==========================================
# 1. CONFIGURACIÓN VISUAL (FORZANDO MODO CLARO)
# ==========================================
st.set_page_config(
    page_title="Kreación Kerkus | Master",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS MAESTRO: BLOQUEA EL MODO OSCURO ---
st.markdown("""
<style>
    /* FORZAR TEMA CLARO */
    [data-testid="stAppViewContainer"] {
        background-color: #fdfbf7; /* Crema muy suave */
        color: #2b1b17; /* Marrón café oscuro */
    }
    [data-testid="stSidebar"] {
        background-color: #f0e6d2; /* Beige cuero */
        border-right: 1px solid #bcaaa4;
    }
    [data-testid="stHeader"] {
        background-color: #fdfbf7;
    }
    
    /* TEXTOS Y TÍTULOS */
    h1, h2, h3, h4, h5, h6, p, li, span, div, label {
        color: #2b1b17 !important;
        font-family: 'Source Sans Pro', sans-serif;
    }
    h1 {
        font-family: 'Georgia', serif;
        color: #5d4037 !important; /* Marrón chocolate */
        border-bottom: 2px solid #daa520;
    }
    
    /* INPUTS (CAJAS DE ESCRIBIR) - BLANCOS SIEMPRE */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #8d6e63 !important;
    }
    
    /* BOTONES */
    .stButton > button {
        background: linear-gradient(to bottom, #fff59d, #fbc02d);
        color: #000000 !important;
        border: 1px solid #f57f17 !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background: #fdd835 !important;
    }

    /* TABLAS Y DATAFRAMES */
    [data-testid="stDataFrame"] {
        background-color: white !important;
        color: black !important;
    }
    
    /* ALERTAS */
    .stAlert { background-color: #fff9c4; color: #5d4037; border: 1px solid #fbc02d; }
    
</style>
""", unsafe_allow_html=True)

# LOGO
try: st.image("logo_kerkus.jpg", width=220)
except: st.title("🌿 Kerkus Magikus")


# ==========================================
# 2. DATOS MAESTROS
# ==========================================

# A. COSTES (Historial base)
if 'costes_mp' not in st.session_state:
    st.session_state.costes_mp = {
        "SCI": 0.022, "Betaína de Coco": 0.012, "Coco Glucoside": 0.021, "SLSA": 0.069, "SCS": 0.016,
        "Manteca de Karité": 0.023, "Manteca de Cacao": 0.025, "Manteca de Mango": 0.049,
        "Cera de Abejas": 0.035, "Cera Candelilla": 0.096, "BTMS-50": 0.030,
        "Ácido Esteárico": 0.015, "Alcohol Cetílico": 0.029,
        "Aceite de Almendras": 0.012, "Oleato Almendras (Caléndula)": 0.015,
        "Aceite de Argán": 0.108, "Aceite de Coco": 0.022, "Aceite de Girasol AO": 0.010,
        "Oleato Girasol (Manzanilla)": 0.015, "Aceite de Pepita Uva": 0.020,
        "Oleato Pepita Uva (Romero)": 0.025, "Aceite de Jojoba": 0.080, "Aceite de Arroz": 0.024,
        "Aceite de Ricino": 0.038, "Aceite de Té Verde": 0.072,
        "Polvo de Arroz": 0.041, "Caolín": 0.010, "Arcilla Verde": 0.020,
        "Avena Coloidal": 0.032, "Ortiga Verde": 0.060, "Aloe Vera 200x": 0.200,
        "Miel en Polvo": 0.085, "Semillas de Amapola": 0.057,
        "Pantenol (B5)": 0.116, "Hidroqueratina": 0.120, "Niacinamida (B3)": 0.200,
        "Glicerina": 0.041, "Vitamina E": 0.166,
        "AAEE (Geranio/Ylang)": 0.550, "AAEE (Naranja/Cedro)": 0.150, 
        "AAEE (Menta/Romero/Limón)": 0.200, "AAEE (Lavanda/Geranio)": 0.400,
        "Ácido Láctico": 0.05, "Bicarbonato": 0.01
    }

# B. RECETAS (Tus 6 Fórmulas Maestras)
# NOTA: Cantidades divididas entre 10 para simular 1 unidad de ~90g-100g.
# Si quieres hacer el lote completo de 1kg, pon "10" en cantidad.
RECETAS = {
    "🧴 1. Champú Nutritivo (Pelo Seco)": {
        "tipo": "Champú",
        "minimo_stock": 4, "conservacion": "Lugar fresco.",
        "ingredientes": {
            "SCI": 44.0, "Polvo de Arroz": 7.0, "Caolín": 3.0,
            "Ácido Esteárico": 5.0, "Alcohol Cetílico": 4.0, "Manteca de Karité": 6.0, "Oleato Almendras (Caléndula)": 6.0, "Aceite de Argán": 1.5,
            "Betaína de Coco": 8.5, "Pantenol (B5)": 1.5, "Hidroqueratina": 1.7, "Vitamina E": 0.8, "AAEE (Geranio/Ylang)": 1.6
        },
        "instrucciones": "1. **Polvos:** Mezclar SCI, Arroz, Caolín.\n2. **Fusión:** Fundir Esteárico, Cetílico, Karité y Aceites.\n3. **Unión:** Mezclar fases.\n4. **Frío:** Añadir Betaína y Activos.\n5. **Fin:** Prensar."
    },
    "🌿 2. Champú Equilibrante (Pelo Normal)": {
        "tipo": "Champú",
        "minimo_stock": 4, "conservacion": "Lugar fresco.",
        "ingredientes": {
            "SCI": 44.0, "Avena Coloidal": 6.5, "Caolín": 2.0, "Aloe Vera 200x": 0.8,
            "Ácido Esteárico": 5.0, "Alcohol Cetílico": 3.5, "Manteca de Karité": 4.5, "Manteca de Mango": 1.5, "Oleato Girasol (Manzanilla)": 6.0,
            "Betaína de Coco": 8.5, "Pantenol (B5)": 1.5, "Hidroqueratina": 1.7, "Vitamina E": 0.8, "AAEE (Naranja/Cedro)": 2.5
        },
        "instrucciones": "1. **Polvos:** Mezclar SCI, Avena, Caolín, Aloe.\n2. **Fusión:** Fundir Esteárico, Cetílico, Mantecas y Oleato.\n3. **Unión:** Mezclar fases.\n4. **Frío:** Añadir Betaína y Activos.\n5. **Fin:** Prensar."
    },
    "🍏 3. Champú Purificante (Pelo Graso)": {
        "tipo": "Champú",
        "minimo_stock": 4, "conservacion": "Lugar fresco.",
        "ingredientes": {
            "SCI": 46.0, "Arcilla Verde": 8.0, "Ortiga Verde": 4.0,
            "Ácido Esteárico": 5.0, "Alcohol Cetílico": 3.5, "Manteca de Karité": 3.0, "Oleato Pepita Uva (Romero)": 4.0, "Aceite de Jojoba": 1.0,
            "Betaína de Coco": 8.5, "Pantenol (B5)": 1.5, "Hidroqueratina": 1.0, "Vitamina E": 0.8, "AAEE (Menta/Romero/Limón)": 3.5
        },
        "instrucciones": "1. **Polvos:** Mezclar SCI, Arcilla Verde, Ortiga.\n2. **Fusión:** Fundir Esteárico, Cetílico, Karité y Aceites.\n3. **Unión:** Mezclar fases.\n4. **Frío:** Añadir Betaína y Activos.\n5. **Fin:** Prensar."
    },
    "✨ 4. Acondicionador Seda (Todo tipo)": {
        "tipo": "Acondicionador",
        "minimo_stock": 4, "conservacion": "❄️ RECOMENDADO: Nevera en verano.",
        "ingredientes": {
            "BTMS-50": 33.0, "Alcohol Cetílico": 9.0, "Manteca de Karité": 6.0, "Oleato Almendras (Caléndula)": 4.5, "Aceite de Argán": 1.5,
            "Hidroqueratina": 1.5, "Pantenol (B5)": 1.0, "Vitamina E": 0.6, "AAEE (Lavanda/Geranio)": 1.2
        },
        "instrucciones": "1. **Fusión:** Fundir BTMS, Cetílico, Karité y Aceites.\n2. **Templado:** Retirar del fuego. Añadir Activos.\n3. **Fin:** Enmoldar rápido."
    },
    "☁️ 5. Limpiador Facial Nube de Arroz": {
        "tipo": "Facial",
        "minimo_stock": 5, "conservacion": "Secar bien tras uso.",
        "ingredientes": {
            "SCI": 18.0, "Caolín": 8.0, "Avena Coloidal": 4.0, "Polvo de Arroz": 4.0,
            "Ácido Esteárico": 3.0, "Alcohol Cetílico": 4.5, "Manteca de Mango": 4.0, "Aceite de Arroz": 4.0,
            "Coco Glucoside": 2.0, "Glicerina": 2.0, "Niacinamida (B3)": 1.5, "Vitamina E": 0.5
        },
        "instrucciones": "1. **Polvos:** Mezclar SCI, Caolín, Avena, Arroz.\n2. **Fusión:** Fundir Esteárico, Cetílico, Mango, Aceite Arroz.\n3. **Líquido:** Disolver Niacinamida en Glicerina + Glucoside.\n4. **Fin:** Unir todo y amasar."
    },
    "💋 6. Bálsamo Labial Beso de Kerkus": {
        "tipo": "Bálsamo",
        "minimo_stock": 10, "conservacion": "Evitar sol.",
        "ingredientes": {
            "Cera de Abejas": 6.0, "Manteca de Karité": 7.0, "Oleato Almendras (Caléndula)": 7.5, "Miel en Polvo": 1.5, "Vitamina E": 0.2
        },
        "instrucciones": "1. **Fusión:** Fundir Cera y Karité.\n2. **Mezcla:** Añade Oleato y Miel (dispersar bien).\n3. **Fin:** Añade Vit E y envasa."
    }
}

# ==========================================
# 3. GESTIÓN DEL ESTADO (STOCKS)
# ==========================================
if 'stock_pt' not in st.session_state:
    st.session_state.stock_pt = {k: 0 for k in RECETAS.keys()}
    # Ajuste inicial aproximado
    st.session_state.stock_pt["🧴 1. Champú Nutritivo (Pelo Seco)"] = 4
    st.session_state.stock_pt["🍏 3. Champú Purificante (Pelo Graso)"] = 5
    st.session_state.stock_pt["☁️ 5. Limpiador Facial Nube de Arroz"] = 4

if 'stock_mp' not in st.session_state:
    st.session_state.stock_mp = {
        "SCI": 1400.0, "Betaína de Coco": 1000.0, "Coco Glucoside": 250.0,
        "Manteca de Karité": 100.0, "Manteca de Cacao": 500.0, "Manteca de Mango": 150.0,
        "Cera de Abejas": 300.0, "Cera Candelilla": 50.0, "BTMS-50": 500.0, 
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
        "Ácido Láctico": 50.0, "Bicarbonato": 500.0, "SLSA": 50.0, "SCS": 400.0
    }

if 'stock_extra' not in st.session_state:
    st.session_state.stock_extra = {
        "Consuelda (Raíz)": 80.0, "Caléndula Seca": 30.0, "Lavanda Seca": 50.0,
        "Romero Fresco": 100.0, "Flores de Hibisco": 20.0
    }

if 'finanzas' not in st.session_state:
    st.session_state.finanzas = {"ingresos": 0.0, "beneficio": 0.0, "gastos": 0.0}

if 'agenda' not in st.session_state: st.session_state.agenda = []
if 'pedidos' not in st.session_state: st.session_state.pedidos = []
if 'cuaderno' not in st.session_state: st.session_state.cuaderno = []

# ==========================================
# 4. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.header("⚙️ Panel de Control")
    modo_prueba = st.toggle("🛠️ MODO PRUEBAS", value=False)
    if modo_prueba: st.warning("⚠️ SIMULACIÓN")
    else: st.success("✅ MODO REAL")
    
    st.divider()
    st.header("💰 Hucha Kerkus")
    c1, c2 = st.columns(2)
    c1.metric("Caja", f"{st.session_state.finanzas['ingresos']:.2f}€")
    c2.metric("Beneficio", f"{st.session_state.finanzas['beneficio']:.2f}€")
    
    st.divider()
    st.header("📝 Notas")
    nota = st.text_input("Nota rápida:")
    if st.button("Guardar"):
        st.session_state.cuaderno.append(f"{datetime.date.today().strftime('%d/%m')} {nota}")
    with st.expander("Ver notas"):
        for n in st.session_state.cuaderno: st.write(f"- {n}")

# ==========================================
# 5. PESTAÑAS PRINCIPALES
# ==========================================
tabs = st.tabs(["🧪 LABORATORIO", "🛒 CARRITO & COSTES", "🤝 VENTAS", "📦 ALMACÉN", "📅 AGENDA"])

# --- TAB 1: LABORATORIO (FABRICACIÓN) ---
with tabs[0]:
    st.subheader("⚗️ Zona de Fabricación")
    c_prod, c_cant, c_metrics = st.columns([2,1,2])
    
    prod = c_prod.selectbox("Receta:", list(RECETAS.keys()))
    cant = c_cant.number_input("Cantidad (Uds):", 1, 100, 10)
    
    receta = RECETAS[prod]
    coste_lote = sum([q * st.session_state.costes_mp.get(i, 0.02) for i, q in receta["ingredientes"].items()]) * cant
    venta_estimada = cant * 10.0 # Precio medio
    beneficio_lote = venta_estimada - coste_lote
    
    with c_metrics:
        st.info(f"💰 Coste Lote: **{coste_lote:.2f}€** | Beneficio: **{beneficio_lote:.2f}€**")
    
    if st.button("📖 Ver Receta y Fabricar"):
        st.divider()
        c_ing, c_pasos = st.columns([1,1])
        
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
        
        with c_pasos:
            st.markdown(f"### Instrucciones ({receta['tipo']})")
            st.markdown(receta["instrucciones"])
            st.divider()
            ph = st.number_input("🧪 pH Medido:", 0.0, 14.0, 5.5)
            if ph < 4.5: st.warning("Ácido -> Subir con Bicarbonato")
            elif ph > 6.0: st.warning("Alcalino -> Bajar con Láctico")
            else: st.success("pH Correcto")
            
            if st.button("✅ Confirmar Fabricación"):
                if falta_stock: st.error("No hay ingredientes suficientes.")
                else:
                    if not modo_prueba:
                        for i, q in receta["ingredientes"].items():
                            st.session_state.stock_mp[i] -= (q * cant)
                        st.session_state.stock_pt[prod] += cant
                        st.session_state.finanzas["gastos"] += coste_lote
                        st.session_state.agenda.append({"f": datetime.date.today(), "t": "Producción", "d": f"{cant}x {prod}"})
                        st.balloons()
                        st.success("Lote registrado.")
                        st.rerun()

# --- TAB 2: CARRITO & COSTES (NUEVO) ---
with tabs[1]:
    st.subheader("💶 Costes y Compras")
    
    c_costes, c_carrito = st.columns(2)
    
    with c_costes:
        st.markdown("### 📝 Historial de Precios (€/g)")
        df_costes = pd.DataFrame(list(st.session_state.costes_mp.items()), columns=["Ingrediente", "Precio/g"])
        # Edición rápida de costes
        ing_edit = st.selectbox("Editar precio de:", list(st.session_state.costes_mp.keys()))
        nuevo_precio = st.number_input(f"Nuevo precio para {ing_edit}:", 0.000, 10.000, st.session_state.costes_mp[ing_edit], format="%.3f")
        if st.button("Actualizar Precio"):
            st.session_state.costes_mp[ing_edit] = nuevo_precio
            st.success("Precio actualizado.")
            st.rerun()
            
    with c_carrito:
        st.markdown("### 🛒 Carrito Inteligente (Proporción)")
        st.info("Calcula qué comprar para gastar el stock a la vez.")
        
        ing_base = st.selectbox("Voy a comprar (Ingrediente Base):", ["SCI", "Betaína de Coco", "Alcohol Cetílico"])
        cant_base = st.number_input(f"Cantidad de {ing_base} (g):", 100, 5000, 1000)
        
        if st.button("Calcular Proporción"):
            st.write(f"Si compras **{cant_base}g de {ing_base}**, necesitarás aprox:")
            # Lógica simple basada en proporción media de champús
            # SCI es aprox 45% de la fórmula solida.
            ratio = cant_base / 45.0 # Ratio por "parte"
            st.write(f"- Betaína de Coco: {8.5 * ratio:.0f}g")
            st.write(f"- Ácido Esteárico: {5.0 * ratio:.0f}g")
            st.write(f"- Mantecas (Karité/Mango): {6.0 * ratio:.0f}g")
            st.write(f"- Aceites Líquidos: {7.0 * ratio:.0f}g")
            st.caption("*Cálculo estimado para fórmulas de champú estándar.")

# --- TAB 3: VENTAS ---
with tabs[2]:
    c_encargos, c_rapida = st.columns(2)
    with c_encargos:
        st.subheader("📋 Encargos")
        with st.expander("Nuevo Encargo"):
            cli = st.text_input("Cliente:")
            p_enc = st.selectbox("Prod:", list(RECETAS.keys()), key="enc_p")
            c_enc = st.number_input("Cant:", 1, 50, 1, key="enc_c")
            if st.button("Apuntar"):
                st.session_state.pedidos.append({"c": cli, "p": p_enc, "q": c_enc})
                st.rerun()
        
        for i, p in enumerate(st.session_state.pedidos):
            st.write(f"{p['c']}: {p['q']}x {p['p']}")
            if st.button("Cobrar", key=f"cob_{i}"):
                if st.session_state.stock_pt[p['p']] >= p['q']:
                    st.session_state.stock_pt[p['p']] -= p['q']
                    ingreso = p['q'] * 10.0
                    st.session_state.finanzas["ingresos"] += ingreso
                    st.session_state.finanzas["beneficio"] += (ingreso * 0.7) # Estimado 70%
                    st.session_state.agenda.append({"f": datetime.date.today(), "t": "Venta", "d": f"Entrega {p['c']}"})
                    st.session_state.pedidos.pop(i)
                    st.rerun()
                else: st.error("Falta Stock")

    with c_rapida:
        st.subheader("⚡ Venta Directa")
        p_rap = st.selectbox("Prod:", list(RECETAS.keys()), key="rap_p")
        c_rap = st.number_input("Cant:", 1, 20, 1, key="rap_c")
        if st.button("Vender Ya"):
            if st.session_state.stock_pt[p_rap] >= c_rap:
                st.session_state.stock_pt[p_rap] -= c_rap
                st.session_state.finanzas["ingresos"] += (c_rap * 10.0)
                st.session_state.finanzas["beneficio"] += (c_rap * 7.0)
                st.session_state.agenda.append({"f": datetime.date.today(), "t": "Venta", "d": f"Venta Rápida {c_rap}x"})
                st.success("Vendido")
                st.rerun()
            else: st.error("Falta Stock")

# --- TAB 4: ALMACÉN (TOTALMENTE EDITABLE) ---
with tabs[3]:
    st.subheader("📦 Gestión de Inventario")
    
    tipo_stock = st.radio("¿Qué quieres editar?", ["Materia Prima", "Producto Terminado", "Extras"], horizontal=True)
    
    if tipo_stock == "Materia Prima":
        diccionario = st.session_state.stock_mp
    elif tipo_stock == "Producto Terminado":
        diccionario = st.session_state.stock_pt
    else:
        diccionario = st.session_state.stock_extra
        
    # EDITOR
    c_edit1, c_edit2 = st.columns([3, 1])
    item_edit = c_edit1.selectbox("Elemento:", sorted(list(diccionario.keys())))
    cant_actual = diccionario[item_edit]
    nueva_cant = c_edit2.number_input("Cantidad Real:", 0.0, 10000.0, float(cant_actual))
    
    if st.button("💾 Guardar Corrección"):
        if not modo_prueba:
            diccionario[item_edit] = nueva_cant
            st.success(f"Stock de {item_edit} actualizado a {nueva_cant}")
            st.rerun()
    
    st.divider()
    st.markdown("### Visualización de Stock")
    # Mostrar tabla simple
    df_stock = pd.DataFrame(list(diccionario.items()), columns=["Item", "Cantidad"])
    st.dataframe(df_stock, use_container_width=True)

# --- TAB 5: AGENDA ---
with tabs[4]:
    st.subheader("📅 Historial")
    for x in st.session_state.agenda[::-1]:
        st.write(f"**{x['f']}** - {x['t']}: {x['d']}")
