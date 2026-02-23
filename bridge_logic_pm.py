import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def bridge_logic():
    print("\n🌉 AXON CORE: Construirea podului logic între Categorii și Repere...")
    
    pm_ref = db.collection("axon_protocols").document("Project_Manager")
    
    # Adăugăm blocul de "Inginerie de Calcul" în DNA-ul său (câmpul content pentru v10.8)
    logic_update = (
        "ALOCARE_TEHNICA_EXPLICITA:\n"
        "- Categoria [Mechanical] include obligatoriu: Trackers, Piloni și Cleme.\n"
        "- MATEMATICA_TRACKER: 2.046.000 Cleme / 6.820 Trackers = EXACT 300 cleme per tracker.\n"
        "- MATEMATICA_PILON: 47.740 Piloni / 6.820 Trackers = EXACT 7 piloni per tracker.\n"
        "- REGULA_AUDIT: Orice raport Mechanical trebuie să valideze acest raport de 300:1 pentru cleme.\n"
        "Sursa datelor: Documentația tehnică de montaj v1.0."
    )

    # Actualizăm câmpul 'content' pe care îl citește interfața v10.8
    current_dna = pm_ref.get().to_dict()
    new_content = current_dna.get("content", "") + "\n\n" + logic_update
    
    pm_ref.update({"content": new_content})
    print("✅ [SUCCESS]: Logica de calcul (300 cleme/tracker) a fost injectată.")

if __name__ == "__main__":
    bridge_logic()
