"""
web_app.py

Premium dark-mode Streamlit UI for ECHOFORM.
- Gemini ADK aware
- Shows reply, scores, traits, reasoning, compressed fingerprint
- Includes a simple session memory viewer (messages + reasoning snapshots)
"""
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import sqlite3

import streamlit as st

from app import EchoformEngine
from config import APP_NAME, APP_TAGLINE, DB_PATH


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================
# MEMORY HELPERS (LOCAL QUERIES TO SQLITE)
# ======================================================

def _load_messages(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE session_uuid = ?
        ORDER BY created_at ASC
        """,
        (session_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def _load_reasoning_snapshots(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT compressed_reasoning, traits_json, created_at
        FROM reasoning_snapshots
        WHERE session_uuid = ?
        ORDER BY created_at ASC
        """,
        (session_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

# ======================================================
# CUSTOM THEME (GLASSMORPHIC DARK MODE)
# ======================================================

CUSTOM_CSS = """
<style>
html, body, [class*="css"] {
    background-color: #0b0d11;
    color: #eaeaea;
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: radial-gradient(circle at top, #171a21 0%, #0b0d11 100%);
}
.glass {
    background: rgba(20, 20, 28, 0.6);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    margin-bottom: 20px;
}
.title {
    font-size: 3em;
    font-weight: 800;
    background: linear-gradient(90deg, #f2b1a0, #9b5cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    font-size: 1.1em;
    color: #aaa;
}
textarea {
    background-color: rgba(17, 17, 22, 0.8) !important;
    border-radius: 12px !important;
    border: 1px solid #2a2a35 !important;
    color: #eee !important;
}
.stButton > button {
    background: linear-gradient(135deg, #f2b1a0, #9b5cff);
    border: none;
    color: black;
    padding: 12px 18px;
    border-radius: 12px;
    font-weight: 600;
    box-shadow: 0 0 12px rgba(155, 92, 255, 0.4);
}
div[data-testid="metric-container"] {
    background: rgba(20, 20, 28, 0.6);
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 6px 20px rgba(73, 18, 112, 0.3);
    border-left: 3px solid #9b5cff;
}
section[data-testid="stSidebar"] {
    background: rgba(11, 13, 17, 0.9);
    backdrop-filter: blur(10px);
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb {
    background: #9b5cff;
    border-radius: 10px;
}
.glow {
    box-shadow: 0 0 18px rgba(155, 92, 255, 0.5);
}
.section-title {
    color: #f2b1a0;
    font-weight: 700;
    margin-bottom: 10px;
}
code {
    color: #9b5cff;
}
pre {
    background-color: rgba(15, 15, 20, 0.8) !important;
    border-radius: 12px !important;
    border: 1px solid #2a2a35 !important;
}
.small-label {
    font-size: 0.8rem;
    color: #999;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ======================================================
# ENGINE CACHE
# ======================================================

@st.cache_resource
def load_engine():
    return EchoformEngine()


engine = load_engine()

# ======================================================
# HEADER
# ======================================================

st.markdown(
    f"""
    <div class="glass glow">
        <div class="title">{APP_NAME}</div>
        <div class="subtitle">{APP_TAGLINE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# SIDEBAR – INTELLIGENCE STATE
# ======================================================

with st.sidebar:
    st.markdown("## 🧬 Intelligence State")

    if "last_output" in st.session_state:
        out = st.session_state.last_output
        traits = out["traits"]
        scores = out["scores"]

        st.metric("Mutation Level", out["mutation_level"])
        st.metric("Gemini Enabled", "Yes" if out["gemini_enabled"] else "No")

        st.markdown("---")
        st.markdown("### 🎛 Traits")
        st.metric("Creativity", round(traits["creativity"], 2))
        st.metric("Abstraction", round(traits["abstraction"], 2))
        st.metric("Verbosity", round(traits["verbosity"], 2))
        st.metric("Formality", round(traits["formality"], 2))

        st.markdown("---")
        st.markdown("### ⚖ Overall")
        st.metric("Overall Score", scores["overall"])

        st.markdown("---")
        st.caption(f"Session ID:\n{out['session_id']}")
    else:
        st.info("No cognition yet. Send a prompt to start a session.")

# ======================================================
# PROMPT INPUT
# ======================================================

prompt = st.text_area("💭 Speak to ECHOFORM", height=120, placeholder="Ask ECHOFORM to reason about something...")

if st.button("⚡ Run Cognition") and prompt.strip():
    result = engine.process_input(prompt)
    st.session_state.last_output = result

# ======================================================
# MAIN OUTPUT PANELS
# ======================================================

if "last_output" in st.session_state:
    output = st.session_state.last_output

    # RESPONSE
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 Response</div>', unsafe_allow_html=True)
    st.write(output["reply"])
    st.markdown('</div>', unsafe_allow_html=True)

    # SCORES
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚖ Evaluation</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for col, (key, value) in zip(cols, output["scores"].items()):
        col.metric(key.capitalize(), value)
    st.markdown('</div>', unsafe_allow_html=True)

    # COMPRESSED FINGERPRINT
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗜 Cognitive Fingerprint</div>', unsafe_allow_html=True)
    st.code(output["compressed"])
    st.markdown('</div>', unsafe_allow_html=True)

    # OBSERVER ANALYSIS
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👁 Observer Analysis</div>', unsafe_allow_html=True)
    st.json(output["analysis"])
    st.markdown('</div>', unsafe_allow_html=True)

    # RAW REASONING
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 Raw Reasoning Trace</div>', unsafe_allow_html=True)
    st.code(output["raw_reasoning"])
    st.markdown('</div>', unsafe_allow_html=True)

    # MEMORY VIEWER
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗃 Session Memory Viewer</div>', unsafe_allow_html=True)

    with st.expander("📜 Dialogue History"):
        messages = _load_messages(output["session_id"])
        if messages:
            for m in messages:
                role = m["role"]
                created = m["created_at"]
                st.markdown(f"**{role.upper()}**  ·  `{created}`")
                st.write(m["content"])
                st.markdown("---")
        else:
            st.caption("No messages found for this session yet.")

    with st.expander("🧠 Reasoning Snapshots"):
        snaps = _load_reasoning_snapshots(output["session_id"])
        if snaps:
            for i, snap in enumerate(snaps, start=1):
                st.markdown(f"**Snapshot {i}**  ·  `{snap['created_at']}`")
                st.markdown("**Compressed**")
                st.code(snap["compressed_reasoning"])
                st.markdown("**Traits JSON**")
                st.code(snap["traits_json"])
                st.markdown("---")
        else:
            st.caption("No reasoning snapshots found yet.")

    st.markdown('</div>', unsafe_allow_html=True)


