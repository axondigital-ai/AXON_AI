import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def receptie_finala():
    print("🚛 AXON: Finalizare recepție materiale critice...")
    
    materiale = {
        "SUN2000-330KTL-H1": {"qty": 40, "cat": "Major Assets"},      # 40 Invertoare
        "DC-SOL-6-BK": {"qty": 15000, "cat": "DC Electrical"},        # 15km Cablu Negru
        "DC-SOL-6-RED": {"qty": 15000, "cat": "DC Electrical"},       # 15km Cablu Roșu
        "AL-NA2XY-4X185": {"qty": 2000, "cat": "AC Electrical"}       # 2km Cablu AC
    }

    for mat, info in materiale.items():
        docs = db.collection("axon_inventory").where("Material", "==", mat).stream()
        for doc in docs:
            doc.reference.update({
                "Cantitate_Receptionata": info["qty"],
                "Status": "STOC_CENTRAL"
            })
            print(f"✅ {mat}: {info['qty']} recepționate în {info['cat']}.")

receptie_finala()
