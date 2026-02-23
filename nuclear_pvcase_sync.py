import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def sync():
    print("🚀 AXON: Pornire Sincronizare Nucleară...")
    docs = db.collection("axon_inventory").stream()
    
    for doc in docs:
        d = doc.to_dict()
        mat = str(d.get("Material", "")).upper()
        
        pv_code = "N/A"
        if "PILE" in mat or "C120" in mat: pv_code = "Foundation"
        elif "CLAMP" in mat: pv_code = "Module Clamp"
        elif "685M" in mat: pv_code = "PV Module"
        elif "330KTL" in mat: pv_code = "Inverter"
        elif "LTEC" in mat: pv_code = "Tracker Unit"
        elif "TT-" in mat or "TUBE" in mat: pv_code = "Torque Tube"
        elif "RED" in mat: pv_code = "DC Cable Red"
        elif "BK" in mat or "BLACK" in mat: pv_code = "DC Cable Black"
        
        doc.reference.update({"Cod_PVcase": pv_code})
        print(f"✅ Mapat: {mat} -> {pv_code}")

if __name__ == "__main__":
    sync()
