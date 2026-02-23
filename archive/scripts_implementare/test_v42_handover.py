import google.cloud.firestore as firestore
db = firestore.Client()
db.collection("axon_inventory").document("LOT_PILE_RETA").set({
    "Material": "IDM-PILE-C120 (RETA)",
    "Categorie": "Mechanical",
    "Cantitate_Custodie": 500,
    "Cantitate_Validata": 0,
    "Contractor_Custodie": "RETA_CONSTRUCT",
    "Status": "ÎN_CUSTODIE"
})
print("✅ Handover finalizat. Tabelul 'SITUAȚIE CONTRACTORI' este acum vizibil.")
