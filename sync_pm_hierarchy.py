import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def sync_pm():
    print("\n🧬 AXON AI: Sincronizare viziune ierarhică pentru Managerul General...")
    
    dna_update = """
CAPACITĂȚI DE VIZUALIZARE ACTUALIZATE (HIERARCHY):
1. RECOGNIZARE CATEGORII: Acum gestionezi 5 categorii Master (Major Assets, Mechanical, DC Electrical, AC & Earthing, Consumables).
2. DRILL-DOWN LOGIC: 
   - La nivel executiv (Nivel 1), raportezi doar componentele principale (Panouri, Trackere, Invertoare, Cabluri MV).
   - La nivel de detaliu (Nivel 2), ai vizibilitate totală asupra celor 2.046.000 cleme, 770.000 coliere și restul materialului mărunt.
3. FILTRARE INTELIGENTĂ: Nu prezenta listele de detaliu decât dacă situația o cere (ex: discrepanțe la inventar sau audit de șantier).

INSTRUCȚIUNE DE AUDIT:
Verifică întotdeauna dacă materialul mărunt (Consumables) este recepționat în ritm cu echipamentele principale pentru a evita blocajele în montaj.
"""
    
    # 🛡️ SAFE SCRIPTING: Actualizăm doar PM-ul, păstrând restul intact
    db.collection("axon_protocols").document("Project_Manager").set({
        "content_update": dna_update,
        "sync_date": "2026-02-22",
        "access_level": "Full_Hierarchy"
    }, merge=True)
    
    print("✅ [SYNC COMPLET]: Managerul General are acum acces la Gestiunea de Detaliu.")

if __name__ == "__main__":
    sync_pm()
