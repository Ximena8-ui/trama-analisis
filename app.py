import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
#   TRAMA STRATEGY ANALYZER — Versión Streamlit
#   Análisis de competencia de agencias de diseño en Colombia
# ============================================================

st.set_page_config(
    page_title="TRAMA Strategy Analyzer",
    page_icon="🖤",
    layout="wide"
)

# ─────────────────────────────────────────
# 1. CARGAR LA BASE DE DATOS
#    ✅ Ruta relativa al repositorio GitHub
#    ❌ Ya NO usa Google Drive
# ─────────────────────────────────────────

@st.cache_data
def cargar_datos():
    file_name = 'datos/Competencia_Agencias_Colombia_2025-2026.xlsx'  # ← ruta GitHub

    try:
        df = pd.read_excel(file_name)
        df = df.dropna(how='all').reset_index(drop=True)
        df = df.dropna(subset=['ID']).reset_index(drop=True)

        if 'Especialidad' not in df.columns:
            st.error(f"Columnas encontradas: {df.columns.tolist()}")
            st.stop()

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        st.stop()


# ─────────────────────────────────────────
# 2. LIMPIAR Y PREPARAR LOS DATOS
#    (mismas funciones del código original)
# ─────────────────────────────────────────

def limpiar_precio(texto):
    """Clasifica el precio en una categoría estándar."""
    texto = str(texto).lower()
    if 'inexpensivo' in texto:
        return 'Inexpensivo'
    elif 'premium' in texto:
        return 'Premium'
    elif 'alto' in texto and 'moderado' not in texto:
        return 'Alto'
    elif 'moderado' in texto and 'alto' in texto:
        return 'Moderado-Alto'
    elif 'moderado' in texto:
        return 'Moderado'
    return 'No especificado'

def extraer_innovacion(texto):
    """Extrae el número de innovación del texto."""
    texto = str(texto)
    for caracter in texto:
        if caracter.isdigit():
            return int(caracter)
    return 0

def detectar_ciudad(texto):
    """Detecta la ciudad principal de la agencia."""
    texto = str(texto)
    if 'Medellín' in texto or 'Medellin' in texto:
        return 'Medellín'
    elif 'Cali' in texto:
        return 'Cali'
    elif 'Remota' in texto:
        return 'Remota'
    return 'Bogotá'

def contar_especialidades(df):
    """Cuenta agencias por categoría de especialidad (ciclo FOR + IF del código original)."""
    conteo = {"Diseño": 0, "Marketing": 0, "Publicidad": 0, "Branding": 0, "Tecnología": 0}
    for i in range(len(df)):
        valor = str(df.loc[i, 'Especialidad']).lower()
        if "diseño" in valor:
            conteo["Diseño"] += 1
        elif "marketing" in valor:
            conteo["Marketing"] += 1
        elif "publicidad" in valor:
            conteo["Publicidad"] += 1
        elif "branding" in valor:
            conteo["Branding"] += 1
        elif "tecnología" in valor or "tecnologia" in valor or "tech" in valor:
            conteo["Tecnología"] += 1
    return conteo

