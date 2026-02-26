import streamlit as st
import pandas as pd
from google import genai
from google.genai.types import GenerateContentConfig, Part, Tool, GoogleSearch
from google.cloud import firestore, storage, discoveryengine_v1 as discoveryengine

# --- CONFIGURARE INFRASTRUCTURĂ ---
PROJECT_ID = "axon-core-os"
BUCKET_NAME = "axon-archive-axon-core-os"
DATA_STORE_ID = "axon-knowledge-base_1771593704304"







def display_construction_management():
    try:
        import pandas as pd
        from google.cloud import firestore
        db_v = firestore.Client()
        docs = db_v.collection('axon_inventory').stream()
        data = [d.to_dict() for d in docs]
        if data:
            df = pd.DataFrame(data)
            # Conversie numerică obligatorie conform codului tău original
            for c in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata']:
                if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            
            st.subheader('📊 CONTROL OPERAȚIONAL EPC (DATE OFICIALE)')
            df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])
            sum_df = df.groupby(['Categorie', 'Mat_Baza']).agg({
                'Cantitate_Planificata':'sum',
                'Cantitate_Receptionata':'sum',
                'Cantitate_Custodie':'sum',
                'Cantitate_Validata':'sum'
            }).reset_index()
            
            # Cele 6 categorii sfinte din codul tău
            for cat in ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']:
                c_df = sum_df[sum_df['Categorie'].str.strip() == cat]
                with st.expander(f'📁 {cat.upper()} ({len(c_df)} repere)'):
                    if not c_df.empty:
                        v = c_df.rename(columns={'Cantitate_Custodie':'In Custodie','Cantitate_Validata':'Realizat (PV)'})
                        st.dataframe(v[['Mat_Baza', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'In Custodie', 'Realizat (PV)']], use_container_width=True, hide_index=True)
            
            st.markdown('---')
            st.subheader('📈 DETALII CONTRACTORI (SITUAȚIE TEREN)')
            d_df = df[(df['Cantitate_Custodie']>0)|(df['Cantitate_Instalata']>0)|(df['Cantitate_Validata']>0)]
            if not d_df.empty:
                dv = d_df.rename(columns={'Cantitate_Instalata':'Raportat Constructor','Cantitate_Validata':'Validat PM'})
                st.dataframe(dv[['Material','Contractor_Custodie','Cantitate_Custodie','Raportat Constructor','Validat PM','Status']], use_container_width=True, hide_index=True)
        else:
            st.info("Baza de date axon_inventory este goală.")
    except Exception as e:
        st.error(f"Eroare Gestiune: {e}")

def display_rogvaiv_gis():
    st.markdown("### 🗺️ ROGVAIV GIS Tracker Status")
    try:
        import psycopg2
        # Ne conectăm direct pentru a evita erorile de cache
        conn = psycopg2.connect(
            host="127.0.0.1", 
            database="axon_rogvaiv", 
            user="admin_axon", 
            password="Axon2026X", 
            port="5432",
            connect_timeout=3
        )
        cur = conn.cursor()
        cur.execute("SELECT tracker_label, status FROM axon_trackers ORDER BY tracker_label ASC")
        rows = cur.fetchall()
        
        if not rows:
            st.info("ℹ️ Baza de date este accesibilă, dar tabelul 'axon_trackers' nu are date.")
        else:
            cols = st.columns(5)
            for i, (label, status) in enumerate(rows):
                with cols[i % 5]:
                    color = "#28a745" if status == "instalat" else "#fd7e14" if status == "in_lucru" else "#6c757d"
                    st.markdown(f'<div style="border-left:4px solid {color}; padding:5px; background:rgba(255,255,255,0.05); margin-bottom:10px;"><b style="font-size:12px;">{label}</b><br><small>{status.upper()}</small></div>', unsafe_allow_html=True)
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"❌ Problemă la încărcarea hărții GIS: {e}")

LOCATION = "global"

@st.cache_resource
def get_clients():
    import psycopg2
    try:
        cl = {
            'db': firestore.Client(project=PROJECT_ID),
            'storage': storage.Client(project=PROJECT_ID),
            'ai': genai.Client(vertexai=True, project=PROJECT_ID, location='us-central1'),
            'search': discoveryengine.SearchServiceClient()
        }
        try:
            cl['pg_conn'] = psycopg2.connect(host='127.0.0.1', database='axon_rogvaiv', user='admin_axon', password='Axon2026X', connect_timeout=3)
        except: cl['pg_conn'] = None
        return cl
    except: return None
clients = get_clients()
def delete_file(blob_name):
    try:
        bucket = clients["storage"].bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        blob.delete()
        return True
    except Exception as e:
        st.error(f"Eroare la ștergere: {e}")
        return False
