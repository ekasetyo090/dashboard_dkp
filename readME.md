# 📊 Dashboard Analisis Unit Pengolahan Ikan (UPI)

Dashboard ini dibangun menggunakan **Streamlit** untuk membantu visualisasi dan analisis data Unit Pengolahan Ikan (UPI).  
Aplikasi ini memudahkan pengguna dalam mengeksplorasi data berdasarkan kecamatan, desa, jenis proses, jenis ikan, serta penerimaan bantuan.

---

## 🚀 Fitur Utama

- 📌 Visualisasi jumlah UPI per Kecamatan  
- 📌 Donut Chart proporsi kategori data  
- 📌 Barplot distribusi jenis proses  
- 📌 Line chart tren data (jika tersedia)  
- 📌 Filter interaktif pada sidebar:
  - Kecamatan
  - Desa
  - Jenis Proses
  - Jenis Ikan
  - Penerimaan Bantuan
- 📌 Opsi pilih semua kategori
- 📌 Tampilan responsif dengan container & columns
- 📌 Modular function (charts dipisah dari main script)

---

## 🗂 Struktur Project

```bash
project/
│
├── main.py                # File utama menjalankan Streamlit
├── pages/
│   ├── PDSPKP.py          # Halaman dashboard utama
│   └── charts.py          # Kumpulan fungsi visualisasi
│
├── data/
│   └── data_upi.csv       # Dataset yang digunakan
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalasi

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2️⃣ Buat Virtual Environment (Opsional)

**Menggunakan venv:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Menggunakan Anaconda:**

```bash
conda create -n streamlit_env python=3.12
conda activate streamlit_env
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Jika belum ada `requirements.txt`, install manual:

```bash
pip install streamlit pandas matplotlib seaborn numpy
```

---

## ▶️ Menjalankan Aplikasi

```bash
streamlit run main.py
```

Atau jika dashboard utama ada di folder `pages`:

```bash
streamlit run pages/PDSPKP.py
```

---

## 📊 Library yang Digunakan

- streamlit
- pandas
- matplotlib
- seaborn
- numpy

---

## 🧠 Tujuan Dashboard

Dashboard ini dirancang untuk:

- Mendukung pengambilan keputusan berbasis data
- Memudahkan monitoring distribusi UPI
- Memberikan insight visual terhadap:
  - Persebaran wilayah
  - Jenis kegiatan pengolahan
  - Penerimaan bantuan
  - Pola distribusi produksi

---

## 🛠 Troubleshooting

### ❗ ModuleNotFoundError
Pastikan environment aktif dan library sudah terinstall.

Cek lokasi Streamlit:

```bash
where streamlit
```

atau

```bash
conda list streamlit
```

---

### ❗ DuplicateWidgetID
Pastikan setiap widget Streamlit memiliki parameter `key` yang unik jika digunakan lebih dari satu kali.

---

## 🌱 Rencana Pengembangan

- [ ] Integrasi database (MySQL/PostgreSQL)
- [ ] Download filtered data (CSV/Excel)
- [ ] Statistik deskriptif otomatis
- [ ] Deployment ke local server yang lebih *advanced*
- [ ] Role-based access (admin/user)

---

## 👨‍💻 Developer

Dikembangkan sebagai bagian dari proyek aktualisasi dan penguatan pengelolaan data perikanan.