def responder_chatbot(pregunta, df):
    """Lógica del chatbot estratégico (mismo código original, adaptado para Streamlit)."""
    p = pregunta.lower()

    if any(x in p for x in ['más innovador', 'mas innovador', 'mayor innovación', 'innova más']):
        top = df.nlargest(3, 'Innovacion')[['Nombre de la Agencia', 'Ciudad', 'Innovacion', 'Especialidad']]
        resp = "**🏆 Las 3 agencias más innovadoras:**\n\n"
        for _, fila in top.iterrows():
            resp += f"- **{fila['Nombre de la Agencia']}** ({fila['Ciudad']}) — Nivel {fila['Innovacion']}/5 — {fila['Especialidad']}\n"
        return resp

    elif any(x in p for x in ['nicho', 'espacio', 'oportunidad', 'saturado']):
        return (
            "**🎯 Nichos con menor competencia:**\n\n"
            "- Emprendedores con ambición de marca (precio moderado-alto)\n"
            "- Marcas emergentes que buscan creatividad + estrategia\n"
            "- Sector moda/estilo de vida en Bogotá (solo 1 agencia directa)\n\n"
            "💡 **TRAMA** podría ser la agencia de branding estratégico para marcas que crecen — "
            "ni tan cara como las premium, ni tan genérica como las moderadas."
        )

    elif any(x in p for x in ['debilidad', 'punto débil', 'flaqueza', 'falla']):
        debilidades_comunes = []
        for i in range(len(df)):
            d = str(df.loc[i, 'Debilidad a Mejorar']).lower()
            if 'personaliz' in d or 'escala' in d:
                debilidades_comunes.append('Falta de personalización')
            elif 'creativ' in d:
                debilidades_comunes.append('Creatividad limitada')
            elif 'ia' in d or 'inteligencia' in d:
                debilidades_comunes.append('Sin uso de IA')

        conteo_d = {}
        for d in debilidades_comunes:
            conteo_d[d] = conteo_d.get(d, 0) + 1

        resp = "**⚠️ Debilidades más repetidas en la competencia:**\n\n"
        for d, c in sorted(conteo_d.items(), key=lambda x: -x[1]):
            resp += f"- {d}: {c} agencias\n"
        resp += "\n💡 Esas son tus oportunidades de diferenciación."
        return resp

    elif any(x in p for x in ['bogotá', 'bogota', 'medellín', 'medellin', 'cali']):
        if 'bogot' in p:
            ciudad_buscada = 'Bogotá'
        elif 'medell' in p:
            ciudad_buscada = 'Medellín'
        else:
            ciudad_buscada = 'Cali'

        agencias = []
        for i in range(len(df)):
            if df.loc[i, 'Ciudad'] == ciudad_buscada:
                agencias.append(df.loc[i, 'Nombre de la Agencia'])

        resp = f"**🏙️ {len(agencias)} agencias en {ciudad_buscada}:**\n\n"
        for a in agencias:
            resp += f"- {a}\n"
        return resp

    elif any(x in p for x in ['trama', 'recomendación', 'recomendacion', 'consejo', 'posicion', 'donde']):
        return (
            "**🎯 Recomendación estratégica para TRAMA:**\n\n"
            "**Posicionamiento sugerido:**\n"
            "- 💰 Precio → Moderado-Alto\n"
            "- 💡 Innovación → Nivel 4–5 (usar IA + storytelling)\n"
            "- 🎯 Nicho → Marcas emergentes con propósito\n"
            "- 🏙️ Ciudad → Bogotá\n\n"
            "**Diferencial clave:**\n"
            "La mayoría de agencias son o muy técnicas (sin alma) o muy artísticas (sin estrategia). "
            "TRAMA puede ser el punto medio: branding con estrategia real + estética auténtica.\n\n"
            "**Debilidades a explotar:**\n"
            "- Las Premium son inaccesibles para marcas medianas\n"
            "- Las Moderadas son genéricas y sin diferenciación\n"
            "- Pocas usan IA de forma creativa — ahí está el gap 🚀"
        )

    elif any(x in p for x in ['ayuda', 'help', 'qué puedes', 'que puedes', 'opciones']):
        return (
            "**💬 Puedes preguntarme:**\n\n"
            "- ¿Quién es el más innovador?\n"
            "- ¿Qué nichos están disponibles?\n"
            "- ¿Cuáles son las debilidades de la competencia?\n"
            "- ¿Cuántas agencias hay en Bogotá / Medellín / Cali?\n"
            "- ¿Dónde debería posicionarse TRAMA?\n"
        )

    else:
        # Búsqueda por nombre de agencia
        for i in range(len(df)):
            nombre_ag = str(df.loc[i, 'Nombre de la Agencia']).lower()
            if any(palabra in nombre_ag for palabra in p.split() if len(palabra) > 3):
                fila = df.loc[i]
                return (
                    f"**📋 {fila['Nombre de la Agencia']}** — {fila['Ciudad']}\n\n"
                    f"- **Especialidad:** {fila['Especialidad']}\n"
                    f"- **Precio:** {fila['Precio_Cat']}\n"
                    f"- **Innovación:** {fila['Innovacion']}/5\n"
                    f"- **Nicho:** {fila['Nicho de Mercado']}\n"
                    f"- **Debilidad:** {fila['Debilidad a Mejorar']}\n"
                )

        return "No entendí bien la pregunta. Escribe **ayuda** para ver qué puedo responderte."


