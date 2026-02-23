import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def report():
    print("🏗️ ALMA CONSTRUCT: Raportare montaj 50 piloni...")
    doc_ref = db.collection("axon_inventory").document("LOT_PILE_ALMA_01")
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        cust = data.get("Cantitate_Custodie", 0)
        real = data.get("Cantitate_Instalata", 0)
        
        doc_ref.update({
            "Cantitate_Custodie": cust - 50,
            "Cantitate_Instalata": real + 50,
            "Status": "MONTAJ_IN_CURS"
        })
        print("✅ ALMA: 50 piloni raportați ca realizați.")

if __name__ == "__main__":
    report()
