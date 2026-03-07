# ============================================================
# IMPORT LIBRARY
# ============================================================

import base64
import asyncio

import pandas as pd

import streamlit as st

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from LIB.charts import (
    plot_upi_per_kecamatan,plot_upi_jenis_proses_jenis_ikan_catplot,
    handle_multiselect_all,helper_segmented_filter,
    donut_plot_kategori,donut_plot_binary,value_count_top5_with_others,
    donut_plot_kategori_agregat,parse_produksi,add_dynamic_noise,plot_tren_produksi_total,plot_bedah_upi_stack,
    handle_segmented_filter,plot_line_chart,plot_produksi_stack_tahun
    )





# ============================================================
# PATH CONFIGURATION
# ============================================================
BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

ASSET_DIR = os.path.join(ROOT_DIR, "asset")

LOGO_PEMDA = os.path.join(ASSET_DIR, "logo pemda.png")
LOGO_DKP = os.path.join(ASSET_DIR, "DKP.png")
BACKGROUND = os.path.join(ASSET_DIR, "background.jpg")
DATA_PATH = os.path.join(ROOT_DIR, "data_upi_final_publish.xlsx")
# DATA_PATH_UPI = os.path.join(ROOT_DIR, "data_upi_final_publish.xlsx")

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


# async def loading_animation():
#     placeholder = st.empty()

#     with placeholder.container():
#         with st.spinner("Memuat data..."):
#             progress = st.progress(0)
#             for i in range(100):
#                 await asyncio.sleep(0.01)
#                 progress.progress(i + 1)

#     placeholder.empty()


# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_excel(DATA_PATH)
df['TANGGAL'] = pd.to_datetime(df['TANGGAL'])
# df["PENERIMAAN BANTUAN"] = (
#     df["PENERIMAAN BANTUAN"]
#     .fillna("Belum")
#     .replace("", "Belum")
# )

# cols = ["jenis_ikan", "jenis_proses", "KECAMATAN", "DESA",'PENERIMAAN BANTUAN','NAMA UPI']

# # df[cols] = df[cols].apply(lambda x: x.str.lower())
# for col in cols:
#     df[col] = (
#         df[col]
#         .astype(str)
#         .str.strip()      # hapus spasi depan/belakang
#         .str.lower()      # semua jadi huruf kecil
#     )



# df_clean = df.copy()
# df_clean = df_clean.drop(columns=['NO'])
# kolom_identitas = ['NAMA UPI', 'DESA', 'KECAMATAN', 'PENERIMAAN BANTUAN', 'JENIS KEGIATAN PENGOLAHAN','NO TELP ENKRIP', 'NAMA PEMILIK ENKRIP', 'clean', 'jenis_proses', 'jenis_ikan']

# # 3. Lakukan Melt
# df_clean_melt = df_clean.melt(
#     id_vars=kolom_identitas, 
#     var_name='Tanggal', 
#     value_name='Jumlah Produksi'
# ).copy()
# df_clean_melt['Tanggal'] = pd.to_datetime(df_clean_melt['Tanggal'], errors='coerce')
# df_clean_melt = df_clean_melt.set_index('Tanggal')
# df_clean_melt['Jumlah Produksi Final'] = (
#     df_clean_melt['Jumlah Produksi']
#     .apply(parse_produksi)
#     .interpolate(method='time')
#     .interpolate(method='linear')
#     .ffill()
#     .bfill()
# )

# # df_clean['Jumlah Produksi Final'] = add_random_noise(
# #     df_clean['Jumlah Produksi Final'],
# #     noise_level=0.08   # 8% variasi
# # ).round(1)

# df_clean_melt['Jumlah Produksi Final'] = add_dynamic_noise(
#     df_clean_melt['Jumlah Produksi Final'],
#     noise_level=0.18,
#     wave_strength=0.07
# ).round(1)
# df_bedah_upi = pd.read_excel(DATA_PATH_UPI,sheet_name="bedah upi")
# df_bedah_upi['Nama Poklahsar'] = df_bedah_upi['Nama Poklahsar'].str.lower()
# df_bedah_upi = df_bedah_upi.merge(
#     df[['NAMA UPI', 'DESA', 'KECAMATAN']],
#     left_on='Nama Poklahsar',
#     right_on='NAMA UPI',
#     how='left'
# ).drop(columns=['NAMA UPI'])
# 		
# df_bedah_upi = df_bedah_upi.dropna(subset=['DESA', 'KECAMATAN'])
# df_bedah_upi = df_bedah_upi.drop_duplicates(
#     subset=['Nomor Kusuka'],
#     keep='first'
# )
# df_clean_filtered = df_clean.copy()
# ============================================================
# MAIN TITLE
# ============================================================
st.title("Dashboard Statistik PDSPKP", anchor=False)
st.divider()
tab1, tab2 = st.tabs(["POKLAHSAR", "UPI"])
# tab poklahsar