# ─────────────────────────────────────────
# 3. CARGAR Y PREPARAR DATOS
# ─────────────────────────────────────────

df = cargar_datos()
df['Precio_Cat']  = df['Precios (Est.)'].apply(limpiar_precio)
df['Innovacion']  = df['Innovación'].apply(extraer_innovacion)
df['Ciudad']      = df['Ubicación'].apply(detectar_ciudad)

# Orden para gráficas
orden_precio = ['Inexpensivo', 'Moderado', 'Moderado-Alto', 'Alto', 'Premium']
colores_ciudad = {
    'Bogotá': '#3266ad',
    'Medellín': '#5DCAA5',
    'Cali': '#EF9F27',
    'Remota': '#E24B4A'
}

# ─────────────────────────────────────────
# 4. INTERFAZ — ENCABEZADO
# ─────────────────────────────────────────

st.markdown("## 🖤 TRAMA Strategy Analyzer")
st.markdown("**Análisis de competencia de agencias de diseño en Colombia 2025–2026**")
st.divider()

# Métricas rápidas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total agencias", len(df))
col2.metric("Ciudades", df['Ciudad'].nunique())
col3.metric("Más innovadoras", len(df[df['Innovacion'] == 5]))
col4.metric("Precio dominante", df['Precio_Cat'].value_counts().idxmax())

st.divider()

# ─────────────────────────────────────────
# 5. PESTAÑAS PRINCIPALES
# ─────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Especialidades",
    "💰 Precios e Innovación",
    "🎯 Mapa de posicionamiento",
    "💬 Chatbot estratégico"
])


# ── TAB 1: ESPECIALIDADES ─────────────────
with tab1:
    st.subheader("Análisis de especialidades del mercado")
    st.caption("Ciclo FOR + IF/ELIF del código original aplicado a los datos reales")

    conteo = contar_especialidades(df)
    ganador = max(conteo, key=conteo.get)

    fig = px.bar(
        x=list(conteo.keys()),
        y=list(conteo.values()),
        labels={'x': 'Especialidad', 'y': 'Número de agencias'},
        color=list(conteo.values()),
        color_continuous_scale='teal',
        text=list(conteo.values())
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"**Tendencia dominante:** {ganador} con {conteo[ganador]} agencias. "
            f"Para destacar, busca un sub-nicho que no esté saturado.")


# ── TAB 2: PRECIOS E INNOVACIÓN ───────────
with tab2:
    st.subheader("Distribución de precios e innovación")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Agencias por rango de precio**")
        conteo_precios = {}
        for i in range(len(df)):
            precio = df.loc[i, 'Precio_Cat']
            conteo_precios[precio] = conteo_precios.get(precio, 0) + 1

        datos_precio = [(nivel, conteo_precios.get(nivel, 0)) for nivel in orden_precio]
        fig2 = px.bar(
            x=[d[0] for d in datos_precio],
            y=[d[1] for d in datos_precio],
            color=[d[1] for d in datos_precio],
            color_continuous_scale='teal',
            text=[d[1] for d in datos_precio],
            labels={'x': 'Precio', 'y': 'Agencias'}
        )
        fig2.update_traces(textposition='outside')
        fig2.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown("**Innovación promedio por ciudad**")
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Remota']
        promedios = []
        for ciudad in ciudades:
            valores = []
            for i in range(len(df)):
                if df.loc[i, 'Ciudad'] == ciudad:
                    valores.append(df.loc[i, 'Innovacion'])
            if valores:
                promedios.append(round(sum(valores) / len(valores), 1))
            else:
                promedios.append(0)

        fig3 = px.bar(
            x=ciudades,
            y=promedios,
            color=ciudades,
            color_discrete_map=colores_ciudad,
            text=promedios,
            labels={'x': 'Ciudad', 'y': 'Innovación promedio (1-5)'}
        )
        fig3.update_traces(textposition='outside')
        fig3.update_layout(showlegend=False, height=350, yaxis_range=[0, 5.5])
        st.plotly_chart(fig3, use_container_width=True)

    st.info(f"💡 El segmento **Moderado-Alto** tiene {conteo_precios.get('Moderado-Alto', 0)} agencias "
            f"— es el hueco con más potencial para TRAMA.")


