import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def transfer_to_custody():
    print("🚚 AXON LOGISTICS: Executare transfer piloni în custodie...")
    
    inv_ref = db.collection("axon_inventory")
    # Căutăm pilonii C120
    docs = inv_ref.where("Material", "==", "IDM-PILE-C120").stream()
    
    for doc in docs:
        data = doc.to_dict()
        cantitate_totala = data.get("Cantitate_Receptionata", 0)
        
        # Transferăm tot lotul în custodie
        doc.reference.update({
            "Cantitate_Custodie": cantitate_totala,
            "Cantitate_Receptionata": 0, # Scade din stocul central "liber"
            "Contractor_Custodie": "RETA_STRUCT_TEAM_01",
            "Status": "IN_CUSTODIE_MONTAJ"
        })
        print(f"✅ Succes: {cantitate_totala} piloni predați către RETA_STRUCT_TEAM_01.")

if __name__ == "__main__":
    transfer_to_custody()
