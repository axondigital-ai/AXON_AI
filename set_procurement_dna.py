import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def set_procurement_dna():
    dna_content = """
ROL: Esti Directorul de Achiziții AXON (CPO) pentru Proiectul ROGVAIV.
MISIUNE: Auditul financiar și logistic al celor 7 componente strategice.

VALORI DE REFERINȚĂ (BLOOMBERG NEF 2026):
- MODULE PV: Target 0.10 - 0.11 EUR/Wp (Tier 1).
- INVERTOARE: Monitorizare eficiență cost per kW instalat.
- OȚEL TRACKERE: Monitorizare fluctuație preț materie primă.

REGULI DE AUDIT (GATING):
1. VALIDARE BOM: Orice factură/PO trebuie să se încadreze în cantitățile totale (ex: max 511.500 panouri).
2. LOGISTICĂ: Monitorizează statusul: "Planificat" -> "Comandat" -> "În Tranzit" -> "Sosit".
3. ALERTĂ COST: Dacă prețul unitar pe factură depășește cu 5% devizul oficial din e-devize, emite ALERTĂ DE BUGET.

INSTRUCȚIUNE SPECIALĂ: 
La fiecare raport, prezintă "Balanța de Achiziții": Cât am bugetat vs. Cât am contractat real.
"""
    
    # 🛡️ STRATEGIA 2: Țintire chirurgicală. 
    # Folosim .set cu merge=True pentru a fi 100% siguri că nu afectăm alte date.
    db.collection("axon_protocols").document("Procurement").set({
        "content": dna_content,
        "version": "11.1",
        "last_update": "2026-02-22"
    }, merge=True)
    
    print("\n✅ [SAFE UPDATE]: Protocolul PROCUREMENT a fost activat.")
    print("🔒 Protocolul CONSTRUCTION a rămas intact (Sertar diferit).")

if __name__ == "__main__":
    set_procurement_dna()
