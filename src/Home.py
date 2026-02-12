import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import base64
import time



# ---------- helpers ----------
def bg_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def stream_text(text):
    for char in text:
        yield char
        time.sleep(0.005)
    
# ---------- paths ----------
BASE_DIR = os.path.dirname(__file__)
logo_pemda_path = os.path.join(BASE_DIR, "..", "asset", "logo pemda.png")
logo_dkp_path = os.path.join(BASE_DIR, "..", "asset", "DKP.png")
background_path = os.path.join(BASE_DIR, "..", "asset", "background.jpg")
data_path = os.path.join(BASE_DIR, "..", "output.csv")

# ---------- page config ----------
st.set_page_config(
    page_title='HOME',
    page_icon=logo_pemda_path,
    initial_sidebar_state="expanded",
    layout ='wide'
)



loading_placeholder = st.empty()

with loading_placeholder.container():
    with st.spinner("Memuat dashboard..."):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

loading_placeholder.empty()


paragraf = """
Web application dashboard ini disusun sebagai bentuk intervensi strategis dalam optimalisasi 
penyajian data guna meningkatkan kualitas informasi, akuntabilitas, serta efektivitas 
pemanfaatan data dalam mendukung pelaksanaan tugas dan fungsi organisasi. Pengembangan 
dashboard ini merupakan bagian dari implementasi aktualisasi CPNS yang berorientasi pada 
penguatan tata kelola berbasis data, sehingga informasi dapat disajikan secara sistematis, 
transparan, dan mudah diakses oleh pemangku kepentingan.
"""
# ---------- sidebar ----------
st.sidebar.image(logo_dkp_path, width=200)

# ---------- main content ----------
st.title("Dashboard Statistik PDSPKP")
st.divider()

st.write_stream(stream_text(paragraf))
