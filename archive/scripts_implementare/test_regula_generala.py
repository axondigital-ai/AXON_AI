import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def aplică_regula_generală(lot_id, qty_pv):
    print(f"⚖️ AXON: Se aplică Regula Generală pentru {qty_pv} unități...")
    doc_ref = db.collection("axon_inventory").document(lot_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        custodie_actuala = data.get("Cantitate_Custodie", 0)
        validat_actual = data.get("Cantitate_Validata", 0)
        
        # REGULA: Scădem din custodie, adunăm la validat
        if qty_pv <= custodie_actuala:
            doc_ref.update({
                "Cantitate_Custodie": custodie_actuala - qty_pv,
                "Cantitate_Validata": validat_actual + qty_pv,
                "Status": "PROGRES_VALIDAT"
            })
            print(f"✅ Succes! {qty_pv} unități au fost scăzute din stocul contractorului și trecute la realizat.")
        else:
            print("❌ Eroare: Nu poți valida mai mult decât are contractorul în mână!")

if __name__ == "__main__":
    # Validăm 150 de piloni din cei 500 existenți
    aplică_regula_generală("LOT_PILE_RETA", 150)
