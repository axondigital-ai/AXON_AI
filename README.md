# AXON CORE v59.0 🚀
### Sistem de Gestiune EPC - Parcuri Fotovoltaice

Sistem de monitorizare a stocului și progresului în timp real, bazat pe **Regula Generală de Conservare a Cantității**.

## 📊 Reguli de Aur
1. **Total Intrat** = Depozit + Custodie + Realizat (PV).
2. **Validarea (PV)** scade automat din Custodia contractorului și adaugă la Progresul Real.
3. **Progres Real (%)** = (Suma Validată / Suma Planificată) * 100.

## 📁 Organizare Categorii
- MAJOR ASSETS (Invertoare, Panouri, Trackere)
- MECHANICAL (Piloni, Structură)
- DC ELECTRICAL (Cabluri DC, String Boxes)
- AC ELECTRICAL (Cabluri AC, Posturi Trafo)
- EARTHING
- CONSUMABLES

## 🛠 Tehnologii
- **Backend:** Google Firestore (NoSQL)
- **Frontend:** Streamlit
- **Containerizare:** Docker
