import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

# Definim noul cod pentru Tab-ul 2
new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V31 (ORGANIZAT) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]
                    if data:
                        df = pd.DataFrame(data)
                        # Conversie numerica sigura
                        for c in ['Cantitate_Planificata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Receptionata']:
                            if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
                        
                        st.subheader('📊 CONTROL OPERAȚIONAL EPC')
                        df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])
                        
                        # Tabelul de sus: Organizat pe categorii si componente principale
                        summ = df.groupby(['Categorie', 'Material_Baza']).agg({
                            'Cantitate_Planificata': 'sum', 'Cantitate_Receptionata': 'sum', 
                            'Cantitate_Custodie': 'sum', 'Cantitate_Instalata': 'sum'
                        }).reset_index()
                        
                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        for c in cats:
                            c_df = summ[summ['Categorie'].str.strip() == c]
                            with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):
                                if not c_df.empty:
                                    c_view = c_df.rename(columns={'Cantitate_Instalata': 'Realizat'})
                                    cols_v = ['Material_Baza', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Realizat']
                                    st.dataframe(c_view[cols_v], use_container_width=True, hide_index=True)

                        st.markdown('---')
                        st.subheader('📈 DETALII CUSTODIE CONTRACTORI')
                        cust_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0)]
                        if not cust_df.empty:
                            cust_view = cust_df.rename(columns={'Cantitate_Instalata': 'Realizat'})
                            cols_c = ['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Realizat', 'Status']
                            st.dataframe(cust_view[[col for col in cols_c if col in cust_view.columns]], use_container_width=True, hide_index=True)
                        else:
                            st.info('Nu există materiale predate în custodie.')
                except Exception as e: st.error('Eroare: ' + str(e))
                # --- END AXON GESTIUNE ---"""

# Inlocuim tot ce este intre 'with tabs[2]:' si '# --- END AXON GESTIUNE ---'
content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("✅ [V31.0]: Interfata restaurata cu categorii si fara sectiunea problematica.")