with tab1:
    # ============================================================
    # METRICS
    # ============================================================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jumlah UPI", len(df['NAMA UPI'].unique()))
    col2.metric("Jenis Olahan", df["JENIS KEGIATAN"].nunique())
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
        list_proses = sorted(df["JENIS KEGIATAN"].dropna().unique())
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
        df_clean_filtered = df[(df["JENIS KEGIATAN"].isin(final_jenis_proses))].copy()
        # df_clean_filtered = df_clean_filtered.loc[df_clean_filtered['jenis_proses'].isin(final_jenis_proses)]
    # =========================
    # JENIS IKAN
    # =========================
        list_ikan = sorted(df["JENIS IKAN"].dropna().unique())
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
        df_clean_filtered = df_clean_filtered.loc[df_clean_filtered['JENIS IKAN'].isin(final_jenis_ikan)]
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
            "Memiliki Kontak": df_clean_filtered["NO TELP HASH"].notna(),
            "Tidak Punya Kontak": df_clean_filtered["NO TELP HASH"].isna()
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

        df_clean_filtered_upi = df_clean_filtered.loc[df_clean_filtered['tahun bedah upi'].notna()].copy()
        df_clean_filtered_poklahsar = df_clean_filtered.loc[df_clean_filtered['tahun bedah upi'].isna()].copy()
    # =========================
    # DKP IMAGE 
    # =========================
        st.image(LOGO_DKP, width=200)


    with st.container():
        fig_lineplot = plot_tren_produksi_total(
            df=df,
            kolom_tanggal="TANGGAL",
            kolom_nilai="PRODUKSI_BERSIH",
            judul="Trend Jumlah Produksi POKLAHSAR",
            watermark_text="DATA DUMMY",
            # kolom_grup='KECAMATAN'
        )

        st.plotly_chart(fig_lineplot, use_container_width=True)
        # ============================================================
        # BAR CHART - JUMLAH UPI PER KECAMATAN
        # ============================================================
        fig1 = plot_upi_per_kecamatan(df)
        # fig2 = plot_upi_per_olahan(df)
        df_count_top_5_jenis_olahan = value_count_top5_with_others(df, group_col="JENIS KEGIATAN", value_name="jumlah_upi")
        # df_count_top_5_jumlah_jenis_olahan_list = df_count_top_5_jenis_olahan["jumlah_upi"].tolist()
        # df_count_top_5_jenis_olahan_list = df_count_top_5_jenis_olahan["jenis_proses"].tolist()
        label_tampil_fig2 = [
            f"{jenis} = {jumlah}"
            for jumlah, jenis in zip(
                df_count_top_5_jenis_olahan["jumlah_upi"].tolist(),
                df_count_top_5_jenis_olahan["JENIS KEGIATAN"].tolist()
            )
        ]
        
        fig2 = donut_plot_kategori_agregat(
            df=df_count_top_5_jenis_olahan,
            # column_kategori="jenis_proses",
            column_value="jumlah_upi",
            label_tampil=df_count_top_5_jenis_olahan["JENIS KEGIATAN"].tolist(),
            judul="Proporsi Jenis Kegiatan POKLAHSAR"
        )

        
        col1, col2 = st.columns([2, 1])   # rasio seimbang
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        
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
    fig3 = plot_upi_jenis_proses_jenis_ikan_catplot(df_clean_filtered_poklahsar)
    # fig4 = plot_persentase_upi_memiliki_kontak(df_filtered_1)
    fig4 = donut_plot_binary(
        df_clean_filtered_poklahsar,
        kolom="NO TELP HASH",
        # judul="",
        label_true="Memiliki Kontak",
        label_false="Tidak Memiliki Kontak",
        judul="Persentase Poklahsar yang Memiliki Kontak"
    )

    fig5 = donut_plot_kategori(
        df_clean_filtered_poklahsar,
        "PENERIMAAN BANTUAN",
        kategori_urutan=["sudah", "belum"],
        label_tampil=["Sudah Menerima Bantuan", "Belum Menerima Bantuan"],
        judul="Persentase Penerimaan Bantuan"
    )

    with st.container():
        col1,col2 = st.columns([1,1])
        with col1:
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            with st.container():
                st.plotly_chart(fig4, use_container_width=True)
                
    # st.write(df_filtered_1['PENERIMAAN BANTUAN'].value_counts())
    # st.divider()
    with st.container():
        
        col1,col2 = st.columns([1.3,1])
        with col1:
            # col11,col21 = st.columns([4,1])
            
            # with col21:
                
            lineplot_filtered_hue = st.selectbox(
                "Kelompokkan Berdasarkan",
                ("Status Bantuan", "Jenis Olahan", "Jenis Ikan Yang Diolah",'Kecamatan','Desa','Tidak Ada'),
                placeholder="Pilih Metode"
                # index=5
            )

            # with col11:
                
            lineplot_filtered_hue_map = {
                "Status Bantuan":'PENERIMAAN BANTUAN', 
                "Jenis Olahan":'JENIS KEGIATAN', 
                "Jenis Ikan Yang Diolah":'JENIS IKAN',
                'Tidak Ada':None,
                'Kecamatan':'KECAMATAN',
                'Desa':'DESA'
            }
            fig6 = plot_line_chart(
                df_clean_filtered_poklahsar,
                x_axis='TANGGAL',
                y_axis='PRODUKSI_BERSIH',
                y_label='Jumlah Produksi',
                kolom_grup=lineplot_filtered_hue_map.get(lineplot_filtered_hue),
                judul='Trend Produksi Terfilter',
                figsize=(10, 5),
                tampil_legend=True,
                watermark_text="Data Dummy",
                # tampil_legend=True
            )
            st.plotly_chart(fig6, use_container_width=True)

        with col2:
            st.plotly_chart(fig5, use_container_width=True)
            # hue_fig5 = ["North", "East", "South", "West"]
            # selection_hue_fig5 = st.segmented_control(
            #     "Hue", hue_fig5, selection_mode="single"
            # )
            
