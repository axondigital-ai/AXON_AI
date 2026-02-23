import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def run_diagnostic():
    print("\n🕵️ AXON AI: Diagnostic de Sistem - Căutăm 'Problema'...")
    print("-" * 50)
    
    # 1. Verificăm ce documente de protocol există (Numele corecte)
    print("1. Verificare Protocoale DNA existente:")
    protocols = db.collection("axon_protocols").stream()
    found_pm = False
    for p in protocols:
        print(f"   [Found]: {p.id}")
        if "Project_Manager" in p.id: found_pm = True
    
    if not found_pm:
        print("   ⚠️ ALERTA: Documentul 'Project_Manager' nu pare a fi cel citit de UI!")

    # 2. Verificăm dacă există un document de 'Configurație Globală'
    print("\n2. Verificare Configurație de Sistem:")
    config = db.collection("axon_config").document("settings").get()
    if config.exists:
        print(f"   [Config]: {config.to_dict()}")
    else:
        print("   [Info]: Nu există o configurație globală (UI-ul e probabil hardcoded).")

    # 3. Verificăm ultimele 5 intrări din inventar
    print("\n3. Verificare Vizibilitate Inventar (Top 5):")
    inv = db.collection("axon_inventory").limit(5).stream()
    for i in inv:
        d = i.to_dict()
        print(f"   📦 {i.id} -> Categorie: {d.get('Categorie')}, Cantitate: {d.get('Cantitate')}")

if __name__ == "__main__":
    run_diagnostic()
