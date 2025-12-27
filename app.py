import streamlit as st
import datetime

# ==========================================
# 1. CONFIGURACIÓN VISUAL (ESTILO LIMPIO)
# ==========================================
st.set_page_config(
    page_title="Kreación Kerkus | Finanzas",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS: COLORES CLAROS Y LEGIBLES ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; color: #1a1a1a; }
    h1, h2, h3 { font-family: 'Georgia', serif; color: #5d4037 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #fff !important; color: #000 !important; border: 1px solid #aaa !important;
    }
    .stButton > button {
        background-color: #daa520 !important; color: #000 !important; font-weight: bold; border: 1px solid #8b4513 !important;
    }
    .stMetric { background-color: #fff; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    .stAlert { background-color: #fff3cd; color: #856404; }
</style>
""", unsafe_allow_html=True)

try: st.image("logo_kerkus.jpg", width=200)
except: st.title("🌿 Kerkus Magikus")

# ==========================================
# 2. DATOS INICIALES (COSTES Y RECETAS)
# ==========================================
# Estos son los costes base calculados de tus facturas.
# Ahora podrás editarlos desde la App si cambian.
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
        "Glicerina": 0.041, "Vitamina E": 0.166, "Leucidal": 0.183, "Euxyl Eco": 0.196,
        "AAEE (Geranio/Ylang)": 0.550, "AAEE (Naranja/Cedro)": 0.150, 
        "AAEE (Menta/Romero/Limón)": 0.200, "AAEE (Lavanda/Geranio)": 0.400,
        "AAEE Salvia": 0.500, "AAEE Incienso": 1.00, "AAEE Sándalo": 0.66,
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
# 3. GESTIÓN DEL ESTADO (Stock inicial + Corrección de Nombres)
# ==========================================

# Corrección automática de claves antiguas si existen
if 'stock_pt' not in st.session_state:
    st.session_state.stock_pt = {k: 0 for k in RECETAS.keys()}
else:
    # Si detectamos claves viejas, saneamos el diccionario
    claves_nuevas = set(RECETAS.keys())
    claves_actuales = set(st.session_state.stock_pt.keys())
    if claves_actuales != claves_nuevas:
        nuevo_pt = {k: 0 for k in claves_nuevas}
        # Preservamos cantidades si coinciden nombres
        for k, v in st.session_state.stock_pt.items():
            if k in nuevo_pt: nuevo_pt[k] = v
        st.session_state.stock_pt = nuevo_pt

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
    c_h1, c_h2 = st.columns(2)
    c_h1.metric("Caja", f"{st.session_state.finanzas['ingresos_totales']:.2f}€")
    c_h2.metric("Beneficio", f"{st.session_state.finanzas['beneficio_total']:.2f}€")
    
    st.divider()
    st.header("📝 Notas")
    nota = st.text_input("Apuntar:")
    if st.button("Guardar"):
        st.session_state.cuaderno.append(f"{datetime.date.today().strftime('%d/%m')} {nota}")
    with st.expander("Ver notas"):
        for n in st.session_state.cuaderno: st.write(f"- {n}")

# ==========================================
# 5. PESTAÑAS
# ==========================================
tabs = st.tabs(["🧪 FABRICACIÓN", "🤝 VENTAS", "⚗️ ALQUIMIA", "📅 AGENDA", "📦 ALMACÉN (Stock)"])

# --- TAB 1: FABRICACIÓN ---
with tabs[0]:
    st.subheader("Laboratorio de Producción")
    c1, c2, c3 = st.columns(3)
    prod = c1.selectbox("Producto:", list(RECETAS.keys()))
    cant = c2.number_input("Cantidad (Uds):", 1, 100, 10)
    
    receta = RECETAS[prod]
    coste = sum([q * st.session_state.costes_mp.get(i, 0.02) * cant for i, q in receta["ingredientes"].items()])
    venta = cant * 10.0
    beneficio = venta - coste
    margen = (beneficio / venta) * 100 if venta > 0 else 0
    
    with c3:
        st.info(f"💰 Coste Lote: **{coste:.2f}€**\n\nBeneficio: **{beneficio:.2f}€** ({margen:.0f}%)")

    if st.button("📜 Ver y Fabricar"):
        st.divider()
        c_ing, c_inst = st.columns([1, 2])
        
        falta = False
        with c_ing:
            st.markdown("### Ingredientes")
            for i, q in receta["ingredientes"].items():
                nec = q * cant
                tengo = st.session_state.stock_mp.get(i, 0)
                if tengo < nec:
                    st.error(f"{i}: Falta {nec-tengo:.1f}g")
                    falta = True
                else:
                    st.success(f"{i}: {nec:.1f}g")
        
        with c_inst:
            st.markdown(receta["instrucciones"])
            st.divider()
            
            st.markdown("#### 🩺 Doctor pH")
            ph = st.number_input("pH medido:", 0.0, 14.0, 5.5, step=0.1)
            if ph < 4.5: st.error("🚨 ÁCIDO -> Bicarbonato")
            elif ph > 6.0: st.error("🚨 ALCALINO -> Láctico")
            else: st.success("✅ pH Correcto")
            
            if st.button("✅ Confirmar Lote"):
                if falta: st.error("❌ Falta Stock")
                else:
                    if not modo_prueba:
                        for i, q in receta["ingredientes"].items():
                            st.session_state.stock_mp[i] -= (q * cant)
                        st.session_state.stock_pt[prod] += cant
                        st.session_state.finanzas["gastos_material"] += coste
                        
                        hoy = datetime.date.today().strftime("%Y-%m-%d")
                        st.session_state.agenda.append({"fecha": hoy, "tipo": "Producción", "nota": f"Lote {cant}x {prod}"})
                        st.session_state.agenda.append({"fecha": hoy, "tipo": "Instagram", "nota": f"📸 FOTO: {prod}"})
                        st.balloons()
                        st.success("Fabricado.")
                        st.rerun()
                    else: st.info("Simulación OK")

# --- TAB 2: VENTAS ---
with tabs[1]:
    c_ped, c_rap = st.columns([2, 1])
    with c_ped:
        st.subheader("📋 Encargos")
        with st.expander("➕ Nuevo"):
            cli = st.text_input("Cliente:")
            pp = st.selectbox("Prod:", list(RECETAS.keys()), key="p_en")
            qq = st.number_input("Cant:", 1, 50, 1, key="q_en")
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
                        # Coste estimado para beneficio
                        c_est = sum([q * st.session_state.costes_mp.get(i, 0.02) for i, q in RECETAS[p['p']]["ingredientes"].items()]) * p['q']
                        st.session_state.finanzas["ingresos_totales"] += ingreso
                        st.session_state.finanzas["beneficio_total"] += (ingreso - c_est)
                        st.session_state.agenda.append({"fecha": datetime.date.today().strftime("%Y-%m-%d"), "tipo": "Venta", "nota": f"ENTREGA: {p['c']}"})
                        st.session_state.pedidos.pop(k)
                        st.rerun()
                    else: st.error("Falta Stock")
            st.divider()

    with c_rap:
        st.subheader("⚡ Venta Rápida")
        vp = st.selectbox("Prod:", list(RECETAS.keys()), key="v_fa")
        vq = st.number_input("Cant:", 1, 20, 1, key="q_fa")
        if st.button("Cobrar Rápido"):
            if not modo_prueba:
                if st.session_state.stock_pt[vp] >= vq:
                    st.session_state.stock_pt[vp] -= vq
                    ingreso = vq * 10.0
                    c_est = sum([q * st.session_state.costes_mp.get(i, 0.02) for i, q in RECETAS[vp]["ingredientes"].items()]) * vq
                    st.session_state.finanzas["ingresos_totales"] += ingreso
                    st.session_state.finanzas["beneficio_total"] += (ingreso - c_est)
                    st.session_state.agenda.append({"fecha": datetime.date.today().strftime("%Y-%m-%d"), "tipo": "Venta", "nota": f"Venta {vq}x {vp}"})
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
        icon = "🧴" if x["tipo"] == "Producción" else "💰" if x["tipo"] == "Venta" else "📸"
        st.write(f"**{x['fecha']}** {icon} {x['nota']}")
        st.divider()

# --- TAB 5: ALMACÉN (NUEVO: EDITOR MANUAL) ---
with tabs[4]:
    st.subheader("📦 Gestión de Inventario")
    
    # 1. HERRAMIENTA DE AJUSTE MANUAL
    with st.expander("📝 Recepción de Pedidos / Ajuste Manual", expanded=True):
        c_aj1, c_aj2, c_aj3 = st.columns(3)
        ing_ajuste = c_aj1.selectbox("Ingrediente:", sorted(list(st.session_state.stock_mp.keys())))
        tipo_ajuste = c_aj2.radio("Acción:", ["Sumar Compra (+)", "Corregir Inventario (=)"], horizontal=True)
        cant_ajuste = c_aj3.number_input("Cantidad (g):", 0.0, 5000.0, 0.0, step=10.0)
        
        c_p1, c_p2 = st.columns(2)
        nuevo_precio = c_p1.number_input(f"Coste actual ({st.session_state.costes_mp.get(ing_ajuste, 0):.3f} €/g). Nuevo:", 0.000, 5.000, st.session_state.costes_mp.get(ing_ajuste, 0.0), format="%.3f")
        
        if st.button("💾 Guardar Cambios en Stock"):
            if not modo_prueba:
                # 1. Actualizar Precio
                st.session_state.costes_mp[ing_ajuste] = nuevo_precio
                
                # 2. Actualizar Cantidad
                if "Sumar" in tipo_ajuste:
                    st.session_state.stock_mp[ing_ajuste] += cant_ajuste
                    msg = f"Añadidos {cant_ajuste}g a {ing_ajuste}."
                else:
                    st.session_state.stock_mp[ing_ajuste] = cant_ajuste
                    msg = f"Stock de {ing_ajuste} corregido a {cant_ajuste}g."
                
                st.success(f"✅ {msg} Precio actualizado a {nuevo_precio} €/g.")
                st.rerun()
            else: st.info("Simulación.")

    st.divider()

    # 2. VISUALIZACIÓN
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🛍️ PRODUCTO TERMINADO")
        for p, c in st.session_state.stock_pt.items():
            min_s = RECETAS.get(p, {}).get("minimo_stock", 0)
            if c < min_s: st.error(f"🔴 {p}: {c}")
            elif c > 20: st.warning(f"⚠️ {p}: {c}")
            else: st.success(f"🟢 {p}: {c}")

    with c2:
        st.warning("📦 MATERIA PRIMA")
        # Mostrar solo si hay stock o si se ha editado
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
