import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validare_pv_generala(lot_id, cantitate_de_validat):
    """
    REGULA GENERALĂ: 
    Validarea scade automat din Custodie și adună la Validat.
    """
    print(f"⚖️ AXON LOGIC: Validare PV pentru {lot_id}...")
    doc_ref = db.collection("axon_inventory").document(lot_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        custodie_actuala = data.get("Cantitate_Custodie", 0)
        validat_anterior = data.get("Cantitate_Validata", 0)
        raportat_constructor = data.get("Cantitate_Instalata", 0)
        
        if cantitate_de_validat <= (custodie_actuala + raportat_constructor):
            # EXECUTĂM TRANSFERUL DE STOC
            doc_ref.update({
                # Scădem din custodie (materialul a fost "consumat" prin montaj)
                "Cantitate_Custodie": custodie_actuala if cantitate_de_validat > custodie_actuala else custodie_actuala - cantitate_de_validat,
                # Adunăm la validat (progres oficial)
                "Cantitate_Validata": firestore.Increment(cantitate_de_validat),
                # Resetăm/Scădem din raportarea constructorului pentru a curăța vizualul
                "Cantitate_Instalata": 0 if cantitate_de_validat >= raportat_constructor else raportat_constructor - cantitate_de_validat,
                "Status": "VALIDAT_CONFORM_PV"
            })
            print(f"✅ REGULĂ APLICATĂ: {cantitate_de_validat} unități mutate din Custodie în Realizat.")
        else:
            print("❌ EROARE: Cantitatea de validat depășește stocul în custodie!")
    else:
        print("❌ EROARE: Documentul nu a fost găsit.")

if __name__ == "__main__":
    # Testăm pe lotul existent de piloni
    validare_pv_generala("LOT_PILE_RETA_START", 5)
