import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

# Maparea extinsă bazată pe BOM-ul tău
pv_map = {
    "IDM-PILE-C120": "Foundation / Pilon",
    "IDM-CLAMP-FIX": "Module Clamp / Clemă",
    "LR7-72HGD-685M": "PV Module / Panou 685W",
    "SUN2000-330KTL-H1": "Inverter / Invertor Huawei",
    "IDM-LTEC-1P-75": "Tracker Unit / Sistem Tracking",
    "IDM-TT-OCT-80": "Torque Tube / Ax Octogonal",
    "DC-SOL-6-RED": "Solar Cable Red",
    "DC-SOL-6-BK": "Solar Cable Black"
}

def sync():
    print("🔍 AXON DEEP AUDIT: Verificare și Sincronizare PVcase...")
    inv_ref = db.collection("axon_inventory")
    docs = inv_ref.stream()
    
    updated_count = 0
    found_materials = []

    for doc in docs:
        data = doc.to_dict()
        mat_name = data.get("Material", "").strip()
        found_materials.append(mat_name)
        
        # Căutăm o potrivire în maparea noastră (case-insensitive)
        matched_pv_code = None
        for key, code in pv_map.items():
            if key.lower() == mat_name.lower():
                matched_pv_code = code
                break
        
        if matched_pv_code:
            doc.reference.update({"Cod_PVcase": matched_pv_code})
            print(f"✅ UPDATED: {mat_name} -> {matched_pv_code}")
            updated_count += 1
        else:
            # Dacă nu are cod, îi punem un placeholder ca să apară coloana
            doc.reference.update({"Cod_PVcase": "N/A (Pending Design)"})
            updated_count += 1

    print(f"\n📊 Rezultat: {updated_count} repere au acum câmpul Cod_PVcase.")
    if not updated_count:
        print("❌ ATENȚIE: Nu am găsit niciun material în axon_inventory!")
        print(f"Materiale găsite în DB: {found_materials}")

if __name__ == "__main__":
    sync()
