import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V46 (ORGANIZARE CATEGORII) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]
                    
                    if data:
                        df = pd.DataFrame(data)
                        
                        # 1. STANDARDIZARE DATE
                        cols_num = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Validata']
                        for col in cols_num:
                            if col in df.columns:
                                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                        
                        df['Categorie'] = df['Categorie'].astype(str).str.strip()
                        # 'Mat_Baza' elimină orice text din paranteze: "IDM-TRK-S1 (ALMA)" -> "IDM-TRK-S1"
                        df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0].strip())
                        
                        st.subheader('📊 CONTROL OPERAȚIONAL EPC')
                        
                        # 2. CALCUL SINTEZĂ (PENTRU TABELUL DE SUS)
                        summary = df.groupby(['Categorie', 'Mat_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Custodie': 'sum',
                            'Cantitate_Validata': 'sum'
                        }).reset_index()

                        # 3. ORGANIZARE PE CELE 6 CATEGORII OFICIALE
                        ord_cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        
                        for cat_name in ord_cats:
                            # Filtrare precisă pe categorie
                            c_df = summary[summary['Categorie'] == cat_name].copy()
                            
                            with st.expander(f"📁 {cat_name.upper()} ({len(c_df)})"):
                                if not c_df.empty:
                                    # Calculăm 'În Depozit' conform regulii generale
                                    c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])
                                    
                                    # Redenumire coloane pentru interfață
                                    c_view = c_df.rename(columns={
                                        'Mat_Baza': 'Articol / Cod Material',
                                        'Cantitate_Planificata': 'Planificat',
                                        'Cantitate_Receptionata': 'Total Intrat',
                                        'Cantitate_Custodie': 'În Custodie',
                                        'Cantitate_Validata': 'Realizat (PV)'
                                    })
                                    
                                    # Afișare tabel sinteză
                                    display_cols = ['Articol / Cod Material', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)']
                                    st.dataframe(c_view[display_cols], use_container_width=True, hide_index=True)
                                else:
                                    st.info(f"Niciun material înregistrat în categoria {cat_name}.")

                        st.markdown('---')
                        # 4. TABELUL DE JOS - DETALIU CUSTODIE
                        st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')
                        cust_df = df[df['Material'].str.contains(r'\(', na=False) | (df['Cantitate_Custodie'] > 0) | (df['Cantitate_Validata'] > 0)].copy()
                        if not cust_df.empty:
                            cust_view = cust_df.rename(columns={'Cantitate_Validata': 'Validat (PV)'})
                            st.dataframe(cust_view[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']], 
                                         use_container_width=True, hide_index=True)
                        else:
                            st.write("ℹ️ Nu există materiale predate în custodie către contractori.")
                            
                except Exception as e:
                    st.error(f"Eroare Gestiune: {e}")
                # --- END AXON GESTIUNE ---"""

content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("✅ [V46.0]: Sistem de categorii și grupare consolidat.")