# ── TAB 3: MAPA DE POSICIONAMIENTO ───────
with tab3:
    st.subheader("Mapa de posicionamiento competitivo")
    st.caption("Precio vs. Innovación — la zona verde es la oportunidad de TRAMA")

    orden_num = {'Inexpensivo': 1, 'Moderado': 2, 'Moderado-Alto': 3, 'Alto': 4, 'Premium': 5}

    scatter_data = []
    for i in range(len(df)):
        scatter_data.append({
            'Agencia': df.loc[i, 'Nombre de la Agencia'],
            'Ciudad': df.loc[i, 'Ciudad'],
            'Precio_Num': orden_num.get(df.loc[i, 'Precio_Cat'], 0),
            'Precio': df.loc[i, 'Precio_Cat'],
            'Innovacion': df.loc[i, 'Innovacion'],
            'Nicho': df.loc[i, 'Nicho de Mercado'],
        })

    df_scatter = pd.DataFrame(scatter_data)

    fig4 = px.scatter(
        df_scatter,
        x='Precio_Num',
        y='Innovacion',
        color='Ciudad',
        color_discrete_map=colores_ciudad,
        hover_name='Agencia',
        hover_data={'Precio': True, 'Nicho': True, 'Precio_Num': False},
        labels={'Precio_Num': 'Rango de Precio', 'Innovacion': 'Nivel de Innovación (1-5)'},
        height=500
    )

    # Zona TRAMA
    fig4.add_shape(
        type="rect",
        x0=2.6, x1=3.4, y0=3.7, y1=5.3,
        fillcolor="rgba(34, 197, 94, 0.12)",
        line=dict(color="#22c55e", width=2, dash="dash")
    )
    fig4.add_annotation(
        x=3, y=5.4,
        text="⭐ Zona TRAMA",
        showarrow=False,
        font=dict(color="#22c55e", size=13)
    )
    fig4.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Inexpensivo', 'Moderado', 'Mod-Alto', 'Alto', 'Premium']
        )
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.success("**Zona estratégica para TRAMA:** Moderado-Alto + Innovación 4–5. "
               "Solo 5 agencias compiten aquí y ninguna combina creatividad emocional + estrategia digital.")


# ── TAB 4: CHATBOT ────────────────────────
with tab4:
    st.subheader("Chatbot estratégico de TRAMA")
    st.caption("Pregúntame sobre la competencia, nichos, o dónde posicionarte")

    # Inicializar historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"rol": "bot", "texto": "¡Hola! Soy el analizador estratégico de TRAMA 🖤 "
             "Tengo cargados los datos de las 49 agencias. Escribe **ayuda** para ver qué puedo responderte."}
        ]

    # Mostrar historial
    for msg in st.session_state.mensajes:
        if msg["rol"] == "bot":
            with st.chat_message("assistant"):
                st.markdown(msg["texto"])
        else:
            with st.chat_message("user"):
                st.markdown(msg["texto"])

    # Input del usuario
    pregunta = st.chat_input("Escribe tu pregunta aquí...")

    if pregunta:
        st.session_state.mensajes.append({"rol": "user", "texto": pregunta})
        respuesta = responder_chatbot(pregunta, df)
        st.session_state.mensajes.append({"rol": "bot", "texto": respuesta})
        st.rerun()
