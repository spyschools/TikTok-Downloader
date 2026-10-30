#!/usr/bin/env python3
"""
TikTok Downloader v3 - yt-dlp + requests (+ pyktok / gallery-dl opsional)

Fitur:
  - Video (termasuk file besar: resume, retry, download per-chunk)
  - Foto & slideshow foto (otomatis terdeteksi, + musik slide opsional)
  - Audio saja (MP3), short link (vm.tiktok.com / vt.tiktok.com)
  - Akun, hashtag, batch URL / file .txt
  - Cookie dari browser atau cookies.txt (untuk konten yang butuh login)
  - Arsip anti-duplikat, log gagal, jeda acak anti-blokir

Mode interaktif : python3 tiktok_downloader.py
Mode CLI        : python3 tiktok_downloader.py -h
"""

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from types import SimpleNamespace

try:
    import yt_dlp
    YTDLP_OK = True
except ImportError:
    YTDLP_OK = False

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    import pyktok as pyk
    PYKTOK_OK = True
except ImportError:
    PYKTOK_OK = False

FFMPEG_OK = shutil.which("ffmpeg") is not None
GALLERYDL_OK = shutil.which("gallery-dl") is not None

BROWSERS = ["chrome", "firefox", "chromium", "edge", "brave", "opera", "vivaldi", "safari"]
QUALITY = {
    "best": "bv*+ba/b",
    "1080": "bv*[height<=1080]+ba/b[height<=1080]/b",
    "720": "bv*[height<=720]+ba/b[height<=720]/b",
    "540": "bv*[height<=540]+ba/b[height<=540]/b",
    "360": "bv*[height<=360]+ba/b[height<=360]/b",
}
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
ID_RE = re.compile(r"/(?:video|photo)/(\d+)")


# ───────────────────────── Util ─────────────────────────
def default_cfg():
    return SimpleNamespace(
        folder="downloads",
        quality="best",
        audio_only=False,
        meta=False,            # simpan info .json + caption
        music=False,           # simpan musik slideshow foto
        browser=None,          # ambil cookie dari browser
        cookie_file=None,      # atau cookies.txt (format Netscape)
        sleep_min=2.0,
        sleep_max=5.0,
        session=None,
    )


def log(tag, msg):
    print(f"[{tag}] {msg}")


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def extract_id(url):
    m = ID_RE.search(url)
    return m.group(1) if m else None


def load_archive(folder):
    path = os.path.join(folder, "archive.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return {l.strip() for l in f if l.strip()}
    return set()


def add_archive(folder, vid):
    with open(os.path.join(folder, "archive.txt"), "a", encoding="utf-8") as f:
        f.write(vid + "\n")


def add_failed(folder, url, err):
    with open(os.path.join(folder, "failed.txt"), "a", encoding="utf-8") as f:
        f.write(f"{url}\t{str(err)[:150]}\n")


def make_session(cfg):
    """Session requests (untuk foto/slideshow) dengan cookie opsional."""
    if not REQUESTS_OK:
        return None
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Referer": "https://www.tiktok.com/",
                      "Accept-Language": "en-US,en;q=0.9"})
    try:
        if cfg.cookie_file and os.path.exists(cfg.cookie_file):
            from http.cookiejar import MozillaCookieJar
            jar = MozillaCookieJar(cfg.cookie_file)
            jar.load(ignore_discard=True, ignore_expires=True)
            s.cookies.update(jar)
        elif cfg.browser and YTDLP_OK:
            from yt_dlp.cookies import extract_cookies_from_browser
            s.cookies.update(extract_cookies_from_browser(cfg.browser))
    except Exception as e:
        log("WARNING", f"Cookie gagal dimuat: {e}")
    return s


def resolve_url(url, session):
    """Ikuti short link (vm.tiktok.com, vt.tiktok.com, /t/) ke URL asli."""
    if not session:
        return url
    if re.search(r"//(vm|vt)\.tiktok\.com|tiktok\.com/t/", url):
        try:
            r = session.get(url, allow_redirects=True, timeout=20)
            return r.url.split("?")[0]
        except Exception as e:
            log("WARNING", f"Gagal resolve short link: {e}")
    return url


def sleep_random(cfg):
    time.sleep(random.uniform(cfg.sleep_min, cfg.sleep_max))


