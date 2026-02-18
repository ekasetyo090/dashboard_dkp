# charts.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.ticker import MaxNLocator
import streamlit as st
import numpy as np


def plot_upi_per_kecamatan(df, figsize=(12, 8)):
    """
    Membuat bar chart Jumlah UPI per Kecamatan.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame asli
    figsize : tuple, optional
        Ukuran figure (default: (12, 8))

    Returns
    -------
    fig : matplotlib.figure.Figure
    """
    df_kec = (
        df
        .groupby("KECAMATAN")
        .size()
        .reset_index(name="jumlah_upi")
    )

    fig, ax = plt.subplots(figsize=figsize)

    sns.barplot(
        data=df_kec,
        x="KECAMATAN",
        y="jumlah_upi",
        ax=ax
    )

   
    ax.set_xlabel("Kecamatan")
    ax.set_ylabel("Jumlah UPI")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    # Garis rata-rata
#    avg_value = df_kec["jumlah_upi"].mean()
#    ax.axhline(
#        y=avg_value,
#        linestyle="--",
#        linewidth=2,
#        label="Rata-rata"
#    )

    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.suptitle("Jumlah Unit Pengolahan Ikan (UPI) per Kecamatan", fontsize=30)
    #ax.legend(title="Keterangan")

    plt.tight_layout()

    return fig

def value_count_top5_with_others(df, group_col, value_name="jumlah_proses"):
    """
    Mengelompokkan data berdasarkan kolom tertentu,
    mengambil 5 kategori dengan jumlah terbesar,
    dan menggabungkan sisanya ke dalam kategori 'Lain-lain'.

    Parameters
    ----------
    df : pandas.DataFrame
        Data sumber yang akan diolah.

    group_col : str
        Nama kolom yang digunakan untuk pengelompokan
        (contoh: "jenis_proses", "kecamatan", dll).

    value_name : str, default="jumlah_upi"
        Nama kolom hasil agregasi (jumlah per kategori).

    Returns
    -------
    pandas.DataFrame
        DataFrame berisi:
        - 5 kategori terbesar
        - 1 baris tambahan "Lain-lain" (jika ada sisa kategori)
    """

    # 1. Hitung jumlah per kategori
    counted_df = df[group_col].value_counts().reset_index().rename(columns={"count": value_name})
    # (df['jenis_proses'].value_counts().reset_index().rename(columns={"count": "xxxx"}))

    # 2. Urutkan dari terbesar ke terkecil
    sorted_df = counted_df.sort_values(
        by=value_name,
        ascending=False
    ).copy()

    # # 3. Ambil 5 kategori teratas
    top_five = sorted_df.head(5).copy()

    # # 4. Hitung total kategori di luar top 5
    others_total = sorted_df.iloc[5:][value_name].sum()

    # 5. Jika ada kategori lain, gabungkan sebagai "Lain-lain"
    if others_total > 0:
        others_row = pd.DataFrame({
            group_col: ["Lain-lain"],
            value_name: [others_total]
        })

        result_df = pd.concat(
            [top_five, others_row],
            ignore_index=True
        )
    else:
        result_df = top_five

    return result_df


