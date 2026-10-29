"""Métricas de xGol (Instagram Graph API). Corre en GitHub Actions.

  python scripts/metrics.py   -> metrics/posts.json   (insights de cada post nuestro)
                               -> metrics/market.json  (cuentas comparables vía business_discovery)
                               -> metrics/_errors.json (lo que falló, para diagnosticar sin leer logs)

Secretos: IG_USER_ID, IG_ACCESS_TOKEN. Nunca se imprimen.
"""
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v26.0"
IG = os.environ.get("IG_USER_ID", "").strip()
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
ERR = []

# Métricas por post. Si alguna no existe para el tipo de medio, se pide de una en una.
METRICS = ["views", "reach", "likes", "comments", "saved", "shares", "total_interactions", "profile_visits", "follows"]


def get(path, **params):
    params["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:400]
        ERR.append({"path": path.split("?")[0], "params": {k: v for k, v in params.items() if k != "access_token"}, "status": e.code, "error": body})
        return None


def insights(media_id):
    out = {}
    js = get(f"{media_id}/insights", metric=",".join(METRICS))
    if js:
        for m in js.get("data", []):
            out[m["name"]] = (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value"))
        return out
    ERR.pop()  # reintento métrica por métrica
    for m in METRICS:
        js = get(f"{media_id}/insights", metric=m)
        if js and js.get("data"):
            d = js["data"][0]
            out[m] = (d.get("values") or [{}])[0].get("value", d.get("total_value", {}).get("value"))
    return out


def own():
    me = get(IG, fields="username,followers_count,media_count") or {}
    media = get(f"{IG}/media", fields="id,caption,media_type,timestamp,permalink,like_count,comments_count", limit=100) or {}
    posts = []
    for m in media.get("data", []):
        m["insights"] = insights(m["id"])
        m["caption"] = (m.get("caption") or "")[:120]
        posts.append(m)
    return {"fetched_at": dt.datetime.utcnow().isoformat() + "Z", "account": me, "posts": posts}


def market():
    with open("metrics/competitors.txt", encoding="utf-8") as f:
        handles = [l.strip().lstrip("@") for l in f if l.strip() and not l.startswith("#")]
    rows = []
    for h in handles:
        fields = (f"business_discovery.username({h})"
                  "{username,name,followers_count,media_count,biography,"
                  "media.limit(25){timestamp,media_type,like_count,comments_count,caption,permalink}}")
        js = get(IG, fields=fields)
        if not js:
            rows.append({"username": h, "ok": False})
            continue
        bd = js.get("business_discovery", {})
        media = bd.get("media", {}).get("data", [])
        for m in media:
            m["caption"] = (m.get("caption") or "")[:160]
        rows.append({"username": h, "ok": True, "name": bd.get("name"), "followers": bd.get("followers_count"),
                     "media_count": bd.get("media_count"), "bio": bd.get("biography"), "media": media})
    return {"fetched_at": dt.datetime.utcnow().isoformat() + "Z", "accounts": rows}


def save(path, obj):
    os.makedirs("metrics", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if not IG or not TOKEN:
        raise SystemExit("Faltan IG_USER_ID / IG_ACCESS_TOKEN")
    save("metrics/posts.json", own())
    save("metrics/market.json", market())
    save("metrics/_errors.json", ERR)
    print(f"ok · errores: {len(ERR)}")
