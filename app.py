import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN Y ESTILO KERKUS MAGIKUS
st.set_page_config(page_title="Kerkus Magikus Lab Pro", layout="wide", page_icon="🌿")

# 2. INICIALIZACIÓN DE DATOS (Stock real de facturas y audio del 26/12/2025)
if 'raw_stock' not in st.session_state:
    st.session_state.raw_stock = {
        "SCI": 2000.0, "Polvo de Arroz": 22.0, "Caolín": 1000.0, "Manteca de Karité": 965.0, 
        "Aceite de Almendras (Oleato)": 1000.0, "Betaína de Coco": 1125.0, "Ácido Esteárico": 500.0, 
        "Alcohol Cetílico": 400.0, "Manteca de Mango": 150.0, "Aceite de Argán": 125.0, 
        "Avena Coloidal": 200.0, "Aloe Vera 200x": 180.0, "Hidroqueratina": 60.0, 
        "Pantenol": 125.0, "Vitamina E": 60.0, "Cera de Abejas": 500.0, "Niacinamida": 50.0, 
        "Miel en Polvo": 50.0, "BTMS-50": 500.0, "Aceite de Jojoba": 125.0, "Aceite de Pepita de Uva": 500.0
    }

if 'product_stock' not in st.session_state:
    st.session_state.product_stock = {
        "Champú Nutritivo": 4, "Champú Equilibrante": 3, "Champú Purificante": 6,
        "Limpiador Nube de Arroz": 6, "Acondicionador Seda": 0, "Bálsamo Labial": 5
    }

if 'historial' not in st.session_state:
    st.session_state.historial = [] # Para trazabilidad y pH

if 'agenda' not in st.session_state:
    st.session_state.agenda = []

# 3. DICCIONARIO DE RECETAS (Actualizado y verificado)
RECETAS = {
    "🧴 Champú Nutritivo (Seco)": {"id": "Champú Nutritivo", "ing": {"SCI": 440, "Polvo de Arroz": 70, "Caolín": 30, "Ácido Esteárico": 50, "Alcohol Cetílico": 40, "Manteca de Karité": 60, "Aceite de Almendras (Oleato)": 60, "Aceite de Argán": 15, "Betaína de Coco": 85, "Pantenol": 15, "Hidroqueratina": 17, "Vitamina E": 8, "AAEE Geranio/Ylang": 16}},
    "🌿 Champú Equilibrante (Normal)": {"id": "Champú Equilibrante", "ing": {"SCI": 440, "Avena Coloidal": 65, "Caolín": 20, "Aloe Vera 200x": 8, "Ácido Esteárico": 50, "Alcohol Cetílico": 35, "Manteca de Karité": 45, "Manteca de Mango": 15, "Aceite de Girasol (Oleato)": 60, "Betaína de Coco": 85, "Pantenol": 15, "Hidroqueratina": 17, "Vitamina E": 8, "AAEE Naranja/Cedro": 25}},
    "🍏 Champú Purificante (Graso)": {"id": "Champú Purificante", "ing": {"SCI": 460, "Arcilla Verde": 80, "Ortiga Verde": 40, "Ácido Esteárico": 50, "Alcohol Cetílico": 35, "Manteca de Karité": 30, "Aceite de Pepita de Uva": 40, "Aceite de Jojoba": 10, "Betaína de Coco": 85, "Pantenol": 15, "Hidroqueratina": 10, "Vitamina E": 8, "AAEE Menta/Romero/Limón": 35}},
    "✨ Acondicionador Seda": {"id": "Acondicionador Seda", "ing": {"BTMS-50": 330, "Alcohol Cetílico": 90, "Manteca de Karité": 60, "Aceite de Almendras (Oleato)": 45, "Aceite de Argán": 15, "Hidroqueratina": 15, "Pantenol": 10, "Vitamina E": 6, "AAEE Lavanda/Geranio": 12}},
    "☁️ Limpiador Facial Nube de Arroz": {"id": "Limpiador Nube de Arroz", "ing": {"SCI": 180, "Caolín": 80, "Avena Coloidal": 40, "Polvo de Arroz": 40, "Ácido Esteárico": 30, "Alcohol Cetílico": 45, "Manteca de Mango": 40, "Aceite de Arroz": 40, "Coco Glucoside": 20, "Glicerina": 20, "Niacinamida": 15, "Vitamina E": 5}},
    "💋 Bálsamo Labial Beso de Kerkus": {"id": "Bálsamo Labial", "ing": {"Cera de Abejas": 60, "Manteca de Karité": 70, "Aceite de Almendras (Oleato)": 75, "Miel en Polvo": 15, "Vitamina E": 2}}
}

