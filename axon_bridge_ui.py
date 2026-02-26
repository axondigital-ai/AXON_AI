import streamlit as st
import psycopg2

st.set_page_config(page_title="AXON CORE", layout="wide")
st.title("🚀 AXON CORE | Progres Șantier")

def get_data():
    conn = psycopg2.connect("postgresql://admin:axon_pass@localhost:5432/axon_db")
    cur = conn.cursor()
    cur.execute("SELECT proiect, status, panouri_instalate, valoare_ron FROM progres_santier")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

try:
    data = get_data()
    
    # Header Tabel
    st.write("---")
    h1, h2, h3, h4 = st.columns([1, 2, 1, 2])
    h1.subheader("Proiect")
    h2.subheader("Status")
    h3.subheader("Panouri")
    h4.subheader("Valoare (RON)")
    st.write("---")

    # Rânduri Date
    for r in data:
        c1, c2, c3, c4 = st.columns([1, 2, 1, 2])
        c1.write(f"**{r[0]}**")
        
        # Culoare în funcție de status
        if r[1] == 'COMPLETED':
            c2.success(f"✅ {r[1]}")
        else:
            c2.warning(f"🏗️ {r[1]}")
            
        c3.write(str(r[2]))
        c4.write(f"{r[3]:,.2f}")

except Exception as e:
    st.error(f"Eroare: {e}")

st.sidebar.info("AXON v1.0 | Status: Connected")
