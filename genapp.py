import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import random

st.set_page_config(layout="wide", page_title="Generative Art Creator")
st.title("🎨 Generative Art Creator")

# --- Basic expression parser ---
def simple_function(expr):
    def func(x):
        try:
            return eval(expr, {"x": x, "math": math, "random": random})
        except:
            return 0
    return func

# --- Sidebar ---
st.sidebar.header("Art Settings")
f1_expr = st.sidebar.text_input("Function f1(x)", "math.sin(x)")
f2_expr = st.sidebar.text_input("Function f2(x)", "math.cos(x)")
num_points = st.sidebar.slider("Number of points", 1000, 10000, 5000, step=500)
dot_size = st.sidebar.slider("Dot size", 1, 10, 3)
color = st.sidebar.color_picker("Dot color", "#000000")

# --- Generate Button ---
if st.sidebar.button("Generate"):
    f1 = simple_function(f1_expr)
    f2 = simple_function(f2_expr)

    x_vals = np.linspace(-10, 10, num_points)
    y1_vals = [f1(x) for x in x_vals]
    y2_vals = [f2(x) for x in x_vals]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y1_vals, y2_vals, s=dot_size, c=color)
    ax.axis('off')
    st.pyplot(fig)
