import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def phase_2():
    print("🏗️ RETA REPORTS: Raportare progres zilnic - 150 piloni...")
    doc_ref = db.collection("axon_inventory").document("LOT_PILE_RETA_START")
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        cust = data.get("Cantitate_Custodie", 0)
        
        doc_ref.update({
            "Cantitate_Custodie": cust - 150,
            "Cantitate_Instalata": 150, # Acesta este 'Raportat Constructor'
            "Status": "MONTAJ_ÎN_CURS"
        })
        print("✅ RETA a raportat 150 piloni instalați. Așteaptă validarea PM.")

if __name__ == "__main__":
    phase_2()
