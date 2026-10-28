# xGol · Playbook editorial y técnico

Cuenta: **@xgolmx** (Instagram). Marca: **xGol | Datos deportivos**. Dueño: Pablo.
Objetivo de la etapa 1: crecer audiencia con análisis deportivo **muy numérico y "pro"**. Sin monetización todavía.

## Flujo diario
1. Revisar partidos de hoy y mañana (NFL, NBA, futbol europeo, Liga MX; tenis en temporada; MLB a partir de marzo).
2. Proponer a Pablo **3 a 5 opciones** de post, cada una con una imagen de muestra (portada) y un resumen de 2 líneas del dato clave. Mezclar formatos:
   - **Previa en números** (probabilidad del modelo, métricas, el dato clave del duelo).
   - **Prueba de hipótesis** (p-valor explicado en simple, con veredicto honesto, incluso "inconcluso").
   - **Tendencia / regresión a la media** (récord vs. calidad real).
   - **Ranking recurrente** (power ranking semanal).
3. Pablo elige. Solo entonces: renderizar el carrusel completo, escribir el caption y ponerlo en la cola.
4. Nunca publicar nada que Pablo no haya aprobado.

## Reglas legales y de plataforma (no negociables)
- **Cero fotos de jugadores** (LFDA art. 87, derecho a la propia imagen) y **cero logos/escudos** (marcas). Equipos solo por nombre o abreviatura en texto.
- **Nada de lenguaje de apuestas**: no "pick", "momio", "cuota", "parlay", "apuesta", "lock", "valor". No mostrar líneas de casas de apuestas. TikTok trata pronósticos y análisis de momios como contenido de apuestas.
- Decir "nuestro modelo estima 56%", nunca "va a ganar". En deportes que no son futbol, no usar "modelo xGol" en títulos (confunde): "Modelo NBA v1", "Modelo NFL v0".
- Aviso legal en letra pequeña (≈19 px) al pie del slide de método.
- Siempre: "Análisis independiente, no afiliado a ninguna liga" y "No es recomendación de apuesta" en el slide de método o caption.
- **No copiar tablas crudas** de proveedores. Publicar métricas y conclusiones propias.
- Crédito de datos cuando la licencia lo pide (nflverse: CC-BY 4.0 → "Datos: nflverse").
- Si se usa voz con IA en video: activar la etiqueta de contenido generado por IA.

## Fuentes de datos
| Deporte | Fuente | Licencia / notas |
|---|---|---|
| NFL | nflverse (GitHub releases: `schedules/games.csv`, `pbp/play_by_play_<año>.csv.gz`) | CC-BY 4.0. Accesible desde la sesión. |
| NBA, EPL, LaLiga, Champions, ATP/WTA | BALLDONTLIE API | Términos permiten uso comercial y publicar derivados sin atribución; no decir "oficial". Requiere API key (pendiente). |
| Futbol europeo | football-data.org (plan gratis, 12 competiciones) | Pendiente de key. |
| Liga MX | SportsAPI Pro (plan gratis, 100 req/día) | Permite publicar análisis y resultados de modelos; prohíbe republicar datos crudos. Pendiente de key. |
| Plan B Liga MX | Modelo Elo solo con marcadores | Hechos públicos. |

**Limitación actual:** la sesión de Claude solo tiene salida a GitHub y registros de paquetes. Las APIs que no estén en GitHub deben consultarse desde GitHub Actions (pendiente de montar). Mientras tanto, las opciones diarias se basan sobre todo en NFL.

## Modelo NBA v1
- Ataque y defensa por equipo con regresión ridge sobre cada marcador; prior = 60% del nivel de la temporada pasada; σ ≈ 14.7.
- Backtest 2025-26 (1,090 partidos, fuera de muestra): 69% aciertos, Brier 0.205 vs 0.248; calibrado.
- Código y datos en el repo privado `xgol-data` (`models/`). Revisar reporte de lesiones antes de publicar (el modelo no las ve).

## TikTok
- Pablo sube manualmente los mismos JPG como carrusel de fotos. Evitar cualquier lenguaje de apuestas.

## Modelo v0 (NFL)
- Margen esperado = 0.5 × (EPA neta/jugada local − EPA neta/jugada visitante) × 61.6 jugadas + 1.5 pts de localía.
- Probabilidad = Φ(margen / 13.5).
- El factor 0.5 es regresión a la media por muestra corta; revisarlo conforme avance la temporada.

## Estilo visual (provisional)
- Lienzo 1080×1350 (4:5). Fondo `#0A0E13`, superficie `#141B24`, línea `#232C38`, texto `#F2F4F7`, secundario `#8A94A3`, acento lima `#C6FF3D`, alerta coral `#FF6B5B`.
- Tipografía Inter / Inter Display (Black para títulos, Bold para cifras). Kicker en mayúsculas lima.
- Footer: wordmark "xGol" (x en lima) + número de slide.
- Código de referencia en `studio/` (helpers en `render_car_gb.py`).
- Verificar cada número contra la fuente y revisar visualmente cada slide antes de proponerlo.

## Publicación (este repo)
- `posts/<AAAA-MM-DD>-<tema>/01.jpg…` (JPEG, máx. 10) + `caption.txt` (≤ 2,200 caracteres).
- `queue/<misma-carpeta>.json` → `{"post": "<carpeta>", "publish_at": "2026-10-29T12:00:00-06:00"}`.
- `.github/workflows/publish.yml` publica lo vencido cada 15 min (o al hacer push a `queue/`) y lo mueve a `published/` con el permalink.
- Secretos: `IG_USER_ID` (17841451380567277) e `IG_ACCESS_TOKEN` (token de la Página XGol, no caduca).
- Horarios sugeridos: previas ~6 h antes del partido; posts generales entre 12:00 y 19:00 CDMX; separar posts del mismo día al menos 2 h.
- La foto de perfil no se puede cambiar por API.
