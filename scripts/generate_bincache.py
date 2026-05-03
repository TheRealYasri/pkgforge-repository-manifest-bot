import requests, json, os

INPUT_URL = "https://raw.githubusercontent.com/pkgforge/bincache/main/SBUILD_LIST.json"
OUTPUT_FILE = "manifests/bincache.json"

def get_manifest():
    try:
        print(f"Fetching bincache source from {INPUT_URL}...")
        resp = requests.get(INPUT_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        manifest = []
        for p in data:
            name = p.get("pkg_family") or p.get("pkg")
            if not name:
                continue
            
            manifest.append({
                "pkg": name,
                "pkg_id": name,
                "pkg_name": name,
                "pkg_type": "static",
                "host": ["x86_64-linux"], 
                "version": str(p.get("version") or "latest"),
                "download_url": str(p.get("download_url") or ""),
                "size": p.get("size") or 0,
                "description": str(p.get("description") or ""),
                "src_url": [p.get("build_script")] if p.get("build_script") else []
            })
        return manifest
    except Exception as e:
        print(f"Error generating bincache manifest: {e}")
        return []

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    package_list = get_manifest()
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(package_list, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(package_list)} packages.")


