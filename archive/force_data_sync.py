import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def sync():
    print("🔄 Sincronizare forțată date realizate...")
    docs = db.collection("axon_inventory").where("Material", "==", "IDM-PILE-C120").stream()
    for doc in docs:
        d = doc.to_dict()
        # Ne asigurăm că valoarea de 200 este în câmpul Cantitate_Instalata
        if "Lot" not in d.get("Material", ""):
            doc.reference.update({"Cantitate_Instalata": 200, "Cantitate_Custodie": 885})
            print(f"✅ Piloni Master: 200 Realizat / 885 Custodie")
        else:
            doc.reference.update({"Cantitate_Instalata": 0, "Cantitate_Custodie": 0})
sync()
