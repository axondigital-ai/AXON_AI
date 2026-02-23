import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def report_production():
    print("🏗️ AXON CONSTRUCTION: Se raportează montajul a 100 panouri PV...")
    
    # Referință către lotul aflat în custodia RETA
    doc_ref = db.collection("axon_inventory").document("LOT_PV_RETA_01")
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        custodie_actuala = data.get("Cantitate_Custodie", 0)
        realizat_anterior = data.get("Cantitate_Instalata", 0)
        
        if custodie_actuala >= 100:
            doc_ref.update({
                "Cantitate_Custodie": custodie_actuala - 100,
                "Cantitate_Instalata": realizat_anterior + 100,
                "Status": "MONTAJ_IN_CURS"
            })
            print(f"✅ Succes: 100 panouri au fost montate pe trackere.")
            print(f"📊 Rămase în custodia RETA: {custodie_actuala - 100}")
            print(f"📈 Total realizat pe acest lot: {realizat_anterior + 100}")
        else:
            print("⚠️ Eroare: Cantitate insuficientă în custodie pentru raportare!")
    else:
        print("⚠️ Eroare: Lotul de custodie PV pentru RETA nu a fost găsit!")

if __name__ == "__main__":
    report_production()
