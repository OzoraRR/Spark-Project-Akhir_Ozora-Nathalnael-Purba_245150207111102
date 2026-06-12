# Spark-Project-Akhir_Ozora-Nathalnael-Purba_245150207111102
Mengimplementasikan pengolahan big data menggunakan Spark dengan dataset berupa informasi lowongan pekerjaan yang didapat dari teknik web scraping (jobstreet.com)

# 🔍 Analisis Lowongan Kerja IT Indonesia dengan Apache Spark

> **Mata Kuliah:** Big Data Analytics  
> **Dataset:** JobStreet Indonesia — 962 lowongan kerja bidang IT  
> **Tools:** Python, PySpark, Structured Streaming, MLlib

---

## 📋 Deskripsi Proyek

Proyek ini mengimplementasikan pipeline Big Data Analytics end-to-end menggunakan **Apache Spark** untuk menganalisis data lowongan kerja IT di Indonesia yang di-scrape dari platform JobStreet. Pipeline mencakup data ingestion, preprocessing, analisis batch, query SQL, clustering dengan MLlib, hingga simulasi Structured Streaming.

---

## 📂 Struktur Repository

```
├── jobstreet_spark_analysis.ipynb   # Notebook utama (PySpark)
├── jobstreet_scraper_final.py       # Script scraping GraphQL API JobStreet
├── jobstreet_jobs_final.json        # Dataset hasil scraping (962 records)
├── output/
│   ├── jobstreet_cleaned.csv        # Data setelah preprocessing
│   └── jobstreet_clusters.csv       # Hasil KMeans clustering
└── README.md
```

---

## 📊 Dataset

| Atribut | Detail |
|---|---|
| **Sumber** | JobStreet Indonesia (via GraphQL API) |
| **Jumlah Records** | 962 lowongan |
| **Cakupan** | Seluruh Indonesia |
| **Kategori** | IT & Teknologi Informasi |
| **Periode** | Mei – Juni 2026 |
| **Salary Disclosed** | 274 dari 962 lowongan (28.5%) |

### Fields Utama

| Field | Deskripsi |
|---|---|
| `id` | ID unik lowongan |
| `title` | Judul posisi |
| `companyName` | Nama perusahaan |
| `location` | Lokasi kerja |
| `category` / `subCategory` | Kategori & sub-kategori jabatan |
| `salaryLabel` | Informasi gaji (jika tersedia) |
| `workType` | Tipe pekerjaan (Full time, Kontrak, dll) |
| `postedAt` | Tanggal posting |
| `isFeatured` | Status iklan berbayar |

---

## ⚙️ Cara Menjalankan

### 1. Install Dependencies

```bash
pip install pyspark nest_asyncio requests
```

### 2. Scraping Data (opsional — dataset sudah tersedia)

```bash
python jobstreet_scraper_final.py
```

> **Catatan:** Scraper memerlukan Bearer Token dari sesi browser JobStreet yang aktif. Token berlaku ±1 jam.

### 3. Jalankan Notebook

Buka `jobstreet_spark_analysis.ipynb` di Jupyter / Google Colab, pastikan `jobstreet_jobs_final.json` ada di direktori yang sama, lalu **Run All**.

---

## 🔬 Alur Analisis

```
Raw JSON
   │
   ▼
[1] Load & Inspect          → printSchema, count
   │
   ▼
[2] Preprocessing           → flatten nested, null handling, salary parsing
   │
   ▼
[3] Analisis Batch          → top perusahaan, lokasi, workType, kategori, salary, trend
   │
   ▼
[4] Spark SQL               → 3 query analitik menggunakan createOrReplaceTempView
   │
   ▼
[5] MLlib KMeans            → clustering job berdasarkan subCategory, workType, lokasi
   │
   ▼
[6] Structured Streaming    → simulasi realtime stream dari file JSON
   │
   ▼
[7] Output                  → CSV + Parquet
```

---

## 📈 Temuan Utama

- **80.67%** lowongan berstatus Full Time
- **Jakarta Raya** mendominasi dengan 207 lowongan (21.5% total)
- Sub-kategori terbanyak: **Developer/Programmer** (219 lowongan)
- Sub-kategori dengan rata-rata salary tertinggi: **Teknik – Perangkat Lunak**
- KMeans clustering membagi 962 lowongan ke dalam **4 cluster** berdasarkan posisi, lokasi, dan tipe kerja

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|---|---|
| Big Data Processing | Apache Spark (PySpark) |
| DataFrame API | Spark DataFrame + Spark SQL |
| Machine Learning | Spark MLlib (KMeans, StringIndexer, VectorAssembler) |
| Streaming | Spark Structured Streaming |
| Data Collection | Python `requests` + GraphQL API |
| Environment | Google Colab / Jupyter Notebook |

---

## 👤 Author

**Ozora Nathalnael Purba**  
NIM 245150207111102