# ───────────────────── Foto / Slideshow ─────────────────────
def fetch_item(url, session):
    r = session.get(url, timeout=30)
    r.raise_for_status()
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
                  r.text, re.S)
    if not m:
        raise RuntimeError("Data halaman tidak ditemukan (kena throttle / butuh cookie)")
    scope = json.loads(m.group(1)).get("__DEFAULT_SCOPE__", {})
    item = scope.get("webapp.video-detail", {}).get("itemInfo", {}).get("itemStruct")
    if not item:
        raise RuntimeError("Post tidak ditemukan / privat / dihapus")
    return item


def save_stream(session, urls, dest_base, retries=4):
    """Download file dari daftar URL alternatif. Ekstensi ditentukan dari Content-Type."""
    ext_map = {"image/jpeg": ".jpg", "image/webp": ".webp", "image/png": ".png",
               "image/heic": ".heic", "audio/mpeg": ".mp3", "audio/mp4": ".m4a",
               "video/mp4": ".mp4"}
    last = None
    for u in urls:
        for attempt in range(retries):
            try:
                with session.get(u, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    ctype = r.headers.get("Content-Type", "").split(";")[0].strip()
                    path = dest_base + ext_map.get(ctype, ".jpg")
                    tmp = path + ".part"
                    with open(tmp, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024 * 256):
                            f.write(chunk)
                    os.replace(tmp, path)
                    return path
            except Exception as e:
                last = e
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Gagal download file: {last}")


def download_photo_post(url, cfg):
    if not cfg.session:
        raise RuntimeError("Library 'requests' belum terinstall (pip install requests)")
    item = fetch_item(url, cfg.session)
    images = (item.get("imagePost") or {}).get("images") or []
    if not images:
        raise RuntimeError("Post ini bukan foto/slideshow")

    author = item.get("author")
    author = author.get("uniqueId") if isinstance(author, dict) else (author or "unknown")
    post_id = item.get("id") or extract_id(url) or "post"
    post_dir = os.path.join(cfg.folder, f"{author}_{post_id}")
    os.makedirs(post_dir, exist_ok=True)

    log("INFO", f"Slideshow foto: {len(images)} gambar -> {post_dir}")
    for i, img in enumerate(images, 1):
        urls = (img.get("imageURL") or {}).get("urlList") or []
        if not urls:
            continue
        existing = [f for f in os.listdir(post_dir) if f.startswith(f"{i:02d}.")
                    and not f.endswith(".part")]
        if existing:
            continue
        path = save_stream(cfg.session, urls, os.path.join(post_dir, f"{i:02d}"))
        print(f"  [{i}/{len(images)}] {os.path.basename(path)} ({human(os.path.getsize(path))})")

    if cfg.music:
        play = (item.get("music") or {}).get("playUrl")
        if play:
            try:
                save_stream(cfg.session, [play], os.path.join(post_dir, "musik"))
                print("  [musik] tersimpan")
            except Exception as e:
                log("WARNING", f"Musik gagal: {e}")
    if cfg.meta:
        with open(os.path.join(post_dir, "info.json"), "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        with open(os.path.join(post_dir, "caption.txt"), "w", encoding="utf-8") as f:
            f.write(item.get("desc", ""))
    return post_dir


# ───────────────────────── Video ─────────────────────────
def _progress_hook(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        done = d.get("downloaded_bytes", 0)
        speed = d.get("speed")
        pct = f"{done / total * 100:5.1f}%" if total else "  ... "
        sp = f"{human(speed)}/s" if speed else "-"
        eta = d.get("eta")
        eta_s = f"ETA {eta}s" if eta is not None else ""
        total_s = human(total) if total else "?"
        print(f"\r  {pct}  {human(done)}/{total_s}  {sp}  {eta_s}      ", end="", flush=True)
    elif d["status"] == "finished":
        print(f"\r  100.0%  {human(d.get('downloaded_bytes', 0))}  selesai" + " " * 20)


def ytdlp_opts(cfg, tolerant=False):
    opts = {
        "outtmpl": os.path.join(cfg.folder, "%(uploader)s_%(id)s.%(ext)s"),
        "format": QUALITY.get(cfg.quality, QUALITY["best"]) if FFMPEG_OK else "b",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "progress_hooks": [_progress_hook],
        # --- stabilitas untuk file besar ---
        "continuedl": True,                 # lanjutkan file .part jika terputus
        "retries": 10,
        "fragment_retries": 10,
        "file_access_retries": 5,
        "extractor_retries": 3,
        "socket_timeout": 30,
        "http_chunk_size": 10 * 1024 * 1024,  # unduh per 10MB, tahan throttle
        "concurrent_fragment_downloads": 4,
        "overwrites": False,
        "restrictfilenames": True,
        "trim_file_name": 120,
        "ignoreerrors": tolerant,
    }
    if FFMPEG_OK:
        opts["merge_output_format"] = "mp4"
    if cfg.audio_only:
        opts["format"] = "ba/b"
        if FFMPEG_OK:
            opts["postprocessors"] = [{"key": "FFmpegExtractAudio",
                                       "preferredcodec": "mp3", "preferredquality": "192"}]
    if cfg.meta:
        opts["writeinfojson"] = True
        opts["writedescription"] = True
        opts["writethumbnail"] = True
    if cfg.cookie_file and os.path.exists(cfg.cookie_file):
        opts["cookiefile"] = cfg.cookie_file
    elif cfg.browser:
        opts["cookiesfrombrowser"] = (cfg.browser,)
    return opts


def download_video(url, cfg):
    if not YTDLP_OK:
        raise RuntimeError("yt-dlp belum terinstall (pip install yt-dlp)")
    with yt_dlp.YoutubeDL(ytdlp_opts(cfg)) as ydl:
        ydl.download([url])


def download_pyktok(url, cfg, metadata_fn=""):
    if not PYKTOK_OK:
        raise RuntimeError("pyktok belum terinstall")
    cwd = os.getcwd()
    os.makedirs(cfg.folder, exist_ok=True)
    os.chdir(cfg.folder)
    try:
        pyk.save_tiktok(url, save_video=True, metadata_fn=metadata_fn,
                        browser_name=cfg.browser or "chrome")
    finally:
        os.chdir(cwd)


# ───────────────────── Router pintar ─────────────────────
def smart_download(url, cfg):
    """Deteksi otomatis: video / foto / slideshow. Fallback berlapis."""
    url = resolve_url(url, cfg.session)
    os.makedirs(cfg.folder, exist_ok=True)

    if "/photo/" in url:
        return download_photo_post(url, cfg)

    try:
        return download_video(url, cfg)
    except Exception as video_err:
        # Banyak post slideshow berbentuk /video/ tapi sebenarnya foto
        try:
            return download_photo_post(url, cfg)
        except Exception as photo_err:
            if PYKTOK_OK:
                try:
                    return download_pyktok(url, cfg)
                except Exception:
                    pass
            raise RuntimeError(f"video: {video_err} | foto: {photo_err}")


def download_many(urls, cfg):
    os.makedirs(cfg.folder, exist_ok=True)
    archive = load_archive(cfg.folder)
    ok = skipped = 0
    failed = []
    total = len(urls)
    try:
        for i, url in enumerate(urls, 1):
            vid = extract_id(url)
            print(f"\n[{i}/{total}] {url}")
            if vid and vid in archive:
                print("  sudah pernah didownload, dilewati")
                skipped += 1
                continue
            try:
                smart_download(url, cfg)
                if vid:
                    add_archive(cfg.folder, vid)
                    archive.add(vid)
                ok += 1
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"  [GAGAL] {str(e)[:200]}")
                add_failed(cfg.folder, url, e)
                failed.append(url)
            if i < total:
                sleep_random(cfg)
    except KeyboardInterrupt:
        print("\n[INFO] Dihentikan pengguna. Jalankan lagi, file .part akan dilanjutkan.")

    print(f"\n[SELESAI] sukses={ok}  dilewati={skipped}  gagal={len(failed)}  folder={cfg.folder}")
    if failed:
        print(f"[INFO] Daftar gagal tersimpan di {os.path.join(cfg.folder, 'failed.txt')}")


# ───────────────── Akun / Hashtag / Playlist ─────────────────
def list_entries(url, cfg, limit=None):
    if not YTDLP_OK:
        raise RuntimeError("yt-dlp belum terinstall")
    opts = {"quiet": True, "no_warnings": True, "extract_flat": True,
            "ignoreerrors": True, "socket_timeout": 30}
    if limit:
        opts["playlistend"] = limit
    if cfg.cookie_file and os.path.exists(cfg.cookie_file):
        opts["cookiefile"] = cfg.cookie_file
    elif cfg.browser:
        opts["cookiesfrombrowser"] = (cfg.browser,)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    urls = []
    for e in (info or {}).get("entries") or []:
        if not e:
            continue
        u = e.get("url") or e.get("webpage_url")
        if u and u.startswith("http"):
            urls.append(u)
    return urls


def gallerydl_fallback(url, cfg):
    log("INFO", "Mencoba gallery-dl (mendukung foto & slideshow di profil)...")
    cmd = ["gallery-dl", "-d", cfg.folder, url]
    if cfg.browser:
        cmd[1:1] = ["--cookies-from-browser", cfg.browser]
    elif cfg.cookie_file:
        cmd[1:1] = ["--cookies", cfg.cookie_file]
    subprocess.run(cmd)


def download_collection(url, cfg, limit=None):
    log("INFO", "Mengambil daftar konten...")
    try:
        urls = list_entries(url, cfg, limit)
    except Exception as e:
        log("WARNING", f"Gagal ambil daftar: {e}")
        urls = []
    if not urls:
        if GALLERYDL_OK:
            gallerydl_fallback(url, cfg)
        else:
            log("ERROR", "Daftar kosong. Coba pakai cookie browser (menu Pengaturan) "
                         "atau install gallery-dl: pip install gallery-dl")
        return
    log("INFO", f"Ditemukan {len(urls)} konten.")
    download_many(urls, cfg)


# ───────────────────── Menu interaktif ─────────────────────
def ask(prompt, default=""):
    v = input(f"{prompt}" + (f" [default: {default}]" if default != "" else "") + ": ").strip()
    return v or default


def yesno(prompt, default=False):
    d = "y" if default else "n"
    return ask(f"{prompt} (y/n)", d).lower().startswith("y")


def menu_settings(cfg):
    print("\n=== PENGATURAN ===")
    print(f"  Folder     : {cfg.folder}")
    print(f"  Kualitas   : {cfg.quality}")
    print(f"  Audio saja : {cfg.audio_only}")
    print(f"  Metadata   : {cfg.meta}")
    print(f"  Musik slide: {cfg.music}")
    print(f"  Cookie     : {cfg.cookie_file or cfg.browser or '-'}")
    print(f"  ffmpeg     : {'ada' if FFMPEG_OK else 'TIDAK ADA (sudo apt install ffmpeg)'}")
    cfg.folder = ask("Folder simpan", cfg.folder)
    q = ask("Kualitas (best/1080/720/540/360)", cfg.quality)
    cfg.quality = q if q in QUALITY else "best"
    cfg.audio_only = yesno("Download audio saja (MP3)?", cfg.audio_only)
    cfg.meta = yesno("Simpan metadata & caption?", cfg.meta)
    cfg.music = yesno("Simpan musik dari slideshow foto?", cfg.music)
    print("Sumber cookie (untuk konten yang butuh login):")
    print("  0. Tidak ada")
    for i, b in enumerate(BROWSERS, 1):
        print(f"  {i}. {b}")
    print("  f. File cookies.txt")
    c = ask("Pilih", "0").lower()
    cfg.browser = cfg.cookie_file = None
    if c == "f":
        cfg.cookie_file = ask("Path cookies.txt") or None
    elif c.isdigit() and 1 <= int(c) <= len(BROWSERS):
        cfg.browser = BROWSERS[int(c) - 1]
    cfg.session = make_session(cfg)


def interactive():
    cfg = default_cfg()
    cfg.session = make_session(cfg)
    print("=" * 52)
    print("      TIKTOK DOWNLOADER v3")
    print("      Video · Foto · Slideshow · Akun · Hashtag")
    print("=" * 52)
    print(f"  yt-dlp : {'OK' if YTDLP_OK else 'tidak ada'}   requests: {'OK' if REQUESTS_OK else 'tidak ada'}")
    print(f"  ffmpeg : {'OK' if FFMPEG_OK else 'tidak ada'}   pyktok  : {'OK' if PYKTOK_OK else 'opsional'}"
          f"   gallery-dl: {'OK' if GALLERYDL_OK else 'opsional'}")
    if not YTDLP_OK:
        log("ERROR", "Install dulu: pip install yt-dlp requests --break-system-packages")
        sys.exit(1)

    while True:
        print("\n=== MENU UTAMA ===")
        print("  1. Download 1 URL (video / foto / slideshow otomatis)")
        print("  2. Download semua konten dari akun")
        print("  3. Download banyak URL (ketik manual atau dari file .txt)")
        print("  4. Download dari hashtag")
        print("  5. Pengaturan (kualitas, audio, cookie, folder)")
        print("  0. Keluar")
        p = input("\nPilih menu: ").strip()

        if p == "1":
            url = ask("URL TikTok")
            if url.startswith("http"):
                download_many([url], cfg)
            else:
                log("ERROR", "URL harus diawali http(s)://")
        elif p == "2":
            user = ask("Username (tanpa @)").lstrip("@")
            if not user:
                continue
            n = ask("Jumlah maksimal [kosong = semua]")
            sub = SimpleNamespace(**vars(cfg))
            sub.folder = os.path.join(cfg.folder, user)
            download_collection(f"https://www.tiktok.com/@{user}", sub,
                                int(n) if n.isdigit() else None)
        elif p == "3":
            src = ask("Path file .txt berisi URL [kosong = ketik manual]")
            urls = []
            if src and os.path.exists(src):
                with open(src, encoding="utf-8") as f:
                    urls = [l.strip() for l in f if l.strip().startswith("http")]
            else:
                print("Masukkan URL satu per baris, ketik 'selesai' untuk mulai.")
                while True:
                    u = input(f"URL {len(urls) + 1}: ").strip()
                    if u.lower() == "selesai":
                        break
                    if u.startswith("http"):
                        urls.append(u)
            if urls:
                download_many(urls, cfg)
        elif p == "4":
            tag = ask("Hashtag (tanpa #)").lstrip("#")
            if not tag:
                continue
            n = ask("Jumlah video", "30")
            sub = SimpleNamespace(**vars(cfg))
            sub.folder = os.path.join(cfg.folder, f"tag_{tag}")
            download_collection(f"https://www.tiktok.com/tag/{tag}", sub,
                                int(n) if n.isdigit() else 30)
        elif p == "5":
            menu_settings(cfg)
        elif p == "0":
            print("Sampai jumpa!")
            return
        else:
            log("WARNING", "Pilihan tidak valid.")


# ───────────────────────── CLI ─────────────────────────
def cli(argv):
    ap = argparse.ArgumentParser(description="TikTok Downloader v3 (video, foto, slideshow)")
    ap.add_argument("urls", nargs="*", help="URL video/foto/slideshow")
    ap.add_argument("-f", "--file", help="file .txt berisi daftar URL")
    ap.add_argument("-u", "--user", help="download semua konten akun (tanpa @)")
    ap.add_argument("-t", "--tag", help="download dari hashtag (tanpa #)")
    ap.add_argument("-n", "--limit", type=int, help="batas jumlah konten (akun/hashtag)")
    ap.add_argument("-o", "--output", default="downloads", help="folder output")
    ap.add_argument("-q", "--quality", default="best", choices=list(QUALITY))
    ap.add_argument("-a", "--audio", action="store_true", help="audio saja (MP3)")
    ap.add_argument("--meta", action="store_true", help="simpan metadata & caption")
    ap.add_argument("--music", action="store_true", help="simpan musik slideshow foto")
    ap.add_argument("--browser", choices=BROWSERS, help="ambil cookie dari browser")
    ap.add_argument("--cookies", help="path cookies.txt (Netscape)")
    a = ap.parse_args(argv)

    cfg = default_cfg()
    cfg.folder, cfg.quality, cfg.audio_only = a.output, a.quality, a.audio
    cfg.meta, cfg.music = a.meta, a.music
    cfg.browser, cfg.cookie_file = a.browser, a.cookies
    cfg.session = make_session(cfg)

    urls = list(a.urls)
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            urls += [l.strip() for l in f if l.strip().startswith("http")]

    if a.user:
        cfg.folder = os.path.join(cfg.folder, a.user.lstrip("@"))
        download_collection(f"https://www.tiktok.com/@{a.user.lstrip('@')}", cfg, a.limit)
    elif a.tag:
        cfg.folder = os.path.join(cfg.folder, f"tag_{a.tag.lstrip('#')}")
        download_collection(f"https://www.tiktok.com/tag/{a.tag.lstrip('#')}", cfg, a.limit)
    elif urls:
        download_many(urls, cfg)
    else:
        ap.print_help()


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            cli(sys.argv[1:])
        else:
            interactive()
    except KeyboardInterrupt:
        print("\n[INFO] Dibatalkan.")
