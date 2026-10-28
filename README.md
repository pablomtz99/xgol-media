# xGol · media

Imágenes públicas de los posts de [@xgolmx](https://www.instagram.com/xgolmx/) y el publicador automático (GitHub Actions).

## Cómo funciona
- `posts/<fecha>-<tema>/` → imágenes `01.jpg…` (máx. 10) + `caption.txt`.
- `queue/<post>.json` → `{"post": "<carpeta>", "publish_at": "2026-10-29T12:00:00-06:00"}`.
- GitHub Actions (`.github/workflows/publish.yml`) revisa la cola cada 15 min y al hacer push; publica lo vencido vía Instagram Graph API y lo mueve a `published/`.
- Secretos requeridos: `IG_USER_ID`, `IG_ACCESS_TOKEN`.
