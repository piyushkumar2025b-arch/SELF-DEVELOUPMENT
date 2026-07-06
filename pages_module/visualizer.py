"""
Algorithm Visualizer page — embeds the React + Tailwind Stack & Binary Search visual simulators
"""
import streamlit as st
import os
from utils.styles import inject_css

def show_visualizer():
    inject_css()

    st.markdown("""
    <h1>🔍 Algorithm Visualizer</h1>
    <p style="color:#94a3b8">Interactive visual simulations of fundamental data structures and algorithms built using React and Tailwind CSS.</p>
    """, unsafe_allow_html=True)

    # Embed React + Tailwind frontend frame
    try:
        frontend_dir = "frontend"
        with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as f:
            html_template = f.read()
        with open(os.path.join(frontend_dir, "badge_animator.js"), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(frontend_dir, "AlgorithmVisualizer.jsx"), "r", encoding="utf-8") as f:
            jsx_code = f.read()
            
        # Inline assets directly, overriding the script router with the visualizer source
        inlined_html = html_template.replace(
            '<script src="badge_animator.js"></script>',
            f'<script>{js_code}</script>'
        ).split('<script type="text/javascript">')[0] + f'<script type="text/babel">{jsx_code}</script></body></html>'
        
        # Render the component
        import streamlit.components.v1 as components
        components.html(inlined_html, height=520, scrolling=True)
        
    except Exception as e:
        st.error(f"Error loading algorithm visualizer: {e}")
