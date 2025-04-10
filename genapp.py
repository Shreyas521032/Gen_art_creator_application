import streamlit as st
import math
import random
import matplotlib.pyplot as plt
from samila import GenerativeImage

# --- Function compiler ---
def parse_function(expr):
    def func(x):
        try:
            result = eval(expr, {"x": x, "math": math, "random": random})
            return result if isinstance(result, (int, float)) else None
        except:
            return None
    return func

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🎨 Generative Art Creator")

st.sidebar.header("Customize Art")
color = st.sidebar.color_picker("Color", "#000000")
alpha = st.sidebar.slider("Transparency (Alpha)", 0.0, 1.0, 0.5)
size = st.sidebar.slider("Dot Size", 1, 20, 5)
point_count = st.sidebar.slider("Number of Points", 1000, 10000, 5000, step=500)

st.sidebar.header("Define Your Functions")
f1_expr = st.sidebar.text_input("Function f1(x)", "math.sin(x)")
f2_expr = st.sidebar.text_input("Function f2(x)", "math.cos(x * 1.5)")

# --- Button to generate ---
if st.button("Generate Art"):
    f1 = parse_function(f1_expr)
    f2 = parse_function(f2_expr)
    
    try:
        g = GenerativeImage(f1, f2)
        g.n = point_count
        g.generate()
        
        # Check if valid data was generated
        if not g.data1 or not g.data2:
            raise ValueError("Generated data is empty. This might be due to invalid functions (math errors, etc.).")

        # Filter out any None values
        points = [(x, y) for x, y in zip(g.data1, g.data2) if x is not None and y is not None]
        if not points:
            raise ValueError("All generated points are invalid (None). Check your math functions.")

        x_vals, y_vals = zip(*points)

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.scatter(x_vals, y_vals, c=color, alpha=alpha, s=size)
        ax.axis("off")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
