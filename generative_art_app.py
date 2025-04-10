
import streamlit as st
from samila import GenerativeImage, Projection
import matplotlib.pyplot as plt
import random
import matplotlib.cm as cm
import io

st.set_page_config(page_title="Generative Art Creator", layout="centered")

st.title("🎨 Generative Art Creator")
st.write("Customize mathematical generative art with your own functions and settings!")

# Session state initialization
if "function1" not in st.session_state:
    st.session_state.function1 = "math.sin(x ** 2) - math.cos(y ** 2)"
if "function2" not in st.session_state:
    st.session_state.function2 = "math.cos(x ** 2) + math.sin(y ** 2)"
if "projection" not in st.session_state:
    st.session_state.projection = Projection.POLAR
if "color" not in st.session_state:
    st.session_state.color = "viridis"
if "art" not in st.session_state:
    st.session_state.art = None

# Sidebar
st.sidebar.header("Settings")
st.session_state.function1 = st.sidebar.text_input("Function 1 (use x, y)", st.session_state.function1)
st.session_state.function2 = st.sidebar.text_input("Function 2 (use x, y)", st.session_state.function2)
st.session_state.projection = st.sidebar.selectbox("Projection", list(Projection), index=list(Projection).index(st.session_state.projection))

valid_colormaps = sorted(m for m in plt.colormaps() if not m.endswith("_r"))
color_index = valid_colormaps.index(st.session_state.color) if st.session_state.color in valid_colormaps else 0
st.session_state.color = st.sidebar.selectbox("Color Palette", valid_colormaps, index=color_index)

# Generate button
if st.button("Generate Art"):
    def f1(x, y):
        return eval(st.session_state.function1)

    def f2(x, y):
        return eval(st.session_state.function2)

    g = GenerativeImage(f1, f2)
    g.generate()
    g.set_projection(st.session_state.projection)
    try:
        g.set_color(st.session_state.color)
    except Exception:
        g.set_color("viridis")
        st.warning("Invalid color palette selected. Using 'viridis' instead.")

    fig = g.plot()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.session_state.art = buf
    st.pyplot(fig)

# Show last generated image
if st.session_state.art:
    st.subheader("🖼️ Your Generated Art")
    st.image(st.session_state.art)

    st.download_button(
        label="Download Art as PNG",
        data=st.session_state.art,
        file_name="generative_art.png",
        mime="image/png"
    )
