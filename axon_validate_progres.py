import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validare_pv_finala(lot_id, cantitate_ok):
    """
    REGULA GENERALĂ: 
    Validarea scade automat din stocul contractorului (Custodie).
    """
    print(f"⚖️ AXON LOGIC: Se validează {cantitate_ok} unități pentru {lot_id}...")
    doc_ref = db.collection("axon_inventory").document(lot_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        custodie_actuala = data.get("Cantitate_Custodie", 0)
        validat_anterior = data.get("Cantitate_Validata", 0)
        
        if cantitate_ok <= custodie_actuala:
            # EXECUTĂM MUTAREA FIZICĂ A STOCULUI
            doc_ref.update({
                # Materialul a fost montat, deci NU mai este în custodie (stoc de lucru)
                "Cantitate_Custodie": custodie_actuala - cantitate_ok,
                # Materialul devine progres oficial
                "Cantitate_Validata": validat_anterior + cantitate_ok,
                "Status": "MONTAJ_VALIDAT_PV"
            })
            print(f"✅ REZULTAT: {cantitate_ok} unități au ieșit din Custodie și au intrat în Realizat.")
        else:
            print(f"❌ EROARE: Nu poți valida {cantitate_ok} unități. Contractorul are doar {custodie_actuala} în custodie!")
    else:
        print("❌ EROARE: Lotul specificat nu există.")

if __name__ == "__main__":
    # Exemplu: Validăm 100 de piloni pentru lotul RETA
    # Această comandă va face Custodia 400 și Validatul 100
    validare_pv_finala("LOT_PILE_RETA", 100)
