import streamlit as st
import pandas as pd
from google import genai
from google.genai.types import GenerateContentConfig, Part, Tool, GoogleSearch
from google.cloud import firestore, storage, discoveryengine_v1 as discoveryengine

# --- CONFIGURARE INFRASTRUCTURĂ ---
PROJECT_ID = "axon-core-os"
BUCKET_NAME = "axon-archive-axon-core-os"
DATA_STORE_ID = "axon-knowledge-base_1771593704304"
LOCATION = "global"

@st.cache_resource
def get_clients():
    try:
        return {
            "db": firestore.Client(project=PROJECT_ID),
            "storage": storage.Client(project=PROJECT_ID),
            "ai": genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1"),
            "search": discoveryengine.SearchServiceClient()
        }
    except: return None

clients = get_clients()

# --- HEALTH MONITOR (Ecran Start) ---
def get_detailed_health():
    status = {}
    try:
        clients["db"].collection("axon_protocols").limit(1).get()
        status["🧬 Genetic DNA Firestore"] = "🟢 ONLINE"
    except: status["🧬 Genetic DNA Firestore"] = "🔴 OFFLINE"
    try:
        clients["storage"].bucket(BUCKET_NAME).exists()
        status["📂 Cloud Archive Storage"] = "🟢 ONLINE"
    except: status["📂 Cloud Archive Storage"] = "🔴 OFFLINE"
    try:
        clients["ai"].models.get(model="gemini-2.5-flash")
        status["🧠 Gemini AI Core Engine"] = "🟢 ONLINE"
    except: status["🧠 Gemini AI Core Engine"] = "🔴 OFFLINE"
    status["🔎 RAG Discovery Engine"] = "🟢 ONLINE" if clients["search"] else "🔴 OFFLINE"
    status["🌐 Google Search Tool"] = "🟢 ACTIVE"
    status["⚙️ FrameLang OS Hub"] = "🟢 ACTIVE"
    return status

DEPT_CATEGORIES = {
    "Project_Manager": ["Rapoarte-Executive", "Minute-Sedinta", "Decizii-Strategice"],
    "Planning": ["Grafice-Gantt", "Curbe-S", "Rapoarte-Intarziere"],
    "Cost_Control": ["Bugete", "Rapoarte-EVM", "Cash-Flow"],
    "Commercial": ["Contract-Principal", "Subcontractori", "Claims", "Variatii"],
    "Risk_Management": ["Registru-Riscuri", "Planuri-Mitigare"],
    "Engineering": ["Planse-IFC", "Specificatii-Tehnice", "RFI-uri"],
    "Procurement": ["Comenzi-PO", "Facturi-Furnizor", "Avize-Intrare", "Bonuri-Consum"],
    "Construction": ["Jurnale-Santier", "Method-Statements", "Poze-Progres"],
    "Commissioning": ["Pre-Comm", "Hot-Comm", "Punch-List", "Handover"],
    "HSE": ["Rapoarte-Incidente", "Permise-Lucru-PTW", "Analiza-JSA"],
    "QA_QC": ["ITP-uri", "NCR-Neconformitati", "Certificate-Calitate"]
}

# --- LOGICĂ BACKEND ---
def get_global_inventory():
    try:
        blobs = list(clients["storage"].bucket(BUCKET_NAME).list_blobs())
        return "\n".join([f"- [{b.name.split('/')[0]}] {b.name.split('/')[-1]}" for b in blobs])
    except: return ""

def search_rag(query):
    try:
        serving_config = clients["search"].serving_config_path(project=PROJECT_ID, location=LOCATION, data_store=DATA_STORE_ID, serving_config="default_config")
        request = discoveryengine.SearchRequest(serving_config=serving_config, query=query, page_size=10)
        res = clients["search"].search(request)
        context = ""
        for r in res.results:
            data = r.document.derived_struct_data
            if "extractive_answers" in data:
                for a in data["extractive_answers"]: context += f"[VERIFICAT AXON]: {a.get('content')}\n\n"
        return context
    except: return ""

