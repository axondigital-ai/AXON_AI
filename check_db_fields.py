import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

docs = db.collection("axon_inventory").stream()
print(f"{'MATERIAL':<25} | {'COD_PVCASE':<20}")
print("-" * 50)
for doc in docs:
    d = doc.to_dict()
    print(f"{str(d.get('Material')):<25} | {str(d.get('Cod_PVcase')):<20}")
