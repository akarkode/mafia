
# MAFIA - Middleware AI Firewall Application

**MAFIA** adalah middleware Python yang berfungsi untuk mendeteksi dan mencegah serangan brute force serta memblokir payload berbahaya (XSS, SQL Injection, dan sejenisnya). Middleware ini cocok diintegrasikan pada aplikasi berbasis FastAPI atau Starlette.

---

## 🔧 Instalasi

```bash
pip install git+https://github.com/akarkode/mafia.git
```

---

## 🚀 Cara Menggunakan

Tambahkan middleware pada aplikasi FastAPI kamu:
```python
from mafia.middleware import BruteForceMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")
```

Middleware akan secara otomatis:
- Mendeteksi dan memblokir permintaan mencurigakan dari IP yang sama.
- Menjalankan klasifikasi AI untuk percobaan brute-force.
- Memblokir request yang mengandung payload berbahaya.

---

## 🛡️ Fitur Keamanan

### 1. Deteksi Brute Force
Model AI `BruteForceDetector` menganalisis pola login mencurigakan berdasarkan fitur seperti frekuensi dan interval permintaan.

### 2. Filter Payload Berbahaya
`SecurityFilter` menyaring:
- Serangan XSS: `<script>`, `onerror=`, `javascript:`
- SQL Injection: `' OR 1=1`, `UNION SELECT`, `--`, dll

### 3. Rate Limiting
`RedisClient` digunakan untuk membatasi jumlah permintaan berdasarkan alamat IP.

---

## 🧠 Struktur Internal

```text
[Client] → [BruteForceMiddleware]
   ├─ [RedisClient] - rate limiting
   ├─ [BruteForceDetector] - klasifikasi brute force
   └─ [SecurityFilter] - blokir XSS/SQLi
```

### Kelas dan Fungsi Penting
- `BruteForceMiddleware`
  - `dispatch()`: Middleware utama
- `BruteForceDetector`
  - `predict(features: list) -> bool`
  - `train()`, `save_model()`
- `SecurityFilter`
  - `is_malicious(payload: str) -> bool`

---

## 📈 Rencana Pengembangan

- Visualisasi log secara real-time.
- Integrasi ElasticSearch untuk pencatatan keamanan.
- Dukungan klasifikasi AI berbasis LSTM.
- Otomatisasi pelatihan model periodik.

---

## 📄 Lisensi dan Kontribusi

Silakan buka `LICENSE` untuk informasi lisensi. Pull request, issue, dan kontribusi sangat disambut.

---

> Dokumentasi ini disusun menggunakan MkDocs Material dalam satu halaman untuk kesederhanaan dan kecepatan akses.
