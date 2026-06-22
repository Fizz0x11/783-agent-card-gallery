"""
sync_to_github.py — 同步 BD 本地 Gallery 文件到 GitHub Pages repo
用法: python sync_to_github.py [--file 文件名] [--all]
"""
import os, json, urllib.request, base64, glob, argparse
from datetime import datetime

TOKEN_FILE = os.path.expanduser("~/.hermes/auth.json")
REPO = "Fizz0x11/783-agent-card-gallery"

def get_token():
    with open(TOKEN_FILE) as f:
        return json.load(f)["credential_pool"]["copilot"][0]["access_token"]

def get_sha(name):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/contents/{name}",
        headers={"Authorization": f"token {get_token()}", "Accept": "application/vnd.github.v3+json"}
    )
    try:
        return json.loads(urllib.request.urlopen(req, timeout=15).read().decode()).get("sha")
    except:
        return None

def upload(name, local_path, token):
    with open(local_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    sha = get_sha(name)
    payload = {"message": f"sync: {name} ({datetime.now().strftime('%Y-%m-%d')})", "content": b64}
    if sha:
        payload["sha"] = sha
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/contents/{name}",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json",
                 "Content-Type": "application/json"},
        method="PUT", data=json.dumps(payload).encode()
    )
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())

def sync_all(src_dir, token):
    files = glob.glob(os.path.join(src_dir, "*"))
    ok, fail = 0, []
    for path in sorted(files):
        name = os.path.basename(path)
        # 跳过目录和 .py 脚本自身
        if os.path.isdir(path) or name.endswith(".py") or name.endswith(".sh"):
            continue
        try:
            upload(name, path, token)
            print(f"  ✓ {name}")
            ok += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            fail.append(name)
    return ok, fail

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", "-f", help="只上传指定文件名（不含路径）")
    ap.add_argument("--all", "-a", action="store_true", help="同步目录下所有文件")
    args = ap.parse_args()

    # 默认：src = 本脚本所在目录
    src = os.path.dirname(os.path.abspath(__file__))
    token = get_token()

    print(f"[sync] REPO={REPO}  SRC={src}\n")

    if args.file:
        upload(args.file, os.path.join(src, args.file), token)
        print(f"  ✓ {args.file}")

    elif args.all:
        print(f"[sync_all] 共 {len(glob.glob(os.path.join(src, '*')))} 个条目...")
        ok, fail = sync_all(src, token)
        print(f"\n结果: {ok} ok, {len(fail)} fail")
        if fail:
            print("失败:", fail)
    else:
        print("用法: python sync_to_github.py --all     # 同步全部")
        print("       python sync_to_github.py --file index.html  # 只传一个")
