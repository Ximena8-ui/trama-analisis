import pandas as pd

# ============================================================
#   TRAMA STRATEGY ANALYZER
#   Análisis de competencia de agencias de diseño en Colombia
# ============================================================

# ─────────────────────────────────────────
# 1. CARGAR LA BASE DE DATOS
# ─────────────────────────────────────────
file_name = 'datos/Competencia_Agencias_Colombia_2025-2026.xlsx'

try:
    df = pd.read_excel(file_name)
    df = df.dropna(how='all').reset_index(drop=True)
    df = df.dropna(subset=['ID']).reset_index(drop=True)

    if 'Especialidad' not in df.columns:
        print("Columnas encontradas:", df.columns.tolist())
        raise KeyError("No se encontró la columna 'Especialidad'.")

    print(f"✅ Éxito: Se cargaron {len(df)} agencias para el análisis.\n")

except Exception as e:
    print(f"❌ Error al procesar el archivo: {e}")
    exit()


# ─────────────────────────────────────────
# 2. LIMPIAR Y PREPARAR LOS DATOS
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

# Aplicar limpieza columna por columna
df['Precio_Cat']  = df['Precios (Est.)'].apply(limpiar_precio)
df['Innovacion']  = df['Innovación'].apply(extraer_innovacion)
df['Ciudad']      = df['Ubicación'].apply(detectar_ciudad)


# ─────────────────────────────────────────
# 3. ANÁLISIS 1 — ESPECIALIDADES (tu código original mejorado)
# ─────────────────────────────────────────

def analizar_especialidades(df):
    print("=" * 50)
    print("  ANÁLISIS 1: ESPECIALIDADES DEL MERCADO")
    print("=" * 50)

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

    print("\n--- RESULTADOS DEL ANÁLISIS ---")
    for categoria, total in conteo.items():
        barra = "█" * total
        print(f"  {categoria:<12}: {barra} ({total})")

    print("\n--- TENDENCIA IDENTIFICADA ---")
    ganador = max(conteo, key=conteo.get)
    if conteo[ganador] > 0:
        print(f"  La corriente más fuerte actualmente es: {ganador}.")
        print("  Consejo: Para destacar, busca un sub-nicho que no esté saturado.\n")
    else:
        print("  No se encontraron categorías claras.\n")


# ─────────────────────────────────────────
# 4. ANÁLISIS 2 — PRECIOS DEL MERCADO
# ─────────────────────────────────────────

def analizar_precios(df):
    print("=" * 50)
    print("  ANÁLISIS 2: RANGOS DE PRECIO EN EL MERCADO")
    print("=" * 50)

    conteo_precios = {}

    for i in range(len(df)):
        precio = df.loc[i, 'Precio_Cat']
        if precio in conteo_precios:
            conteo_precios[precio] += 1
        else:
            conteo_precios[precio] = 1

    print("\n--- DISTRIBUCIÓN DE PRECIOS ---")
    orden = ['Inexpensivo', 'Moderado', 'Moderado-Alto', 'Alto', 'Premium']
    for nivel in orden:
        total = conteo_precios.get(nivel, 0)
        barra = "█" * total
        print(f"  {nivel:<14}: {barra} ({total})")

    # Conclusión
    precio_dominante = max(conteo_precios, key=conteo_precios.get)
    print(f"\n  💡 El precio dominante en el mercado es: {precio_dominante}.")
    print(f"  El segmento 'Moderado-Alto' tiene {conteo_precios.get('Moderado-Alto', 0)} agencias — es el hueco con más potencial.\n")


# ─────────────────────────────────────────
# 5. ANÁLISIS 3 — INNOVACIÓN POR CIUDAD
# ─────────────────────────────────────────

