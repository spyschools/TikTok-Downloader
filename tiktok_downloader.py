#!/usr/bin/env python3
"""
TikTok Downloader - pyktok + yt-dlp
Jalankan: python3 tiktok_downloader.py
"""

import sys
import os
import subprocess

# Cek pyktok
try:
    import pyktok as pyk
    PYKTOK_OK = True
except ImportError:
    PYKTOK_OK = False
    print("[WARNING] pyktok tidak terinstall. Install: pip install pyktok --break-system-packages")

# Cek yt-dlp
try:
    import yt_dlp
    YTDLP_OK = True
except ImportError:
    YTDLP_OK = False
    print("[WARNING] yt-dlp tidak terinstall. Install: pip install yt-dlp --break-system-packages")

if not PYKTOK_OK and not YTDLP_OK:
    print("[ERROR] Tidak ada library yang terinstall. Keluar.")
    sys.exit(1)

BROWSER = 'chrome'


def set_browser():
    global BROWSER
    browsers = ['chrome', 'firefox', 'chromium', 'safari', 'edge']
    print("\n=== Pilih Browser ===")
    for i, b in enumerate(browsers, 1):
        print(f"  {i}. {b}")
    pilihan = input("\nMasukkan nomor browser [default: 1=chrome]: ").strip()
    if pilihan == "" or not pilihan.isdigit():
        BROWSER = 'chrome'
    else:
        idx = int(pilihan) - 1
        BROWSER = browsers[idx] if 0 <= idx < len(browsers) else 'chrome'
    print(f"[INFO] Menggunakan browser: {BROWSER}")
    if PYKTOK_OK:
        pyk.specify_browser(BROWSER)


# ── DOWNLOAD 1 VIDEO ──────────────────────────────────────────────
def download_video():
    url = input("\nMasukkan URL video TikTok: ").strip()
    if not url.startswith("https://"):
        print("[ERROR] URL tidak valid. Harus diawali https://")
        return

    print("\nPilih metode:")
    print("  1. pyktok (lebih akurat, butuh cookie browser)")
    print("  2. yt-dlp  (lebih stabil, tidak butuh login)")
    metode = input("Pilih [default: 2]: ").strip()

    if metode == '1' and PYKTOK_OK:
        _download_video_pyktok(url)
    else:
        _download_video_ytdlp(url)


def _download_video_pyktok(url):
    simpan_metadata = input("Simpan metadata ke CSV? (y/n) [default: n]: ").strip().lower()
    metadata_file = ""
    if simpan_metadata == 'y':
        metadata_file = input("Nama file metadata [default: metadata.csv]: ").strip() or "metadata.csv"
    print(f"\n[INFO] Mendownload video dengan pyktok...")
    try:
        pyk.save_tiktok(url, save_video=True, metadata_fn=metadata_file, browser_name=BROWSER)
        print("[SUKSES] Video berhasil didownload!")
    except Exception as e:
        print(f"[ERROR] pyktok gagal: {e}")
        print("[INFO] Mencoba dengan yt-dlp...")
        _download_video_ytdlp(url)


def _download_video_ytdlp(url, output_dir=None):
    if not YTDLP_OK:
        print("[ERROR] yt-dlp tidak terinstall.")
        return
    folder = output_dir or os.getcwd()
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(uploader)s_%(id)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'retries': 5,
        'fragment_retries': 5,
        'sleep_interval': 2,
    }
    print(f"[INFO] Mendownload dengan yt-dlp...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[SUKSES] Video berhasil didownload!")
    except Exception as e:
        print(f"[ERROR] yt-dlp gagal: {e}")


# ── DOWNLOAD AKUN ─────────────────────────────────────────────────
def download_user():
    username = input("\nMasukkan username TikTok (tanpa @): ").strip().lstrip('@')
    if not username:
        print("[ERROR] Username tidak boleh kosong.")
        return

    jumlah = input("Berapa video yang ingin didownload? [default: semua]: ").strip()
    folder = input(f"Simpan ke folder [default: {username}_videos]: ").strip() or f"{username}_videos"
    os.makedirs(folder, exist_ok=True)

    print(f"\n[INFO] Mendownload video dari @{username} ke folder '{folder}'...")
    print("[INFO] Menggunakan yt-dlp (lebih stabil untuk download akun)...\n")

    if not YTDLP_OK:
        print("[ERROR] yt-dlp tidak terinstall. Jalankan: pip install yt-dlp --break-system-packages")
        return

    kualitas = input("Kualitas video? (1=terbaik/2=540p/3=360p) [default: 1]: ").strip()
    format_map = {'2': 'h264_540p', '3': 'h264_360p'}
    format_str = format_map.get(kualitas, 'bestvideo+bestaudio/best')

    url_akun = f"https://www.tiktok.com/@{username}"
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(uploader)s_%(id)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,        # skip video gagal, lanjut ke berikutnya
        'sleep_interval': 3,         # jeda 3 detik antar video
        'max_sleep_interval': 6,     # jeda maksimal 6 detik (random)
        'retries': 5,                # coba ulang 5x jika gagal
        'fragment_retries': 5,
        'format': format_str,
        'concurrent_fragment_downloads': 1,
    }
    if jumlah.isdigit():
        ydl_opts['playlistend'] = int(jumlah)

    print("[INFO] Mode: skip otomatis jika ada video yang gagal, lanjut ke berikutnya\n")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_akun])
        print(f"\n[SUKSES] Download selesai! Video tersimpan di folder: {folder}")
    except Exception as e:
        print(f"[ERROR] Gagal download akun: {e}")