# 4. NAVEGACIÓN
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧪 Laboratorio Pro", "💰 Ventas", "📅 Agenda", "📦 Stock", "🛒 Reposición"])

with tab1:
    st.header("Fabricación y Trazabilidad")
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a: seleccion = st.selectbox("Producto", list(RECETAS.keys()))
    with col_b: uds = st.number_input("Cantidad (uds)", min_value=1, value=10)
    with col_c: ph_medido = st.number_input("pH Final Medido", min_value=1.0, max_value=14.0, value=5.5, step=0.1)
    
    receta = RECETAS[seleccion]
    factor = uds / 10.0
    
    # Verificación de Stock
    puedes_fabricar = True
    for ing, cant in receta["ing"].items():
        if st.session_state.raw_stock.get(ing, 0) < (cant * factor):
            puedes_fabricar = False
            st.error(f"Falta: {ing}")

    if st.button("🚀 VALIDAR LOTE Y DESCONTAR"):
        if puedes_fabricar:
            # 1. Descontar materias primas
            for ing, cant in receta["ing"].items():
                st.session_state.raw_stock[ing] -= (cant * factor)
            # 2. Sumar producto terminado
            st.session_state.product_stock[receta["id"]] += uds
            # 3. Registro de Trazabilidad
            lote_id = f"LOT-{datetime.now().strftime('%Y%m%d%H%M')}"
            st.session_state.historial.append({"Lote": lote_id, "Producto": receta["id"], "Unidades": uds, "pH": ph_medido, "Fecha": datetime.now().strftime("%d/%m/%Y")})
            st.success(f"Lote {lote_id} registrado correctamente.")
            st.balloons()

    st.subheader("📜 Historial de Lotes (Trazabilidad)")
    if st.session_state.historial:
        st.table(pd.DataFrame(st.session_state.historial))

with tab2:
    st.header("Mercadillo - Ventas Rápidas")
    v_prod = st.selectbox("Vender producto", list(st.session_state.product_stock.keys()))
    v_uds = st.number_input("Unidades vendidas", min_value=1, value=1)
    if st.button("💰 Registrar Venta"):
        if st.session_state.product_stock[v_prod] >= v_uds:
            st.session_state.product_stock[v_prod] -= v_uds
            st.success("Venta realizada.")
        else: st.error("No hay stock suficiente.")

with tab3: # Agenda (Oleatos, etc.)
    st.header("Gestión de Tiempos")
    nota = st.text_input("Nueva nota (Ej: Puse oleato Caléndula)")
    if st.button("📌 Guardar Nota"):
        st.session_state.agenda.append({"Fecha": datetime.now().strftime("%d/%m/%Y"), "Nota": nota})
    st.write(pd.DataFrame(st.session_state.agenda))

with tab4: # Inventario
    st.header("Estado Almacén")
    c1, c2 = st.columns(2)
    c1.subheader("Materias Primas")
    c1.dataframe(pd.DataFrame(st.session_state.raw_stock.items(), columns=["Ingrediente", "Gramos/ml"]))
    c2.subheader("Productos Terminados")
    c2.dataframe(pd.DataFrame(st.session_state.product_stock.items(), columns=["Producto", "Unidades"]))

with tab5: # Reposición
    st.header("Alertas de Compra")
    for ing, stock in st.session_state.raw_stock.items():
        if stock < 100: st.error(f"🚨 COMPRAR YA: {ing} ({stock:.1f}g/ml)")
