import streamlit as st
import math
import random
import matplotlib.pyplot as plt
from samila import GenerativeImage

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🎨 Generative Art Creator")

st.sidebar.title("Function & Style Settings")
color = st.sidebar.color_picker("Pick a color", "#000000")
alpha = st.sidebar.slider("Alpha (Transparency)", 0.0, 1.0, 0.5)
size = st.sidebar.slider("Dot Size", 1, 20, 5)
point_count = st.sidebar.slider("Number of Points", 1000, 10000, 5000, step=500)

st.sidebar.title("Custom Functions")

f1_expr = st.sidebar.text_input("Function f1 (in terms of x)", "math.sin(x)")
f2_expr = st.sidebar.text_input("Function f2 (in terms of x)", "math.cos(x * 1.5)")

# Compile user-defined functions
def parse_function(expr):
    def func(x):
        try:
            return eval(expr, {"x": x, "math": math, "random": random})
        except:
            return None
    return func

f1 = parse_function(f1_expr)
f2 = parse_function(f2_expr)

if st.button("Generate Art"):
    try:
        g = GenerativeImage(f1, f2)
        g.n = point_count
        g.generate()

        # Check if data was generated
        if not g.data1:
            raise ValueError("No data generated. Please check your functions.")

        fig = plt.figure(figsize=(10, 10))
        x_vals, y_vals = zip(*[(x, y) for x, y in zip(g.data1, g.data2) if x is not None and y is not None])
        plt.scatter(x_vals, y_vals, c=color, alpha=alpha, s=size)
        plt.axis("off")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred while generating the art. Please try different parameters.\n\nError details: {e}")
