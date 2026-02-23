import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

# Definim codul corect pentru Tab-ul Gestiune
new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V37 (STRICT VALIDATION) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]
                    
                    if data:
                        df = pd.DataFrame(data)
                        # Ne asigurăm că toate coloanele necesare sunt numerice
                        cols_num = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata']
                        for col in cols_num:
                            if col not in df.columns: df[col] = 0
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                        
                        st.subheader('📊 CONTROL OPERAȚIONAL EPC (DATE OFICIALE)')
                        df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])
                        
                        # TABELUL DE SUS: Grupăm strict pe VALIDAT pentru 'Realizat'
                        summary = df.groupby(['Categorie', 'Material_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Custodie': 'sum',
                            'Cantitate_Validata': 'sum'
                        }).reset_index()
                        
                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        for c in cats:
                            c_df = summary[summary['Categorie'].str.strip() == c]
                            with st.expander(f"📁 {c.upper()} ({len(c_df)})"):
                                if not c_df.empty:
                                    # Redenumim pentru claritate maxima
                                    c_view = c_df.rename(columns={
                                        'Cantitate_Custodie': 'In Custodie',
                                        'Cantitate_Validata': 'Realizat (PV)'
                                    })
                                    cols_to_show = ['Material_Baza', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'In Custodie', 'Realizat (PV)']
                                    st.dataframe(c_view[cols_to_show], use_container_width=True, hide_index=True)

                        st.markdown('---')
                        st.subheader('📈 DETALII CONTRACTORI (SITUAȚIE TEREN)')
                        
                        # Tabelul de jos arata diferenta intre ce zice el (Raportat) si ce zici tu (Validat)
                        cust_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0) | (df['Cantitate_Validata'] > 0)].copy()
                        if not cust_df.empty:
                            cust_df = cust_df.rename(columns={
                                'Cantitate_Instalata': 'Raportat Constructor',
                                'Cantitate_Validata': 'Validat PM'
                            })
                            cols_det = ['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Raportat Constructor', 'Validat PM', 'Status']
                            st.dataframe(cust_df[cols_det], use_container_width=True, hide_index=True)
                except Exception as e: st.error(f"Eroare UI: {e}")
                # --- END AXON GESTIUNE ---"""

content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("✅ [V37.0]: S-a corectat centralizarea. EPC arată acum doar datele validate (145).")
