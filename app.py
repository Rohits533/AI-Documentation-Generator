import streamlit as st
import ast
import requests
import json
from pathlib import Path
from core.doc_engine import DocEngine
from ai_review import explain_code

st.set_page_config(
    page_title="AI Documentation Generator",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .stApp { background: #0f1117; }
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 14px rgba(0, 212, 255, 0.3);
    }
    .stTextArea textarea, .stTextInput input {
        background: #1e1e2e !important;
        color: #cdd6f4 !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
    }
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #1e1e2e;
    }
    .footer a { color: #00d4ff; text-decoration: none; }
    .code-block {
        background: #1e1e2e;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #2a2a3e;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-header">📚 AI Documentation Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Auto-generate READMEs, docstrings, and AI explanations from your code</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/python.png", width=80)
    st.markdown("---")
    st.markdown("### ⚙️ How It Works")
    st.markdown("""
    1. **Paste** your Python code  
    2. **Generate** README and docstrings  
    3. **Get AI explanation** (optional)  
    """)
    st.markdown("---")
    st.markdown("### 🔐 Security")
    st.markdown("✅ Your code is **not stored**")
    st.markdown("✅ API key is securely stored in Streamlit Secrets")

# ============================================================
# GET API KEY FROM SECRETS
# ============================================================

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("🚨 GROQ_API_KEY not found in Streamlit Secrets. Please add it in the app settings.")
    groq_api_key = None

# ============================================================
# MAIN UI
# ============================================================

col_left, col_right = st.columns([3, 1])

with col_left:
    code_input = st.text_area(
        "📄 Paste your Python code here:",
        height=300,
        value='''def add(a, b):
    """Returns the sum of a and b."""
    return a + b

def greet(name):
    print(f"Hello, {name}")
''',
        help="Paste your Python code and click 'Generate' to create documentation."
    )
    
    project_name = st.text_input("📁 Project Name", "My Project")

with col_right:
    st.markdown("### ⚡ Quick Actions")
    generate_btn = st.button("📄 Generate Documentation", use_container_width=True)
    st.markdown("---")
    st.markdown("### 📌 Tips")
    st.markdown("""
    ✅ Works best with Python  
    ✅ Paste any code snippet  
    ✅ Generates README + docstrings  
    ✅ AI explanation optional  
    """)

# ============================================================
# GENERATION LOGIC
# ============================================================

if generate_btn:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code to document.")
    else:
        with st.spinner("📄 Generating documentation..."):
            # Use the DocEngine from core/
            engine = DocEngine(code_input)
            functions = engine.extract_functions()
            readme = engine.generate_readme(project_name)
            docstrings = {func["name"]: f"Args: {', '.join(func['args'])}\nReturns: None" for func in functions}
            
            st.markdown("---")
            st.subheader("📊 Extracted Functions")
            
            if functions:
                for func in functions:
                    st.markdown(f"""
                    <div class="code-block">
                        <strong>🔹 {func['name']}</strong><br>
                        <span style="color:#888;">Args: {', '.join(func['args'])}</span><br>
                        <span style="color:#00d4ff;">{func['docstring'] or 'No description.'}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No functions found in the code.")
            
            st.subheader("📄 Generated README")
            st.code(readme, language="markdown")
            
            st.subheader("📝 Generated Docstrings")
            if docstrings:
                for func_name, docstring in docstrings.items():
                    st.code(f"def {func_name}:\n    \"\"\"{docstring}\"\"\"", language="python")
            else:
                st.info("No docstrings generated.")
            
            if groq_api_key:
                with st.spinner("🧠 Getting AI explanation..."):
                    explanation = explain_code(code_input, groq_api_key)
                st.subheader("🧠 AI Explanation")
                st.write(explanation)
            else:
                st.info("ℹ️ Add a GROQ_API_KEY to enable AI explanations.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit • AST • Groq API<br>
    <a href="https://github.com/Rohits533/AI-Documentation-Generator" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)