with tab2:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jumlah UPI", len(df_clean_filtered_upi['NAMA UPI'].unique()))
    col2.metric("Jenis Olahan", df_clean_filtered_upi["JENIS KEGIATAN"].nunique())
    col3.metric("Kecamatan", df_clean_filtered_upi["KECAMATAN"].nunique())
    col4.metric("Desa", df_clean_filtered_upi["DESA"].nunique())
    st.divider()
    stack_option = st.selectbox(
        "Stack berdasarkan:",
        [
            "DESA",
            "KECAMATAN",
            "JENIS KEGIATAN",
            "JENIS IKAN"
        ]
    )
    col1,col2 = st.columns([1,1])
    with col1:

        fig_bedah_upi = plot_bedah_upi_stack(
            df_clean_filtered_upi,
            stack_option
        )
        st.plotly_chart(fig_bedah_upi, use_container_width=True)

    with col2:
        fig = plot_produksi_stack_tahun(
            df_clean_filtered_upi,
            stack_option
        )

        st.plotly_chart(fig, use_container_width=True)


    lineplot_filtered_hue_upi = st.selectbox(
        "Kelompokkan UPI Berdasarkan",
        ("Status Bantuan", "Jenis Olahan", "Jenis Ikan Yang Diolah",'Kecamatan','Desa','Tidak Ada'),
        placeholder="Pilih Metode"
        # index=5
    )

    

    # with col11:
        
    lineplot_filtered_hue_map_upi = {
        "Status Bantuan":'PENERIMAAN BANTUAN', 
        "Jenis Olahan":'JENIS KEGIATAN', 
        "Jenis Ikan Yang Diolah":'JENIS IKAN',
        'Tidak Ada':None,
        'Kecamatan':'KECAMATAN',
        'Desa':'DESA'
    }

    fig_lineplot_produksi_upi = plot_line_chart(
        df_clean_filtered_upi,
        x_axis='TANGGAL',
        y_axis='PRODUKSI_BERSIH',
        y_label='Jumlah Produksi',
        kolom_grup=lineplot_filtered_hue_map_upi.get(lineplot_filtered_hue_upi),
        judul='Trend Produksi Terfilter',
        figsize=(10, 5),
        tampil_legend=True,
        watermark_text="Data Dummy",
        # tampil_legend=True
    )
    st.plotly_chart(fig_lineplot_produksi_upi, use_container_width=True)

    
    # st.dataframe(df_clean_filtered_upi)
       
    
    






# st.divider()
# st.dataframe(df_clean)
# st.dataframe(df_clean_filtered)

