import streamlit as st
import math
import random
import matplotlib.pyplot as plt
from samila import GenerativeImage

# --- Helper function to safely evaluate expression ---
def safe_function(expr):
    def func(x):
        try:
            result = eval(expr, {"x": x, "math": math, "random": random})
            return result if isinstance(result, (int, float)) else None
        except Exception:
            return None
    return func

# --- Streamlit UI setup ---
st.set_page_config(layout="wide")
st.title("🎨 Generative Art Creator")

# Sidebar for user inputs
st.sidebar.header("Customize Art")
color = st.sidebar.color_picker("Color", "#000000")
alpha = st.sidebar.slider("Transparency (Alpha)", 0.0, 1.0, 0.5)
size = st.sidebar.slider("Dot Size", 1, 20, 5)
point_count = st.sidebar.slider("Number of Points", 1000, 10000, 5000, step=500)

# Functions
st.sidebar.header("Function Expressions")
f1_expr = st.sidebar.text_input("f1(x)", "math.sin(x)", key="f1_input")
f2_expr = st.sidebar.text_input("f2(x)", "math.cos(x)", key="f2_input")

# --- On Generate Button ---
if st.button("Generate Art"):
    f1 = safe_function(f1_expr)
    f2 = safe_function(f2_expr)

    g = GenerativeImage(f1, f2)
    g.n = point_count
    g.generate()

    if not g.data1 or not g.data2:
        st.error("❌ Could not generate data. Likely cause: one of your functions returned invalid values.")
    else:
        # Clean the data
        points = [(x, y) for x, y in zip(g.data1, g.data2) if x is not None and y is not None]

        if len(points) == 0:
            st.error("❌ All generated points are invalid. Try using different math functions.")
        else:
            x_vals, y_vals = zip(*points)
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.scatter(x_vals, y_vals, c=color, alpha=alpha, s=size)
            ax.axis("off")
            st.pyplot(fig)
