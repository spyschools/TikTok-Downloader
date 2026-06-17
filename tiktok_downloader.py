#!/usr/bin/env python3
"""
TikTok Downloader - pyktok
Jalankan: python3 tiktok_downloader.py
"""

import sys
import os

# Cek pyktok terinstall
try:
    import pyktok as pyk
except ImportError:
    print("[ERROR] pyktok belum terinstall.")
    print("Jalankan: pip install pyktok --break-system-packages")
    sys.exit(1)


def set_browser():
    browsers = ['chrome', 'firefox', 'chromium', 'safari', 'edge']
    print("\n=== Pilih Browser ===")
    for i, b in enumerate(browsers, 1):
        print(f"  {i}. {b}")
    pilihan = input("\nMasukkan nomor browser [default: 1=chrome]: ").strip()
    if pilihan == "" or not pilihan.isdigit():
        browser = 'chrome'
    else:
        idx = int(pilihan) - 1
        browser = browsers[idx] if 0 <= idx < len(browsers) else 'chrome'
    print(f"[INFO] Menggunakan browser: {browser}")
    pyk.specify_browser(browser)
    return browser


def download_video():
    url = input("\nMasukkan URL video TikTok: ").strip()
    if not url.startswith("https://"):
        print("[ERROR] URL tidak valid. Harus diawali https://")
        return

    simpan_metadata = input("Simpan metadata ke CSV? (y/n) [default: n]: ").strip().lower()
    metadata_file = None
    if simpan_metadata == 'y':
        metadata_file = input("Nama file metadata [default: metadata.csv]: ").strip()
        if not metadata_file:
            metadata_file = "metadata.csv"

    print(f"\n[INFO] Mendownload video...")
    try:
        if metadata_file:
            pyk.save_tiktok(url, True, metadata_file)
        else:
            pyk.save_tiktok(url, True)
        print("[SUKSES] Video berhasil didownload!")
    except Exception as e:
        print(f"[ERROR] Gagal download: {e}")


def download_user():
    username = input("\nMasukkan username TikTok (tanpa @): ").strip().lstrip('@')
    if not username:
        print("[ERROR] Username tidak boleh kosong.")
        return

    simpan_metadata = input("Simpan metadata ke CSV? (y/n) [default: y]: ").strip().lower()
    metadata_file = "metadata.csv"
    if simpan_metadata == 'n':
        metadata_file = None

    if metadata_file:
        nama = input(f"Nama file metadata [default: {metadata_file}]: ").strip()
        if nama:
            metadata_file = nama

    print(f"\n[INFO] Mendownload semua video dari @{username}...")
    try:
        if metadata_file:
            pyk.save_tiktok_user(username, True, metadata_file)
        else:
            pyk.save_tiktok_user(username, True)
        print("[SUKSES] Semua video berhasil didownload!")
    except Exception as e:
        print(f"[ERROR] Gagal download: {e}")


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

    metadata_file = "metadata_batch.csv"
    print(f"\n[INFO] Mendownload {len(urls)} video...")
    sukses = 0
    for i, url in enumerate(urls, 1):
        print(f"  [{i}/{len(urls)}] {url}")
        try:
            pyk.save_tiktok(url, True, metadata_file)
            print(f"  [OK] Berhasil")
            sukses += 1
        except Exception as e:
            print(f"  [GAGAL] {e}")

    print(f"\n[SELESAI] {sukses}/{len(urls)} video berhasil didownload.")


def main():
    print("=" * 45)
    print("      TIKTOK DOWNLOADER - pyktok")
    print("=" * 45)
    print(f"[INFO] Direktori kerja: {os.getcwd()}")

    # Pilih browser
    set_browser()

    while True:
        print("\n=== MENU UTAMA ===")
        print("  1. Download 1 video (dari URL)")
        print("  2. Download semua video dari 1 akun")
        print("  3. Download banyak video (batch URL)")
        print("  4. Ganti browser")
        print("  0. Keluar")

        pilihan = input("\nPilih menu: ").strip()

        if pilihan == '1':
            download_video()
        elif pilihan == '2':
            download_user()
        elif pilihan == '3':
            download_batch()
        elif pilihan == '4':
            set_browser()
        elif pilihan == '0':
            print("\n[INFO] Keluar. Sampai jumpa!")
            sys.exit(0)
        else:
            print("[WARNING] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