# ── DOWNLOAD BATCH URL ────────────────────────────────────────────
def download_batch():
    print("\nMasukkan URL video satu per baris.")
    print("Ketik 'selesai' jika sudah.\n")
    urls = []
    while True:
        url = input(f"URL {len(urls)+1}: ").strip()
        if url.lower() == 'selesai':
            break
        if url.startswith("https://"):
            urls.append(url)
        elif url:
            print("[WARNING] URL tidak valid, dilewati.")

    if not urls:
        print("[INFO] Tidak ada URL yang dimasukkan.")
        return

    folder = input(f"Simpan ke folder [default: batch_videos]: ").strip() or "batch_videos"
    os.makedirs(folder, exist_ok=True)

    print(f"\n[INFO] Mendownload {len(urls)} video...\n")
    sukses = 0
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        try:
            if YTDLP_OK:
                ydl_opts = {
                    'outtmpl': os.path.join(folder, '%(uploader)s_%(id)s.%(ext)s'),
                    'quiet': True,
                    'retries': 5,
                    'fragment_retries': 5,
                    'sleep_interval': 2,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            elif PYKTOK_OK:
                pyk.save_tiktok(url, save_video=True, browser_name=BROWSER)
            print(f"  [OK] Berhasil")
            sukses += 1
        except Exception as e:
            print(f"  [GAGAL] {e}")

    print(f"\n[SELESAI] {sukses}/{len(urls)} video berhasil didownload. Folder: {folder}")


# ── DOWNLOAD HASHTAG ──────────────────────────────────────────────
def download_hashtag():
    hashtag = input("\nMasukkan hashtag (tanpa #): ").strip().lstrip('#')
    if not hashtag:
        print("[ERROR] Hashtag tidak boleh kosong.")
        return

    jumlah = input("Berapa video yang ingin didownload? [default: 30]: ").strip()
    folder = input(f"Simpan ke folder [default: {hashtag}_videos]: ").strip() or f"{hashtag}_videos"
    os.makedirs(folder, exist_ok=True)

    if not YTDLP_OK:
        print("[ERROR] yt-dlp tidak terinstall.")
        return

    url_hashtag = f"https://www.tiktok.com/tag/{hashtag}"
    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(uploader)s_%(id)s.%(ext)s'),
        'quiet': False,
        'ignoreerrors': True,
        'sleep_interval': 3,
        'max_sleep_interval': 6,
        'retries': 5,
        'fragment_retries': 5,
    }
    if jumlah.isdigit():
        ydl_opts['playlistend'] = int(jumlah)

    print(f"\n[INFO] Mendownload video dari #{hashtag}...\n")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_hashtag])
        print(f"\n[SUKSES] Selesai! Video tersimpan di: {folder}")
    except Exception as e:
        print(f"[ERROR] Gagal: {e}")


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    print("=" * 45)
    print("      TIKTOK DOWNLOADER v2")
    print("      pyktok + yt-dlp")
    print("=" * 45)
    print(f"[INFO] Direktori kerja : {os.getcwd()}")
    print(f"[INFO] pyktok          : {'✓ OK' if PYKTOK_OK else '✗ Tidak terinstall'}")
    print(f"[INFO] yt-dlp          : {'✓ OK' if YTDLP_OK else '✗ Tidak terinstall'}")

    if PYKTOK_OK:
        set_browser()
    else:
        print("\n[INFO] Melanjutkan tanpa pyktok (hanya yt-dlp)")

    while True:
        print("\n=== MENU UTAMA ===")
        print("  1. Download 1 video (dari URL)")
        print("  2. Download semua video dari 1 akun")
        print("  3. Download banyak video (batch URL)")
        print("  4. Download video dari hashtag")
        if PYKTOK_OK:
            print("  5. Ganti browser")
        print("  0. Keluar")

        pilihan = input("\nPilih menu: ").strip()

        if pilihan == '1':
            download_video()
        elif pilihan == '2':
            download_user()
        elif pilihan == '3':
            download_batch()
        elif pilihan == '4':
            download_hashtag()
        elif pilihan == '5' and PYKTOK_OK:
            set_browser()
        elif pilihan == '0':
            print("\n[INFO] Keluar. Sampai jumpa!")
            sys.exit(0)
        else:
            print("[WARNING] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
