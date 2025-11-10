# app.py
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tendencia de barniz - MPC", layout="wide")

st.title("Tendencia de formación de barniz - MPC")
st.caption("Visualización interactiva del valor Delta E (MPC) en el tiempo.")

with st.sidebar:
    st.header("Parámetros")
    x_max = st.number_input("Tiempo máximo (horas)", min_value=1000, max_value=50000, value=15000, step=500)
    y_max = st.number_input("Delta E máximo", min_value=10.0, max_value=200.0, value=60.0, step=1.0)
    x_end = st.number_input("Tiempo del punto (horas)", min_value=0, max_value=50000, value=12000, step=100)
    y_end = st.number_input("Delta E del punto", min_value=0.0, max_value=200.0, value=35.0, step=0.5)
    show_shades = st.checkbox("Mostrar zonas de riesgo", value=True)
    show_grid = st.checkbox("Mostrar rejilla", value=True)
    legend_loc = st.selectbox("Posición de la leyenda",
                              ["upper left","upper right","lower left","lower right","best"], index=0)
    interactive = st.checkbox("Habilitar gráfico interactivo (mpld3)", value=False)

fig, ax = plt.subplots(figsize=(10, 6))

# Zonas de riesgo
if show_shades:
    ax.axhspan(15, 19.9, facecolor='lightgreen', alpha=0.5, label='15-19.9: Potencial menor')
    ax.axhspan(20, 29.9, facecolor='khaki', alpha=0.5, label='20-29.9: Potencial moderado')
    ax.axhspan(30, 39.9, facecolor='gold', alpha=0.5, label='30-39.9: Potencial significativo')
    ax.axhspan(40, y_max, facecolor='lightpink', alpha=0.5, label=f'40-{int(y_max)}: Formación grave')

# Línea MPC y puntos
ax.plot([0, x_end], [0, y_end], color='blue', linestyle='-', linewidth=2, label='MPC Line')
ax.plot(x_end, y_end, 'o', color='blue')
ax.text(x_end, y_end, ' MPC Taurus T70', va='bottom', ha='left')
ax.plot(0, 0, 'o', color='blue')

# Etiquetas y límites
ax.set_xlabel('Tiempo (horas)')
ax.set_ylabel('Valor Delta E (MPC)')
ax.set_xlim(0, x_max)
ax.set_ylim(0, y_max)
ax.legend(loc=legend_loc)
ax.grid(show_grid)

# Render Matplotlib en Streamlit
st.pyplot(fig, use_container_width=True)

# Interactividad opcional con mpld3
if interactive:
    import mpld3
    import streamlit.components.v1 as components
    components.html(mpld3.fig_to_html(fig), height=500)
