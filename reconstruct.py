import os

path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Găsim limitele craterei (de la funcția nouă până la codul agenților departamentali)
start_idx = content.find("def get_dynamic_context_for_agent")
end_string = "st.session_state[pm_mem_key].append({'role': 'assistant', 'content': full_response})"
end_idx = content.find(end_string)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_string)
    
    # RECONSTRUCȚIA MILIMETRICĂ A INTERFEȚEI ȘI LOGICII PIERDUTE
    rebuilt_code = """def get_dynamic_context_for_agent(agent_name, user_query, conversation_history_list):
    context_parts = []
    if agent_name != 'Project_Manager':
        dna = get_protocol(agent_name)
        if dna: context_parts.append(f"--- PROTOCOL AGENT ({agent_name}) ---\\n{dna}")
    k = search_rag(user_query)
    if k: context_parts.append(f"--- REZULTATE RAG ---\\n{k}")
    agent_docs = read_agent_texts(agent_name)
    if agent_docs and "Niciun text găsit" not in agent_docs:
        context_parts.append(f"--- DOCUMENTE AGENT ---\\n{agent_docs}")
    keywords = ["material", "inventar", "stoc", "cant", "factur", "doc", "fisier", "progres"]
    if agent_name == 'Project_Manager' or any(kw in user_query.lower() for kw in keywords):
        inv = get_global_inventory() if agent_name == 'Project_Manager' else get_agent_inventory(agent_name)
        context_parts.append(f"--- INVENTAR ---\\n{inv}")
    recent_history = conversation_history_list[-10:] if len(conversation_history_list) > 10 else conversation_history_list
    if recent_history:
        h_str = '\\n'.join([str(m['role']) + ': ' + str(m['content']) for m in recent_history])
        context_parts.append(f"--- ISTORIC RECENT ---\\n{h_str}")
    return "\\n\\n".join(context_parts)

# --- UI ---
with st.sidebar:
    st.divider()
    up = st.file_uploader('⬆️ Încarcă Document AXON', type=['pdf', 'docx', 'txt'])
    if up and up.name != st.session_state.get('last_uploaded'):
        with st.spinner('Transfer în Storage...'):
            dest = f'{st.session_state.current_p}/{up.name}' if 'current_p' in st.session_state else up.name
            if upload_to_gcs(up, dest):
                st.session_state.last_uploaded = up.name
                st.success('✅ Document stocat.')
                st.rerun()
    elif up:
        st.success('✅ Document activ în sesiune.')
    st.divider()
    if st.button('🏠 Ecran Principal'):
        if 'current_p' in st.session_state: del st.session_state.current_p
        st.rerun()
    st.divider()
    if st.button('📁 Lead: Project Manager'): st.session_state.current_p = 'Project_Manager'
    for grp, ags in {'🧠 Control': ['Planning', 'Cost_Control', 'Commercial', 'Risk_Management'], 
                     '🛠️ Execuție': ['Engineering', 'Procurement', 'Construction', 'Commissioning'],
                     '🛡️ Guvernanță': ['HSE', 'QA_QC', 'Finance_Audit']}.items():
        with st.expander(grp):
            for a in ags:
                if st.button(a.replace('_', ' ')): st.session_state.current_p = a

if "current_p" not in st.session_state:
    st.title("🚀 AXON AI Dashboard")
    h = get_detailed_health()
    h_cols = st.columns(3)
    for i, (serv, stat) in enumerate(h.items()):
        color = "#28a745" if "🟢" in stat else "#dc3545"
        h_cols[i % 3].markdown(f'<div style="padding:15px; border:2px solid {color}; border-radius:10px; text-align:center; margin-bottom:10px;"><p style="margin:0; font-size:14px; font-weight:bold;">{serv}</p><h4 style="margin:0; color:{color}; font-size:22px;">{stat}</h4></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📋 Facilități și Funcționalități Complete")
    f1, f2, f3 = st.columns(3)
    with f1: st.info('**🧬 Genetic DNA Protocols**\\nProtocoale NoSQL Firestore.')
    with f2: st.info('**📂 Hybrid RAG System**\\nVertex AI Search cu Storage Injection.')
    with f3: st.info('**🛡️ Multi-Agent Audit**\\n12 departamente sincronizate.')
    
    st.markdown("---")
    st.subheader("👨‍💻 Agent Programator (AXON Architect)")
    if st.button("🔄 Sincronizare Cod AXON (Read Codebase)", use_container_width=True):
        with st.spinner("Scanez arhitectura, structura de fișiere și bibliotecile..."):
            st.session_state.axon_codebase_cache = get_axon_codebase()
            st.success("✅ Cod sincronizat în memoria agentului!")
    mem_key_dev = 'chat_history_Programator'
    if mem_key_dev not in st.session_state: st.session_state[mem_key_dev] = []
    for msg in st.session_state[mem_key_dev]:
        with st.chat_message(msg['role']): st.markdown(msg['content'])
    if p_dev := st.chat_input("Discută cu arhitectul AXON despre cod sau structură..."):
        st.session_state[mem_key_dev].append({'role': 'user', 'content': p_dev})
        with st.chat_message('user'): st.markdown(p_dev)
        with st.chat_message('assistant'):
            code_context = st.session_state.get('axon_codebase_cache', '[Apasă Sincronizare pentru a citi fișierele]')
            history_text = '\\n'.join([str(m['role']) + ': ' + str(m['content']) for m in st.session_state[mem_key_dev][:-1]])
            sys_msg = f'''DIRECTIVĂ: Ești Agentul Programator AXON CORE.\\nRol: analizezi, faci debugging și scrii cod pe baza structurii de mai jos.\\n\\nCOD ACTUAL:\\n{code_context[:800000]}\\n\\nISTORIC:\\n{history_text}'''
            conf = GenerateContentConfig(temperature=0.1)
            response_placeholder = st.empty()
            full_response = ''
            try:
                for chunk in clients['ai'].models.generate_content_stream(model='gemini-2.5-flash', contents=[sys_msg, p_dev], config=conf):
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + '▌')
                response_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f'❌ Eroare AI: {e}'
                response_placeholder.error(full_response)
            st.session_state[mem_key_dev].append({'role': 'assistant', 'content': full_response})

else:
    agent = st.session_state.current_p
    if agent == 'Project_Manager':
        st.title(f'👑 Lead: {agent.replace("_", " ")}')
        pulse_cols = st.columns(len(DEPT_CATEGORIES))
        all_blobs = list(clients['storage'].bucket(BUCKET_NAME).list_blobs())
        for i, (dept, _) in enumerate(DEPT_CATEGORIES.items()):
            active = any(b.name.startswith(f'{dept}/') for b in all_blobs)
            pulse_cols[i].caption(f"{'🟢' if active else '⚪'} {dept[:4]}")
        st.markdown('##### 📂 Hub Management')
        with st.expander('Arhivă & Protocol', expanded=False):
            t1, t2 = st.tabs(['🔒 Protocol DNA', '📂 Arhivă Globală'])
            with t1:
                dna_v = get_protocol(agent)
                new_dna = st.text_area('DNA:', dna_v, height=150, key='pm_dna_input')
                if st.button('💾 Salvează Protocol', key='pm_save_btn'):
                    save_protocol(agent, new_dna)
                    st.rerun()
            with t2:
                st.subheader('📂 Management Arhivă Globală')
                if all_blobs:
                    for idx, f_b in enumerate(all_blobs):
                        c1, c2, c3 = st.columns([0.6, 0.2, 0.2])
                        c1.markdown(f'📄 `{f_b.name}`')
                        url_f = f'https://storage.cloud.google.com/{BUCKET_NAME}/{f_b.name}'
                        c2.link_button('👁️', url_f, use_container_width=True)
                        if c3.button('🗑️', key=f'del_l_{idx}_{f_b.name.replace("/", "_")}', use_container_width=True):
                            if delete_file(f_b.name): st.rerun()
                else:
                    st.info('Arhiva globală este goală.')
        st.divider()
        
        pm_mem_key = 'chat_history_PM_MASTER'
        if pm_mem_key not in st.session_state:
            st.session_state[pm_mem_key] = []
        for msg in st.session_state[pm_mem_key]:
            with st.chat_message(msg['role']): st.markdown(msg['content'])
            
        if p := st.chat_input('Introdu directiva strategică pentru PM MASTER...'):
            st.session_state[pm_mem_key].append({'role': 'user', 'content': p})
            with st.chat_message('user'): st.markdown(p)
            with st.chat_message('assistant'):
                conf = GenerateContentConfig(tools=[Tool(google_search=GoogleSearch())], temperature=0.1)
                dynamic_context = get_dynamic_context_for_agent('Project_Manager', p, st.session_state[pm_mem_key][:-1])
                sys_msg = f'''DIRECTIVĂ STRICTĂ: Ești PM MASTER (Lead) în AXON CORE. Ești comandantul suprem.\\nNU da disclaimere. NU spune că ești AI. Ai acces TOTAL la fișiere.\\n\\n--- CONTEXT DINAMIC PENTRU ANALIZĂ ---\\n{dynamic_context}'''
                response_placeholder = st.empty()
                full_response = ''
                try:
                    for chunk in clients['ai'].models.generate_content_stream(model='gemini-2.5-flash', contents=[sys_msg, p], config=conf):
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + '▌')
                    response_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f'❌ Eroare AI: {e}'
                    response_placeholder.error(full_response)
                st.session_state[pm_mem_key].append({'role': 'assistant', 'content': full_response})"""
    
    # Executăm sudura
    content = content[:start_idx] + rebuilt_code + content[end_idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ [RESURRECTION]: Interfața Streamlit a fost reconstruită complet și cuplată la Creierul Dinamic!")
else:
    print("❌ EROARE CRITICĂ: Nu am găsit zona de impact. Fișierul este compromis diferit.")
