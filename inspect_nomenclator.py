import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

print("\n--- 🔎 LISTA COMPLETĂ MATERIALE ÎN BAZA DE DATE ---")
docs = db.collection("axon_inventory").stream()
for doc in docs:
    d = doc.to_dict()
    print(f"ID: {doc.id.ljust(25)} | Mat: {str(d.get('Material')).ljust(25)} | Cat: {d.get('Categorie')}")
print("---------------------------------------------------\n")
