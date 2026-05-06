from pathlib import Path
import unicodedata
import re

import pandas as pd
import plotly.express as px
import streamlit as st

CSV_PATH = Path("data/dafont_fuentes.csv")

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================

st.set_page_config(
    page_title="DaFont · Análisis tipográfico",
    layout="wide",
    page_icon="🎨",
    initial_sidebar_state="expanded"
)

# =========================
# CSS PERSONALIZADO
# =========================

st.markdown("""
<style>
    /* Netflix-style dark theme */
    
    /* Main body background */
    .main {
        background-color: #0f0f0f !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0f0f0f !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #0f0f0f !important;
    }

    /* Main header - Netflix style */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-left: 4px solid #E50914;
        color: white;
        padding: 3rem 2rem;
        border-radius: 0;
        margin-bottom: 2.5rem;
        text-align: left;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        margin-left: -1rem;
        margin-right: -1rem;
        margin-top: -1rem;
        padding-left: 3rem;
    }

    .main-header h1 {
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: none;
        letter-spacing: -1px;
        color: #ffffff;
    }

    .main-header p {
        font-size: 1.3rem;
        opacity: 0.85;
        margin: 0;
        color: #b3b3b3;
        font-weight: 400;
    }

    /* Tab containers - Netflix style */
    .tab-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-left: 4px solid #E50914;
        padding: 2rem 1.5rem;
        border-radius: 0;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }

    .tab-header {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: none;
        letter-spacing: -0.5px;
    }
    
    .tab-header + p {
        color: #b3b3b3 !important;
        font-size: 1.1rem !important;
    }

    /* Metric cards - Netflix style */
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 4px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin: 0.5rem;
        border: 1px solid #333333;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #E50914;
        box-shadow: 0 6px 20px rgba(229,9,20,0.2);
    }

    .metric-card .metric-value {
        font-size: 2.8rem;
        font-weight: 900;
        display: block;
        margin-bottom: 0.5rem;
        color: #E50914;
    }

    .metric-card .metric-label {
        font-size: 0.95rem;
        opacity: 0.8;
        color: #b3b3b3;
        font-weight: 500;
    }

    /* Chart container - Netflix style */
    .chart-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
        padding: 1.8rem;
        border-radius: 4px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        margin: 1.5rem 0;
        border: 1px solid #333333;
    }

    /* Dataframe container */
    .dataframe-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
        border-radius: 4px;
        padding: 1.2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        border: 1px solid #333333;
    }
    
    .dataframe-container table {
        background-color: #262626 !important;
        color: #ffffff !important;
    }
    
    .dataframe-container th {
        background-color: #1a1a1a !important;
        color: #E50914 !important;
        border-color: #333333 !important;
    }
    
    .dataframe-container td {
        color: #b3b3b3 !important;
        border-color: #333333 !important;
    }

    /* Expander styling */
    .stExpander {
        border-radius: 4px;
        border: 1px solid #333333;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin: 0.8rem 0;
        background-color: #1a1a1a;
    }

    .stExpander > div:first-child {
        background: linear-gradient(135deg, #262626 0%, #1a1a1a 100%);
        color: #ffffff;
        border-radius: 4px 4px 0 0;
        font-weight: 600;
        border-bottom: 1px solid #333333;
    }
    
    .stExpander > div:first-child:hover {
        background: linear-gradient(135deg, #2d2d2d 0%, #262626 100%);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f0f0f !important;
        border-right: 1px solid #333333;
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 4px;
        margin-bottom: 1rem;
        border-left: 3px solid #E50914;
    }

    .sidebar-content h3 {
        color: #E50914;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 700;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #1a1a1a;
        padding: 0.5rem;
        border-radius: 4px;
        border-bottom: 2px solid #333333;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 0;
        border: none;
        border-bottom: 3px solid transparent;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #b3b3b3;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(229,9,20,0.1);
        color: #ffffff;
        border-bottom-color: #E50914;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: transparent;
        color: #E50914;
        border-bottom-color: #E50914;
        box-shadow: none;
    }

    /* Text styling */
    h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, span, div, label {
        color: #b3b3b3 !important;
    }
    
    .stMarkdown {
        color: #b3b3b3 !important;
    }

    /* Input and select styling */
    .stRadio > div, .stCheckbox > div {
        color: #b3b3b3 !important;
    }
    
    .stRadio [role="radio"], .stCheckbox [role="checkbox"] {
        background-color: #262626 !important;
        border-color: #E50914 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }

    ::-webkit-scrollbar-thumb {
        background: #E50914;
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #ff3333;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER PRINCIPAL
# =========================

st.markdown("""
<div class="main-header">
    <h1>🎨 DaFont Analytics</h1>
    <p>Explora el universo tipográfico de DaFont con visualizaciones interactivas</p>
</div>
<br>
""", unsafe_allow_html=True)

# =========================
# CARGA Y LIMPIEZA INICIAL
# =========================

if not CSV_PATH.exists():
    st.error(f"No encuentro el CSV en: {CSV_PATH}")
    st.stop()

df = pd.read_csv(CSV_PATH)

required = ["seccion", "categoria", "font_url", "fuente"]
missing = [c for c in required if c not in df.columns]

if missing:
    st.error(f"Faltan columnas en el CSV: {missing}")
    st.stop()

for col in ["seccion", "categoria", "fuente", "font_url", "autor", "licencia"]:
    if col in df.columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

def normalizar_nombre(nombre):
    nombre = str(nombre).lower().strip()
    nombre = unicodedata.normalize("NFKD", nombre)
    nombre = "".join(c for c in nombre if not unicodedata.combining(c))
    nombre = re.sub(r"[^a-z0-9]+", "", nombre)
    return nombre

df["fuente_normalizada"] = df["fuente"].apply(normalizar_nombre)

# =========================
# PROCESAMIENTO DE DATOS
# =========================

total_filas = len(df)
total_urls = df["font_url"].nunique()
total_nombres = df["fuente_normalizada"].nunique()

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🎯 Panel de Control</h3>
    </div>
    """, unsafe_allow_html=True)

    modo = st.radio(
        "📊 Modo de conteo",
        [
            "Con duplicados",
            "Sin duplicados por URL",
            "Sin duplicados por nombre normalizado",
        ],
        help="Elige cómo contar las fuentes según tus necesidades de análisis"
    )

    st.markdown("---")

    # Procesar datos según el modo seleccionado
    if modo == "Sin duplicados por URL":
        df_base = df.drop_duplicates(subset=["font_url"]).copy()
    elif modo == "Sin duplicados por nombre normalizado":
        df_base = df.drop_duplicates(subset=["fuente_normalizada"]).copy()
    else:
        df_base = df.copy()

    # Métricas en sidebar
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📄 Filas CSV", f"{total_filas:,}")
        st.metric("🔗 URLs únicas", f"{total_urls:,}")
    with col2:
        st.metric("📝 Nombres únicos", f"{total_nombres:,}")
        st.metric("📊 Filas usadas", f"{len(df_base):,}")

    if total_filas == total_urls:
        st.success("✅ No hay duplicados por URL en tu CSV")

