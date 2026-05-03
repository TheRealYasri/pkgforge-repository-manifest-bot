import requests, json, os

FILES_TO_FILTER = ["anylinux.json", "bincache.json", "pkgcache.json"]
SOARP_TREE_URL = "https://api.github.com/repos/pkgforge/soarpkgs/git/trees/main?recursive=1"
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"} if os.getenv('GITHUB_TOKEN') else {}

def get_soar_names():
    """Fetches official package names from soarpkgs/packages/ for deduplication."""
    try:
        resp = requests.get(SOARP_TREE_URL, headers=HEADERS, timeout=25)
        resp.raise_for_status()
        
        tree_data = resp.json().get('tree', [])
        names = {
            item['path'].replace('packages/', '') 
            for item in tree_data 
            if item['path'].startswith('packages/') and item['type'] == 'tree'
        }
        names.discard('') 
        return names
    except Exception as e:
        print(f"Warning: Could not fetch official Soar package list: {e}")
        return set()

def process_filters():
    soar_blacklist = get_soar_names()
    print(f"Blacklist loaded with {len(soar_blacklist)} official packages.")

    if not soar_blacklist:
        print("Error: Blacklist is empty. Check API access.")
        return

    for filename in FILES_TO_FILTER:
        input_path = f"manifests/{filename}"
        output_path = f"manifests/{filename.replace('.json', '_filtered.json')}"
        
        if not os.path.exists(input_path):
            continue

        try:
            with open(input_path, "r") as f:
                data = json.load(f)
            
            if isinstance(data, dict) and "packages" in data:
                raw_list = data["packages"]
                is_wrapped = True
            else:
                raw_list = data
                is_wrapped = False

            filtered_list = [pkg for pkg in raw_list if pkg.get("pkg_id") not in soar_blacklist]
            
            output_data = {"packages": filtered_list} if is_wrapped else filtered_list
            
            with open(output_path, "w") as f:
                json.dump(output_data, f, indent=2)
            
            removed_count = len(raw_list) - len(filtered_list)
            print(f"Processed {filename} -> {output_path} (Removed {removed_count} duplicates).")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    process_filters()
