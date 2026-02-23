# 🚀 AXON CORE OS - v59.0 (Stability Edition)
### Sistem de Gestiune și Control Operațional EPC - Parcuri Fotovoltaice

AXON CORE este un sistem digital de tip "Single Source of Truth" conceput pentru monitorizarea fluxului de materiale și a progresului execuției pe șantierele fotovoltaice de mare anvergură.

---

## 🏗️ 1. Arhitectura Tehnică
- **Frontend:** Streamlit (Python) - Interfață dinamică de raportare.
- **Backend/Database:** Google Firestore (NoSQL) - Stocare în cloud cu latență zero.
- **Infrastructură:** Docker & Docker-Compose - Containerizare pentru portabilitate totală.
- **Versionare:** GitHub - Controlul versiunilor și backup de cod.

---

## 🧠 2. Logica de Gestiune și Reguli de Aur

Sistemul funcționează pe baza **Regulei Generale de Conservare a Cantității**, eliminând erorile umane de raportare.

### A. Ecuația de Balanță (Fluxul de Stoc)
Pentru orice material, suma stării acestuia trebuie să fie egală cu totalul recepționat:
> **Total Recepționat = În Depozit + În Custodie + Realizat (PV)**

### B. Regula de Aur a Validării (PV)
La semnarea unui Proces Verbal (PV) de montaj:
1. Cantitatea validată se **scade automat** din *Custodia Contractorului*.
2. Cantitatea validată se **adaugă automat** la coloana *Realizat (PV)*.
3. Astfel, răspunderea materială a contractorului scade pe măsură ce progresul proiectului crește.

---

## 📊 3. Formule de Calcul în Timp Real

Sistemul extrage date brute din Firestore și aplică următoarele calcule dinamice în interfață:

| Câmp Calculat | Formulă de Calcul | Explicație |
| :--- | :--- | :--- |
| **În Depozit** | `Total_Receptionat - (Cantitate_Custodie + Cantitate_Validata)` | Ce se află fizic sub cheia Beneficiarului. |
| **Progres Real (%)** | `(Suma_Validata_Loturi / Cantitate_Planificata_Master) * 100` | Procentul de execuție certificat prin PV. |
| **Agregare EPC** | `Group By: Material_Baza` | Combină Master Record-ul cu toate loturile contractorilor (ex: elimină " (ELMA)" din nume). |

---

## 📂 4. Organizarea Nomenclatorului
Datele sunt structurate în 6 categorii logice de execuție:
1. **MAJOR ASSETS:** Panouri, Invertoare, Trackere.
2. **MECHANICAL:** Piloni, Structură metalică.
3. **DC ELECTRICAL:** Cabluri DC, String Boxes, Conectori.
4. **AC ELECTRICAL:** Cabluri AC, Posturi Trafo, Celule Medie Tensiune.
5. **EARTHING:** Platbandă, Electrozii de împământare.
6. **CONSUMABLES:** Materiale mărunte de șantier.

---

## 🛠️ 5. Instrucțiuni de Lucru (Workflow Standard)

1. **Recepția (MRR):** Se actualizează `Cantitate_Receptionata` în Master Record-ul materialului. Status: `STOC_CENTRAL`.
2. **Predarea (Handover):** Se creează un lot nou cu sufixul contractorului (ex: `+ (ELMA)`). Cantitatea se adaugă în `Cantitate_Custodie`.
3. **Validarea (PV):** Se rulează scriptul de validare care mută cantitatea din `Custodie` în `Validat`.
4. **Raportarea:** Se accesează Tab-ul "Gestiune" pentru vizualizarea Progresului Real.

---

## 🛡️ 6. Note de Siguranță
- **Zero Date Injectate:** Interfața nu permite modificarea manuală a procentelor; acestea rezultă exclusiv din calculul bazei de date.
- **Integritate:** Orice discrepanță în ecuația de balanță indică pierderi de material în teren.

---
**Documentație generată de AXON AI la v59.0.**
