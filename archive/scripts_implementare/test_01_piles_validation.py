import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def phase_3():
    print("📋 AXON PM: Validare Proces Verbal de Recepție...")
    doc_ref = db.collection("axon_inventory").document("LOT_PILE_RETA_START")
    doc = doc_ref.get()
    
    if doc.exists:
        # Validăm 145 din cei 150 raportați
        doc_ref.update({
            "Cantitate_Validata": 145,
            "Status": "VALIDAT_PARTIAL_PV"
        })
        print("✅ PV Semnat: 145 piloni au fost validați calitativ.")
        print("⚠️ Notă: 5 piloni raportați rămân nevalidați până la remediere.")

if __name__ == "__main__":
    phase_3()
