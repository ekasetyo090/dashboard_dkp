# ============================================================
# IMPORT LIBRARY
# ============================================================

import base64
import asyncio
import nest_asyncio

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from LIB.charts import (
    plot_upi_per_kecamatan,plot_upi_per_olahan,plot_upi_jenis_proses_jenis_ikan_catplot,
    plot_persentase_upi_memiliki_kontak,handle_multiselect_all
    )


nest_asyncio.apply()


# ============================================================
# PATH CONFIGURATION
# ============================================================
BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

ASSET_DIR = os.path.join(ROOT_DIR, "asset")

LOGO_PEMDA = os.path.join(ASSET_DIR, "logo pemda.png")
LOGO_DKP = os.path.join(ASSET_DIR, "DKP.png")
BACKGROUND = os.path.join(ASSET_DIR, "background.jpg")
DATA_PATH = os.path.join(ROOT_DIR, "output.csv")


# ============================================================
# PAGE CONFIG
# ============================================================
#st.set_page_config(
#    page_title="Dashboard Statistik PDSPKP",
#    page_icon=LOGO_PEMDA,
#    layout="wide",
#    initial_sidebar_state="expanded"
#)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def encode_image(path):
    """Convert image to base64."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


async def loading_animation():
    placeholder = st.empty()

    with placeholder.container():
        with st.spinner("Memuat data..."):
            progress = st.progress(0)
            for i in range(100):
                await asyncio.sleep(0.01)
                progress.progress(i + 1)

    placeholder.empty()


# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv(DATA_PATH)

cols = ["jenis_ikan", "jenis_proses", "KECAMATAN", "DESA"]

df[cols] = df[cols].apply(lambda x: x.str.lower())

# ============================================================
# RUN LOADING
# ============================================================
# asyncio.run(loading_animation())


# ============================================================
# SIDEBAR
# ============================================================



# ============================================================
# MAIN TITLE
# ============================================================
st.title("Dashboard Statistik PDSPKP", anchor=False)
st.divider()


# ============================================================
# METRICS
# ============================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah UPI", len(df))
col2.metric("Jenis Olahan", df["jenis_proses"].nunique())
col3.metric("Kecamatan", df["KECAMATAN"].nunique())
col4.metric("Desa", df["DESA"].nunique())
st.divider()

# ============================================================
# BAR CHART - JUMLAH UPI PER KECAMATAN
# ============================================================
fig1 = plot_upi_per_kecamatan(df)
fig2 = plot_upi_per_olahan(df)


# ============================================================
# SIDE BAR
# ============================================================
# st.sidebar.header("Filter Data")



# =========================
# JENIS PROSES
# =========================
list_proses = sorted(df["jenis_proses"].dropna().unique())
opsi_proses = ["Semua Jenis Proses"] + list_proses

pilih_proses = st.sidebar.multiselect(
    "Pilih Jenis Proses",
    options=opsi_proses,
    default=["Semua Jenis Proses"]
)

if "Semua Jenis Proses" in pilih_proses:
    final_proses = list_proses
else:
    final_proses = pilih_proses

# =========================
# JENIS IKAN
# =========================
list_ikan = sorted(df["jenis_ikan"].dropna().unique())
opsi_ikan = ["Semua Jenis Ikan"] + list_ikan

pilih_ikan = st.sidebar.multiselect(
    "Pilih Jenis Ikan",
    options=opsi_ikan,
    default=["Semua Jenis Ikan"]
)

if "Semua Jenis Ikan" in pilih_ikan:
    final_ikan = list_ikan
else:
    final_ikan = pilih_ikan

   
st.sidebar.image(LOGO_DKP, width=200)
# ============================================================
# BODY DISPLAY CHART
# ============================================================
# with st.container():
#     col1, col2 = st.columns([1, 1])   # rasio seimbang
#     with col1:
#         st.subheader(
#             "Jumlah Unit Pengolahan Ikan (UPI) per Kecamatan"
#         )
#     with col2:
#         st.subheader(
#             "Proporsi Unit Pengolahan Ikan (UPI) Berdasarkan Jenis Olahan"
#         )
#st.divider()

with st.container():
    col1, col2 = st.columns([1, 1])   # rasio seimbang
    with col1:
        st.pyplot(fig1, use_container_width=True)
    with col2:
        st.pyplot(fig2, use_container_width=True)
        
# ============================================================
# BODY SEC 2
# ============================================================
st.divider()
with st.container():
    col1,col2 = st.columns([1,1])
    with col1:
        # =========================
        # KECAMATAN
        # =========================
        list_kecamatan = sorted(df["KECAMATAN"].dropna().unique())
        opsi_kecamatan = ["Semua Kecamatan"] + list_kecamatan

        pilih_kecamatan = st.multiselect(
            "Pilih Kecamatan",
            options=opsi_kecamatan,
            default=["Semua Kecamatan"]
        )
        final_kecamatan = handle_multiselect_all(
            selected=pilih_kecamatan,
            default_label="Semua Kecamatan",
            full_list=list_kecamatan
        )
    df_filtered_1 = df[(df["KECAMATAN"].isin(final_kecamatan))]
    with col2:
        # =========================
        # DESA
        # =========================
        list_desa = sorted(df_filtered_1["DESA"].dropna().unique())
        opsi_desa = ["Semua Desa"] + list_desa

        pilih_desa = st.multiselect(
            "Pilih Desa",
            options=opsi_desa,
            default=["Semua Desa"]
        )
        final_desa = handle_multiselect_all(
            selected=pilih_desa,
            default_label="Semua Desa",
            full_list=list_desa
        )
    df_filtered_1 = df_filtered_1[(df_filtered_1["DESA"].isin(final_desa))]
    #df_olahan

# ============================================================
# BODY SEC 3
# ============================================================
with st.container():
    col1,col2 = st.columns([1,1])
    with col1:
        options_kontak = ["Memiliki Kontak", "Tidak Punya Kontak", "Keduanya"]
        selection = st.segmented_control(
            "Filter Kontak", options_kontak, selection_mode="single"
        )
# st.text(opsi_desa)
# ============================================================
# DATA TABLE
# ============================================================
# df_filtered_1 = df[
#     (df["KECAMATAN"].isin(final_kecamatan)) &
#     (df["DESA"].isin(final_desa)) &
#     (df["jenis_proses"].isin(final_proses)) &
#     (df["jenis_ikan"].isin(final_ikan))
# ]
# st.divider()
fig3 = plot_upi_jenis_proses_jenis_ikan_catplot(df_filtered_1)
fig4 = plot_persentase_upi_memiliki_kontak(df_filtered_1)
with st.container():
    col1,col2 = st.columns([1,1])
    with col1:
        st.pyplot(fig3, use_container_width=True)
    with col2:
        st.pyplot(fig4, use_container_width=True)

st.divider()
with st.container():
    col1,col2 = st.columns([1,1])
    
st.dataframe(df)
st.divider()
st.dataframe(df_filtered_1)
df_filtered_2 = (df_filtered_1.groupby("NO TELP ENKRIP").size())#.reset_index(name="jumlah_upi"))
st.dataframe(df_filtered_2)
