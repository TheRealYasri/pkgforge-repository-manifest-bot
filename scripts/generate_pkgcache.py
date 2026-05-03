import requests, json, os

INPUT_URL = "https://raw.githubusercontent.com/pkgforge/pkgcache/main/SBUILD_LIST.json"
OUTPUT_FILE = "manifests/pkgcache.json"

def get_manifest():
    try:
        resp = requests.get(INPUT_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        manifest = []
        for p in data:
            name = p.get("pkg_family") or p.get("pkg")
            if not name: continue
            
            manifest.append({
                "pkg": name,
                "pkg_id": name,
                "pkg_name": name,
                "pkg_type": "appimage",
                "host": ["x86_64-linux"],
                "version": p.get("version") or "latest",
                "download_url": p.get("download_url") or "",
                "size": p.get("size") or 0,
                "description": p.get("description") or "",
                "src_url": [p.get("build_script")] if p.get("build_script") else []
            })
        return manifest
    except Exception as e:
        print(f"Error fetching pkgcache: {e}")
        return []

if __name__ == "__main__":
    os.makedirs("manifests", exist_ok=True)
    package_list = get_manifest()
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(package_list, f, indent=2)
    print(f"Generated {OUTPUT_FILE} with {len(package_list)} packages.")