def analizar_innovacion(df):
    print("=" * 50)
    print("  ANÁLISIS 3: INNOVACIÓN POR CIUDAD")
    print("=" * 50)

    ciudades = ['Bogotá', 'Medellín', 'Cali', 'Remota']
    resultados = {}

    for ciudad in ciudades:
        agencias_ciudad = []
        for i in range(len(df)):
            if df.loc[i, 'Ciudad'] == ciudad:
                agencias_ciudad.append(df.loc[i, 'Innovacion'])

        if len(agencias_ciudad) > 0:
            promedio = sum(agencias_ciudad) / len(agencias_ciudad)
            resultados[ciudad] = round(promedio, 1)

    print("\n--- PROMEDIO DE INNOVACIÓN (escala 1-5) ---")
    for ciudad, promedio in resultados.items():
        estrellas = "★" * int(promedio) + "☆" * (5 - int(promedio))
        print(f"  {ciudad:<10}: {estrellas}  ({promedio}/5)")

    ciudad_top = max(resultados, key=resultados.get)
    print(f"\n  🏆 Ciudad más innovadora: {ciudad_top} con {resultados[ciudad_top]}/5\n")


# ─────────────────────────────────────────
# 6. ANÁLISIS 4 — MAPA DE POSICIONAMIENTO
# ─────────────────────────────────────────

def mapa_posicionamiento(df):
    print("=" * 50)
    print("  ANÁLISIS 4: MAPA DE POSICIONAMIENTO COMPETITIVO")
    print("=" * 50)

    orden_precio = {'Inexpensivo': 1, 'Moderado': 2, 'Moderado-Alto': 3, 'Alto': 4, 'Premium': 5}
    etiquetas_precio = {1: 'Inexpensivo', 2: 'Moderado', 3: 'Mod-Alto', 4: 'Alto', 5: 'Premium'}

    # Mapa de 5x5: precio (columnas) vs innovación (filas)
    mapa = {}
    for i in range(len(df)):
        precio_num = orden_precio.get(df.loc[i, 'Precio_Cat'], 0)
        innov      = df.loc[i, 'Innovacion']
        if precio_num > 0 and innov > 0:
            clave = (innov, precio_num)
            mapa[clave] = mapa.get(clave, 0) + 1

    print("\n  Cada número = cuántas agencias ocupan ese cuadrante")
    print("  (★) = Zona estratégica recomendada para TRAMA\n")
    print(f"  {'':>12}", end="")
    for p in range(1, 6):
        print(f"  {etiquetas_precio[p]:<10}", end="")
    print()
    print("  " + "-" * 70)

    for innov in range(5, 0, -1):
        print(f"  Innov {innov}/5  |", end="")
        for precio in range(1, 6):
            cantidad = mapa.get((innov, precio), 0)
            # Marcar zona TRAMA
            if innov >= 4 and precio == 3:
                celda = f"  [★{cantidad}]      "
            else:
                celda = f"  {cantidad}          " if cantidad == 0 else f"  {cantidad}          "
            print(celda[:13], end="")
        print()

    print("\n  💡 La zona [★] (Moderado-Alto + Innovación 4-5) es donde")
    print("     TRAMA tiene la mayor oportunidad con menos competidores.\n")


# ─────────────────────────────────────────
# 7. CHATBOT ESTRATÉGICO
# ─────────────────────────────────────────

