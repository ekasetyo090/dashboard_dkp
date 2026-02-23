# charts.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# from matplotlib.ticker import MaxNLocator
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import hex_to_rgb


def plot_upi_per_kecamatan(df):
    """
    Membuat bar chart Jumlah UPI per Kecamatan (Plotly version)

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame asli

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """

    df_kec = (
        df
        .groupby("KECAMATAN")
        .size()
        .reset_index(name="jumlah_upi")
    )

    fig = px.bar(
        df_kec,
        x="KECAMATAN",
        y="jumlah_upi",
        title="Jumlah Unit Pengolahan Ikan (UPI) per Kecamatan",
        labels={
            "KECAMATAN": "Kecamatan",
            "jumlah_upi": "Jumlah UPI"
        }
    )

    # Styling tambahan
    fig.update_layout(
        xaxis_tickangle=-45,
        title_x=0.1,  # center title
        yaxis=dict(showgrid=True),
    )

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


# def plot_upi_per_olahan(df):
#     """
#     Donut chart Proporsi UPI Berdasarkan Jenis Olahan (Plotly version)
#     """

#     # Hitung jumlah per jenis_proses
#     df_olahan = (
#         df
#         .groupby("jenis_proses")
#         .size()
#         .reset_index(name="jumlah_upi")
#         .sort_values("jumlah_upi", ascending=False)
#     )

#     # Ambil top 5
#     top5 = df_olahan.head(5)

#     # Hitung sisanya
#     others_sum = df_olahan.iloc[5:]["jumlah_upi"].sum()

#     if others_sum > 0:
#         others_row = pd.DataFrame({
#             "jenis_proses": ["Lain-lain"],
#             "jumlah_upi": [others_sum]
#         })
#         df_final = pd.concat([top5, others_row], ignore_index=True)
#     else:
#         df_final = top5

#     # Buat donut chart
#     fig = px.pie(
#         df_final,
#         names="jenis_proses",
#         values="jumlah_upi",
#         title="Proporsi Unit Pengolahan Ikan (UPI) Berdasarkan Jenis Olahan",
#         hole=0.6  # <- ini bikin donut
#     )

#     # Styling tambahan
#     fig.update_traces(
#         textinfo="percent+label",
#         hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}"
#     )

#     fig.update_layout(
#         title_x=0.5,
#         legend_title="Jenis Olahan"
#     )

#     return fig

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

    fig = px.bar(
        df_grouped,
        y="jenis_proses",          # <- pindah ke Y
        x="jumlah_upi",
        color="jenis_ikan",
        barmode="stack",
        orientation="h",          # <- horizontal
        title="Jumlah UPI Berdasarkan Jenis Proses dan Jenis Ikan",
        labels={
            "jenis_proses": "Jenis Proses",
            "jumlah_upi": "Jumlah UPI",
            "jenis_ikan": "Jenis Ikan"
        }
    )

    fig.update_layout(
        title_x=0.1,
        legend_title="Jenis Ikan",
        height=600
    )

    return fig

def handle_multiselect_all(selected, default_label, full_list):
    # Jika default + pilihan lain → hapus default
    if default_label in selected and len(selected) > 1:
        selected.remove(default_label)

    # Jika kosong atau default dipilih → kembalikan semua data
    if not selected or default_label in selected:
        return full_list

    # Jika pilih spesifik
    return selected

def handle_segmented_filter(label,options):
    selection = st.segmented_control(
        label,
        options,
        default="Semuanya",
        selection_mode="single"
    )
    return selection

def helper_segmented_filter(
                     df,
                     map_condition,
                     selection
                     ):
    """
    label         : Judul segmented control
    options       : List opsi segmented
    df            : DataFrame yang akan difilter
    map_condition: Dict mapping opsi -> kondisi filter
    """


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
):
    """
    Donut plot kategori (Plotly version, aman jika data kosong).
    """

    # Jika dataframe kosong
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title=judul,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    counts = (
        df[column]
        .value_counts()
        .reindex(kategori_urutan, fill_value=0)
    )

    values = counts.values.astype(int)
    labels = label_tampil

    # Jika total 0
    if values.sum() == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title=judul,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    total = int(values.sum())

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,  # donut
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}"
            )
        ]
    )

    # Tambahkan total di tengah
    fig.add_annotation(
        text=f"<b>Total<br>{total}</b>",
        showarrow=False,
        font=dict(size=16)
    )

    fig.update_layout(
        title=judul,
        title_x=0.1,
        legend_title="Kategori",
        # height=figsize[1] * 100,
        # width=figsize[0] * 100
    )

    return fig

