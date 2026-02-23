import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V36 (VALIDATION LOGIC) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]
                    
                    if data:
                        df = pd.DataFrame(data)
                        # Asigurăm coloanele numerice (adăugăm Cantitate_Validata)
                        cols_num = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata']
                        for col in cols_num:
                            if col not in df.columns: df[col] = 0
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                        
                        st.subheader('📊 CONTROL OPERAȚIONAL EPC (DATE VALIDATE)')
                        df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])
                        
                        # Tabelul de sus calculează suma doar pe VALIDAT
                        summary = df.groupby(['Categorie', 'Material_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Validata': 'sum'
                        }).reset_index()
                        
                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        for c in cats:
                            c_df = summary[summary['Categorie'].str.strip() == c]
                            with st.expander(f"📁 {c.upper()} ({len(c_df)})"):
                                if not c_df.empty:
                                    st.dataframe(c_df.rename(columns={'Cantitate_Validata': 'Realizat (Validat)'}), 
                                                 use_container_width=True, hide_index=True)

                        st.markdown('---')
                        st.subheader('📈 DETALII CONTRACTORI (RAPORTAT VS VALIDAT)')
                        
                        # Tabelul de jos arată tot: Custodie, ce a raportat el și ce ai validat tu
                        cust_view = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0) | (df['Cantitate_Validata'] > 0)].copy()
                        if not cust_view.empty:
                            cust_view = cust_view.rename(columns={
                                'Cantitate_Instalata': 'Raportat Constructor',
                                'Cantitate_Validata': 'Validat PM'
                            })
                            cols_det = ['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Raportat Constructor', 'Validat PM', 'Status']
                            st.dataframe(cust_view[cols_det], use_container_width=True, hide_index=True)
                except Exception as e: st.error(f"Eroare: {e}")
                # --- END AXON GESTIUNE ---"""

content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("✅ [V36.0]: Interfață actualizată cu logica de Validare PM.")
