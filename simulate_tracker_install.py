import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def simulate():
    print("🏗️ AXON: Simulare Montaj Structură...")
    inv_ref = db.collection("axon_inventory")
    
    # 1. Pregătim Torque Tubes (IDM-TT-OCT-80)
    tt_docs = inv_ref.where("Material", "==", "IDM-TT-OCT-80").stream()
    for doc in tt_docs:
        doc.reference.update({
            "Cantitate_Custodie": 1000, # Predăm 1000 ml în custodie
            "Cantitate_Instalata": 450, # Din care 450 ml sunt deja montați
            "Contractor_Custodie": "RETA_STRUCT_TEAM_01",
            "Status": "MONTAJ_STRUCTURA"
        })
        print("✅ Torque Tubes: 1000ml în Custodie / 450ml Realizat")

    # 2. Pregătim Drive Systems (IDM-DRV-LTEC-C)
    drv_docs = inv_ref.where("Material", "==", "IDM-DRV-LTEC-C").stream()
    for doc in drv_docs:
        doc.reference.update({
            "Cantitate_Custodie": 20, # Predăm 20 motoare
            "Cantitate_Instalata": 5,  # 5 sunt deja pe poziție
            "Contractor_Custodie": "RETA_STRUCT_TEAM_01",
            "Status": "INSTALARE_MOTOARE"
        })
        print("✅ Drive Systems: 20 unități în Custodie / 5 Realizat")

simulate()
