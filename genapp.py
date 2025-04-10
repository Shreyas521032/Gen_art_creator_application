import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import random
import math
import io  # Added import at the top

# Set page configuration
st.set_page_config(layout="wide", page_title="Generative Art Creator")
st.title("🎨 Generative Art Creator")

# --- Helper function to safely evaluate expression ---
def safe_function(expr):
    def func(x, y=None):
        try:
            # Create a safe environment with limited functions
            safe_env = {
                "x": x,
                "y": y,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "exp": math.exp,
                "log": math.log,
                "sqrt": math.sqrt,
                "pi": math.pi,
                "e": math.e,
                "abs": abs,
                "random": random.random
            }
            result = eval(expr, {"__builtins__": {}}, safe_env)
            return result if isinstance(result, (int, float, complex)) and not math.isnan(result) else 0
        except Exception:
            return 0
    return func

# Predefined function options
function_options = {
    "sin(x)": "sin(x)",
    "cos(x)": "cos(x)",
    "sin(x) * cos(x)": "sin(x) * cos(x)",
    "sin(x) * cos(x * 0.5)": "sin(x) * cos(x * 0.5)",
    "sin(x*x)": "sin(x*x)",
    "cos(x) * sin(x * 0.1)": "cos(x) * sin(x * 0.1)",
    "x * sin(x)": "x * sin(x)",
    "sin(1/x)": "sin(1/x)",
    "sin(x) + cos(3*x)": "sin(x) + cos(3*x)",
    "random() * sin(x)": "random() * sin(x)",
    "exp(-x*x) * sin(x)": "exp(-x*x) * sin(x)",
    "Custom...": "custom"
}

polar_function_options = {
    "2 * sin(3 * t)": "2 * sin(3 * t)",
    "sin(5 * t)": "sin(5 * t)",
    "1 + cos(t)": "1 + cos(t)",
    "2 + sin(7 * t) * 0.5": "2 + sin(7 * t) * 0.5",
    "abs(sin(4 * t)) + 0.5": "abs(sin(4 * t)) + 0.5",
    "t/3": "t/3",
    "Custom...": "custom"
}

# Sidebar for user inputs
with st.sidebar:
    st.header("Art Style")
    art_style = st.selectbox("Choose Style", 
                           ["Points", "Lines", "Connected Lines", "Polar"])
    
    st.header("Color Settings")
    use_gradient = st.checkbox("Use Color Gradient", True)
    if use_gradient:
        color1 = st.color_picker("Start Color", "#1E88E5")
        color2 = st.color_picker("End Color", "#D81B60")
    else:
        color = st.color_picker("Color", "#000000")
    
    bg_color = st.color_picker("Background Color", "#FFFFFF")
    alpha = st.slider("Transparency (Alpha)", 0.0, 1.0, 0.5)
    
    st.header("Shape Settings")
    if art_style == "Points":
        size = st.slider("Point Size", 0.1, 10.0, 1.0)
    elif art_style in ["Lines", "Connected Lines"]:
        line_width = st.slider("Line Width", 0.1, 5.0, 0.5)
    
    point_count = st.slider("Number of Points", 1000, 20000, 5000, step=500)
    
    # Function expressions with dropdown options
    st.header("Function Expressions")
    st.write("Use x, sin, cos, sqrt, exp, pi, random(), etc.")
    
    if art_style == "Polar":
        r_option = st.selectbox("r(t) function", list(polar_function_options.keys()), index=0)
        if r_option == "Custom...":
            r_expr = st.text_input("Custom r(t)", "2 * sin(3 * t)")
        else:
            r_expr = polar_function_options[r_option]
            
        theta_option = st.selectbox("θ(t) function", list(polar_function_options.keys()), index=5)
        if theta_option == "Custom...":
            theta_expr = st.text_input("Custom θ(t)", "t")
        else:
            theta_expr = polar_function_options[theta_option]
    else:
        f1_option = st.selectbox("f1(x) function", list(function_options.keys()), index=3)
        if f1_option == "Custom...":
            f1_expr = st.text_input("Custom f1(x)", "sin(x) * cos(x * 0.5)")
        else:
            f1_expr = function_options[f1_option]
            
        f2_option = st.selectbox("f2(x) function", list(function_options.keys()), index=5)
        if f2_option == "Custom...":
            f2_expr = st.text_input("Custom f2(x)", "cos(x) * sin(x * 0.1)")
        else:
            f2_expr = function_options[f2_option]
    
    # Additional effects
    st.header("Effects")
    jitter = st.slider("Jitter", 0.0, 1.0, 0.0)
    mirror = st.checkbox("Mirror Effect", False)
    rotate = st.slider("Rotation (degrees)", 0, 360, 0)

