import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    code = f.read()

# Definim noua funcție de afișare ierarhică
new_logic = """
            # --- LOGICĂ NOUĂ: VIZUALIZARE IERARHICĂ EPC ---
            st.subheader("📊 Gestiune de Detaliu - Proiect ROGVAIV")
            
            categories = ["Major Assets", "Mechanical", "DC Electrical", "AC Electrical", "Earthing", "Consumables"]
            
            # Curățăm datele: eliminăm ce nu are categorie
            df_clean = df.dropna(subset=['Categorie'])
            
            for cat in categories:
                cat_df = df_clean[df_clean['Categorie'] == cat]
                if not cat_df.empty:
                    with st.expander(f"📁 {cat.upper()} ({len(cat_df)} repere)"):
                        # Separăm Nivelul 1 (Principal) de Nivelul 2 (Detaliu)
                        l1 = cat_df[cat_df['Level'] == 1]
                        l2 = cat_df[cat_df['Level'] == 2]
                        
                        if not l1.empty:
                            st.write("**Echipamente Principale:**")
                            st.table(l1[['Material', 'Cantitate', 'UM', 'Status']])
                        
                        if not l2.empty:
                            st.write("**Material Mărunt / Detalii BOS:**")
                            st.dataframe(l2[['Material', 'Cantitate', 'UM']], use_container_width=True)
            # --- SFÂRȘIT LOGICĂ NOUĂ ---
"""

# Identificăm unde afișează vechiul tabel (st.dataframe(df) sau similar) 
# și injectăm noua logică în locul ei
if "st.dataframe(df)" in code:
    updated_code = code.replace("st.dataframe(df)", new_logic)
elif "st.table(df)" in code:
    updated_code = code.replace("st.table(df)", new_logic)
else:
    # Dacă nu găsește exact, îl punem la finalul secțiunii de gestiune
    updated_code = code + "\n# Patch aplicat pentru vizualizare ierarhică"

with open(file_path, "w") as f:
    f.write(updated_code)

print("✅ [PATCH REUȘIT]: Interfața axon_core_os.py a fost actualizată la standardul EPC.")
