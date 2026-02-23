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
    handle_multiselect_all,helper_segmented_filter,
    donut_plot_kategori,donut_plot_binary,value_count_top5_with_others,
    donut_plot_kategori_agregat,parse_produksi,add_dynamic_noise,plot_tren_produksi_total,
    handle_segmented_filter,plot_line_chart
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
df["PENERIMAAN BANTUAN"] = (
    df["PENERIMAAN BANTUAN"]
    .fillna("Belum")
    .replace("", "Belum")
)

cols = ["jenis_ikan", "jenis_proses", "KECAMATAN", "DESA",'PENERIMAAN BANTUAN','NAMA UPI']

# df[cols] = df[cols].apply(lambda x: x.str.lower())
for col in cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()      # hapus spasi depan/belakang
        .str.lower()      # semua jadi huruf kecil
    )



df_clean = df.copy()
df_clean = df_clean.drop(columns=['NO'])
kolom_identitas = ['NAMA UPI', 'DESA', 'KECAMATAN', 'PENERIMAAN BANTUAN', 'JENIS KEGIATAN PENGOLAHAN','NO TELP ENKRIP', 'NAMA PEMILIK ENKRIP', 'clean', 'jenis_proses', 'jenis_ikan']

# 3. Lakukan Melt
df_clean = df_clean.melt(
    id_vars=kolom_identitas, 
    var_name='Tanggal', 
    value_name='Jumlah Produksi'
)
df_clean['Tanggal'] = pd.to_datetime(df_clean['Tanggal'], errors='coerce')
df_clean = df_clean.set_index('Tanggal')
df_clean['Jumlah Produksi Final'] = (
    df_clean['Jumlah Produksi']
    .apply(parse_produksi)
    .interpolate(method='time')
    .interpolate(method='linear')
    .ffill()
    .bfill()
)

# df_clean['Jumlah Produksi Final'] = add_random_noise(
#     df_clean['Jumlah Produksi Final'],
#     noise_level=0.08   # 8% variasi
# ).round(1)

df_clean['Jumlah Produksi Final'] = add_dynamic_noise(
    df_clean['Jumlah Produksi Final'],
    noise_level=0.18,
    wave_strength=0.07
).round(1)


# df_clean_filtered = df_clean.copy()
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
# SIDE BAR
# ============================================================
# st.sidebar.header("Filter Data")
with st.sidebar:
    st.header("Filter Data")
# =========================
# JENIS PROSES
# =========================
    list_proses = sorted(df["jenis_proses"].dropna().unique())
    opsi_proses = ["Semua Jenis Proses"] + list_proses
    
    pilih_proses = st.multiselect(
        "Pilih Jenis Proses",
        options=opsi_proses,
        default=["Semua Jenis Proses"]
    )
    
    # if "Semua Jenis Proses" in pilih_proses:
    #     final_proses = list_proses
    # else:
    #     final_proses = pilih_proses
    
    final_jenis_proses = handle_multiselect_all(
        selected=pilih_proses,
        default_label="Semua Jenis Proses",
        full_list=list_proses
    )
    df_clean_filtered = df_clean[(df_clean["jenis_proses"].isin(final_jenis_proses))].copy()
    # df_clean_filtered = df_clean_filtered.loc[df_clean_filtered['jenis_proses'].isin(final_jenis_proses)]
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
    final_jenis_ikan = handle_multiselect_all(
        selected=pilih_ikan,
        default_label="Semua Jenis Ikan",
        full_list=list_ikan
    )
    df_clean_filtered = df_clean_filtered.loc[df_clean_filtered['jenis_ikan'].isin(final_jenis_ikan)]
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
    df_clean_filtered = df_clean_filtered.loc[df_clean_filtered['KECAMATAN'].isin(final_kecamatan)]

# =========================
# DESA
# =========================
    list_desa = sorted(df_clean_filtered["DESA"].dropna().unique())
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
    df_clean_filtered = df_clean_filtered.loc[df_clean_filtered['DESA'].isin(final_desa)]

# =========================
# Kontak
# =========================
    options_kontak = ["Semuanya", "Memiliki Kontak", "Tidak Punya Kontak"]

    kontak_conditions= {
        "Memiliki Kontak": df_clean_filtered["NO TELP ENKRIP"].notna(),
        "Tidak Punya Kontak": df_clean_filtered["NO TELP ENKRIP"].isna()
    }
    
    kontak_filter_option = handle_segmented_filter(label='Filter Kontak', options=options_kontak)

    
    df_clean_filtered = helper_segmented_filter(
        df_clean_filtered,
        map_condition=kontak_conditions,
        selection=kontak_filter_option
    )


# =========================
# Bantuan
# =========================
    options_bantuan = ["Semuanya", "Sudah Menerima Bantuan", "Belum Menerima Bantuan"]
    bantuan_conditions = {
        "Sudah Menerima Bantuan": df_clean_filtered["PENERIMAAN BANTUAN"] == "sudah",
        "Belum Menerima Bantuan": df_clean_filtered["PENERIMAAN BANTUAN"] == "belum"
    }
    bantuan_filter_option = handle_segmented_filter(label='Filter Bantuan', options=options_bantuan)
    df_clean_filtered = helper_segmented_filter(
        df_clean_filtered,
        map_condition=bantuan_conditions,
        selection=bantuan_filter_option
    )
