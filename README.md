
### 🛠️ Prerequisites
Make sure ~/.config/soar/config.toml exists. If not, run:
```bash
soar defconfig
```

---
### 🚀 Soar Configuration
Paste this into your `~/.config/soar/config.toml` to use these filtered repositories:

```toml
[[repositories]]
name = "anylinux-filtered"
url = "https://githubusercontent.com"
enabled = true
type = "json" 

[[repositories]]
name = "bincache-filtered"
url = "https://githubusercontent.com"
enabled = true
type = "json" 

[[repositories]]
name = "pkgcache-filtered"
url = "https://githubusercontent.com"
enabled = true
type = "json"
```

### 🔄 Sync Commands
After pasting, run these commands to update your local database:
```bash
soar sync 
soar list
```

