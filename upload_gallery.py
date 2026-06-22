import os, json, urllib.request, base64

with open(os.path.expanduser("~/.hermes/auth.json")) as f:
    token = json.load(f)["credential_pool"]["copilot"][0]["access_token"]

REPO = "Fizz0x11/783-agent-card-gallery"
GAL_DIR = r"C:\Users\HONOR\AppData\Local\hermes\skills\795-omnigent-meta-harness\references\agent-角色"

def gh_get(path):
    req = urllib.request.Request(f"https://api.github.com/{path}",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"})
    try:
        return json.loads(urllib.request.urlopen(req).read().decode())
    except:
        return {}

def gh_put(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"https://api.github.com/{path}",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json",
                 "Content-Type": "application/json"},
        method="PUT", data=body)
    return json.loads(urllib.request.urlopen(req).read().decode())

count = 0
errors = []
for root, dirs, files in os.walk(GAL_DIR):
    for fname in files:
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, GAL_DIR).replace("\\", "/")
        is_img = fname.endswith((".jpg", ".jpeg", ".png", ".ico", ".webp", ".gif"))
        try:
            with open(fpath, "rb" if is_img else "r", encoding=None if is_img else "utf-8") as f:
                content = f.read()
            if not is_img and isinstance(content, str):
                content = content.encode("utf-8")
            b64 = base64.b64encode(content).decode()
            sha = gh_get(f"repos/{REPO}/contents/{rel}").get("sha")
            gh_put(f"repos/{REPO}/contents/{rel}", {
                "message": f"Upload {rel}",
                "content": b64,
                "sha": sha
            })
            count += 1
            if count % 20 == 0:
                print(f"{count} files...")
        except Exception as e:
            errors.append(f"{rel}: {str(e)[:80]}")

print(f"Done: {count}, Errors: {len(errors)}")
for e in errors[:10]:
    print(" ERR:", e)