# --- Function to generate the art ---
def generate_art():
    fig, ax = plt.subplots(figsize=(10, 10), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    
    if art_style == "Polar":
        # Polar coordinates
        r_func = safe_function(r_expr)
        theta_func = safe_function(theta_expr)
        
        t_values = np.linspace(0, 2 * np.pi, point_count)
        r_values = [r_func(t) for t in t_values]
        theta_values = [theta_func(t) for t in t_values]
        
        # Convert polar to cartesian
        x_values = [r * np.cos(theta) for r, theta in zip(r_values, theta_values)]
        y_values = [r * np.sin(theta) for r, theta in zip(r_values, theta_values)]
    else:
        # Cartesian coordinates
        f1 = safe_function(f1_expr)
        f2 = safe_function(f2_expr)
        
        x_values = np.linspace(-10, 10, point_count)
        y_values = [f1(x) for x in x_values]
        z_values = [f2(x) for x in x_values]
        
        # Apply jitter if requested
        if jitter > 0:
            y_values = [y + (random.random() - 0.5) * jitter for y in y_values]
            z_values = [z + (random.random() - 0.5) * jitter for z in z_values]
        
        # Mirror effect if requested
        if mirror:
            x_values = np.concatenate([x_values, x_values])
            y_values = np.concatenate([y_values, [-y for y in y_values]])
            z_values = np.concatenate([z_values, [-z for z in z_values]])
    
    # Apply rotation
    if rotate != 0:
        theta = np.radians(rotate)
        rot_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        if art_style == "Polar":
            coords = np.array([x_values, y_values])
        else:
            coords = np.array([y_values, z_values])
            
        rotated = np.dot(rot_matrix, coords)
        
        if art_style == "Polar":
            x_values, y_values = rotated[0], rotated[1]
        else:
            y_values, z_values = rotated[0], rotated[1]
    
    # Prepare colors
    if use_gradient:
        start_rgba = np.array(to_rgba(color1))
        end_rgba = np.array(to_rgba(color2))
        
        if art_style == "Polar":
            # Normalize distances for color gradient
            distances = np.sqrt(np.array(x_values)**2 + np.array(y_values)**2)
            norm_distances = (distances - min(distances)) / (max(distances) - min(distances) + 1e-10)
            colors = [start_rgba * (1 - t) + end_rgba * t for t in norm_distances]
        else:
            # Linear gradient along the line
            t_values = np.linspace(0, 1, len(y_values))
            colors = [start_rgba * (1 - t) + end_rgba * t for t in t_values]
        
        # Set alpha
        for c in colors:
            c[3] = alpha
    else:
        # Single color with alpha
        rgba_color = to_rgba(color, alpha)
        colors = [rgba_color] * len(y_values if art_style == "Polar" else z_values)
    
    # Plot based on style
    if art_style == "Polar":
        if art_style == "Points":
            ax.scatter(x_values, y_values, s=size, c=colors, alpha=alpha)
        elif art_style == "Lines":
            # Create line segments
            for i in range(len(x_values)-1):
                ax.plot([x_values[i], x_values[i+1]], [y_values[i], y_values[i+1]], 
                       color=colors[i], linewidth=line_width)
        else:  # Connected Lines
            ax.plot(x_values, y_values, linewidth=line_width, c=colors[0])
    else:
        if art_style == "Points":
            ax.scatter(y_values, z_values, s=size, c=colors, alpha=alpha)
        elif art_style == "Lines":
            # Create line segments
            for i in range(len(y_values)-1):
                ax.plot([y_values[i], y_values[i+1]], [z_values[i], z_values[i+1]], 
                       color=colors[i], linewidth=line_width)
        else:  # Connected Lines
            ax.plot(y_values, z_values, linewidth=line_width, c=colors[0])
    
    # Remove axis for artistic appeal
    ax.axis('off')
    ax.set_aspect('equal')
    
    return fig

# --- On Generate Button ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    if st.button("🖌️ Generate Art", use_container_width=True):
        try:
            fig = generate_art()
            st.pyplot(fig)
            
            # Add download buttons
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", facecolor=bg_color)
            buf.seek(0)
            st.download_button(
                label="📥 Download as PNG",
                data=buf,
                file_name="generative_art.png",
                mime="image/png",
                use_container_width=True
            )
            
            # Save as SVG option
            buf_svg = io.BytesIO()
            fig.savefig(buf_svg, format="svg", bbox_inches="tight", facecolor=bg_color)
            buf_svg.seek(0)
            st.download_button(
                label="📥 Download as SVG",
                data=buf_svg,
                file_name="generative_art.svg",
                mime="image/svg+xml",
                use_container_width=True
            )
            
            # Save expressions and settings
            if art_style == "Polar":
                settings = f"Art Style: {art_style}\nr(t): {r_expr}\nθ(t): {theta_expr}\n"
            else:
                settings = f"Art Style: {art_style}\nf1(x): {f1_expr}\nf2(x): {f2_expr}\n"
                
            settings += f"Points: {point_count}\nJitter: {jitter}\nMirror: {mirror}\nRotation: {rotate}°"
            
            st.download_button(
                label="📥 Save Settings as Text",
                data=settings,
                file_name="art_settings.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error generating art: {str(e)}")

# Add explanation
with st.expander("How to use this app"):
    st.markdown("""
    ## How to create your own generative art
    
    1. **Choose a style**: Points, Lines, Connected Lines, or Polar coordinates
    2. **Adjust colors**: Pick colors and transparency
    3. **Select mathematical expressions**: Choose from presets or create your own
    4. **Apply effects**: Add jitter, mirroring or rotation
    5. **Generate and download**: Create your artwork and save it as PNG or SVG
    
    ### Function options:
    Select from the dropdown menu or choose "Custom..." to enter your own expression.
    You can use variables (x, t), functions (sin, cos, sqrt, exp), constants (pi, e),
    and operators (+, -, *, /).
    """)
