import streamlit as st
import pandas as pd
import os
from collections import Counter

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Encuentra tu estilo",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .stApp {
        background-color: #FDFBF7;
        color: #2D231E;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stHeaderActionElements"], .stHeaderActionElements, a.anchor-link {
        display: none !important;
    }

    .css-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(74, 59, 50, 0.08);
        margin-bottom: 20px;
        border: 1px solid rgba(226, 210, 203, 0.5);
    }

    .stButton>button {
        background-color: #9A536B;
        color: white;
        border-radius: 30px;
        padding: 0.5rem 1.5rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #7B3E53;
        color: white;
        box-shadow: 0 4px 12px rgba(154, 83, 107, 0.4);
    }

    h1, h2, h3 {
        color: #2D231E !important;
        font-family: Georgia, serif;
    }
    p, label, span, .streamlit-expanderHeader {
        color: #3E302A !important;
        font-size: 1.02rem;
    }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS (CSV) ---
@st.cache_data
def cargar_datos():
    ruta_csv = "Base_de_datos_moda_Prendas.csv"
    if os.path.exists(ruta_csv):
        try:
            return pd.read_csv(ruta_csv)
        except Exception:
            pass
    data = {
        "nombre_prenda": ["Jeans rectos", "Camiseta blanca básica", "Cárdigan rosa pastel", "Blazer estructurado", "Vestido midi floreado", "Tenis blancos casuales", "Pantalón amplio beige", "Blusa suave satinada"],
        "color": ["Azul", "Blanco", "Rosa", "Negro", "Multicolor", "Blanco", "Beige", "Rosa claro"],
        "categoria": ["Partes inferiores", "Tops", "Capas", "Capas", "Vestidos", "Zapatos", "Partes inferiores", "Tops"],
        "estilo": ["Casual", "Minimalista", "Coquette", "Old money", "Romántico", "Casual", "Minimalista", "Elegante"],
        "temporada": ["Todo el año", "Todo el año", "Invierno/Otoño", "Otoño", "Primavera/Verano", "Todo el año", "Todo el año", "Primavera"],
        "formalidad": ["Casual", "Casual", "Casual", "Formal", "Semi-formal", "Casual", "Casual", "Semi-formal"]
    }
    return pd.DataFrame(data)

df_prendas = cargar_datos()

# --- INICIALIZAR ESTADOS ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []
if 'test_paso' not in st.session_state:
    st.session_state.test_paso = 1
if 'respuestas_test' not in st.session_state:
    st.session_state.respuestas_test = {}
if 'resultado_estilo' not in st.session_state:
    st.session_state.resultado_estilo = None

# --- NAVEGACIÓN SUPERIOR ---
col_logo, col_nav = st.columns([2, 5])
with col_logo:
    st.markdown("### ✨ Encuentra tu estilo")

with col_nav:
    nav_cols = st.columns(7)
    with nav_cols[0]:
        if st.button("Inicio", key="n_inicio"): st.session_state.pagina_actual = "Inicio"
    with nav_cols[1]:
        if st.button("Test", key="n_test"): st.session_state.pagina_actual = "Test"
    with nav_cols[2]:
        if st.button("Estilos", key="n_estilos"): st.session_state.pagina_actual = "Estilos"
    with nav_cols[3]:
        if st.button("Outfits", key="n_outfits"): st.session_state.pagina_actual = "Outfits"
    with nav_cols[4]:
        if st.button("Mi armario", key="n_armario"): st.session_state.pagina_actual = "Mi armario"
    with nav_cols[5]:
        if st.button("Consejos", key="n_consejos"): st.session_state.pagina_actual = "Consejos"
    with nav_cols[6]:
        fav_count = len(st.session_state.favoritos)
        if st.button(f"Favoritos ({fav_count})", key="n_fav"): st.session_state.pagina_actual = "Favoritos"

st.markdown("<hr style='border: 1px solid #E2D2CB; margin-top: 0px;'>", unsafe_allow_html=True)

# ==========================================
# 1. INICIO
# ==========================================
if st.session_state.pagina_actual == "Inicio":
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("<p style='color: #9A536B; font-weight: 700; letter-spacing: 1px;'>UN ESPACIO PARA DESCUBRIRTE</p>", unsafe_allow_html=True)
        st.markdown("# Tu estilo, tu decisión")
        st.markdown("<p style='font-size: 1.1rem; line-height: 1.5;'>Explora prendas, colores y combinaciones que conecten contigo, sin etiquetas ni reglas rígidas.</p>", unsafe_allow_html=True)
        
        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("Descubre tu estilo"):
                st.session_state.pagina_actual = "Test"
                st.rerun()
        with bc2:
            if st.button("Ver ideas de outfits"):
                st.session_state.pagina_actual = "Outfits"
                st.rerun()
                
        st.markdown("<br><p style='font-size: 0.95rem; border-left: 3px solid #9A536B; padding-left: 12px; color: #2D231E;'><b>|</b> No tienes que encajar en un estilo, puedes crear el tuyo.</p>", unsafe_allow_html=True)
        
    with c2:
        st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80", use_container_width=True)