# =========================
# COLORES
# =========================

colores = {
    "Fantasía": "#E50914",
    "Aspecto extranjero": "#FF6B6B",
    "Tecno": "#4ECDC4",
    "Bitmap": "#1ABC9C",
    "Gótico": "#FF1744",
    "Básico": "#00E676",
    "Script": "#E91E63",
    "Dingbats": "#FFC107",
    "Holiday": "#FF5722",
}

# =========================
# GRUPOS CONCEPTUALES
# =========================

def asignar_grupo(row):
    seccion = row["seccion"]
    categoria = row["categoria"]

    funcionales = {
        ("Básico", "Sans serif"),
        ("Básico", "Serif"),
        ("Básico", "Ancho fijo"),
        ("Básico", "Varios"),
        ("Tecno", "Cuadrado"),
        ("Tecno", "LCD"),
        ("Tecno", "Ciencia ficción"),
        ("Tecno", "Varios"),
        ("Bitmap", "Pixel, Bitmap"),
    }

    expresivas_secciones = {
        "Fantasía",
        "Aspecto extranjero",
        "Gótico",
        "Script",
        "Dingbats",
        "Holiday",
    }

    if (seccion, categoria) in funcionales:
        return "Funcionales / normales"

    if seccion in expresivas_secciones:
        return "Expresivas / fantasía / manuscritas"

    return "Otras"

df_base["grupo_analitico"] = df_base.apply(asignar_grupo, axis=1)

# =========================
# FUNCIONES
# =========================

def preparar_resumen(data):
    return (
        data.groupby(["seccion", "categoria"], dropna=False)
        .agg(total=("font_url", "count"))
        .reset_index()
        .sort_values("total", ascending=False)
    )