def chatbot(df):
    print("=" * 50)
    print("  CHATBOT ESTRATÉGICO DE TRAMA")
    print("=" * 50)
    print("  Pregúntame sobre la competencia.")
    print("  Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("  Tú → ").strip().lower()

        if pregunta == 'salir':
            print("  Bot → ¡Hasta pronto! Mucho éxito con TRAMA. 🖤\n")
            break

        elif pregunta == '':
            continue

        # ── ¿Quién es el más innovador? ──────────────────
        elif any(p in pregunta for p in ['más innovador', 'mas innovador', 'mayor innovación', 'innova más']):
            top = df.nlargest(3, 'Innovacion')[['Nombre de la Agencia', 'Ciudad', 'Innovacion', 'Especialidad']]
            print("\n  Bot → Las 3 agencias más innovadoras son:")
            for _, fila in top.iterrows():
                print(f"        • {fila['Nombre de la Agencia']} ({fila['Ciudad']}) — Nivel {fila['Innovacion']}/5 — {fila['Especialidad']}")
            print()

        # ── Nichos disponibles ───────────────────────────
        elif any(p in pregunta for p in ['nicho', 'espacio', 'oportunidad', 'saturado']):
            print("\n  Bot → Según los datos, los nichos con menor competencia son:")
            print("        • Emprendedores con ambición de marca (precio moderado-alto)")
            print("        • Marcas emergentes que buscan creatividad + estrategia")
            print("        • Sector moda/estilo de vida en Bogotá (solo 1 agencia directa)")
            print("        💡 TRAMA podría ser la agencia de branding estratégico para")
            print("           marcas que crecen — ni tan cara como las premium,")
            print("           ni tan genérica como las moderadas.\n")

        # ── Debilidades de la competencia ────────────────
        elif any(p in pregunta for p in ['debilidad', 'punto débil', 'flaqueza', 'falla']):
            debilidades_comunes = []
            for i in range(len(df)):
                d = str(df.loc[i, 'Debilidad a Mejorar']).lower()
                if 'personaliz' in d or 'escala' in d:
                    debilidades_comunes.append('falta de personalización')
                elif 'creativ' in d:
                    debilidades_comunes.append('creatividad limitada')
                elif 'ia' in d or 'inteligencia' in d:
                    debilidades_comunes.append('sin uso de IA')

            conteo_d = {}
            for d in debilidades_comunes:
                conteo_d[d] = conteo_d.get(d, 0) + 1

            print("\n  Bot → Debilidades más repetidas en la competencia:")
            for d, c in sorted(conteo_d.items(), key=lambda x: -x[1]):
                print(f"        • {d.capitalize()}: {c} agencias")
            print("        💡 Esas son tus oportunidades de diferenciación.\n")

        # ── Buscar agencia por nombre ─────────────────────
        elif any(p in pregunta for p in ['buscar', 'información de', 'dime sobre', 'quién es']):
            print("\n  Bot → ¿Cuál es el nombre de la agencia que buscas?")
            nombre = input("  Tú (nombre) → ").strip().lower()
            encontrada = False
            for i in range(len(df)):
                if nombre in str(df.loc[i, 'Nombre de la Agencia']).lower():
                    fila = df.loc[i]
                    print(f"\n        📋 {fila['Nombre de la Agencia']} — {fila['Ciudad']}")
                    print(f"        Especialidad : {fila['Especialidad']}")
                    print(f"        Precio       : {fila['Precio_Cat']}")
                    print(f"        Innovación   : {fila['Innovacion']}/5")
                    print(f"        Nicho        : {fila['Nicho de Mercado']}")
                    print(f"        Debilidad    : {fila['Debilidad a Mejorar']}\n")
                    encontrada = True
                    break
            if not encontrada:
                print(f"  Bot → No encontré '{nombre}' en la base de datos. Verifica el nombre.\n")

        # ── Agencias por ciudad ───────────────────────────
        elif any(p in pregunta for p in ['bogotá', 'bogota', 'medellín', 'medellin', 'cali', 'ciudad']):
            if 'bogot' in pregunta:
                ciudad_buscada = 'Bogotá'
            elif 'medell' in pregunta:
                ciudad_buscada = 'Medellín'
            elif 'cali' in pregunta:
                ciudad_buscada = 'Cali'
            else:
                ciudad_buscada = None

            if ciudad_buscada:
                agencias = []
                for i in range(len(df)):
                    if df.loc[i, 'Ciudad'] == ciudad_buscada:
                        agencias.append(df.loc[i, 'Nombre de la Agencia'])
                print(f"\n  Bot → Hay {len(agencias)} agencias en {ciudad_buscada}:")
                for a in agencias:
                    print(f"        • {a}")
                print()

        # ── Recomendación para TRAMA ──────────────────────
        elif any(p in pregunta for p in ['trama', 'recomendación', 'recomendacion', 'consejo', 'posicion']):
            print("\n  Bot → 🎯 Recomendación estratégica para TRAMA:")
            print()
            print("        POSICIONAMIENTO SUGERIDO:")
            print("        • Precio    → Moderado-Alto")
            print("        • Innovación → Nivel 4–5 (usar IA + storytelling)")
            print("        • Nicho     → Marcas emergentes con propósito")
            print("        • Ciudad    → Bogotá (mayor mercado, más competencia")
            print("                      pero también más oportunidad)")
            print()
            print("        DIFERENCIAL CLAVE:")
            print("        • La mayoría de agencias son o muy técnicas (sin alma)")
            print("          o muy artísticas (sin estrategia).")
            print("        • TRAMA puede ser el punto medio: branding con")
            print("          estrategia real + estética auténtica.")
            print()
            print("        DEBILIDADES A EXPLOTAR de la competencia:")
            print("        • Las Premium son inaccesibles para marcas medianas.")
            print("        • Las Moderadas son genéricas y sin diferenciación.")
            print("        • Pocas usan IA de forma creativa — ahí está el gap.\n")

        # ── Listar todas las agencias ─────────────────────
        elif any(p in pregunta for p in ['listar', 'lista', 'todas', 'mostrar todas']):
            print(f"\n  Bot → Las {len(df)} agencias en la base de datos:\n")
            for i in range(len(df)):
                nombre   = df.loc[i, 'Nombre de la Agencia']
                ciudad   = df.loc[i, 'Ciudad']
                precio   = df.loc[i, 'Precio_Cat']
                innov    = df.loc[i, 'Innovacion']
                print(f"        {int(df.loc[i,'ID']):>2}. {nombre:<25} {ciudad:<10} {precio:<14} Innov:{innov}/5")
            print()

        # ── Ayuda ─────────────────────────────────────────
        elif any(p in pregunta for p in ['ayuda', 'help', 'qué puedes', 'que puedes', 'opciones']):
            print("\n  Bot → Puedes preguntarme:")
            print("        • '¿Quién es el más innovador?'")
            print("        • '¿Qué nichos están disponibles?'")
            print("        • '¿Cuáles son las debilidades de la competencia?'")
            print("        • 'Buscar' (para ver info de una agencia específica)")
            print("        • '¿Cuántas agencias hay en Bogotá?'")
            print("        • '¿Dónde debería posicionarse TRAMA?'")
            print("        • 'Listar todas' (para ver todas las agencias)")
            print("        • 'salir' para terminar\n")

        else:
            print("  Bot → No entendí bien la pregunta. Escribe 'ayuda' para ver")
            print("        qué puedo responderte.\n")


# ─────────────────────────────────────────
# 8. MENÚ PRINCIPAL
# ─────────────────────────────────────────

def menu():
    print("\n" + "═" * 50)
    print("   🖤  TRAMA STRATEGY ANALYZER  🖤")
    print("   Análisis de Competencia — Colombia 2025–2026")
    print("═" * 50)

    while True:
        print("\n  ¿Qué quieres hacer?")
        print("  [1] Análisis de especialidades")
        print("  [2] Análisis de precios")
        print("  [3] Innovación por ciudad")
        print("  [4] Mapa de posicionamiento")
        print("  [5] Chatbot estratégico")
        print("  [6] Ejecutar todo el análisis")
        print("  [0] Salir")

        opcion = input("\n  Tu opción → ").strip()

        if opcion == '1':
            print()
            analizar_especialidades(df)
        elif opcion == '2':
            print()
            analizar_precios(df)
        elif opcion == '3':
            print()
            analizar_innovacion(df)
        elif opcion == '4':
            print()
            mapa_posicionamiento(df)
        elif opcion == '5':
            print()
            chatbot(df)
        elif opcion == '6':
            print()
            analizar_especialidades(df)
            analizar_precios(df)
            analizar_innovacion(df)
            mapa_posicionamiento(df)
        elif opcion == '0':
            print("\n  ¡Hasta pronto! Mucho éxito con TRAMA. 🖤\n")
            break
        else:
            print("  Opción no válida. Intenta de nuevo.")


# ─────────────────────────────────────────
# EJECUTAR EL PROGRAMA
# ─────────────────────────────────────────
menu()