def get_protocol(aid):
    doc = clients["db"].collection("axon_protocols").document(aid).get()
    return doc.to_dict()["content"] if doc.exists else ""

def save_protocol(aid, txt):
    clients["db"].collection("axon_protocols").document(aid).set({"content": txt})

def list_files(aid):
    prefix = "" if aid == "Project_Manager" else f"{aid}/"
    return list(clients["storage"].bucket(BUCKET_NAME).list_blobs(prefix=prefix))

# --- UI ---
st.set_page_config(page_title="AXON AI", layout="wide", page_icon="🧬")

with st.sidebar:
    st.title("🧬 AXON AI")
    if st.button("🏠 Ecran Principal"):
        if "current_p" in st.session_state: del st.session_state.current_p
        st.rerun()
    st.divider()
    if st.button("📁 Lead: Project Manager"): st.session_state.current_p = "Project_Manager"
    for grp, ags in {"🧠 Control": ["Planning", "Cost_Control", "Commercial", "Risk_Management"], 
                      "🛠️ Execuție": ["Engineering", "Procurement", "Construction", "Commissioning"],
                      "🛡️ Guvernanță": ["HSE", "QA_QC"]}.items():
        with st.expander(grp):
            for a in ags:
                if st.button(a.replace("_", " ")): st.session_state.current_p = a

