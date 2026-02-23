import os
import re

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    content = f.read()

# Definim codul curat pentru Tab-ul Gestiune
# Am eliminat complet sectiunea "CONTROL CUSTODIE ȘI PROGRES"
# Am asigurat vizibilitatea coloanei Realizat (Instalata)
new_gestiune_code = """with tabs[2]:
                # --- START AXON GESTIUNE V32 (CLEAN) ---
                try:
                    import pandas as pd
                    from google.cloud import firestore
                    db_v = firestore.Client()
                    
                    # Citire date din Firestore
                    docs = db_v.collection('axon_inventory').stream()
                    data = [d.to_dict() for d in docs]
                    
                    if data:
                        df = pd.DataFrame(data)
                        
                        # Conversie numerica obligatorie pentru a vedea sumele corect
                        numeric_cols = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata']
                        for col in numeric_cols:
                            if col in df.columns:
                                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                        
                        st.subheader('📊 CONTROL OPERAȚIONAL EPC')
                        
                        # Pregatire Summary (Tabelul de sus)
                        # Extragerea numelui de baza (ex: IDM-PILE din IDM-PILE-C120)
                        df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])
                        
                        summary = df.groupby(['Categorie', 'Material_Baza']).agg({
                            'Cantitate_Planificata': 'sum',
                            'Cantitate_Receptionata': 'sum',
                            'Cantitate_Custodie': 'sum',
                            'Cantitate_Instalata': 'sum'
                        }).reset_index()
                        
                        # Afisare pe categorii
                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
                        for c in cats:
                            c_df = summary[summary['Categorie'].str.strip() == c]
                            with st.expander(f"📁 {c.upper()} ({len(c_df)})"):
                                if not c_df.empty:
                                    # Redenumim pentru interfata: Cantitate_Instalata -> Realizat
                                    c_disp = c_df.rename(columns={'Cantitate_Instalata': 'Realizat'})
                                    st.dataframe(c_disp[['Material_Baza', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Realizat']], 
                                                 use_container_width=True, hide_index=True)

                        st.markdown('---')
                        st.subheader('📈 DETALII CUSTODIE CONTRACTORI')
                        
                        # Tabelul de jos (Doar ce e in lucru)
                        custody_view = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0)].copy()
                        if not custody_view.empty:
                            custody_view = custody_view.rename(columns={'Cantitate_Instalata': 'Realizat'})
                            cols_detaliu = ['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Realizat', 'Status']
                            st.dataframe(custody_view[[c for c in cols_detaliu if c in custody_view.columns]], 
                                         use_container_width=True, hide_index=True)
                        else:
                            st.info("Momentan nu există materiale predate în custodie.")
                            
                except Exception as e:
                    st.error(f"Eroare Gestiune: {e}")
                # --- END AXON GESTIUNE ---"""

# Inlocuire folosind marcatorii de inceput de tab si sfarsit de sectiune
# Aceasta metoda elimina tot ce era intre ele (inclusiv dashboard-ul vechi)
content = re.sub(r"with tabs\[2\]:.*?# --- END AXON GESTIUNE ---", new_gestiune_code, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("✅ [V32.0]: Sectiunea veche stearsa. Coloana 'Realizat' activata. Nomenclatorul nu a fost atins.")
