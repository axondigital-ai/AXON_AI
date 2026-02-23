import streamlit as st
import pandas as pd
import google.cloud.firestore as firestore
import os

# Configurare acces
PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def run_view():
    st.set_page_config(layout="wide")
    st.title("📂 Gestiune Proiect ROGVAIV - Vizualizare Ierarhică")
    st.write("---")

    # 1. Extragem datele
    docs = db.collection("axon_inventory").stream()
    data = [doc.to_dict() for doc in docs]
    
    if not data:
        st.error("❌ Nu am găsit date în 'axon_inventory'. Rulează mai întâi scriptul de injectare!")
        return

    df = pd.DataFrame(data)

    # 2. Categorii Master (Ordinea EPC)
    categories = ["Major Assets", "Mechanical", "DC Electrical", "AC Electrical", "Earthing", "Consumables"]

    # 3. Interfața de tip Drill-Down
    for cat in categories:
        cat_df = df[df['Categorie'] == cat]
        
        if not cat_df.empty:
            # Creăm un expander care stă închis implicit (clean UI)
            with st.expander(f"📁 {cat.upper()} — {len(cat_df)} repere identificate"):
                # Selectăm doar coloanele importante pentru manager
                cols_to_show = ['Material', 'Cantitate', 'UM', 'Status']
                st.table(cat_df[cols_to_show].reset_index(drop=True))
                
                # Calcul rapid total pe categorie
                total_cat = cat_df['Cantitate'].sum()
                st.info(f"💡 Total unități planificate în categoria {cat}: {total_cat:,}")
        else:
            st.sidebar.warning(f"Categoria {cat} nu are date.")

if __name__ == "__main__":
    # Notă: Acest script se rulează cu 'streamlit run'
    run_view()
