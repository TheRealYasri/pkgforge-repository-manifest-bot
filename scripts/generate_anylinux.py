import requests, json, os

ORG = "pkgforge-dev"
MAINTAINER_TAG = "@Samueru-sama"
OUTPUT_FILE = "manifests/anylinux.json"
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"} if os.getenv('GITHUB_TOKEN') else {}

def get_manifest():
    manifest = []
    page = 1
    print(f"Starting scan of {ORG} for {MAINTAINER_TAG}...")

    while True:
        url = f"https://api.github.com/orgs/{ORG}/repos?per_page=100&page={page}"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code != 200: break
            
        repos = resp.json()
        if not repos: break
            
        for repo in repos:
            description = repo.get("description") or ""
            if MAINTAINER_TAG in description:
                repo_name = repo["name"]
                pkg_id = repo_name.lower().replace("-appimage", "").replace("-enhanced", "")
                
                rel_url = f"https://api.github.com/repos/{ORG}/{repo_name}/releases/latest"
                rel_resp = requests.get(rel_url, headers=HEADERS, timeout=10)
                
                if rel_resp.status_code == 200:
                    rel_data = rel_resp.json()
                    for asset in rel_data.get("assets", []):
                        asset_name = asset["name"].lower()
                        if asset_name.endswith(".appimage") and "x86_64" in asset_name:
                            manifest.append({
                                "pkg": pkg_id,
                                "pkg_id": pkg_id,
                                "pkg_name": pkg_id,
                                "pkg_type": "appimage",
                                "host": ["x86_64-linux"], 
                                "version": rel_data["tag_name"],
                                "download_url": asset["browser_download_url"],
                                "size": asset["size"],
                                "description": description,
                                "src_url": [repo["html_url"]]
                            })
                            break
        page += 1
    return manifest

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    package_list = get_manifest()
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(package_list, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(package_list)} packages.")