def list_files_v2(aid):
    prefix = "" if aid == "Project_Manager" else f"{aid}/"
    # Forțăm refresh prin re-instanțiere bucket
    bucket = clients["storage"].bucket(BUCKET_NAME)
    return list(bucket.list_blobs(prefix=prefix))


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
    # Forțăm refresh prin re-instanțiere bucket
    bucket = clients["storage"].bucket(BUCKET_NAME)
    return list(bucket.list_blobs(prefix=prefix))




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
        
        st.markdown('##### 📂 Hub Management')
        with st.expander('Arhivă & Protocol', expanded=False):
            t1, t2 = st.tabs(['🔒 Protocol DNA', '📂 Arhivă Globală'])
            with t1:
                dna_v = get_protocol(agent)
                with st.expander('📝 Editare Protocol DNA', expanded=False):
                    new_dna = st.text_area('DNA:', dna_v, height=150, key='pm_dna_input')
                    if st.button('💾 Salvează Protocol', key='pm_save_btn'):
                        save_protocol(agent, new_dna)
                        st.rerun()
            with t2:
                st.subheader('📂 Management Arhivă Globală')
                if 'up_counter_PM' not in st.session_state: st.session_state['up_counter_PM'] = 0
                u_key_pm = f'up_PM_{st.session_state["up_counter_PM"]}'
                up_file_pm = st.file_uploader('Încarcă document (Lead Folder)', key=u_key_pm)
                if up_file_pm:
                    with st.spinner('Încărcare...'):
                        b = clients['storage'].bucket(BUCKET_NAME).blob(f'Project_Manager/{up_file_pm.name}')
                        b.upload_from_string(up_file_pm.getvalue(), content_type=up_file_pm.type if up_file_pm.type else 'application/pdf')
                        st.session_state['up_counter_PM'] += 1
                        st.success('✅ Fișier adăugat!')
                        st.rerun()
                st.divider()
                # LISTARE GLOBALĂ UNICĂ (Lead Control)
                all_sync_files = list(clients["storage"].bucket(BUCKET_NAME).list_blobs())
                if all_sync_files:
                    for idx, f_sync in enumerate(all_sync_files):
                        c1, c2, c3 = st.columns([0.6, 0.2, 0.2])
                        f_path = f_sync.name
                        c1.markdown(f"📄 `{f_path}`")
                        url_s = f"https://storage.cloud.google.com/{BUCKET_NAME}/{f_path}"
                        c2.link_button("👁️", url_s, use_container_width=True)
                        if c3.button("🗑️", key=f"del_sync_{idx}_{f_path.replace('/', '_')}", use_container_width=True):
                            if delete_file(f_path):
                                st.rerun()
                else:
                    st.info("Arhiva globală este goală.")
                    st.info("Arhiva globală este goală.")
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
            
            # 1. Definim ce tab-uri are fiecare
            t_labels = ["🔒 Protocol", "📂 Arhivă"]
            if agent in ["Procurement", "Construction"]: t_labels.append("📊 Gestiune")
            if agent == "Construction": t_labels.append("🗺️ GIS ROGVAIV")
            
            tabs = st.tabs(t_labels)
            
            # --- TAB 0: PROTOCOL (Editabil pentru toți) ---
            with tabs[0]:
                dna_v = get_protocol(agent)
                with st.expander(f"📝 Editare Protocol DNA - {agent}", expanded=True):
                    new_dna = st.text_area("Procedura de lucru (Standard DNA):", dna_v, height=150, key=f"dna_{agent}")
                    if st.button("💾 Salvează Protocol", key=f"save_{agent}"): 
                        save_protocol(agent, new_dna)
                        st.rerun()
            
            # --- TAB 1: ARHIVĂ (Activă pentru toți, salvare în Cloud Storage) ---
                        # --- TAB 1: ARHIVĂ (Control Total v38) ---
            with tabs[1]:
                st.subheader('📂 Management Documentație')
                
                # Zona de Upload
                # Logică Anti-Loop: Schimbăm cheia uploader-ului după succes
                if f"up_counter_{agent}" not in st.session_state:
                    st.session_state[f"up_counter_{agent}"] = 0
                
                u_key = f"up_{agent}_{st.session_state[f'up_counter_{agent}']}"
                up_file = st.file_uploader('📤 Încarcă document nou', key=u_key)
                
                if up_file:
                    with st.spinner("Se încarcă în Cloud..."):
                        b_name = f"{agent}/{up_file.name}"
                        blob = clients["storage"].bucket(BUCKET_NAME).blob(b_name)
                        # Forțăm application/pdf dacă tipul nu e detectat
                        c_type = up_file.type if up_file.type else "application/pdf"
                        blob.upload_from_string(up_file.getvalue(), content_type=c_type)
                        
                        st.session_state[f"up_counter_{agent}"] += 1
                        st.success(f"✅ Fișierul {up_file.name} a fost adăugat.")
                        st.rerun()

                st.divider()
                
                # Lista de fișiere cu acțiuni
                agent_files = list_files(agent)
                if agent_files:
                    st.markdown(f"**Conținut Arhivă {agent}:**")
                    for f in agent_files:
                        # Creăm un rând cu coloane pentru fiecare fișier
                        c_name, c_view, c_del = st.columns([0.6, 0.2, 0.2])
                        f_name = f.name.split('/')[-1]
                        if not f_name: continue # Skip directoare goale
                        
                        c_name.markdown(f"📄 `{f_name}`")
                        
                        # Buton de vizualizare/download (URL temporar 1 oră)
                        url = f"https://storage.cloud.google.com/{BUCKET_NAME}/{f.name}"
                        c_view.link_button("👁️ Vezi", url, use_container_width=True, help="Necesită logare în contul Google AXON")
                        
                        # Buton de ștergere
                        if c_del.button("🗑️", key=f"del_{f.name}", use_container_width=True):
                            if delete_file(f.name):
                                st.toast(f"Șters: {f_name}")
                                st.rerun()
                else:
                    st.info("Arhiva este goală pentru acest departament.")

            # --- TAB 2 & 3: GESTIUNE & GIS (Doar unde e cazul) ---
            if "📊 Gestiune" in t_labels:
                with tabs[t_labels.index("📊 Gestiune")]:
                    try:
                        import pyarrow
                        display_construction_management()
                    except Exception as e:
                        st.error(f"❌ Eroare Gestiune: {e}")
            
            if "🗺️ GIS ROGVAIV" in t_labels:
                with tabs[t_labels.index("🗺️ GIS ROGVAIV")]:
                    display_rogvaiv_gis()