def donut_plot_kategori_agregat(
    df,
    # column_kategori,
    column_value,
    label_tampil,
    judul,
    figsize=(6, 6)
):
    """
    Donut plot untuk dataframe yang sudah berbentuk agregasi (Plotly version).
    """

    # Jika dataframe kosong
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16
        )
        fig.update_layout(
            title=judul,
            xaxis_visible=False,
            yaxis_visible=False
        )
        return fig

    values = df[column_value].astype(int).values

    # Jika total 0
    if values.sum() == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16
        )
        fig.update_layout(
            title=judul,
            xaxis_visible=False,
            yaxis_visible=False
        )
        return fig

    # Gunakan label_tampil untuk legend
    df_plot = df.copy()
    df_plot["Kategori"] = label_tampil

    fig = px.pie(
        df_plot,
        names="Kategori",
        values=column_value,
        hole=0.6,
        title=judul
    )

    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}"
    )

    total = int(values.sum())

    fig.add_annotation(
        text=f"<b>Total<br>{total}</b>",
        showarrow=False,
        font_size=16
    )

    fig.update_layout(
        title_x=0.1,
        legend_title="Kategori",
        height=figsize[0] * 100,
        width=figsize[1] * 100
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

    # =========================
    # DATA KOSONG
    # =========================
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16
        )
        fig.update_layout(title=judul)
        return fig

    # =========================
    # HITUNG KONDISI
    # =========================
    kondisi_true = (
        df[kolom].notna() &
        (df[kolom].astype(str).str.strip() != "")
    )

    jumlah_true = int(kondisi_true.sum())
    jumlah_false = int((~kondisi_true).sum())

    values = [jumlah_true, jumlah_false]

    # Jika semua nol
    if sum(values) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16
        )
        fig.update_layout(title=judul)
        return fig

    labels = [label_true, label_false]
    total = sum(values)

    # =========================
    # WARNA
    # =========================
    colors = ["#2E86C1", "#E74C3C"]  # biru & merah elegan

    # =========================
    # DONUT PLOT
    # =========================
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors),
        textinfo="percent",
        hovertemplate=
            "<b>%{label}</b><br>" +
            "Jumlah: %{value}<br>" +
            "Persentase: %{percent}<extra></extra>"
    ))

    # =========================
    # TOTAL DI TENGAH
    # =========================
    fig.add_annotation(
        text=f"<b>Total<br>{total}</b>",
        showarrow=False,
        font_size=16
    )

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        title=judul,
        title_x=0.1,
        legend_title="Kategori",
        height=figsize[0] * 100,
        width=figsize[1] * 100,
        template="plotly_white"
    )

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

