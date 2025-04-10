import streamlit as st
from samila import GenerativeImage
import math

st.set_page_config(page_title="Generative Art Creator", layout="wide")

st.title("🎨 Generative Art Creator using Samila")

st.markdown(
    """
Welcome to the Generative Art Creator! 🎉  
Customize your own piece of art using mathematical functions and projections.
"""
)

with st.sidebar:
    st.header("🛠️ Configuration")

    func_options = {
        "sin(x*y)": lambda x, y: math.sin(x * y),
        "cos(x+y)": lambda x, y: math.cos(x + y),
        "x*sin(y)": lambda x, y: x * math.sin(y),
        "y*cos(x)": lambda x, y: y * math.cos(x),
        "tan(x*y)": lambda x, y: math.tan(x * y),
        "x^2 - y^2": lambda x, y: x**2 - y**2,
    }

    f1_label = st.selectbox("Function 1", list(func_options.keys()), index=0)
    f2_label = st.selectbox("Function 2", list(func_options.keys()), index=1)

    f1 = func_options[f1_label]
    f2 = func_options[f2_label]

    color = st.color_picker("🎨 Pick a color", "#1f77b4")

    projection = st.selectbox(
        "🌀 Projection",
        ["default", "3d", "polar", "log"],
        index=0,
    )

    seed = st.number_input("🌱 Random Seed", min_value=0, max_value=9999, value=42, step=1)
    dpi = st.slider("🖼️ Save DPI", min_value=72, max_value=300, value=100)
    size = st.slider("📐 Figure Size", min_value=4, max_value=20, value=10)
    alpha = st.slider("🔆 Transparency (alpha)", min_value=0.0, max_value=1.0, value=0.7)

if st.button("✨ Generate Art"):
    try:
        g = GenerativeImage(f1, f2)
        g.seed = seed
        if projection != "default":
            g.projection = projection

        g.generate()
        fig = g.plot(color=color, alpha=alpha, size=size)
        st.pyplot(fig)  

        with st.expander("💾 Save Options"):
            filename = st.text_input("Filename", value="art.png")
            if st.button("Save Image"):
                g.save_image(file_adr=filename, dpi=dpi)  # ✅ dpi here
                st.success(f"Image saved as {filename}")

    except Exception as e:
        st.error(f"An error occurred while generating the art. Please try different parameters.\n\nError details: {e}")
