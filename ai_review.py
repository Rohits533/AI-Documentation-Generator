import streamlit as st
import requests
import json

# ==========================================
# BACKEND: GROQ INTEGRATION (ai_review)
# ==========================================
def explain_code(code, api_key):
    """Sends code to Groq and returns an AI explanation."""
    url = "https://groq.com"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"You are a senior developer. Explain the following Python code in simple, clear language. Focus on what the code does, not how it works.\n\n```python\n{code}\n```"
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"


# ==========================================
# FRONTEND: STREAMLIT MINIMAL UI
# ==========================================
# Mock class placeholder for DocEngine imports
# Replace this or keep your local core.doc_engine import as needed
try:
    from core.doc_engine import DocEngine
except ImportError:
    # Fallback placeholder if local file structure isn't detected
    class DocEngine:
        def __init__(self, code): self.code = code
        def extract_functions(self): return [{"name": "add", "docstring": "Returns the sum of a and b."}]
        def extract_classes(self): return []
        def generate_readme(self, title): return f"# {title}\nAutomated documentation generation."

st.set_page_config(page_title="AI Documentation Generator", layout="wide")
st.title("📚 AI Documentation Generator")
st.markdown("Generate READMEs, docstrings, and AI explanations from your code.")

# Text Box Input Area
code_input = st.text_area(
    "📄 Paste your Python code here:", 
    height=300, 
    value="def add(a, b):\n    '''Returns the sum of a and b.'''\n    return a + b"
)

# API Secrets Verification
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY not found in Streamlit Secrets.")
    groq_api_key = None

# Interface action controls layout split
col1, col2 = st.columns(2)

with col1:
    generate_docs = st.button("🚀 Generate Documentation", use_container_width=True)

with col2:
    get_ai = st.button("🧠 Get AI Explanation", disabled=(groq_api_key is None), use_container_width=True)

# Process block 1: Local Documentation Analysis
if generate_docs:
    if not code_input.strip():
        st.warning("Please paste some code.")
    else:
        with st.spinner("Generating documentation..."):
            engine = DocEngine(code_input)
            functions = engine.extract_functions()
            classes = engine.extract_classes()
            readme = engine.generate_readme("My Project")
            
            st.subheader("📊 Extracted Functions")
            if functions:
                for func in functions:
                    st.write(f"**{func['name']}** — {func['docstring']}")
            else:
                st.info("No functions found.")
                
            st.subheader("📄 Generated README")
            st.code(readme, language="markdown")

# Process block 2: Independent Third-Party LLM Evaluation
if get_ai:
    if not code_input.strip():
        st.warning("Please paste some code.")
    else:
        with st.spinner("Getting AI explanation..."):
            explanation = explain_code(code_input, groq_api_key)
            st.subheader("🧠 AI Explanation")
            st.write(explanation)
