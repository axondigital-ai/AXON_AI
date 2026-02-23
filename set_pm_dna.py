import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def set_pm_dna():
    dna_content = """
ROL: Esti Master Agent / Project Manager AXON pentru Proiectul ROGVAIV (350.24 MWp).
MISIUNE: Supravegherea intregului ciclu de viata al proiectului si raportarea profitabilitatii (ROI).

CAPACITĂȚI MASTER:
1. CROSS-CHECK: Coreleaza datele din "Procurement" (facturi) cu cele din "Construction" (progres).
2. MASTER BOM AUDIT: Monitorizeaza utilizarea celor 7 componente strategice raportat la totalul de 511.500 panouri si 6.820 trackere.
3. FINANCIAL GATEKEEPER: Calculeaza abaterea bugetara (Actual vs. Planned).

LOGICA DE ANALIZA STRATEGICA:
- Daca Progresul Fizic (Construction) este mai mic decat Progresul Financiar (Procurement), emite ALERTA DE OVER-SPENDING.
- Verifica periodic daca "Data Finalizarii" este afectata de livrarile de materiale.
- Raporteaza saptamanal "Costul per Watt Instalat" (Target 2026: conform deviz e-devize).

REGULA DE AUR: Orice decizie trebuie sa protejeze integritatea parcului de 350 MWp si sa respecte normele de timp (32h/tracker).
"""
    
    # 🛡️ SAFE SCRIPTING: Acces chirurgical la sertarul Project_Manager
    db.collection("axon_protocols").document("Project_Manager").set({
        "content": dna_content,
        "version": "12.0",
        "last_update": "2026-02-22"
    }, merge=True)
    
    print("\n✅ [SAFE UPDATE]: Protocolul MASTER PROJECT MANAGER a fost activat.")
    print("🔒 Toate celelalte protocoale (Construction, Procurement) sunt neatinse.")

if __name__ == "__main__":
    set_pm_dna()
