import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

# Mapare extrasă din documentul "BOM pentru un singur modul e-devize"
pvcase_mapping = {
    "LR7-72HGD-685M": "PV Module",
    "SUN2000-330KTL-H1": "Inverter",
    "STS-7000K-H1": "Transformer",
    "IDM-LTEC-1P-75": "Tracker Unit",
    "IDM-PILE-C120": "Foundation",
    "IDM-MC-35-EPDM": "Module Clamp",
    "IDM-TT-OCT-80": "Torque Tube",
    "DC-SOL-6-RED": "DC Cable (Red)",
    "DC-SOL-6-BK": "DC Cable (Black)",
    "IDM-JB-800-MC4": "Jumper Cable"
}

def sync_codes():
    print("🔄 AXON SYNC: Injectare coduri PVcase în inventar...")
    inv_ref = db.collection("axon_inventory")
    
    docs = inv_ref.stream()
    count = 0
    
    for doc in docs:
        data = doc.to_dict()
        material = data.get("Material")
        
        if material in pvcase_mapping:
            doc.reference.update({
                "Cod_PVcase": pvcase_mapping[material]
            })
            print(f"✅ Mapat: {material} -> {pvcase_mapping[material]}")
            count += 1
            
    print(f"\n✨ Sincronizare finalizată. {count} repere au acum referință PVcase.")

if __name__ == "__main__":
    sync_codes()
