import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V39 (TOTAL STOCK CONTROL) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]
                    
                    if data:
                        df = pd.DataFrame(data)
                        for c in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata']:
                            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
                        
                        df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])
                        
                        # --- LOGICA GENERALĂ DE CALCUL ---
                        # 1. Recepționat Total = Suma tuturor intrărilor
                        # 2. În Custodie = Ce e la contractori dar NU e încă validat
                        # 3. Realizat = Ce e validat prin PV
                        # 4. În Depozit = Recepționat - (Custodie + Realizat)
                        
                        summary = df.groupby(['Categorie', 'Mat_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Custodie': 'sum',
                            'Cantitate_Validata': 'sum'
                        }).reset_index()

                        st.subheader('📊 CONTROL OPERAȚIONAL EPC (STOCURI ȘI PROGRES)')
                        
                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        for c in cats:
                            c_df = summary[summary['Categorie'].str.strip() == c].copy()
                            if not c_df.empty:
                                # Aplicăm Regula Generală pe coloane
                                c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])
                                c_df = c_df.rename(columns={
                                    'Cantitate_Planificata': 'Planificat',
                                    'Cantitate_Receptionata': 'Total Intrat',
                                    'Cantitate_Custodie': 'În Custodie',
                                    'Cantitate_Validata': 'Realizat (PV)'
                                })
                                with st.expander(f"📁 {c.upper()} ({len(c_df)})"):
                                    st.dataframe(c_df[['Mat_Baza', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)']], 
                                                 use_container_width=True, hide_index=True)

                        st.markdown('---')
                        st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')
                        cust_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0) | (df['Cantitate_Validata'] > 0)].copy()
                        if not cust_df.empty:
                            st.dataframe(cust_df[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata', 'Status']], 
                                         use_container_width=True, hide_index=True)
                except Exception as e: st.error(f"Eroare Gestiune: {e}")
                # --- END AXON GESTIUNE ---"""

content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)
