import google.cloud.firestore as firestore
import os
import sys

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validate_work(material_id, qty_to_validate):
    """
    Regula Generală: Validează o cantitate specifică din ce a raportat constructorul.
    """
    print(f"🔍 AXON QC: Inițiere proces verbal de recepție pentru {material_id}...")
    
    # Căutăm lotul specific (ID-ul documentului din tabelul de jos)
    doc_ref = db.collection("axon_inventory").document(material_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        raportat = data.get("Cantitate_Instalata", 0)
        
        if qty_to_validate <= raportat:
            doc_ref.update({
                "Cantitate_Validata": qty_to_validate,
                "Status": "VALIDAT_CONFORM_PV" if qty_to_validate == raportat else "VALIDAT_PARTIAL"
            })
            print(f"✅ VALIDARE REUȘITĂ: {qty_to_validate} unități confirmate oficial.")
            if qty_to_validate < raportat:
                print(f"⚠️ ATENȚIE: Există o diferență de {raportat - qty_to_validate} unități nevalidate (necesită remedieri).")
        else:
            print(f"❌ EROARE: Nu poți valida {qty_to_validate} când constructorul a raportat doar {raportat}!")
    else:
        print(f"❌ EROARE: Lotul {material_id} nu a fost găsit în sistem.")

# Exemplu de utilizare (poate fi apelat cu argumente din terminal)
if __name__ == "__main__":
    # Parametri: ID_LOT, CANTITATE_DE_VALIDAT
    # Pentru testul nostru: 
    validate_work("LOT_PILE_RETA_START", 150)
