import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def split_lot():
    print("✂️ AXON LOGISTICS: Divizare lot pentru al doilea contractor...")
    
    # 1. Găsim lotul curent de piloni de la RETA (unde avem 885 rămași)
    piloni_ref = db.collection("axon_inventory").where("Material", "==", "IDM-PILE-C120").stream()
    
    for doc in piloni_ref:
        data = doc.to_dict()
        custodie_reta = data.get("Cantitate_Custodie", 0)
        
        if custodie_reta >= 300:
            # 2. Scădem 300 de la RETA
            doc.reference.update({"Cantitate_Custodie": custodie_reta - 300})
            
            # 3. Creăm o linie NOUĂ pentru ALMA_CONSTRUCT
            new_lot = data.copy()
            new_lot["Material"] = data["Material"] + " (Lot ALMA)"
            new_lot["Cantitate_Custodie"] = 300
            new_lot["Cantitate_Planificata"] = 0 # Punem 0 ca sa nu dublam necesarul proiectului la total
            new_lot["Contractor_Custodie"] = "ALMA_CONSTRUCT"
            new_lot["Status"] = "IN_CUSTODIE_ALMA"
            
            db.collection("axon_inventory").add(new_lot)
            print(f"✅ Transferat 300 piloni de la RETA către ALMA_CONSTRUCT.")
        else:
            print("Nu sunt destui piloni în custodia RETA pentru split.")

if __name__ == "__main__":
    split_lot()
