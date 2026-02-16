# charts.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.ticker import MaxNLocator
import streamlit as st

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
        .size()
        .reset_index(name="jumlah_upi")
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

def segmented_filter(label, options, df, column, map_condition):
    """
    label         : Judul segmented control
    options       : List opsi segmented
    df            : DataFrame yang akan difilter
    column        : Nama kolom target
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

    values = counts.values.astype(int)

    # Jika total 0
    if values.sum() == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Tidak ada data", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=figsize)

    ax.pie(
        values,
        labels=label_tampil,
        autopct="%1.1f%%",
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

    return fig

# def plot_persentase_upi_memiliki_kontak(df, kolom_kontak="NO TELP ENKRIP", figsize=(6, 6)):
#     """
#     Membuat donut plot persentase UPI yang memiliki kontak.

#     Parameters
#     ----------
#     df : pandas.DataFrame
#         DataFrame asli
#     kolom_kontak : str
#         Nama kolom kontak (default: "KONTAK")
#     figsize : tuple
#         Ukuran figure

#     Returns
#     -------
#     fig : matplotlib.figure.Figure
#     """

#     # Buat flag memiliki kontak / tidak
#     memiliki_kontak = df[kolom_kontak].notna() & (df[kolom_kontak].astype(str).str.strip() != "")

#     jumlah_memiliki = memiliki_kontak.sum()
#     jumlah_tidak = (~memiliki_kontak).sum()

#     labels = ["Memiliki Kontak", "Tidak Memiliki Kontak"]
#     values = [jumlah_memiliki, jumlah_tidak]

#     fig, ax = plt.subplots(figsize=figsize)

#     wedges, texts, autotexts = ax.pie(
#         values,
#         labels=labels,
#         autopct="%1.1f%%",
#         startangle=90,
#         wedgeprops=dict(width=0.4)
#     )

#     fig.suptitle("Persentase UPI yang Memiliki Kontak", fontsize=20)
#     ax.axis("equal")
#     total = values.sum()
#     ax.text(0, 0, f"Total\n{total}", ha="center", va="center",
#             fontsize=12, weight="bold")

#     return fig



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
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.4)
    )

    ax.axis("equal")
    ax.set_title(judul)

    total = sum(values)
    ax.text(0, 0, f"Total\n{total}",
            ha="center", va="center",
            fontsize=12, weight="bold")

    return fig
