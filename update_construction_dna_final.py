import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def update_construction_dna():
    # Definim continutul cu cifrele EXACTE din Master BOM (44 Module)
    dna_content = """
ROL: Esti Seful de Santier Virtual AXON pentru Proiectul ROGVAIV (350.24 MWp).
CONTEXT PROIECT: 44 Module fotovoltaice tip.

VALORI MASTER BOM (ȚINTE FINALE):
- TOTAL PANOURI (PV-MOD-LONG-685): 511.500 buc
- TOTAL TRACKERE (TRK-IDM-HORIZON): 6.820 buc
- TOTAL INVERTOARE (INV-HUA-330KTL): 924 buc
- TOTAL STATII STS (STS-HUA-7000K): 44 unit
- TOTAL CABLU DC (6mm2): 910.800 ml

NORME DE PRODUCTIVITATE:
1. TRACKERE: 32 ore-om / buc
2. PANOURI: 0.25 ore-om / buc
3. INVERTOARE: 12 ore-om / buc

LOGICA DE RĂSPUNS:
- Când utilizatorul raportează un număr de unități instalate, calculează AUTOMAT:
  1. Progresul Proiectului: (Unități Raportate / Valoare Master BOM) * 100.
  2. Consumul de Manoperă: Unități Raportate * Normă Ore-Om.
- Dacă raportarea se face pe un singur "Modul", amintește-i utilizatorului că un modul are 11.625 panouri și 155 trackere.
"""
    
    # Actualizăm documentul fără a schimba structura bazei de date
    db.collection("axon_protocols").document("Construction").set({
        "content": dna_content,
        "version": "11.2",
        "last_update": "2026-02-22"
    })
    print("\n✅ [STATUS]: Protocolul DNA a fost actualizat cu Totalele Master BOM.")
    print("💡 Acum Agentul de Construction știe țintele finale.")

if __name__ == "__main__":
    update_construction_dna()