def grafico_barras(data, x, y, color=None, title="", color_map=None, height=None, key=None):
    data = data.sort_values(x, ascending=True)

    # Configuración mejorada del gráfico
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation="h",
        color=color,
        text=x,
        color_discrete_map=color_map or colores,
    )

    # Estilo mejorado para tema oscuro Netflix
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        textfont=dict(size=13, color="#ffffff", family="Arial", weight="bold"),
        marker=dict(
            line=dict(width=0),
            opacity=0.95
        ),
        hovertemplate="<b style='font-size:14px;'>%{y}</b><br><span style='color:#b3b3b3;'>Cantidad:</span> <b style='color:#E50914;'>%{x}</b><extra></extra>"
    )

    # Layout mejorado para tema oscuro
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=18, color="#ffffff", family="Arial Black"),
            x=0,
            xanchor="left"
        ),
        height=height or max(420, len(data) * 45),
        margin=dict(l=240, r=60, t=50, b=40),
        font=dict(size=12, family="Arial", color="#b3b3b3"),
        yaxis=dict(
            title="",
            tickfont=dict(size=13, color="#b3b3b3", family="Arial"),
            showgrid=False
        ),
        xaxis=dict(
            title=dict(text="Número de fuentes", font=dict(size=13, color="#b3b3b3", family="Arial")),
            tickfont=dict(size=11, color="#b3b3b3"),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False
        ),
        showlegend=bool(color),
        plot_bgcolor="rgba(15,15,15,0.5)",
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(
            bgcolor="#262626",
            font_size=13,
            font_family="Arial",
            bordercolor="#E50914"
        )
    )

    # Contenedor con estilo
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key=key)
    st.markdown('</div>', unsafe_allow_html=True)

def pintar_macro_y_expanders(resumen, titulo, key_prefix):
    st.markdown(f"""
    <div class="tab-container">
        <div class="tab-header">{titulo}</div>
    </div>
    """, unsafe_allow_html=True)

    macro = (
        resumen.groupby("seccion", dropna=False)
        .agg(total=("total", "sum"))
        .reset_index()
        .sort_values("total", ascending=False)
    )

    grafico_barras(
        macro,
        x="total",
        y="seccion",
        color="seccion",
        title=f"📊 {titulo}",
        color_map=colores,
        key=f"{key_prefix}_macro",
    )

    st.markdown("### 🎯 Subcategorías desplegables")

    for _, row in macro.iterrows():
        seccion = row["seccion"]
        total = int(row["total"])
        safe_seccion = str(seccion).replace(" ", "_").replace("/", "_")

        with st.expander(f"📁 {seccion} · {total} fuentes", expanded=False):
            subset = resumen[resumen["seccion"] == seccion].copy()

            grafico_barras(
                subset,
                x="total",
                y="categoria",
                color=None,
                title=f"📈 {seccion} · subcategorías",
                height=max(350, len(subset) * 48),
                key=f"{key_prefix}_sub_{safe_seccion}",
            )

            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.dataframe(
                subset.sort_values("total", ascending=False),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABS PRINCIPALES
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "🌟 Todas las categorías",
    "⚖️ Expresivas vs Funcionales",
    "🔍 Diagnóstico CSV",
    "🔎 Explorar datos",
])

# =========================
# TAB 1: TODAS LAS CATEGORÍAS
# =========================

with tab1:
    st.markdown("""
    <div class="tab-container">
        <div class="tab-header">🌟 Todas las categorías</div>
        <p style="color: white; margin: 0; opacity: 0.9;">Vista completa del universo tipográfico de DaFont</p>
    </div>
    """, unsafe_allow_html=True)

    resumen = preparar_resumen(df_base)

    pintar_macro_y_expanders(
        resumen,
        f"Grandes categorías sumadas · {modo}",
        "todas",
    )

# =========================
# TAB 2: EXPRESIVAS VS FUNCIONALES
# =========================

