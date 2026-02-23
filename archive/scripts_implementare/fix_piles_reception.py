import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def fix_reception():
    print("⚖️ AXON: Corecție cifre recepție piloni...")
    inv_ref = db.collection("axon_inventory")
    
    # Căutăm toate înregistrările pentru piloni
    docs = inv_ref.where("Material", "in", ["IDM-PILE-C120", "IDM-PILE-C120 (Lot RETA)"]).stream()
    
    for doc in docs:
        d = doc.to_dict()
        mat_name = d.get("Material", "")
        
        if "(" not in mat_name: # Acesta este Master Record (Sursa de Adevăr)
            doc.reference.update({
                "Cantitate_Receptionata": 1085,
                "Cantitate_Validata": 145,
                "Cantitate_Instalata": 0 # EPC-ul de sus nu citește Raportat
            })
            print(f"✅ Master Piloni setat la 1.085 Recepționați.")
        else: # Acesta este Lotul de custodie al contractorului
            doc.reference.update({
                "Cantitate_Receptionata": 0, # Contractorul nu face recepție de marfă
                "Cantitate_Custodie": 455,  # 600 inițial - 145 validați
                "Cantitate_Instalata": 150, # Ce a raportat el
                "Cantitate_Validata": 145   # Ce ai validat tu
            })
            print(f"✅ Lot RETA curățat (Recepție setată pe 0 pentru a nu dubla totalul).")

if __name__ == "__main__":
    fix_reception():
