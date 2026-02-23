import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def reset_all():
    print("🧹 AXON: Resetare generală pentru testare regulă...")
    docs = db.collection("axon_inventory").stream()
    for doc in docs:
        d = doc.to_dict()
        if "(" in d.get("Material", "") or doc.id.startswith("LOT_"):
            doc.reference.delete()
        else:
            doc.reference.update({
                "Cantitate_Receptionata": 0,
                "Cantitate_Custodie": 0,
                "Cantitate_Instalata": 0,
                "Cantitate_Validata": 0,
                "Status": "PLANIFICAT"
            })
    print("✅ Sistemul este acum curat. Gata pentru Testul Oficial.")

reset_all()
