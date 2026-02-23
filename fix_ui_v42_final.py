import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V42 (TITLURI FINALE) ---
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
                        
                        # Tabelul EPC (SUS)
                        summary = df.groupby(['Categorie', 'Mat_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Custodie': 'sum',
                            'Cantitate_Validata': 'sum'
                        }).reset_index()

                        st.subheader('📊 CONTROL OPERAȚIONAL EPC')
                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        for c in cats:
                            c_df = summary[summary['Categorie'].str.strip() == c].copy()
                            if not c_df.empty:
                                c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])
                                c_df = c_df.rename(columns={'Cantitate_Planificata': 'Planificat', 'Cantitate_Receptionata': 'Total Intrat', 'Cantitate_Custodie': 'În Custodie', 'Cantitate_Validata': 'Realizat (PV)'})
                                with st.expander(f"📁 {c.upper()} ({len(c_df)})"):
                                    st.dataframe(c_df[['Mat_Baza', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)']], use_container_width=True, hide_index=True)

                        st.markdown('---')
                        st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')
                        # Afișăm loturile contractorilor (cele care au paranteze în nume sau au custodie/validat)
                        cust_df = df[df['Material'].str.contains(r'\(', na=False) | (df['Cantitate_Custodie'] > 0) | (df['Cantitate_Validata'] > 0)].copy()
                        if not cust_df.empty:
                            cust_df = cust_df.rename(columns={'Cantitate_Validata': 'Validat (PV)'})
                            st.dataframe(cust_df[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']], use_container_width=True, hide_index=True)
                        else:
                            st.info("ℹ️ Nu există materiale predate în custodie. Efectuați un 'Handover' pentru a popula acest tabel.")
                except Exception as e: st.error(f"Eroare UI: {e}")
                # --- END AXON GESTIUNE ---"""

content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)
with open(file_path, "w") as f:
    f.write(content)
