# 📥 Social Media Downloader

> Skrip Python berbasis terminal untuk mendownload konten dari **TikTok** dan **Instagram** — ringan, cepat, dan cocok untuk pengguna Kali Linux.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-orange?style=flat-square)
![instaloader](https://img.shields.io/badge/Powered%20by-instaloader-purple?style=flat-square)

---

## ✨ Tentang Project

Kumpulan skrip Python interaktif untuk mendownload konten media sosial langsung dari terminal tanpa perlu GUI. Dibangun di atas library terpercaya seperti `yt-dlp`, `pyktok`, dan `instaloader` dengan menu yang mudah digunakan bahkan untuk pemula.

---

## 🚀 Fitur

### 📱 TikTok Downloader (`tiktok_downloader.py`)
- ✅ Download 1 video dari URL
- ✅ Download **semua video** dari sebuah akun
- ✅ Download video dari **hashtag**
- ✅ Download **batch** (banyak URL sekaligus)
- ✅ Skip otomatis jika ada video yang gagal (lanjut ke berikutnya)
- ✅ Jeda otomatis antar download agar tidak diblokir TikTok
- ✅ Pilihan kualitas video (terbaik / 540p / 360p)
- ✅ Retry otomatis hingga 5x jika koneksi gagal
- ✅ Video tersimpan ke folder terpisah per akun/hashtag

### 📸 Instagram Downloader (`instagram_downloader.py`)
- ✅ Download 1 post/reel dari URL
- ✅ Download **semua post** dari sebuah akun
- ✅ Download **Stories** (butuh login)
- ✅ Download **Highlights** (butuh login)
- ✅ Download post dari **hashtag**
- ✅ Download **batch** (banyak URL sekaligus)
- ✅ Login dengan sesi tersimpan (tidak perlu login ulang)
- ✅ Support **2FA** (Two-Factor Authentication)
- ✅ Fallback otomatis: jika instaloader gagal → coba yt-dlp
- ✅ Download foto, video, carousel/album sekaligus

---

## 📦 Requirements

```
Python 3.8+
yt-dlp
pyktok
instaloader
```

---

## ⚡ Instalasi

**1. Clone repository:**
```bash
git clone https://github.com/spyschools/social-media-downloader.git
cd social-media-downloader
```

**2. Install semua dependensi:**
```bash
pip install yt-dlp pyktok instaloader --break-system-packages
```

> **Catatan:** Flag `--break-system-packages` diperlukan di Kali Linux / Debian-based yang menggunakan Python managed environment.

---

## 🎯 Cara Penggunaan

### TikTok Downloader
```bash
python3 tiktok_downloader.py
```

```
=============================================
      TIKTOK DOWNLOADER v2
      pyktok + yt-dlp
=============================================

=== MENU UTAMA ===
  1. Download 1 video (dari URL)
  2. Download semua video dari 1 akun
  3. Download banyak video (batch URL)
  4. Download video dari hashtag
  5. Ganti browser
  0. Keluar
```

### Instagram Downloader
```bash
python3 instagram_downloader.py
```

```
=============================================
      INSTAGRAM DOWNLOADER v1
      instaloader + yt-dlp
=============================================

=== MENU UTAMA ===
  1. Download 1 post/reel (dari URL)
  2. Download semua post dari 1 akun
  3. Download Stories akun  [butuh login]
  4. Download Highlights    [butuh login]
  5. Download dari Hashtag
  6. Download banyak post (batch URL)
  7. Login / Ganti akun
  0. Keluar
```

---

## 📁 Struktur File Output

```
social-media-downloader/
│
├── tiktok_downloader.py
├── instagram_downloader.py
├── README.md
│
├── bundagiora_videos/          ← hasil download akun TikTok
│   ├── bundagiora_7644552046544358664.mp4
│   └── ...
│
├── username_posts/             ← hasil download akun Instagram
│   ├── 2024-01-01_UTC.jpg
│   ├── 2024-01-01_UTC.mp4
│   └── ...
│
└── batch_videos/               ← hasil download batch
    └── ...
```

---

## ⚠️ Troubleshooting

| Error | Solusi |
|-------|--------|
| `ModuleNotFoundError` | Jalankan `pip install <nama_module> --break-system-packages` |
| `Unexpected response from webpage` | Normal — skrip otomatis skip dan lanjut ke video berikutnya |
| `Connection closed while reading from driver` | Error Playwright, gunakan menu download akun (sudah pakai yt-dlp) |
| Login Instagram gagal | Coba lagi, atau periksa koneksi internet |
| Video TikTok tidak bisa didownload | Pastikan URL valid dan akun tidak privat |

---

## 🛠️ Library yang Digunakan

| Library | Fungsi |
|---------|--------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download video TikTok & Instagram Reels |
| [pyktok](https://github.com/dfreelon/pyktok) | Scraping metadata & video TikTok |
| [instaloader](https://github.com/instaloader/instaloader) | Download konten Instagram lengkap |

---

## 📋 Catatan Penting

- Gunakan tool ini hanya untuk konten yang **kamu miliki** atau yang **diizinkan untuk didownload**
- Menghormati **Terms of Service** platform masing-masing adalah tanggung jawab pengguna
- Tool ini dibuat untuk tujuan **edukasi dan pengarsipan pribadi**
- Jangan gunakan untuk tujuan **komersial** atau **melanggar hak cipta**

---

## 📄 License

Didistribusikan di bawah lisensi **MIT**. Lihat file `LICENSE` untuk informasi lebih lanjut.

---

## 👤 Author

**spyschools**  
🐙 GitHub: [@spyschools](https://github.com/spyschools)

---

<div align="center">
  <sub>Dibuat dengan ❤️ untuk komunitas Kali Linux Indonesia</sub>
</div>