def plot_upi_per_olahan(df, figsize=(12, 8)):
    """
    Membuat bar chart Jumlah UPI per Kecamatan.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame asli
    figsize : tuple, optional
        Ukuran figure (default: (12, 8))

    Returns
    -------
    fig : matplotlib.figure.Figure
    """
    df_olahan = (
        df.groupby("jenis_proses")
        .value_counts()
        # .reset_index(name="jumlah_upi")
        .reset_index()
        )
    
    # Urutkan dari terbesar
    df_olahan = df_olahan.sort_values("jumlah_upi", ascending=False)
    
    # Ambil 5 terbesar
    top5 = df_olahan.head(5)
    
    # Jumlahkan sisanya
    others_sum = df_olahan.iloc[5:]["jumlah_upi"].sum()
    
    # Jika ada kategori di luar top 5
    if others_sum > 0:
        others_row = pd.DataFrame({
            "jenis_proses": ["Lain-lain"],
            "jumlah_upi": [others_sum]
        })
        df_olahan = pd.concat([top5, others_row], ignore_index=True)
    else:
        df_olahan = top5

    fig, ax = plt.subplots(figsize=figsize)

    wedges, texts, autotexts = ax.pie(
        df_olahan["jumlah_upi"],
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.85
    )
    
    # Lubang tengah (donut)
    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    ax.add_artist(centre_circle)
    
    
    
    # Legend
    labels = [
        f"{j} ({v})"
        for j, v in zip(df_olahan["jenis_proses"], df_olahan["jumlah_upi"])
    ]
    
    ax.legend(
        wedges,
        labels,
        title="Jenis Olahan",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    fig.suptitle("Proporsi Unit Pengolahan Ikan (UPI) Berdasarkan Jenis Olahan", fontsize=30)
    ax.axis("equal")  # memastikan lingkaran bulat
    plt.tight_layout()
    

    return fig

def plot_upi_jenis_proses_jenis_ikan_catplot(df, figsize=(12, 8)):
    """
    Membuat catplot bar Jumlah UPI per Jenis Proses
    dengan pembedaan berdasarkan Jenis Ikan.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame asli
    figsize : tuple, optional
        Ukuran figure (default: (12, 8))

    Returns
    -------
    fig : matplotlib.figure.Figure
    """
    # Agregasi data
    df_grouped = (
        df
        .groupby(["jenis_proses", "jenis_ikan"])
        .size()
        .reset_index(name="jumlah_upi")
    )

    g = sns.catplot(
        data=df_grouped,
        kind="bar",
        x="jenis_proses",
        y="jumlah_upi",
        hue="jenis_ikan",
        height=figsize[1] / 2,
        aspect=figsize[0] / figsize[1]
    )

    g.set_axis_labels("Jenis Proses", "Jumlah UPI")
    g.fig.suptitle("Jumlah UPI Berdasarkan Jenis Proses dan Jenis Ikan", fontsize=20)

    # Rotasi label x
    for ax in g.axes.flat:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
    if g._legend is not None:
        g._legend.set_title("Jenis Ikan")

    # g._legend.set_title("Jenis Ikan")

    return g.fig

def handle_multiselect_all(selected, default_label, full_list):
    # Jika default + pilihan lain → hapus default
    if default_label in selected and len(selected) > 1:
        selected.remove(default_label)

    # Jika kosong atau default dipilih → kembalikan semua data
    if not selected or default_label in selected:
        return full_list

    # Jika pilih spesifik
    return selected

def segmented_filter(label, options, 
                     df,#column, 
                     map_condition
                     ):
    """
    label         : Judul segmented control
    options       : List opsi segmented
    df            : DataFrame yang akan difilter
    map_condition: Dict mapping opsi -> kondisi filter
    """

    selection = st.segmented_control(
        label,
        options,
        default="Semuanya",
        selection_mode="single"
    )

    if selection in map_condition:
        return df[map_condition[selection]]
    else:
        return df
    
def donut_plot_kategori(
    df,
    column,
    kategori_urutan,
    label_tampil,
    judul,
    # label_value=None,
    figsize=(6, 6)
):
    """
    Donut plot kategori (aman jika data kosong).
    """

    # Jika dataframe kosong
    if df.empty:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    counts = (
        df[column]
        .value_counts()
        .reindex(kategori_urutan, fill_value=0)
    )
    # if label_value == None:
    #     values = counts.values.astype(int)
    # else:
    #     values = label_value
    values = counts.values.astype(int)
    # Jika total 0
    if values.sum() == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=figsize)
    # if label_value == None:
    #     ax_pie_label = values
    ax.pie(
        values,
        labels=None,
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=90,
        wedgeprops={"width": 0.4}
    )

    ax.axis("equal")
    ax.set_title(judul)

    total = int(values.sum())
    ax.text(
        0, 0,
        f"Total\n{total}",
        ha="center", va="center",
        fontsize=12, weight="bold"
    )

    ax.legend(
        label_tampil,
        title="Kategori",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    return fig

def donut_plot_kategori_agregat(
    df,
    column_kategori,
    column_value,
    label_tampil,
    judul,
    figsize=(6, 6)
):
    """
    Donut plot untuk dataframe yang sudah berbentuk agregasi.

    df : DataFrame
        Contoh kolom: [column_kategori, column_value]
    column_kategori : str
        Nama kolom kategori (misal: 'jenis_proses')
    column_value : str
        Nama kolom nilai (misal: 'jumlah_upi')
    """

    # Jika dataframe kosong
    if df.empty:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    values = df[column_value].astype(int).values

    # Jika total 0
    if values.sum() == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=figsize)

    ax.pie(
        values,
        labels=None,
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=90,
        wedgeprops={"width": 0.4}
    )

    ax.axis("equal")
    ax.set_title(judul)

    total = int(values.sum())
    ax.text(
        0, 0,
        f"Total\n{total}",
        ha="center", va="center",
        fontsize=12, weight="bold"
    )

    ax.legend(
        label_tampil,
        title="Kategori",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    return fig


def donut_plot_binary(
    df,
    kolom,
    label_true,
    label_false,
    judul,
    figsize=(6, 6)
):
    """
    Donut plot untuk data biner (ada/tidak).
    Aman jika dataframe kosong.
    """

    # Jika dataframe kosong
    if df.empty:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    kondisi_true = (
        df[kolom].notna() &
        (df[kolom].astype(str).str.strip() != "")
    )

    jumlah_true = int(kondisi_true.sum())
    jumlah_false = int((~kondisi_true).sum())

    values = [jumlah_true, jumlah_false]

    # Jika semua nol
    if sum(values) == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    labels = [label_true, label_false]

    fig, ax = plt.subplots(figsize=figsize)

    ax.pie(
        values,
        labels=None,
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    
    ax.legend(
        labels,
        title="Kategori",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
       

    ax.axis("equal")
    ax.set_title(judul)

    total = sum(values)
    ax.text(0, 0, f"Total\n{total}",
            ha="center", va="center",
            fontsize=12, weight="bold")

    return fig

def parse_produksi(x):
    """
    Mengubah nilai campuran menjadi float:
    - '200-300' -> 250
    - '1600/400' -> 1000
    - '350' -> 350
    - None, '', 0 -> NaN
    """
    if pd.isna(x) or x == '' or x == 0:
        return np.nan

    if isinstance(x, str):
        if '-' in x:
            a, b = x.split('-')
            return (float(a) + float(b)) / 2
        if '/' in x:
            a, b = x.split('/')
            return (float(a) + float(b)) / 2
        return float(x)

    return float(x)

def add_dynamic_noise(series, noise_level=0.15, wave_strength=0.05, seed=None):
    """
    Menambahkan variasi dinamis + gelombang agar data terlihat alami.

    Parameters
    ----------
    series : pd.Series
        Data numerik.

    noise_level : float
        Intensitas random utama (0.10 - 0.25 disarankan)

    wave_strength : float
        Kekuatan pola gelombang

    seed : int or None
        Reproducible randomness
    """

    if seed is not None:
        np.random.seed(seed)

    n = len(series)

    # Random noise
    random_noise = np.random.normal(
        loc=0,
        scale=noise_level,
        size=n
    )

    # Wave noise
    x = np.linspace(0, 2*np.pi, n)
    wave_noise = np.sin(x) * wave_strength

    # Gabungkan
    combined_noise = random_noise + wave_noise

    return series * (1 + combined_noise)

def plot_tren_produksi(
    df,
    kolom_tanggal,
    kolom_nilai,
    kolom_grup=None,
    judul="Tren Produksi",
    figsize=(10, 5),
    tampil_legend=False,
    watermark_text="Data Dummy"
):
    """
    Membuat line plot time-series dari data produksi.

    Parameters
    ----------
    df : DataFrame
        Dataframe yang berisi data time series.

    kolom_tanggal : str
        Nama kolom tanggal atau "index".

    kolom_nilai : str
        Nama kolom berisi nilai numerik (y-axis).

    kolom_grup : str, optional
        Kolom pengelompokan (misal: 'NAMA UPI').

    judul : str
        Judul grafik.

    figsize : tuple
        Ukuran figure matplotlib.

    tampil_legend : bool
        Menampilkan legend atau tidak.

    watermark_text : str
        Teks watermark pada grafik.
    """

    # Jika dataframe kosong
    if df.empty:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center")
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=figsize)

    # Tentukan sumbu X
    if kolom_tanggal == "index":
        x_data = df.index
    else:
        x_data = df[kolom_tanggal]

    # Plot
    sns.lineplot(
        data=df,
        x=x_data,
        y=kolom_nilai,
        hue=kolom_grup,
        legend=tampil_legend,
        ax=ax
    )

    # Judul & Label
    ax.set_title(judul)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel(kolom_nilai)

    # Grid
    ax.grid(
        True,
        linestyle="--",
        alpha=0.4
    )

    # Watermark
    ax.text(
        0.5, 0.5,
        watermark_text,
        transform=ax.transAxes,
        fontsize=40,
        color="gray",
        alpha=0.25,
        ha="center",
        va="center",
        rotation=30,
        weight="bold"
    )

    return fig