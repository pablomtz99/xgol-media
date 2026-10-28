"""Publicador de xGol para Instagram (Graph API).

Lee `queue/*.json` ({"post": "<carpeta en posts/>", "publish_at": "<ISO 8601>"}),
publica los que ya vencieron y deja constancia en `published/`.

Modos:
  python scripts/publish.py           -> publica lo que esté pendiente y vencido
  python scripts/publish.py --check   -> solo verifica que el token funcione
  python scripts/publish.py --dry-run -> valida la cola sin llamar a la API

Secretos (GitHub Actions): IG_USER_ID, IG_ACCESS_TOKEN. Nunca se imprimen.
"""
import datetime as dt
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v26.0"
REPO = os.environ.get("GITHUB_REPOSITORY", "pablomtz99/xgol-media")
BRANCH = os.environ.get("BRANCH", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"


def env(name):
    v = os.environ.get(name, "").strip()
    if not v:
        sys.exit(f"Falta el secreto {name}. Agrégalo en Settings → Secrets and variables → Actions.")
    return v


def call(method, path, **params):
    params["access_token"] = env("IG_ACCESS_TOKEN")
    data = urllib.parse.urlencode(params)
    if method == "GET":
        req = urllib.request.Request(f"{API}/{path}?{data}")
    else:
        req = urllib.request.Request(f"{API}/{path}", data=data.encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.exit(f"Error de la API ({e.code}) en {path.split('?')[0]}: {body}")


def wait_ready(container_id, tries=30):
    for _ in range(tries):
        st = call("GET", container_id, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"El contenedor {container_id} quedó en estado {st}.")
        time.sleep(5)
    sys.exit(f"El contenedor {container_id} no terminó de procesarse a tiempo.")


def load_post(slug):
    folder = os.path.join("posts", slug)
    images = sorted(glob.glob(os.path.join(folder, "*.jpg")))
    if not images:
        sys.exit(f"No hay imágenes .jpg en {folder}")
    if len(images) > 10:
        sys.exit(f"{folder} tiene {len(images)} imágenes; Instagram permite máximo 10.")
    with open(os.path.join(folder, "caption.txt"), encoding="utf-8") as f:
        caption = f.read().strip()
    if len(caption) > 2200:
        sys.exit(f"El caption de {slug} pasa de 2,200 caracteres.")
    urls = [f"{RAW}/{p.replace(os.sep, '/')}" for p in images]
    return urls, caption


def publish(slug):
    ig = env("IG_USER_ID")
    urls, caption = load_post(slug)
    if len(urls) == 1:
        creation = call("POST", f"{ig}/media", image_url=urls[0], caption=caption)["id"]
    else:
        children = []
        for u in urls:
            cid = call("POST", f"{ig}/media", image_url=u, is_carousel_item="true")["id"]
            wait_ready(cid)
            children.append(cid)
        creation = call("POST", f"{ig}/media", media_type="CAROUSEL",
                        children=",".join(children), caption=caption)["id"]
    wait_ready(creation)
    media_id = call("POST", f"{ig}/media_publish", creation_id=creation)["id"]
    permalink = call("GET", media_id, fields="permalink").get("permalink", "")
    return media_id, permalink


def due_items(now):
    items = []
    for path in sorted(glob.glob("queue/*.json")):
        with open(path, encoding="utf-8") as f:
            q = json.load(f)
        when = dt.datetime.fromisoformat(q["publish_at"])
        items.append((when, path, q))
    items.sort()
    return [(w, p, q) for w, p, q in items if w <= now], len(items)


def main():
    args = set(sys.argv[1:])
    if "--check" in args:
        ig = env("IG_USER_ID")
        me = call("GET", ig, fields="username,media_count")
        print(f"Token OK · cuenta @{me.get('username')} · {me.get('media_count')} publicaciones")
        return
    now = dt.datetime.now(dt.timezone.utc)
    due, total = due_items(now)
    print(f"Cola: {total} pendiente(s), {len(due)} para publicar ahora.")
    if "--dry-run" in args:
        for w, p, q in due:
            urls, cap = load_post(q["post"])
            print(f"  [ok] {q['post']}: {len(urls)} imagen(es), caption de {len(cap)} caracteres")
        return
    os.makedirs("published", exist_ok=True)
    for i, (w, path, q) in enumerate(due):
        if i:
            time.sleep(30)
        media_id, permalink = publish(q["post"])
        record = dict(q, media_id=media_id, permalink=permalink,
                      published_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
        with open(os.path.join("published", os.path.basename(path)), "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        os.remove(path)
        print(f"Publicado {q['post']} → {permalink}")


if __name__ == "__main__":
    main()