with tab2:
    st.markdown("""
    <div class="tab-container">
        <div class="tab-header">⚖️ Expresivas vs Funcionales</div>
        <p style="color: white; margin: 0; opacity: 0.9;">Comparación entre fuentes expresivas y funcionales</p>
    </div>
    """, unsafe_allow_html=True)

    grupo = (
        df_base.groupby("grupo_analitico", dropna=False)
        .agg(total=("font_url", "count"))
        .reset_index()
        .sort_values("total", ascending=False)
    )

    grafico_barras(
        grupo,
        x="total",
        y="grupo_analitico",
        color="grupo_analitico",
        title=f"🎭 Separación conceptual · {modo}",
        color_map={
            "Expresivas / fantasía / manuscritas": "#E50914",
            "Funcionales / normales": "#00E676",
            "Otras": "#4ECDC4",
        },
        height=430,
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎨 Expresivas / fantasía / manuscritas")
        df_exp = df_base[df_base["grupo_analitico"] == "Expresivas / fantasía / manuscritas"]
        pintar_macro_y_expanders(
            preparar_resumen(df_exp),
            "Categorías expresivas sumadas",
            "expresivas",
        )

    with col2:
        st.markdown("### ⚙️ Funcionales / normales")
        df_fun = df_base[df_base["grupo_analitico"] == "Funcionales / normales"]
        pintar_macro_y_expanders(
            preparar_resumen(df_fun),
            "Categorías funcionales sumadas",
            "funcionales",
        )

# =========================
# TAB 3: DIAGNÓSTICO CSV
# =========================

with tab3:
    st.markdown("""
    <div class="tab-container">
        <div class="tab-header">🔍 Diagnóstico del CSV</div>
        <p style="color: white; margin: 0; opacity: 0.9;">Análisis detallado de la calidad y estructura de tus datos</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{len(df):,}</span>
            <span class="metric-label">📄 Filas totales</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{df['font_url'].nunique():,}</span>
            <span class="metric-label">🔗 URLs únicas</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{df['fuente_normalizada'].nunique():,}</span>
            <span class="metric-label">📝 Nombres únicos</span>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-value">{df['categoria'].nunique():,}</span>
            <span class="metric-label">📂 Categorías</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔄 Duplicados por URL")

    duplicados_url = (
        df.groupby("font_url")
        .agg(
            apariciones=("font_url", "count"),
            fuente=("fuente", "first"),
            categorias=("categoria", lambda x: "; ".join(sorted(set(x)))),
            secciones=("seccion", lambda x: "; ".join(sorted(set(x)))),
        )
        .reset_index()
        .query("apariciones > 1")
        .sort_values("apariciones", ascending=False)
    )

    if duplicados_url.empty:
        st.success("✅ No hay duplicados por URL")
    else:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(duplicados_url, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📝 Duplicados por nombre normalizado")

    duplicados_nombre = (
        df.groupby("fuente_normalizada")
        .agg(
            apariciones=("fuente_normalizada", "count"),
            ejemplos=("fuente", lambda x: "; ".join(sorted(set(x))[:8])),
            categorias=("categoria", lambda x: "; ".join(sorted(set(x))[:8])),
            urls=("font_url", "nunique"),
        )
        .reset_index()
        .query("apariciones > 1")
        .sort_values("apariciones", ascending=False)
    )

    if duplicados_nombre.empty:
        st.info("ℹ️ No hay duplicados claros por nombre normalizado")
    else:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(duplicados_nombre, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📊 Conteo por sección")
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(
        df.groupby("seccion")
        .agg(
            apariciones=("font_url", "count"),
            urls_unicas=("font_url", "nunique"),
            nombres_unicos=("fuente_normalizada", "nunique"),
        )
        .reset_index()
        .sort_values("apariciones", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 4: EXPLORAR DATOS
# =========================

with tab4:
    st.markdown("""
    <div class="tab-container">
        <div class="tab-header">🔎 Explorar datos completos</div>
        <p style="color: white; margin: 0; opacity: 0.9;">Navega y filtra todos los datos de fuentes disponibles</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🎯 Filtros")
        secciones = sorted(df_base["seccion"].dropna().unique())
        seleccion_seccion = st.multiselect(
            "📂 Filtrar por sección",
            secciones,
            default=secciones,
            help="Selecciona las secciones que quieres ver"
        )

    with col2:
        filtrado = df_base[df_base["seccion"].isin(seleccion_seccion)].copy()

        categorias = sorted(filtrado["categoria"].dropna().unique())
        seleccion_categoria = st.multiselect(
            "📁 Filtrar por categoría",
            categorias,
            default=categorias,
            help="Selecciona las categorías que quieres ver"
        )

    filtrado = filtrado[filtrado["categoria"].isin(seleccion_categoria)].copy()

    col1, col2 = st.columns([2, 1])

    with col1:
        busqueda = st.text_input(
            "🔍 Buscar fuente",
            placeholder="Escribe el nombre de una fuente...",
            help="Busca fuentes por nombre"
        )

    with col2:
        st.metric("📊 Resultados", f"{len(filtrado):,}")

    if busqueda:
        filtrado = filtrado[
            filtrado["fuente"].str.contains(busqueda, case=False, na=False)
        ]

    st.write(f"Mostrando **{len(filtrado)}** filas")

    columnas = [
        "seccion",
        "categoria",
        "fuente",
        "font_url",
        "autor",
        "descargas_totales",
        "licencia",
        "preview_url",
    ]

    columnas = [c for c in columnas if c in filtrado.columns]

    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(
        filtrado[columnas],
        use_container_width=True,
        hide_index=True,
        height=700,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(
        filtrado[columnas],
        use_container_width=True,
        hide_index=True,
        height=700,
    )