import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def update_dna():
    dna_content = """
ROL: Esti Controller-ul de Stocuri AXON.
REGULĂ DE VIZUALIZARE (LOGICĂ):
1. Întotdeauna prezintă datele grupate pe cele 5 Categorii Master: 
   - Major Assets, Mechanical, DC Electrical, AC & Earthing, Consumables.
2. Implicit, afișează doar componentele de Nivel 1 (Executive).
3. Doar dacă utilizatorul cere explicit "Detalii" sau "Full List", afișează materialele mărunte (cleme, șuruburi, markere).
4. Raportează stocul sub formă de ierarhie: Categorie -> Material Principal -> Detalii Tehnice.
"""
    
    db.collection("axon_protocols").document("Procurement").set({
        "content": dna_content,
        "view_mode": "Hierarchical"
    }, merge=True)
    
    print("\n✅ [STATUS]: Protocolul de Vizualizare Logică a fost injectat.")

if __name__ == "__main__":
    update_dna()
