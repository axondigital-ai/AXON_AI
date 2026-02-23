import google.cloud.firestore as firestore
import os

# Configurare Proiect
os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def execute_handover():
    print("🚚 AXON LOGISTICS: Inițiere transfer custodie pentru Modulul 01...")
    
    # Căutăm materialul specific
    inventory_ref = db.collection("axon_inventory")
    query = inventory_ref.where("Material", "==", "IDM-CLAMP-FIX").stream()
    
    found = False
    for doc in query:
        # Definim cantitatea de transferat (1/44 din total sau cât ai stabilit)
        cantitate_transfer = 46500
        
        # Actualizăm documentul
        doc.reference.update({
            "Cantitate_Custodie": cantitate_transfer,
            "Contractor_Custodie": "CONTRACTOR_MODUL_01_RETA",
            "Status": "IN_CUSTODIE_MONTAJ",
            "Punct_Descarcare": "COORD_GPS_MODUL_01"
        })
        print(f"✅ TRANSFER REUȘIT: {cantitate_transfer} bucăți predate către CONTRACTOR_MODUL_01_RETA.")
        found = True

    if not found:
        print("❌ EROARE: Nu am găsit materialul IDM-CLAMP-FIX în baza de date.")

if __name__ == "__main__":
    execute_handover()
