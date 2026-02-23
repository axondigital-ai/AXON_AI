import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V48 (PROGRESS ANALYTICS) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]
                    
                    if data:
                        df = pd.DataFrame(data)
                        for c in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Validata']:
                            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
                        
                        df['Categorie'] = df['Categorie'].astype(str).str.strip()
                        df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0].strip())
                        
                        st.subheader('📊 CONTROL OPERAȚIONAL EPC (PROGRES REALIZAT)')
                        
                        summary = df.groupby(['Categorie', 'Mat_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Custodie': 'sum',
                            'Cantitate_Validata': 'sum'
                        }).reset_index()

                        ord_cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        
                        for cat_name in ord_cats:
                            c_df = summary[summary['Categorie'] == cat_name].copy()
                            
                            with st.expander(f"📁 {cat_name.upper()} ({len(c_df)})"):
                                if not c_df.empty:
                                    # LOGICA DE CALCUL
                                    c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])
                                    
                                    # Calcul % Progres (Validat vs Planificat)
                                    c_df['% Progres'] = (c_df['Cantitate_Validata'] / c_df['Cantitate_Planificata']).fillna(0)
                                    
                                    c_view = c_df.rename(columns={
                                        'Mat_Baza': 'Articol',
                                        'Cantitate_Planificata': 'Planificat',
                                        'Cantitate_Receptionata': 'Total Intrat',
                                        'Cantitate_Custodie': 'În Custodie',
                                        'Cantitate_Validata': 'Realizat (PV)'
                                    })
                                    
                                    # Afișare cu Progress Bar
                                    st.dataframe(
                                        c_view[['Articol', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)', '% Progres']],
                                        use_container_width=True,
                                        hide_index=True,
                                        column_config={
                                            "% Progres": st.column_config.ProgressColumn(
                                                "Progres Execuție",
                                                help="Procentul de lucrări validate prin PV",
                                                format="%.0f%%",
                                                min_value=0,
                                                max_value=1
                                            )
                                        }
                                    )
                                else:
                                    st.info(f"Niciun material în {cat_name}.")

                        st.markdown('---')
                        st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')
                        cust_df = df[df['Material'].str.contains(r'\(', na=False) | (df['Cantitate_Custodie'] > 0) | (df['Cantitate_Validata'] > 0)].copy()
                        if not cust_df.empty:
                            st.dataframe(cust_df.rename(columns={'Cantitate_Validata': 'Validat (PV)'})[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']], use_container_width=True, hide_index=True)
                except Exception as e: st.error(f"Eroare Gestiune: {e}")
                # --- END AXON GESTIUNE ---"""

content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)
with open(file_path, "w") as f:
    f.write(content)
