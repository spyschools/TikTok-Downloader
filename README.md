# TikTok-Downloader
Tools berbasis terminal (CLI) yang ringan dan cepat menggunakan Python untuk mengunduh video TikTok tanpa *watermark* langsung di Linux &amp; Terminal apapun

## 🚀 Fitur Utama
Unduh video TikTok
Unduh metadata video
Unduh sekitar 30 video dan/atau baris metadata dari tagar, pengguna, dan bagian "Anda Mungkin Suka" di halaman video (Anda dapat mencoba menentukan jumlah pastinya, tetapi TikTok tidak selalu mengikutinya secara tepat).
Unduh komentar video
Unduh objek data JSON TikTok lengkap (jika Anda ingin mengekstrak data dari bagian objek yang tidak termasuk dalam fungsi di atas)

## 🛠️ Prasyarat
Sebelum menggunakan, pastikan sistem Linux Anda sudah terpasang:
*Python 3.x / Node.js (Sesuaikan dengan bahasa pemrograman Anda)
*`curl` atau `wget`

*Install pyktok dulu:

$ git clone https://github.com/spyschools/TikTok-Downloader.git

$ cd TikTok-Downloader 

$ pip3 install pyktok --break-system-packages

$ pip3 install yt-dlp --break-system-packages
 
$ chmod +x tiktok_downloader.py

$ python3 tiktok_downloader.py


*Nanti akan muncul tampilan seperti ini:

=============================================
      TIKTOK DOWNLOADER - pyktok
=============================================
[INFO] Direktori kerja: /root/Downloads

=== Pilih Browser ===
  1. chrome
  2. firefox
  3. chromium
  ...

