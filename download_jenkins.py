import urllib.request
import sys
import time

url = "https://get.jenkins.io/war-stable/latest/jenkins.war"
target = "d:\\DEVOPS\\jenkins.war"

print(f"[*] Downloading official Jenkins WAR from {url}...")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req) as resp, open(target, "wb") as f:
    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    start = time.time()
    while True:
        chunk = resp.read(1024 * 512)
        if not chunk:
            break
        f.write(chunk)
        downloaded += len(chunk)
        if total:
            pct = (downloaded / total) * 100
            mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            sys.stdout.write(f"\rProgress: {mb:.1f}MB / {total_mb:.1f}MB ({pct:.1f}%)")
            sys.stdout.flush()

print(f"\n[OK] jenkins.war downloaded successfully ({downloaded / (1024*1024):.1f} MB in {time.time() - start:.1f}s)")
