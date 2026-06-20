<div align="center">

# 📥 TikTok Downloader

**Skrip Python berbasis terminal untuk mendownload konten TikTok**  
Video · Akun · Hashtag · Batch URL · Auto-Skip · Auto-Retry

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Powered-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![pyktok](https://img.shields.io/badge/pyktok-Powered-010101?style=for-the-badge&logo=tiktok&logoColor=white)](https://github.com/dfreelon/pyktok)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

---

## 📖 Tentang Project

**TikTok Downloader** adalah skrip Python interaktif yang berjalan di terminal untuk mendownload video dari TikTok — mulai dari 1 video, seluruh video dari sebuah akun, video berdasarkan hashtag, hingga download massal dari banyak URL sekaligus.

Dibangun di atas dua library andalan:
- **`yt-dlp`** — engine utama yang cepat dan stabil untuk download video & akun
- **`pyktok`** — untuk scraping metadata dan download video individual TikTok

> Cocok untuk pengguna **Kali Linux** yang lebih suka bekerja di terminal tanpa perlu aplikasi tambahan.

---

## ✨ Fitur Lengkap

| Fitur | Status | Keterangan |
|-------|--------|------------|
| Download 1 video dari URL | ✅ | Pilih pyktok atau yt-dlp |
| Download semua video dari akun | ✅ | Tanpa batas, tanpa login |
| Download video dari hashtag | ✅ | Tentukan jumlah video |
| Download batch (banyak URL) | ✅ | Input URL satu per satu |
| Skip video gagal otomatis | ✅ | Lanjut ke video berikutnya |
| Retry otomatis | ✅ | Hingga 5x percobaan ulang |
| Jeda antar download | ✅ | 3–7 detik, anti-blokir TikTok |
| Pilihan kualitas video | ✅ | Terbaik / 540p / 360p |
| Fallback otomatis | ✅ | pyktok gagal → yt-dlp |
| Folder terpisah per akun | ✅ | Output rapi & terorganisir |
| Deteksi library otomatis | ✅ | Tampilkan status pyktok & yt-dlp |

---

## 📦 Requirements

- Python 3.8 atau lebih baru
- `yt-dlp`
- `pyktok`

---

## ⚡ Instalasi

### 1. Clone repository

```bash
git clone https://github.com/spyschools/TikTok-Downloader.git
cd TikTok-Downloader
```

### 2. Install dependensi

```bash
pip install yt-dlp pyktok --break-system-packages
```

> **Catatan untuk Kali Linux:** Flag `--break-system-packages` diperlukan karena Kali Linux menggunakan Python managed environment. Ini aman digunakan.

### 3. Jalankan

```bash
python3 tiktok_downloader.py
```

---

## 🎯 Cara Penggunaan

Setelah dijalankan, kamu akan disambut dengan menu interaktif:

```
=============================================
      TIKTOK DOWNLOADER v2
      pyktok + yt-dlp
=============================================
[INFO] Direktori kerja : /home/user/TikTok-Downloader
[INFO] pyktok          : ✓ OK
[INFO] yt-dlp          : ✓ OK

=== Pilih Browser ===
  1. chrome
  2. firefox
  3. chromium
  4. safari
  5. edge

=== MENU UTAMA ===
  1. Download 1 video (dari URL)
  2. Download semua video dari 1 akun
  3. Download banyak video (batch URL)
  4. Download video dari hashtag
  5. Ganti browser
  0. Keluar
```

### Contoh penggunaan

**Download 1 video:**
```
Pilih menu: 1
Masukkan URL video TikTok: https://www.tiktok.com/@username/video/1234567890
Pilih metode:
  1. pyktok
  2. yt-dlp
Pilih [default: 2]: 2
```

**Download semua video dari akun:**
```
Pilih menu: 2
Masukkan username TikTok (tanpa @): bundagiora
Berapa video yang ingin didownload? [default: semua]: semua
Kualitas video? (1=terbaik/2=540p/3=360p) [default: 1]: 1
Simpan ke folder [default: bundagiora_videos]: bundagiora_videos

[INFO] Mendownload video dari @bundagiora ke folder 'bundagiora_videos'...
[INFO] Mode: skip otomatis jika ada video yang gagal, lanjut ke berikutnya

[download] Downloading item 1 of 124
[download] 100% of  6.86MiB in 00:00:05 at 1.26MiB/s ✓
[download] Downloading item 2 of 124
...
```

**Download dari hashtag:**
```
Pilih menu: 4
Masukkan hashtag (tanpa #): fyp
Berapa video yang ingin didownload? [default: 30]: 20
Simpan ke folder [default: fyp_videos]: fyp_videos
```

**Download batch:**
```
Pilih menu: 3
URL 1: https://www.tiktok.com/@user/video/111
URL 2: https://www.tiktok.com/@user/video/222
URL 3: selesai
Simpan ke folder [default: batch_videos]: batch_videos
```

---

## 📁 Struktur Output

```
TikTok-Downloader/
│
├── tiktok_downloader.py          ← skrip utama
├── README.md
│
├── bundagiora_videos/            ← hasil download akun
│   ├── bundagiora_7644552046544358664.mp4
│   ├── bundagiora_7644461079082454290.mp4
│   └── ...
│
├── fyp_videos/                   ← hasil download hashtag
│   ├── user1_7123456789.mp4
│   └── ...
│
└── batch_videos/                 ← hasil download batch
    └── ...
```

---

## 🔧 Konfigurasi Browser

pyktok memerlukan browser yang terinstall di sistem untuk mengambil cookie TikTok. Pilih browser yang kamu gunakan saat pertama kali menjalankan skrip:

```
=== Pilih Browser ===
  1. chrome      ← Google Chrome
  2. firefox     ← Mozilla Firefox
  3. chromium    ← Chromium
  4. safari      ← Safari (macOS)
  5. edge        ← Microsoft Edge
```

> **Tips:** Pastikan kamu pernah membuka TikTok di browser tersebut sebelumnya agar cookie tersedia.

---

## ⚠️ Troubleshooting

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `ModuleNotFoundError: pyktok` | Library belum terinstall | `pip install pyktok --break-system-packages` |
| `ModuleNotFoundError: yt_dlp` | Library belum terinstall | `pip install yt-dlp --break-system-packages` |
| `Unexpected response from webpage` | TikTok throttle request | Normal — skrip otomatis skip & lanjut |
| `Connection closed while reading from driver` | Konflik Playwright + Node.js | Gunakan menu 2 (sudah pakai yt-dlp, bukan Playwright) |
| `module 'pyktok' has no attribute '...'` | Versi pyktok lama | `pip install --upgrade pyktok --break-system-packages` |
| Video tidak bisa didownload | Akun privat / video dihapus | Tidak bisa didownload, skrip otomatis skip |
| Kecepatan download lambat | Koneksi internet / throttle | Normal, tunggu atau coba ulang nanti |

---

## 🛠️ Library yang Digunakan

| Library | Versi | Fungsi |
|---------|-------|--------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | latest | Download video, akun, hashtag (engine utama) |
| [pyktok](https://github.com/dfreelon/pyktok) | latest | Scraping metadata & download video individual |

---

## 📋 Disclaimer

- Tool ini dibuat untuk tujuan **edukasi** dan **pengarsipan konten pribadi** semata
- Gunakan hanya untuk mengarsipkan konten yang **kamu miliki sendiri** atau yang **sudah mendapat izin** dari pemiliknya
- Menghormati **hak cipta** dan **Terms of Service** TikTok adalah tanggung jawab pengguna
- Developer **tidak bertanggung jawab** atas penyalahgunaan tool ini

---

## 📄 License

Didistribusikan di bawah lisensi **MIT**. Lihat file [`LICENSE`](LICENSE) untuk detail lengkapnya.

---

## 👤 Author

<div align="center">

**spyschools**

[![GitHub](https://img.shields.io/badge/GitHub-spyschools-181717?style=for-the-badge&logo=github)](https://github.com/spyschools)

---

*Dibuat dengan ❤️ untuk komunitas Linux Indonesia*

⭐ **Jangan lupa kasih star kalau bermanfaat!** ⭐

</div>