# ==========================================
# 2. TEST INTERACTIVO
# ==========================================
elif st.session_state.pagina_actual == "Test":
    st.markdown("### 01 / TU PUNTO DE PARTIDA")
    st.markdown("## Un test para explorar")
    st.markdown("<p>Cinco preguntas breves. Elige lo que más se acerque a ti hoy.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    
    if st.session_state.resultado_estilo is not None:
        res = st.session_state.resultado_estilo
        st.markdown(f"### 🎉 Tu resultado: **Estilo {res['nombre']}**")
        st.markdown(f"<p style='font-size: 1.1rem; color: #9A536B; font-weight: bold;'>Categoría: {res['tag']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{res['desc']}</p>", unsafe_allow_html=True)
        st.info(f"💡 Sugerencia: Explora las prendas del filtro **{res['nombre']}** en la sección de Outfits.")
        
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            if st.button("Guardar estilo en Favoritos"):
                if res['nombre'] not in st.session_state.favoritos:
                    st.session_state.favoritos.append(res['nombre'])
                    st.success("¡Guardado en Favoritos con éxito!")
        with c_res2:
            if st.button("Reiniciar test"):
                st.session_state.test_paso = 1
                st.session_state.respuestas_test = {}
                st.session_state.resultado_estilo = None
                st.rerun()
    else:
        paso = st.session_state.test_paso
        st.markdown(f"**Tu recorrido** ({paso} de 5)")
        st.progress(paso * 20)
        
        if paso == 1:
            st.markdown("#### 1. ¿Qué tipo de prendas te gusta elegir?")
            op = st.radio("Opciones:", [
                ("Jeans y camisetas", "Casual"),
                ("Vestidos y faldas", "Romántico"),
                ("Prendas amplias y llamativas", "Streetwear"),
                ("Básicos de líneas limpias", "Minimalista")
            ], format_func=lambda x: x[0], label_visibility="collapsed")
            st.session_state.respuestas_test[1] = op[1]

        elif paso == 2:
            st.markdown("#### 2. ¿Qué gama de colores prefieres para tu día a día?")
            op = st.radio("Opciones:", [
                ("Tonos neutros y tierra", "Minimalista"),
                ("Tonos pastel y suaves", "Coquette"),
                ("Colores vivos y llamativos", "Streetwear"),
                ("Elegante sobrio (negro/marfil)", "Old money")
            ], format_func=lambda x: x[0], label_visibility="collapsed")
            st.session_state.respuestas_test[2] = op[1]

        elif paso == 3:
            st.markdown("#### 3. ¿Cómo describes tu nivel de comodidad ideal?")
            op = st.radio("Opciones:", [
                ("Ultra relajado y suelto", "Casual"),
                ("Estructurado y formal", "Elegante"),
                ("Texturas fluidas y libre", "Boho"),
                ("Dinámico y deportivo", "Deportivo")
            ], format_func=lambda x: x[0], label_visibility="collapsed")
            st.session_state.respuestas_test[3] = op[1]

        elif paso == 4:
            st.markdown("#### 4. ¿Cuál es tu calzado de cabecera?")
            op = st.radio("Opciones:", [
                ("Tenis cómodos", "Casual"),
                ("Mocasines o zapatos planos", "Old money"),
                ("Zapatos con toque retro", "Y2K"),
                ("Zapatos cómodos delicados", "Coquette")
            ], format_func=lambda x: x[0], label_visibility="collapsed")
            st.session_state.respuestas_test[4] = op[1]

        elif paso == 5:
            st.markdown("#### 5. ¿Qué palabras definen mejor tu vibra de vestimenta?")
            op = st.radio("Opciones:", [
                ("Práctica y cotidiana", "Casual"),
                ("Pulida y refinada", "Elegante"),
                ("Dulce y femenina", "Romántico"),
                ("Única y audaz", "Streetwear")
            ], format_func=lambda x: x[0], label_visibility="collapsed")
            st.session_state.respuestas_test[5] = op[1]
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns([1, 6])
        with col_b1:
            if paso > 1:
                if st.button("Atrás"):
                    st.session_state.test_paso -= 1
                    st.rerun()
            else:
                if st.button("Inicio"):
                    st.session_state.pagina_actual = "Inicio"
                    st.rerun()
                    
        with col_b2:
            if paso < 5:
                if st.button("Siguiente"):
                    st.session_state.test_paso += 1
                    st.rerun()
            else:
                if st.button("Ver mi resultado final"):
                    conteo = Counter(st.session_state.respuestas_test.values())
                    estilo_ganador = conteo.most_common(1)[0][0]
                    
                    dicc_estilos = {
                        "Casual": {"tag": "01 • CÓMODO", "nombre": "Casual", "desc": "Te priorizas sintiéndote cómoda y ligera sin complicarte, usando piezas clave que sirven para todo el día."},
                        "Minimalista": {"tag": "02 • ESENCIAL", "nombre": "Minimalista", "desc": "Líneas limpias, tonos neutros y elegancia sin esfuerzo son tu sello de identidad."},
                        "Coquette": {"tag": "03 • DELICADO", "nombre": "Coquette", "desc": "Los tonos pastel, detalles suaves y encanto delicado definen perfectamente tu gusto visual."},
                        "Old money": {"tag": "04 • CLÁSICO", "nombre": "Old money", "desc": "Piezas atemporales, cortes estructurados y una estética sobria pero refinada."},
                        "Streetwear": {"tag": "05 • URBANO", "nombre": "Streetwear", "desc": "Tendencias modernas, volumen y un toque audaz que te hace destacar en cualquier lugar."},
                        "Boho": {"tag": "06 • LIBRE", "nombre": "Boho", "desc": "Texturas fluidas y espíritu libre para experimentar con estampados y comodidad."},
                        "Deportivo": {"tag": "07 • ACTIVO", "nombre": "Deportivo", "desc": "El dinamismo en movimiento es lo tuyo: prendas funcionales con mucho estilo."},
                        "Elegante": {"tag": "08 • REFINADO", "nombre": "Elegante", "desc": "Cortes estructurados y sofisticados que marcan presencia en cada ocasión."},
                        "Y2K": {"tag": "09 • NOSTÁLGICO", "nombre": "Y2K", "desc": "Inspiración retro con toques divertidos y de personalidad muy marcada."},
                        "Romántico": {"tag": "10 • SUAVE", "nombre": "Romántico", "desc": "Siluetas fluidas, caída suave y detalles que inspiran calidez y armonía."}
                    }
                    st.session_state.resultado_estilo = dicc_estilos.get(estilo_ganador, dicc_estilos["Casual"])
                    st.rerun()
                    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. ESTILOS
# ==========================================
elif st.session_state.pagina_actual == "Estilos":
    st.markdown("### 02 / INSPIRACIÓN SIN ETIQUETAS")
    st.markdown("## Descubre tu estilo")
    st.markdown("<p>Abre cualquier tarjeta para ver ideas de prendas, colores y combinaciones.</p>", unsafe_allow_html=True)
    
    estilos_lista = [
        ("01 • CÓMODO", "Casual", "Prendas relajadas para el día a día.", "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=600&q=80"),
        ("02 • ESENCIAL", "Minimalista", "Líneas limpias y colores neutros.", "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=600&q=80"),
        ("03 • DELICADO", "Coquette", "Detalles románticos y tonos suaves.", "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=600&q=80"),
        ("04 • CLÁSICO", "Old money", "Elegancia atemporal y sobria.", "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=600&q=80"),
        ("05 • URBANO", "Streetwear", "Tendencias modernas y dinámicas.", "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=600&q=80"),
        ("06 • LIBRE", "Boho", "Texturas fluidas y espíritu libre.", "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=600&q=80")
    ]
    
    cols = st.columns(3)
    for i, (num_tag, nombre_estilo, desc, img_url) in enumerate(estilos_lista):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='css-card'>
                <p style='color: #9A536B; font-size: 0.85rem; font-weight: bold;'>{num_tag}</p>
                <h3 style='margin-bottom: 5px;'>{nombre_estilo}</h3>
                <p style='font-size: 0.95rem; margin-bottom: 12px;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            st.image(img_url, use_container_width=True)
            if st.button(f"Guardar {nombre_estilo}", key=f"fav_est_{i}"):
                if nombre_estilo not in st.session_state.favoritos:
                    st.session_state.favoritos.append(nombre_estilo)
                    st.success(f"¡Guardado en Favoritos!")
            st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. OUTFITS (CONEXIÓN CON CSV)
# ==========================================
elif st.session_state.pagina_actual == "Outfits":
    st.markdown("### 03 / EL MVP EN ACCIÓN")
    st.markdown("## Ideas de outfits y base de datos")
    st.markdown("<p>Consulta y filtra las prendas de tu base de datos CSV con total claridad.</p>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    with f1:
        cat_opts = ["Todas"] + list(df_prendas["categoria"].unique())
        cat_sel = st.selectbox("Filtrar por Categoría", cat_opts)
    with f2:
        est_opts = ["Todos"] + list(df_prendas["estilo"].unique())
        est_sel = st.selectbox("Filtrar por Estilo", est_opts)
    with f3:
        form_opts = ["Todas"] + list(df_prendas["formalidad"].unique())
        form_sel = st.selectbox("Filtrar por Formalidad", form_opts)
        
    df_filtrado = df_prendas.copy()
    if cat_sel != "Todas": df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_sel]
    if est_sel != "Todos": df_filtrado = df_filtrado[df_filtrado["estilo"] == est_sel]
    if form_sel != "Todas": df_filtrado = df_filtrado[df_filtrado["formalidad"] == form_sel]
    
    st.markdown(f"#### Mostrando {len(df_filtrado)} prendas:")
    
    if len(df_filtrado) == 0:
        st.warning("No hay prendas con estos filtros.")
    else:
        grid = st.columns(3)
        for idx, row in df_filtrado.iterrows():
            with grid[idx % 3]:
                st.markdown(f"""
                <div class='css-card'>
                    <h4 style='color: #9A536B; margin-bottom: 8px;'>{row['nombre_prenda']}</h4>
                    <p style='margin: 3px 0;'><b>Color:</b> {row['color']}</p>
                    <p style='margin: 3px 0;'><b>Categoría:</b> {row['categoria']}</p>
                    <p style='margin: 3px 0;'><b>Estilo:</b> {row['estilo']}</p>
                    <p style='margin: 3px 0;'><b>Temporada:</b> {row['temporada']}</p>
                    <p style='margin: 3px 0;'><b>Formalidad:</b> {row['formalidad']}</p>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 5. MI ARMARIO IDEAL
# ==========================================
elif st.session_state.pagina_actual == "Mi armario":
    st.markdown("### 05 / APROVECHA LO TUYO")
    st.markdown("## Mi armario ideal")
    st.markdown("<p>Selecciona prendas que ya tengas para generar combinaciones.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    t = st.multiselect("Tops", ["Camiseta blanca", "Blusa suave", "Top de color", "Cárdigan"])
    inf = st.multiselect("Partes inferiores", ["Jeans", "Pantalón amplio", "Falda cómoda"])
    zap = st.multiselect("Zapatos", ["Tenis", "Mocasines", "Zapatos cómodos"])
    
    if st.button("Crear combinación"):
        st.success(f"¡Combinación creada con éxito usando {len(t) + len(inf) + len(zap)} prendas de tu armario!")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. CONSEJOS DE ESTILO
# ==========================================
elif st.session_state.pagina_actual == "Consejos":
    st.markdown("### 06 / PEQUEÑAS IDEAS")
    st.markdown("## Consejos de estilo")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='css-card'><h4>Comodidad primero</h4><p>Elige prendas con las que puedas vivir tu día a día a gusto.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='css-card'><h4>Prueba otra forma</h4><p>Lleva una camisa abierta o añade una capa a una prenda conocida.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='css-card'><h4>Repite sin culpa</h4><p>Tus prendas favoritas pueden acompañarte muchas veces.</p></div>", unsafe_allow_html=True)

# ==========================================
# 7. FAVORITOS & OPINIÓN
# ==========================================
elif st.session_state.pagina_actual == "Favoritos":
    st.markdown("### 07 / TUS IDEAS GUARDADAS")
    st.markdown(f"## Favoritos ({len(st.session_state.favoritos)})")
    
    if len(st.session_state.favoritos) == 0:
        st.info("Aún no has guardado nada. Explora los estilos y toca guardar.")
    else:
        for f in st.session_state.favoritos:
            st.markdown(f"- ✨ **{f}**")
            
    st.markdown("---")
    st.markdown("### Tu voz importa - Ayúdanos a mejorar")
    st.radio("¿Qué tan útil te resultó la experiencia?", ["Muy útil", "Algo útil", "Poco útil"])
    st.text_area("Comentario (opcional):", placeholder="¿Qué te gustaría encontrar aquí?")
    if st.button("Enviar opinión"):
        st.success("¡Muchas gracias por tus comentarios!")

# --- FOOTER & FAQ ---
st.markdown("<br><hr style='border: 1px solid #E2D2CB;'>", unsafe_allow_html=True)
st.markdown("### Preguntas frecuentes")
with st.expander("¿Cómo se calcula el test?"):
    st.write("El test analiza tus selecciones paso a paso para sugerirte el estilo que mejor se adapta a tus gustos.")
with st.expander("¿Mi resultado es definitivo?"):
    st.write("No, tu estilo evoluciona contigo; puedes cambiar de opinión y repetir el test cuando quieras.")

st.markdown("<p style='text-align: center; font-size: 0.85rem; margin-top: 30px;'>Encuentra tu estilo · Proyecto de empresa escolar para expresar quién eres a tu manera.</p>", unsafe_allow_html=True)