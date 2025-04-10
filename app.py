import streamlit as st
import matplotlib.pyplot as plt
from samila import GenerativeImage, Projection, VALID_COLORS
import random
import numpy as np
from math import sin, cos, tan, log, exp, sqrt

# Page configuration
st.set_page_config(
    page_title="Generative Art Creator 🎨",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'seed' not in st.session_state:
    st.session_state.seed = random.randint(1, 100000)
if 'generate_pressed' not in st.session_state:
    st.session_state.generate_pressed = False
if 'color' not in st.session_state:
    st.session_state.color = 'viridis'
if 'width' not in st.session_state:
    st.session_state.width = 12
if 'height' not in st.session_state:
    st.session_state.height = 10
if 'function_type1' not in st.session_state:
    st.session_state.function_type1 = 'sin'
if 'function_type2' not in st.session_state:
    st.session_state.function_type2 = 'cos'
if 'operation1' not in st.session_state:
    st.session_state.operation1 = '+'
if 'operation2' not in st.session_state:
    st.session_state.operation2 = '*'
if 'custom_function1' not in st.session_state:
    st.session_state.custom_function1 = 'sin(x)*cos(y)'
if 'custom_function2' not in st.session_state:
    st.session_state.custom_function2 = 'cos(x)*sin(y)'
if 'projection' not in st.session_state:
    st.session_state.projection = 'None'
if 'alpha' not in st.session_state:
    st.session_state.alpha = 0.5
if 'random_sampling' not in st.session_state:
    st.session_state.random_sampling = 5000

# Custom CSS for better appearance
st.markdown("""
    <style>
    .main-header {
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        color: #1E88E5;
    }
    .sub-header {
        text-align: center;
        color: #424242;
        margin-bottom: 30px;
    }
    .stButton > button {
        width: 100%;
    }
    .info-box {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and subtitle
st.markdown("<h1 class='main-header'>Generative Art Creator 🎨</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-header'>Create Beautiful NFT-Style Art with Python 🐍</h3>", unsafe_allow_html=True)

# Function to generate art when button is clicked
def set_generate_pressed():
    st.session_state.generate_pressed = True

# Function to generate mathematical expressions
def generate_functions():
    function_options = {
        'sin': sin,
        'cos': cos,
        'tan': tan,
        'exp': exp,
        'sqrt': sqrt,
        'custom': None
    }
    
    operations = ['+', '-', '*', '/']
    
    function_type1 = st.session_state.function_type1
    function_type2 = st.session_state.function_type2
    
    if function_type1 == 'custom':
        custom_function1 = st.session_state.custom_function1
        try:
            def f1(x, y):
                return eval(custom_function1)
        except:
            st.error("Invalid function 1. Using default.")
            f1 = lambda x, y: sin(x)
    else:
        func1 = function_options[function_type1]
        operation1 = st.session_state.operation1
        
        if operation1 == '+':
            f1 = lambda x, y: func1(x) + func1(y)
        elif operation1 == '-':
            f1 = lambda x, y: func1(x) - func1(y)
        elif operation1 == '*':
            f1 = lambda x, y: func1(x) * func1(y)
        else:  # Division with protection against division by zero
            f1 = lambda x, y: func1(x) / (func1(y) if func1(y) != 0 else 0.001)
    
    if function_type2 == 'custom':
        custom_function2 = st.session_state.custom_function2
        try:
            def f2(x, y):
                return eval(custom_function2)
        except:
            st.error("Invalid function 2. Using default.")
            f2 = lambda x, y: cos(y)
    else:
        func2 = function_options[function_type2]
        operation2 = st.session_state.operation2
        
        if operation2 == '+':
            f2 = lambda x, y: func2(x) + func2(y)
        elif operation2 == '-':
            f2 = lambda x, y: func2(x) - func2(y)
        elif operation2 == '*':
            f2 = lambda x, y: func2(x) * func2(y)
        else:  # Division with protection against division by zero
            f2 = lambda x, y: func2(x) / (func2(y) if func2(y) != 0 else 0.001)
    
    return f1, f2

# Function to create generative art
def create_art():
    seed = st.session_state.seed
    color = st.session_state.color
    projection = st.session_state.projection
    
    f1, f2 = generate_functions()
    
    g = GenerativeImage(f1, f2)
    g.generate(seed=seed)
    
    # Apply filters according to settings
    if st.session_state.apply_random_sampling:
        g.generate(st.session_state.random_sampling)
    
    if st.session_state.apply_random_color:
        g.random_color()
        g.plot()
    else:
        g.plot(color=color)
    
    # Apply projections
    if projection != "None":
        g.set_projection(getattr(Projection, projection.upper()))
    
    # Apply other filters
    if st.session_state.apply_gradient:
        fig = plt.figure(figsize=(st.session_state.width, st.session_state.height))
        plt.axis('off')
        g.plot(alpha=st.session_state.alpha, color=color if not st.session_state.apply_random_color else None)
    else:
        fig = plt.figure(figsize=(st.session_state.width, st.session_state.height))
        plt.axis('off')
        g.plot(color=color if not st.session_state.apply_random_color else None)
    
    fig = plt.figure(figsize=(st.session_state.width, st.session_state.height))
    
    plt.axis('off')
    g.plot()
    
    return g, fig

# Sidebar for parameters
with st.sidebar:
    st.header("Art Parameters")
    
    # Mathematical functions
    st.subheader("Equations")
    
    # Create tabs for different function configuration approaches
    function_tab1, function_tab2 = st.tabs(["Function 1", "Function 2"])
    
    with function_tab1:
        st.session_state.function_type1 = st.selectbox(
            "Select Function Type 1",
            ['sin', 'cos', 'tan', 'exp', 'sqrt', 'custom'],
            index=['sin', 'cos', 'tan', 'exp', 'sqrt', 'custom'].index(st.session_state.function_type1)
        )
        
        if st.session_state.function_type1 == 'custom':
            st.session_state.custom_function1 = st.text_input(
                "Custom Function 1 (use x, y variables)",
                value=st.session_state.custom_function1
            )
        else:
            st.session_state.operation1 = st.selectbox(
                "Operation for Function 1",
                ['+', '-', '*', '/'],
                index=['+', '-', '*', '/'].index(st.session_state.operation1)
            )
    
    with function_tab2:
        st.session_state.function_type2 = st.selectbox(
            "Select Function Type 2",
            ['sin', 'cos', 'tan', 'exp', 'sqrt', 'custom'],
            index=['sin', 'cos', 'tan', 'exp', 'sqrt', 'custom'].index(st.session_state.function_type2)
        )
        
        if st.session_state.function_type2 == 'custom':
            st.session_state.custom_function2 = st.text_input(
                "Custom Function 2 (use x, y variables)",
                value=st.session_state.custom_function2
            )
        else:
            st.session_state.operation2 = st.selectbox(
                "Operation for Function 2",
                ['+', '-', '*', '/'],
                index=['+', '-', '*', '/'].index(st.session_state.operation2)
            )
    
    # Random seed
    st.subheader("Seed & Appearance")
    use_random_seed = st.checkbox("Use Random Seed", value=True)
    
    if use_random_seed:
        st.session_state.seed = random.randint(1, 100000)
    else:
        st.session_state.seed = st.number_input(
            "Seed", 
            min_value=1, 
            max_value=100000, 
            value=st.session_state.seed
        )
    
    # Color options
    st.session_state.apply_random_color = st.checkbox("Use Random Colors", value=False)
    
    if not st.session_state.apply_random_color:
        color_index = sorted(VALID_COLORS).index(st.session_state.color) if st.session_state.color in VALID_COLORS else 0
        st.session_state.color = st.selectbox(
            "Color Palette", 
            sorted(VALID_COLORS), 
            index=color_index
        )
    
    # Projection options
    projection_options = ["None", "rectilinear", "polar", "aitoff", "hammer", "lambert", "mollweide"]
    projection_index = projection_options.index(st.session_state.projection) if st.session_state.projection in projection_options else 0
    st.session_state.projection = st.selectbox(
        "Projection", 
        projection_options, 
        index=projection_index
    )
    
    # Advanced options
    st.subheader("Advanced Options")
    
    # Size settings
    cols = st.columns(2)
    with cols[0]:
        st.session_state.width = st.slider("Width", 5, 20, value=st.session_state.width)
    with cols[1]:
        st.session_state.height = st.slider("Height", 5, 20, value=st.session_state.height)
    
    # Additional effects
    st.session_state.apply_gradient = st.checkbox("Apply Gradient", value=True)
    if st.session_state.apply_gradient:
        st.session_state.alpha = st.slider("Transparency", 0.1, 1.0, value=st.session_state.alpha)
    
    st.session_state.apply_random_sampling = st.checkbox("Apply Random Sampling", value=False)
    if st.session_state.apply_random_sampling:
        st.session_state.random_sampling = st.slider(
            "Sample Points", 
            1000, 
            10000, 
            value=st.session_state.random_sampling
        )
    
    # Generate button
    st.button("🎨 Generate Art", on_click=set_generate_pressed, use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if not st.session_state.generate_pressed:
        with st.container():
            st.markdown("""
            <div class="info-box">
            <h3>Welcome to the Generative Art Creator! 🎨</h3>
            <p>This app allows you to create beautiful mathematical art using the Samila library.</p>
            <p>To get started:</p>
            <ol>
                <li>Adjust the parameters in the sidebar</li>
                <li>Click "Generate Art" to create your masterpiece</li>
                <li>Download your creation or experiment with different settings</li>
            </ol>
            <p>Use the sidebar to customize your artwork with different mathematical functions, colors, and effects.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show example image placeholder
            st.image("https://raw.githubusercontent.com/sepandhaghighi/samila/master/otherfiles/images_2.png", 
                    caption="Example of generative art created with Samila", 
                    use_container_width=True)
    else:
        try:
            g, fig = create_art()
            st.pyplot(fig)
            
            # Caption with seed value
            st.caption(f"Seed value to regenerate this image: {g.seed}")
            
            # Download button
            image_filename = f"generative_art_{g.seed}.png"
            plt.savefig(image_filename, dpi=300, bbox_inches='tight')
            
            with open(image_filename, "rb") as file:
                btn = st.download_button(
                    label="Download Image",
                    data=file,
                    file_name=image_filename,
                    mime="image/png",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"An error occurred while generating the art. Please try different parameters.")
            st.error(f"Error details: {str(e)}")

with col2:
    if st.session_state.generate_pressed:
        st.subheader("Art Details")
        st.write(f"**Seed:** {st.session_state.seed}")
        
        # Show function equations
        st.write("**Functions used:**")
        
        if st.session_state.function_type1 == 'custom':
            st.code(f"f1(x,y) = {st.session_state.custom_function1}")
        else:
            operation = st.session_state.operation1
            func = st.session_state.function_type1
            st.code(f"f1(x,y) = {func}(x) {operation} {func}(y)")
        
        if st.session_state.function_type2 == 'custom':
            st.code(f"f2(x,y) = {st.session_state.custom_function2}")
        else:
            operation = st.session_state.operation2
            func = st.session_state.function_type2
            st.code(f"f2(x,y) = {func}(x) {operation} {func}(y)")
        
        # Show other parameters
        color_display = "Random" if st.session_state.apply_random_color else st.session_state.color
        st.write(f"**Color Palette:** {color_display}")
        st.write(f"**Projection:** {st.session_state.projection}")
        
        if st.session_state.apply_gradient:
            st.write(f"**Transparency:** {st.session_state.alpha}")
        
        if st.session_state.apply_random_sampling:
            st.write(f"**Random Sampling Points:** {st.session_state.random_sampling}")
        
        # Add gallery feature
        st.subheader("Art Gallery")
        st.info("Save your favorite pieces to the gallery feature! (Coming soon)")
        
        # Add social share buttons placeholder
        st.subheader("Share Your Art")
        st.write("Copy the seed or download and share your creation!")

# Bottom section with additional information
st.markdown("---")
st.subheader("About Generative Art")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **What is Generative Art?**
    
    Generative art refers to art created with the use of an autonomous system, typically using algorithms and mathematical functions to generate visual compositions.
    """)

with col2:
    st.markdown("""
    **About Samila**
    
    This app uses the [Samila library](https://github.com/sepandhaghighi/samila), an open-source generative art tool created by Sepand Haghighi.
    """)

with col3:
    st.markdown("""
    **Try Different Settings**
    
    Experiment with different mathematical functions, projections, and color schemes to create unique artworks!
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center'>Made with ❤️ by Shreyas | 2025</p>", unsafe_allow_html=True)
