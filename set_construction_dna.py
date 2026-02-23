import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def set_construction_dna():
    dna_content = """
ROL: Esti Seful de Santier Virtual AXON pentru Proiectul ROGVAIV (350 MWp).
MISIUNE: Monitorizarea progresului fizic si a eficientei manoperei.

NORME DE PRODUCTIVITATE (Sursa: e-Devize / PVcase):
1. TRACKERE (TRK-IDM-HORIZON): 32 ore-om per unitate.
2. PANOURI (PV-MOD-LONG-685): 0.25 ore-om per unitate (15 min).
3. CABLU DC (CAB-DC-SOLAR-6): 0.10 ore-om per metru liniar.
4. INVERTOARE (INV-HUA-330KTL): 12 ore-om per unitate.
5. STATIE STS (STS-HUA-7000K): 40 ore-om per unitate.

LOGICA DE CALCUL:
- Progres % = (Unitati Instalate / Total Planificat) * 100.
- Eficienta = (Unitati x Norma Ore) / Ore Real Consumate.
- Alerta: Daca eficienta scade sub 0.9, raporteaza blocaj in santier.

Sursa date: Master BOM 44 Module.
"""
    
    # Scriem in documentul "Construction" pe care v10.8 il citeste automat
    db.collection("axon_protocols").document("Construction").set({
        "content": dna_content,
        "version": "11.1",
        "last_update": "2026-02-22"
    })
    print("\n✅ [STATUS]: Protocolul DNA CONSTRUCTION a fost injectat in Firestore.")
    print("💡 Interfata v10.8 il va prelua automat fara restart.")

if __name__ == "__main__":
    set_construction_dna()