def plot_tren_produksi_total(
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
    Line plot time-series menggunakan Plotly (tanpa ubah cara pemanggilan).
    """

    # Jika dataframe kosong
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16
        )
        fig.update_layout(title=judul)
        return fig

    df_plot = df.copy()

    # =========================
    # TENTUKAN KOLOM X
    # =========================
    if kolom_tanggal == "index":
        df_plot["_x_axis"] = df_plot.index
        x_col = "_x_axis"
    else:
        x_col = kolom_tanggal

    fig = go.Figure()

    # =========================
    # TANPA GROUP
    # =========================
    if not kolom_grup:

        agg = (
            df_plot
            .groupby(x_col)[kolom_nilai]
            .agg(["mean", "min", "max"])
            .reset_index()
            .sort_values(x_col)
        )

        x_vals = agg[x_col]
        y_min = agg["min"]
        y_max = agg["max"]
        y_mean = agg["mean"]

        # AREA RANGE (polygon stabil)
        fig.add_trace(go.Scatter(
            x=list(x_vals) + list(x_vals[::-1]),
            y=list(y_max) + list(y_min[::-1]),
            fill="toself",
            fillcolor="rgba(0,100,200,0.2)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name="Range (Min–Max)"
        ))

        # GARIS MEAN
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_mean,
            mode="lines+markers",
            name="Rata-rata"
        ))

    # =========================
    # DENGAN GROUP
    # =========================
    else:

        groups = df_plot[kolom_grup].unique()

        for g in groups:

            df_g = df_plot[df_plot[kolom_grup] == g]

            agg = (
                df_g
                .groupby(x_col)[kolom_nilai]
                .agg(["mean", "min", "max"])
                .reset_index()
                .sort_values(x_col)
            )

            x_vals = agg[x_col]
            y_min = agg["min"]
            y_max = agg["max"]
            y_mean = agg["mean"]

            # AREA RANGE
            fig.add_trace(go.Scatter(
                x=list(x_vals) + list(x_vals[::-1]),
                y=list(y_max) + list(y_min[::-1]),
                fill="toself",
                fillcolor="rgba(0,100,200,0.15)",
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=False
            ))

            # GARIS MEAN
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_mean,
                mode="lines+markers",
                name=str(g)
            ))

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        title=judul,
        title_x=0.1,
        height=figsize[1] * 100,
        width=figsize[0] * 100,
        showlegend=tampil_legend,
        xaxis_title="Tanggal",
        yaxis_title=kolom_nilai,
        template="plotly_white"
    )

    # =========================
    # WATERMARK
    # =========================
    fig.add_annotation(
        text=watermark_text,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=60, color="rgba(150,150,150,0.2)"),
        textangle=30
    )

    return fig

def plot_line_chart(
    data,
    x_axis,
    y_axis,
    y_label:str=None,
    kolom_grup=None,
    judul:str=None,
    figsize=(10, 5),
    tampil_legend=False,
    watermark_text="Data Dummy"
):
    # =========================
    # PARAMETER TRANSPARANSI AREA
    # =========================
    area_opacity = 0.25  # <-- Ubah di sini (0.1 - 0.5)

    # =========================
    # DATA KOSONG
    # =========================
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16
        )
        fig.update_layout(title=judul)
        return fig

    df_plot = data.copy()

    # =========================
    # HANDLE X AXIS
    # =========================
    if isinstance(x_axis, (pd.Index, pd.Series)):
        df_plot["_x_axis"] = x_axis
    else:
        df_plot["_x_axis"] = x_axis

    x_col = "_x_axis"

    fig = go.Figure()

    colors = px.colors.qualitative.Plotly

    # =========================
    # TANPA GROUP
    # =========================
    if not kolom_grup:

        agg = (
            df_plot
            .groupby(x_col)[y_axis]
            .agg(["mean", "min", "max"])
            .reset_index()
            .sort_values(x_col)
        )

        x_vals = agg[x_col]
        y_min = agg["min"]
        y_max = agg["max"]
        y_mean = agg["mean"]

        color_line = colors[0]
        r, g, b = hex_to_rgb(color_line)
        color_fill = f"rgba({r},{g},{b},{area_opacity})"

        # AREA RANGE
        fig.add_trace(go.Scatter(
            x=list(x_vals) + list(x_vals[::-1]),
            y=list(y_max) + list(y_min[::-1]),
            fill="toself",
            fillcolor=color_fill,
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=False
        ))

        # GARIS MEAN
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_mean,
            mode="lines+markers",
            name="Rata-rata",
            line=dict(color=color_line, width=3),
            customdata=list(zip(y_min, y_max)),
            hovertemplate=
                "<b>Tanggal:</b> %{x}<br>" +
                "<b>Mean:</b> %{y}<br>" +
                "<b>Min:</b> %{customdata[0]}<br>" +
                "<b>Max:</b> %{customdata[1]}<extra></extra>"
        ))

    # =========================
    # DENGAN GROUP
    # =========================
    else:

        # Pastikan kategori dianggap string
        df_plot[kolom_grup] = df_plot[kolom_grup].astype(str)

        groups = df_plot[kolom_grup].dropna().unique()

        for i, g in enumerate(groups):

            df_g = df_plot[df_plot[kolom_grup] == g]

            agg = (
                df_g
                .groupby(x_col)[y_axis]
                .agg(["mean", "min", "max"])
                .reset_index()
                .sort_values(x_col)
            )

            x_vals = agg[x_col]
            y_min = agg["min"]
            y_max = agg["max"]
            y_mean = agg["mean"]

            color_line = colors[i % len(colors)]
            r, g_color, b = hex_to_rgb(color_line)
            color_fill = f"rgba({r},{g_color},{b},{area_opacity})"

            # AREA
            fig.add_trace(go.Scatter(
                x=list(x_vals) + list(x_vals[::-1]),
                y=list(y_max) + list(y_min[::-1]),
                fill="toself",
                fillcolor=color_fill,
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=False
            ))

            # GARIS
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_mean,
                mode="lines+markers",
                name=g,
                line=dict(color=color_line, width=3),
                customdata=list(zip(y_min, y_max)),
                hovertemplate=
                    "<b>Group:</b> %{fullData.name}<br>" +
                    "<b>Tanggal:</b> %{x}<br>" +
                    "<b>Mean:</b> %{y}<br>" +
                    "<b>Min:</b> %{customdata[0]}<br>" +
                    "<b>Max:</b> %{customdata[1]}<extra></extra>"
            ))

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        title=judul,
        title_x=0.1,
        height=figsize[1] * 100,
        width=figsize[0] * 100,
        showlegend=tampil_legend,
        xaxis_title="Tanggal",
        yaxis_title=y_label if y_label else y_axis,
        template="plotly_white"
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")

    # WATERMARK
    fig.add_annotation(
        text=watermark_text,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=60, color="rgba(150,150,150,0.2)"),
        textangle=30
    )

    return fig