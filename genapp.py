import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import random
import math
import io 

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
    "sqrt(abs(x)) * sin(x)": "sqrt(abs(x)) * sin(x)",
    "sin(pi * x) * cos(x)": "sin(pi * x) * cos(x)",
    "sin(x) / (abs(x) + 0.1)": "sin(x) / (abs(x) + 0.1)",
    "Custom...": "custom"
}

# Sidebar for user inputs
with st.sidebar:
    st.header("Art Style")
    art_style = st.selectbox("Choose Style", 
                           ["Points", "Lines", "Connected Lines"])
    
    st.header("Color Settings")
    use_gradient = st.checkbox("Use Color Gradient", True)
    if use_gradient:
        color1 = st.color_picker("Start Color", "#1E88E5")
        color2 = st.color_picker("End Color", "#D81B60")
        
        gradient_type = st.selectbox("Gradient Type", ["Linear", "Radial"])
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
    bounds = st.slider("Plot Bounds", -20.0, 20.0, (-10.0, 10.0), 1.0)
    
    # Function expressions with dropdown options
    st.header("Function Expressions")
    st.write("Use x, sin, cos, sqrt, exp, pi, random(), etc.")
    
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
    
    # Advanced settings
    st.header("Advanced Settings")
    show_advanced = st.checkbox("Show Advanced Settings", False)
    
    if show_advanced:
        frame = st.checkbox("Add Frame", False)
        frame_color = st.color_picker("Frame Color", "#000000") if frame else "#000000"
        frame_width = st.slider("Frame Width", 0.1, 5.0, 1.0) if frame else 1.0
        
        density_factor = st.slider("Point Density Distribution", 1, 10, 1, 
                                 help="Higher values concentrate points in interesting areas")

# --- Function to generate the art ---
def generate_art():
    fig, ax = plt.subplots(figsize=(10, 10), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    
    # Cartesian coordinates
    f1 = safe_function(f1_expr)
    f2 = safe_function(f2_expr)
    
    x_values = np.linspace(bounds[0], bounds[1], point_count)
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
        
        coords = np.array([y_values, z_values])
        rotated = np.dot(rot_matrix, coords)
        y_values, z_values = rotated[0], rotated[1]
    
    # Prepare colors
    if use_gradient:
        start_rgba = np.array(to_rgba(color1))
        end_rgba = np.array(to_rgba(color2))
        
        if gradient_type == "Radial":
            # Radial gradient - based on distance from center
            distances = np.sqrt(np.array(y_values)**2 + np.array(z_values)**2)
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
        colors = [rgba_color] * len(y_values)
    
    # Plot based on style
    if art_style == "Points":
        ax.scatter(y_values, z_values, s=size, c=colors, alpha=alpha)
    elif art_style == "Lines":
        # Create line segments
        for i in range(len(y_values)-1):
            ax.plot([y_values[i], y_values[i+1]], [z_values[i], z_values[i+1]], 
                   color=colors[i], linewidth=line_width)
    else:  # Connected Lines
        ax.plot(y_values, z_values, linewidth=line_width, c=colors[0])
    
    # Add frame if requested
    if show_advanced and frame:
        ax.set_frame_on(True)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(frame_color)
            spine.set_linewidth(frame_width)
    else:
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
            settings = f"Art Style: {art_style}\nf1(x): {f1_expr}\nf2(x): {f2_expr}\n"
            settings += f"Points: {point_count}\nJitter: {jitter}\nMirror: {mirror}\nRotation: {rotate}°"
            if show_advanced and frame:
                settings += f"\nFrame: Yes\nFrame Color: {frame_color}\nFrame Width: {frame_width}"
            
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
    
    1. **Choose a style**: Points, Lines, or Connected Lines
    2. **Adjust colors**: Pick colors and transparency
    3. **Select mathematical expressions**: Choose from presets or create your own
    4. **Apply effects**: Add jitter, mirroring or rotation
    5. **Generate and download**: Create your artwork and save it as PNG or SVG
    
    ### Function options:
    Select from the dropdown menu or choose "Custom..." to enter your own expression.
    You can use variables (x), functions (sin, cos, sqrt, exp), constants (pi, e),
    and operators (+, -, *, /).
    
    ### Tips for beautiful art:
    - Try combining different trigonometric functions (sin, cos)
    - Add some randomness with the jitter effect
    - Experiment with color gradients
    - Mirror effects can create symmetrical patterns
    - Play with rotation to find interesting perspectives
    - Use the radial gradient for circular patterns
    
    ### Examples to try:
    - Lissajous curves: sin(x) and sin(x*1.5)
    - Butterfly curve: exp(-x*x) * sin(x) and cos(x) * sin(x * 0.1)
    - Abstract pattern: sin(x*x) and cos(x) * x
    - Wave forms: sin(x) + cos(3*x) and sin(x) * cos(x)
    """)

# Add credits at the bottom
st.markdown("---")
st.markdown("### Created by Shreyas")
st.markdown("""
This generative art application lets you explore the beauty of mathematical functions
through visual representation. Create unique artwork by experimenting with different
mathematical expressions and visual styles.

© 2025 | All rights reserved
""")