# =========================
# DKP IMAGE 
# =========================
    st.image(LOGO_DKP, width=200)


with st.container():
    fig_lineplot = plot_tren_produksi_total(
        df=df_clean,
        kolom_tanggal="index",
        kolom_nilai="Jumlah Produksi Final",
        judul="Tren Jumlah Produksi UPI",
        watermark_text="DATA DUMMY",
        # kolom_grup='KECAMATAN'
    )

    st.pyplot(fig_lineplot, use_container_width=True)
    # ============================================================
    # BAR CHART - JUMLAH UPI PER KECAMATAN
    # ============================================================
    fig1 = plot_upi_per_kecamatan(df)
    # fig2 = plot_upi_per_olahan(df)
    df_count_top_5_jenis_olahan = value_count_top5_with_others(df, group_col="jenis_proses", value_name="jumlah_upi")
    # df_count_top_5_jumlah_jenis_olahan_list = df_count_top_5_jenis_olahan["jumlah_upi"].tolist()
    # df_count_top_5_jenis_olahan_list = df_count_top_5_jenis_olahan["jenis_proses"].tolist()
    label_tampil_fig2 = [
        f"{jenis} = {jumlah}"
        for jumlah, jenis in zip(
            df_count_top_5_jenis_olahan["jumlah_upi"].tolist(),
            df_count_top_5_jenis_olahan["jenis_proses"].tolist()
        )
    ]
    
    fig2 = donut_plot_kategori_agregat(
        df=df_count_top_5_jenis_olahan,
        column_kategori="jenis_proses",
        column_value="jumlah_upi",
        label_tampil=label_tampil_fig2,
        judul="Proporsi Jenis Proses UPI"
    )

    
    col1, col2 = st.columns([1, 1])   # rasio seimbang
    with col1:
        st.pyplot(fig1, use_container_width=True)
    with col2:
        st.pyplot(fig2, use_container_width=True)
    
# ============================================================
# BODY SEC 2
# ============================================================
st.divider()
st.subheader("Data :blue[Terfilter]")


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
fig3 = plot_upi_jenis_proses_jenis_ikan_catplot(df_clean_filtered)
# fig4 = plot_persentase_upi_memiliki_kontak(df_filtered_1)
fig4 = donut_plot_binary(
    df_clean_filtered,
    kolom="NO TELP ENKRIP",
    # judul="",
    label_true="Memiliki Kontak",
    label_false="Tidak Memiliki Kontak",
    judul="Persentase UPI yang Memiliki Kontak"
)

fig5 = donut_plot_kategori(
    df_clean_filtered,
    "PENERIMAAN BANTUAN",
    kategori_urutan=["sudah", "belum"],
    label_tampil=["Sudah Menerima Bantuan", "Belum Menerima Bantuan"],
    judul="Persentase Penerimaan Bantuan",figsize=(6, 9)
)

with st.container():
    col1,col2 = st.columns([2,1])
    with col1:
        st.pyplot(fig3, use_container_width=True)
    with col2:
        with st.container():
            st.pyplot(fig4, use_container_width=True)
            st.pyplot(fig5, use_container_width=True)
# st.write(df_filtered_1['PENERIMAAN BANTUAN'].value_counts())
st.divider()
with st.container():
    
    col1,col2 = st.columns([3,1])
    
    with col2:
        # hue_fig5 = ["North", "East", "South", "West"]
        # selection_hue_fig5 = st.segmented_control(
        #     "Hue", hue_fig5, selection_mode="single"
        # )
        lineplot_filtered_hue = st.selectbox(
            "Kelompokkan Berdasarkan",
            ("Status Bantuan", "Jenis Olahan", "Jenis Ikan Yang Diolah",'Kecamatan','Desa','Tidak Ada'),
        )
        lineplot_filtered_hue_map = {
            "Status Bantuan":'PENERIMAAN BANTUAN', 
            "Jenis Olahan":'jenis_proses', 
            "Jenis Ikan Yang Diolah":'jenis_ikan',
            'Tidak Ada':None,
            'Kecamatan':'KECAMATAN',
            'Desa':'DESA'
        }
        fig6 = plot_line_chart(
            df_clean_filtered,
            x_axis=df_clean_filtered.index,
            y_axis='Jumlah Produksi Final',
            y_label='Jumlah Produksi',
            kolom_grup=lineplot_filtered_hue_map.get(lineplot_filtered_hue),
            judul='Trend Produksi Terfilter',
            figsize=(10, 5),
            tampil_legend=True,
            watermark_text="Data Dummy",
            # tampil_legend=True
        )
    
    with col1:
        st.pyplot(fig6, use_container_width=True)






# st.divider()
# st.dataframe(df_clean)
# st.dataframe(df_clean_filtered)

