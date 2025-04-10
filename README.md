
# 🎨 Gen Art Creator App

A Streamlit-based web app to generate beautiful generative art using custom mathematical expressions and parameters.

## 🚀 Features

- **Multiple Art Styles**: Points, Lines, Connected Lines, and Polar Coordinates.
- **Custom Functions**: Enter your own mathematical expressions like `sin(x)`, `cos(x*x)`, or `random()`.
- **Color Customization**: Gradient or solid color options for foreground and background.
- **Effects**: Add jitter, mirror effect, and rotation.
- **Download**: Export your creation as a high-resolution PNG image.

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/gen-art-creator-app.git
cd gen-art-creator-app
pip install -r requirements.txt
```

## 🧪 Usage

```bash
streamlit run app.py
```

## ✍️ Expression Examples

### Cartesian
- f1(x): `sin(x) * cos(x * 0.5)`
- f2(x): `cos(x) * sin(x * 0.1)`

### Polar
- r(t): `2 * sin(5 * t)`
- θ(t): `t`

## 🧰 Tech Stack

- Python
- Streamlit
- Matplotlib
- NumPy

## License

© 2025 Shreyas Kasture

All rights reserved.

This software and its source code are the intellectual property of the author. Unauthorized copying, distribution, modification, or usage in any form is strictly prohibited without explicit written permission.

For licensing inquiries, please contact: shreyas200410@gmail.com
