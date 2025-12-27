import streamlit as st
import datetime
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN Y ESTÉTICA (ESTILO MEDIEVAL LEGIBLE)
# ==========================================
st.set_page_config(
    page_title="Kreación Kerkus",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS MAESTRO: ESTILO VISUAL ---
st.markdown("""
<style>
    /* IMPORTAR FUENTES: MedievalSharp (Títulos) y Lato (Texto legible) */
    @import url('https://fonts.googleapis.com/css2?family=MedievalSharp&family=Lato:wght@400;700&display=swap');

    /* 1. FONDO GLOBAL Y TEXTOS (Bloqueo de modo oscuro) */
    .stApp {
        background-color: #fdfbf7 !important; /* Pergamino claro */
    }
    
    /* Forzar color de texto negro/marrón en TODAS partes */
    h1, h2, h3, h4, h5, h6, p, li, span, div, label, button {
        color: #2b1b17 !important;
    }

    /* 2. TIPOGRAFÍA MEDIEVAL */
    h1, h2, h3 {
        font-family: 'MedievalSharp', cursive !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    /* El resto del texto en fuente limpia para leer bien */
    p, div, label, input {
        font-family: 'Lato', sans-serif !important;
    }

    /* 3. LOGO REDONDO (Kerkus Magikus) */
    /* Busca la imagen del logo y la recorta en círculo con borde dorado */
    img[src*="logo_kerkus.jpg"] {
        border-radius: 50%;
        border: 3px solid #daa520;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    /* 4. PESTAÑAS (TABS) - VISIBLES SIEMPRE */
    /* Pestaña inactiva (Fondo beige oscuro, letras negras) */
    button[data-baseweb="tab"] {
        background-color: #eaddcf !important;
        border: 1px solid #bcaaa4 !important;
    }
    button[data-baseweb="tab"] > div > p {
        color: #000000 !important; /* Texto negro SIEMPRE */
        font-weight: bold;
    }
    /* Pestaña activa (Fondo dorado, letras negras) */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #daa520 !important;
        border-bottom: 0px !important;
    }

    /* 5. BARRA LATERAL */
    section[data-testid="stSidebar"] {
        background-color: #f5f5dc; /* Beige suave */
        border-right: 2px solid #daa520;
    }

    /* 6. OCULTAR BOTONES MOLESTOS DE ARRIBA DERECHA */
    .stDeployButton {display:none;}
    #MainMenu {display:none;}
    footer {display:none;}

    /* 7. INPUTS (Cajas de texto) */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: white !important;
        color: black !important;
        border: 1px solid #8b4513 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- CABECERA (LOGO Y TÍTULO) ---
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    # Asegúrate de que tu archivo se llame exactamente así en GitHub
    try:
        st.image("logo_kerkus.jpg", width=150)
    except:
        # Si falla la imagen, muestra un icono
        st.markdown("## 🌿")

with col_titulo:
    st.title("Kreación Kerkus")
    st.markdown("**Sistema de Gestión Alquímica y Artesanal**")

st.divider()

# Aquí irán las pestañas en la siguiente parte...
st.info("👆 Si ves el logo redondo, el fondo claro y las letras oscuras, el diseño está LISTO. Dime qué tal y seguimos.")
