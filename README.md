<div align="center">

# 📥 TikTok Downloader v2

**Download video, foto, slideshow foto, audio, akun, hashtag & batch dari terminal**  
Video Besar · Foto · Slideshow · MP3 · Resume · Anti-Duplikat · Auto-Retry

By        : Spy Schools (Fariz Azhari)
Instagram : https://instagram.com/frzazhri
LinkedIn  : https://linkedin.com/in/farizazhari

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-557C94?style=for-the-badge&logo=linux&logoColor=white)](https://kali.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Powered-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

---

## 📖 Tentang Project

**TikTok Downloader** adalah skrip Python untuk terminal yang bisa mendownload hampir semua jenis konten TikTok. Jenis konten **dideteksi otomatis** (video, foto, atau slideshow), jadi kamu cukup menempel URL-nya.

- **`yt-dlp`**: engine utama untuk video (stabil, mendukung file besar)
- **`requests`**: mengambil foto & slideshow langsung dari data halaman TikTok
- **`pyktok`** *(opsional)*: fallback & metadata
- **`gallery-dl`** *(opsional)*: fallback untuk foto/slideshow di profil

---

## ✨ Fitur

| Fitur | Keterangan |
|-------|------------|
| 🎬 Video ukuran besar | Resume file `.part`, retry 10x, download per-chunk 10MB, timeout aman |
| 🖼️ Foto & slideshow | Semua gambar disimpan berurutan (`01`, `02`, ...) dalam satu folder per post |
| 🎵 Musik slideshow | Opsional, simpan audio dari slide foto |
| 🎧 Audio saja (MP3) | Butuh `ffmpeg` |
| 🔗 Short link | `vm.tiktok.com`, `vt.tiktok.com`, `/t/` otomatis di-resolve |
| 👤 Akun & #hashtag | Dengan batas jumlah, folder otomatis per akun |
| 📋 Batch | Ketik manual atau baca dari file `.txt` |
| 🍪 Cookie | Dari browser (chrome, firefox, edge, brave, dll.) atau `cookies.txt` |
| 🗂️ Anti-duplikat | `archive.txt` mencatat ID yang sudah diunduh, jadi aman dijalankan ulang |
| 📝 Log gagal | `failed.txt` berisi URL yang gagal beserta alasannya |
| ⏱️ Jeda acak | 2–5 detik antar download, mengurangi risiko throttle |
| 💻 Mode CLI | Bisa dipakai di script/cron selain menu interaktif |
| 🎚️ Kualitas | best / 1080 / 720 / 540 / 360 |
| 🔁 Fallback berlapis | yt-dlp → foto/slideshow → pyktok → gallery-dl |

---

## ⚡ Instalasi

```bash
git clone https://github.com/spyschools/TikTok-Downloader.git
cd TikTok-Downloader

pip3 install --upgrade pip --break-system-packages
pip3 install -r requirements.txt --break-system-packages
sudo apt update && sudo apt install ffmpeg        # disarankan: merge video HD & ekstrak MP3
```

Opsional:
```bash
pip3 install pyktok gallery-dl --break-system-packages
```

> `--break-system-packages` hanya diperlukan di distro seperti Kali/Debian terbaru. Alternatifnya pakai `python3 -m venv venv`.

---

## 🎯 Cara Penggunaan

### Mode interaktif

```bash
python3 tiktok_downloader.py
```

```
=== MENU UTAMA ===
  1. Download 1 URL (video / foto / slideshow otomatis)
  2. Download semua konten dari akun
  3. Download banyak URL (ketik manual atau dari file .txt)
  4. Download dari hashtag
  5. Pengaturan (kualitas, audio, cookie, folder)
  0. Keluar
```

### Mode CLI

```bash
# 1 URL (video / foto / slideshow, otomatis)
python3 tiktok_downloader.py https://www.tiktok.com/@user/photo/1234567890

# Beberapa URL + short link
python3 tiktok_downloader.py https://vm.tiktok.com/xxxx/ https://www.tiktok.com/@u/video/111

# Dari file
python3 tiktok_downloader.py -f daftar_url.txt -o hasil

# Semua konten akun, maksimal 50, kualitas 1080p
python3 tiktok_downloader.py -u username -n 50 -q 1080

# Hashtag
python3 tiktok_downloader.py -t fyp -n 20

# Audio MP3 saja
python3 tiktok_downloader.py -a https://www.tiktok.com/@user/video/111

# Dengan cookie browser + metadata + musik slideshow
python3 tiktok_downloader.py --browser firefox --meta --music URL
```

| Opsi | Fungsi |
|------|--------|
| `-o` | Folder output (default `downloads`) |
| `-q` | `best` `1080` `720` `540` `360` |
| `-a` | Audio saja (MP3) |
| `-u` / `-t` | Akun / hashtag |
| `-n` | Batas jumlah konten |
| `-f` | File `.txt` berisi URL |
| `--meta` | Simpan info JSON, caption, thumbnail |
| `--music` | Simpan musik slideshow |
| `--browser` | Ambil cookie dari browser |
| `--cookies` | Pakai file `cookies.txt` |

---

## 📁 Struktur Output

```
downloads/
├── archive.txt                    ← ID yang sudah diunduh (anti-duplikat)
├── failed.txt                     ← URL yang gagal + alasan
├── username_7644552046544358664.mp4        ← video
├── username_7644461079082454290/           ← slideshow foto
│   ├── 01.jpg
│   ├── 02.jpg
│   ├── 03.jpg
│   ├── musik.mp3                  (jika --music)
│   ├── caption.txt                (jika --meta)
│   └── info.json                  (jika --meta)
└── username/                      ← hasil mode akun (-u)
```

---

## 💡 Tips Video Besar

- Install **ffmpeg** agar video HD (video + audio terpisah) bisa digabung.
- Download terputus? Jalankan lagi perintah yang sama. File `.part` dilanjutkan dan yang sudah selesai dilewati.
- Pastikan ruang disk cukup, karena video panjang bisa berukuran ratusan MB.
- Kena throttle? Tambah jeda dengan mengubah `sleep_min` / `sleep_max` di `default_cfg()`.

## 🍪 Kapan Perlu Cookie?

Konten yang butuh login: akun privat yang kamu ikuti, video dibatasi umur/wilayah, atau saat TikTok memblokir request anonim. Login ke TikTok di browser, lalu pilih browser tersebut di **Pengaturan** atau pakai `--browser`.

---

## ⚠️ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError` | `pip install -r requirements.txt --break-system-packages` |
| Foto/slideshow gagal | Pakai `--browser` (cookie), pastikan `requests` terinstall |
| `Data halaman tidak ditemukan` | Throttle: tunggu beberapa menit atau pakai cookie |
| Daftar akun/hashtag kosong | Pakai cookie, `pip install -U yt-dlp`, atau install `gallery-dl` |
| Video HD tidak tergabung / MP3 gagal | Install `ffmpeg` |
| Banyak video gagal | Update: `pip install -U yt-dlp --break-system-packages` (TikTok sering berubah) |
| Akun privat / video dihapus | Tidak bisa diunduh, masuk ke `failed.txt` |

> **Catatan:** TikTok sering mengubah sistemnya. Jika tiba-tiba error semua, update `yt-dlp` dulu.

---

## 📋 Disclaimer

- Dibuat untuk tujuan **edukasi** dan **pengarsipan konten pribadi**
- Gunakan hanya untuk konten **milikmu sendiri** atau yang sudah **mendapat izin** pemiliknya
- Menghormati **hak cipta** dan **Terms of Service** TikTok adalah tanggung jawab pengguna
- Developer **tidak bertanggung jawab** atas penyalahgunaan tool ini

---

## 📄 License

MIT. Lihat file [`LICENSE`](LICENSE).

---

<div align="center">

**spyschools** · [GitHub](https://github.com/spyschools)

*Dibuat dengan ❤️ untuk komunitas Linux Indonesia*

⭐ **Jangan lupa kasih star kalau bermanfaat!** ⭐

</div>