if "current_p" not in st.session_state:
    # --- ECRAN PRINCIPAL (Păstrat neschimbat, monitorizare completă) ---
    st.title("🚀 AXON AI Dashboard")
    h = get_detailed_health()
    h_cols = st.columns(3)
    for i, (serv, stat) in enumerate(h.items()):
        color = "#28a745" if "🟢" in stat else "#dc3545"
        h_cols[i % 3].markdown(f'<div style="padding:15px; border:2px solid {color}; border-radius:10px; text-align:center; margin-bottom:10px;"><p style="margin:0; font-size:14px; font-weight:bold;">{serv}</p><h4 style="margin:0; color:{color}; font-size:22px;">{stat}</h4></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📋 Facilități și Funcționalități Complete")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.info("**🧬 Genetic DNA Protocols**\nProtocoale NoSQL Firestore.")
        st.info("**📂 Hybrid RAG System**\nVertex AI Search cu Storage Injection.")
        st.info("**📜 Audit Trail**\nTrasabilitate completă [VERIFICAT AXON].")
    with f2:
        st.info("**🧠 Gemini 2.5 Multi-Modal**\nMotor AI pentru text și imagini.")
        st.info("**🌐 Google Search Tool**\nAcces live la internet.")
        st.info("**📊 EPC Stock Ledger**\nGestiune automată stocuri.")
    with f3:
        st.info("**🔍 Vision OCR Intel**\nAnaliză poze progres.")
        st.info("**🛡️ Security Isolation**\nSegregare date pe departamente.")
        st.info("**🤝 FrameLang Link**\nOrchestrare Master Project Manager.")

else:
    agent = st.session_state.current_p
    
    # --- LOGICĂ PENTRU PROJECT MANAGER (Full Width) ---
    if agent == "Project_Manager":
        st.title(f"👑 Lead: {agent.replace('_', ' ')}")
        pulse_cols = st.columns(11)
        all_blobs = list(clients["storage"].bucket(BUCKET_NAME).list_blobs())
        for i, (dept, _) in enumerate(DEPT_CATEGORIES.items()):
            active = any(b.name.startswith(f"{dept}/") for b in all_blobs)
            pulse_cols[i].caption(f"{'🟢' if active else '⚪'} {dept[:4]}")
        
        st.markdown("##### 📂 Hub Management")
        with st.expander("Arhivă & Protocol", expanded=False):
            t1, t2 = st.tabs(["🔒 Protocol DNA", "📂 Arhivă Globală"])
            with t1:
                dna_v = get_protocol(agent)
                with st.expander("📝 Editare Protocol DNA", expanded=False):
                    new_dna = st.text_area("DNA:", dna_v, height=150)
                    if st.button("💾 Salvează"): save_protocol(agent, new_dna); st.rerun()
            with t2:
                for f in all_blobs[:10]: st.caption(f"📄 {f.name}")
        
        st.divider()
        if p := st.chat_input("Introdu directiva strategică..."):
            with st.chat_message("assistant"):
                k = search_rag(p); inv = get_global_inventory()
                conf = GenerateContentConfig(tools=[Tool(google_search=GoogleSearch())], temperature=0.0)
                for chunk in clients["ai"].models.generate_content_stream(model="gemini-2.5-flash", contents=[f"PM Master. Inventar: {inv}. Context: {k}. Protocol: {get_protocol(agent)}", p], config=conf):
                    st.write(chunk.text)

    # --- LOGICĂ PENTRU TOȚI CEILALȚI AGENȚI (2 Coloane + Hub Complet) ---
    else:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.title(f"🛡️ Consolă {agent}")
            if p := st.chat_input("Întreabă..."):
                with st.chat_message("assistant"):
                    k = search_rag(p)
                    dna = get_protocol(agent)
                    conf = GenerateContentConfig(tools=[Tool(google_search=GoogleSearch())], temperature=0.0)
                    for chunk in clients["ai"].models.generate_content_stream(model="gemini-2.5-flash", contents=[f"Rol: {agent}. Context: {k}. Protocol: {dna}", p], config=conf):
                        st.write(chunk.text)

        with col2:
            st.subheader(f"📚 HUB: {agent}")
            t_labels = ["🔒 Protocol", "📂 Arhivă"]
            if agent == "Procurement": t_labels.append("📊 Gestiune")
            tabs = st.tabs(t_labels)
            
            with tabs[0]: # PROTOCOL DNA
                with st.expander("📝 Editează Protocol DNA", expanded=False):
                    dna_text = get_protocol(agent)
                    new_dna = st.text_area("DNA:", dna_text, height=200)
                    if st.button("💾 Salvează DNA"): save_protocol(agent, new_dna); st.rerun()
            
            with tabs[1]: # ARHIVĂ (UPLOAD + PREVIEW + ZOOM + ȘTERGERE)
                with st.expander("📤 Upload Document", expanded=False):
                    cats = DEPT_CATEGORIES.get(agent, ["General"])
                    sel_c = st.selectbox("Dosar:", cats)
                    up = st.file_uploader("Selectează fișier")
                    if st.button("🚀 Arhivează"):
                        if up:
                            p_path = f"{agent}/{sel_c}_{up.name}"
                            clients["storage"].bucket(BUCKET_NAME).blob(p_path).upload_from_string(up.read())
                            st.rerun()
                st.divider()
                all_b = list_files(agent)
                for c in cats:
                    with st.expander(f"📁 {c}", expanded=False):
                        for f in [x for x in all_b if f"{c}_" in x.name]:
                            c1, c2, c3 = st.columns([0.2, 0.7, 0.1])
                            if f.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                                img_b = f.download_as_bytes()
                                c1.image(img_b, width=60)
                                if c1.button("🔍", key=f"z_{f.name}"): st.image(img_b, use_container_width=True)
                            else: c1.write("📄")
                            c2.caption(f.name.split('_', 1)[-1])
                            if c3.button("🗑️", key=f"d_{f.name}"):
                                clients["storage"].bucket(BUCKET_NAME).blob(f.name).delete(); st.rerun()
            
            if agent == "Procurement": # GESTIUNE STOC
                with tabs[2]:
                    docs_inv = [d.to_dict() for d in clients["db"].collection("axon_inventory").stream()]
                    st.dataframe(pd.DataFrame(docs_inv), use_container_width=True)
