# xGol · Playbook editorial y técnico

Cuenta: **@xgolmx** (Instagram). Marca: **xGol | Datos deportivos**. Dueño: Pablo.
Objetivo de la etapa 1: crecer audiencia con análisis deportivo **muy numérico y "pro"**. Sin monetización todavía.

## Flujo diario
1. Revisar partidos de hoy y mañana (NFL, NBA, futbol europeo, Liga MX; tenis en temporada; MLB a partir de marzo).
2. **Fijo diario: "Resumen del día anterior"** (~9:00 CDMX). Resultados de lo que publicamos ayer vs. lo que dijo el modelo: aciertos, Brier de la noche, calibración, y los resultados clave. Se publica también cuando fallamos. No necesita elección, pero Pablo ve las imágenes antes.
2b. Además, proponer **4 ideas de posts de deportes** (de partidos/eventos), cada una con su portada y 2 líneas del dato clave + técnica. Pablo elige 3. Mezclar formatos:
   - **Previa en números** (probabilidad del modelo, métricas, el dato clave del duelo).
   - **Prueba de hipótesis** (p-valor explicado en simple, con veredicto honesto, incluso "inconcluso").
   - **Tendencia / regresión a la media** (récord vs. calidad real).
   - **Ranking recurrente** (power ranking semanal).
3. Pablo elige. Solo entonces: renderizar el carrusel completo, escribir el caption y ponerlo en la cola.
4. Nunca publicar nada que Pablo no haya aprobado.

## Estándar técnico (obligatorio desde 28 oct 2026)
Pablo quiere **más análisis estadístico, más técnico, más datos** en cada post. Mínimos:
1. **Modelo explícito** con su método en el último slide (fórmula o pasos) y sus supuestos/límites.
2. **Incertidumbre siempre**: probabilidad + intervalo (p. ej. 80%) o error típico; nunca un número sin rango.
3. **Validación**: métrica fuera de muestra cuando exista (aciertos, Brier vs. referencia, calibración, n).
4. **Métricas ajustadas** (por rival, por ritmo, por localía, por descanso) en lugar de promedios crudos.
5. Al menos **una prueba o contraste formal** por post cuando aplique: prueba de hipótesis con p-valor, tamaño del efecto, regresión a la media (real vs. esperado), simulación Monte Carlo o probabilidad compuesta.
6. **Densidad**: cada slide de partido con ≥ 4 métricas comparadas; contexto (lesiones, back-to-back, abridores) verificado el mismo día.
7. Narrativa persuasiva y creativa: un gancho numérico en la portada ("1 en 15"), tensión entre datos que se contradicen, pregunta final en el caption.
8. Decir n y fuente de cada número. Si un dato no se puede verificar, no va.

## Laboratorio: pruebas de hipótesis (obligatorio desde 28 oct 2026)
- Por cada post, plantear varias hipótesis (incluidas las que contradicen nuestro ángulo) y probarlas con datos históricos (NFL 2010–2025 en games.csv de nflverse; NBA 2025-26 en xgol-data). No casarse con ninguna.
- Corregir por pruebas múltiples (Benjamini-Hochberg); si algo no sobrevive, llamarlo "indicio", no "probado".
- Slide fijo **"Lo que probamos"**: 3–5 hipótesis con ✓ (se sostiene) / ✗ (mito), una línea en palabras + muestra, y el número técnico en chico (p, correlación).
- Mezclar previas con **rompemitos** (ej. "las rachas de pocos puntos no predicen nada: 392 casos").
- Resultados guardados en `xgol-data/lab/`. Hallazgos ya probados: rachas de unders NFL no persisten (p=0.42); jueves y frío no cambian totales vs. mercado; NBA: arranque predice ~27% del margen futuro (r=0.40); ajuste por rival mejora (r 0.42→0.51); back-to-back −2.1 al margen (p=0.011) pero no baja totales (p=0.36); +1 día de descanso no importa (p=0.74); nuestras proyecciones de totales sí discriminan (r=0.31; top 20% 239 vs. bottom 222).

## Ángulos (desde 28 oct 2026, Pablo)
- No todo es "quién gana". Rotar ángulos: cómo será el partido (ritmo, muchos/pocos puntos, por aire/por tierra), jugador vs. su exequipo, revanchas e historias, duelos individuales, rachas que hay que poner a prueba, contradicciones entre datos (y probarlas), riesgos para el favorito.
- Investigar a fondo: notas, estadísticas avanzadas públicas (Basketball-Reference, nflverse, etc.), lesiones, contexto de plantillas (cambios, traspasos).
- Ser crítico: si una "tendencia" no es significativa, decirlo; si hay un riesgo, mostrarlo.
- **Tono sobre nuestro modelo: siempre positivo o neutral.** No publicar que "el mercado acierta más que nosotros" ni similares. Las diferencias con el mercado se presentan como puntos de vista distintos con sus razones.

## Ángulo y venta (desde 28 oct 2026)
- Cada idea necesita un **ángulo único** y una historia: storylines del día (exjugadores, rachas, invictos, sequías), estadísticas públicas en línea y contexto.
- Usar momios como **"probabilidad del mercado"** (quitando el margen de la casa) y compararla con nuestro modelo: "Modelo vs. mercado". Nunca mostrar momios, líneas, nombres de casas, links ni llamados a apostar.
- 4 ideas por día, idealmente de deportes distintos.

## Diseño v7 (vigente desde 28 oct 2026): usar todo el espacio
- Motor `studio/layout_v7.py` + `studio/posts_v7_1029.py` como referencia. Cada slide = kicker + título + bloques (Hero, Stats, VBars, HBars, Table, MvM, Rank, Stacked, Tests, Bullets, Matchup) + panel de idea clave anclado abajo; el motor reparte el espacio.
- Portada con Matchup grande y panel lima; conclusión con viñetas numeradas y panel lima. Nada de "slide de PowerPoint" con texto suelto y huecos.

## Formato «para quien va scrolleando» (v4, vigente desde 28 oct 2026, reemplaza a v3)
- Pablo: "no asumas que sé; debo verlo y entender fácil y rápido con todo ahí".
- Slide 1 = contexto completo: deporte y competencia, equipos con nombre completo y récord, día y hora CDMX, qué está en juego + gancho con la predicción en frecuencias ("gana 2 de cada 3").
- 4 slides "DATO X DE 4": título-conclusión en lenguaje simple, UN número grande, una frase de contexto y una de interpretación. Sin siglas (nombres de ciudad/equipo), sin jerga (EPA, back-to-back, Brier → explicarlos o evitarlos).
- Slide 6 = conclusión en 3–4 viñetas + pregunta + método en letra chica.
- Referencia: `studio/scroll_mlb_1029.py`, `studio/scroll_rest_1029.py`.

## Explicación y narrativa v3 (histórico)
- **Sin cajas "EN SIMPLE"** (Pablo: se siente condescendiente). La explicación va integrada en la historia.
- Estructura: portada con tesis → pasos ①②③ (cada uno prueba una parte) → veredicto → "La lógica detrás" (diagrama de flujo del cálculo).
- El **título de cada slide es la conclusión**; la gráfica la demuestra con anotaciones directas (esperado vs. real, "así terminó", brechas marcadas).
- Bloque discreto **"CÓMO SE CALCULA"** con la lógica usando los números del caso, sin fórmulas.
- **Hilo conductor** al pie de cada slide: una frase que conecta con el siguiente y termina en "→".
- Referencia: `studio/story_mlb_1029.py`.
- Explicar cada término la primera vez (p-valor = "qué tan probable es por pura casualidad"; EPA = "puntos que suma cada jugada"; Brier = "error promedio, menos es mejor").
- Usar frecuencias ("2 de cada 3 veces") antes que porcentajes abstractos. Llevar al lector de la mano: historia → dato → qué significa → qué esperar.
- Carrusel de 6 slides; último = método como glosario + aviso legal pequeño. Generar también video vertical 1080×1920 para TikTok.

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
- Pablo sube manualmente los mismos slides como carrusel de FOTOS (no video; decisión del 28 oct). Mandarle las fotos de cada post en orden con su caption y horario. Evitar cualquier lenguaje de apuestas.

## Modelo v0 (NFL)
- Margen esperado = 0.5 × (EPA neta/jugada local − EPA neta/jugada visitante) × 61.6 jugadas + 1.5 pts de localía.
- Probabilidad = Φ(margen / 13.5).
- El factor 0.5 es regresión a la media por muestra corta; revisarlo conforme avance la temporada.

## Estilo visual (provisional)
- Lienzo 1080×1350 (4:5). Fondo `#0A0E13`, superficie `#141B24`, línea `#232C38`, texto `#F2F4F7`, secundario `#B3BDC9` (antes #8A94A3; subido por contraste), barras inactivas/divisores `#3B4757`, tarjetas `#1A2330`, contorno «esperado» `#D5DCE4`, acento lima `#C6FF3D`, alerta coral `#FF6B5B`.
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

## Medición y crecimiento
- `scripts/metrics.py` + `.github/workflows/metrics.yml` (diario 07:20 CDMX): insights por post → `metrics/posts.json`; cuentas comparables (business_discovery, lista en `metrics/competitors.txt`) → `metrics/market.json`; fallas → `metrics/_errors.json`.
- Requiere permisos `instagram_manage_insights` y `pages_read_engagement` en el token.
- Métrica principal: interacciones / alcance (tasa de interacción) y guardados+compartidos / alcance. Secundarias: vistas, visitas al perfil, follows por post.
- Cada post se etiqueta (deporte, formato, ángulo, tipo de gancho, hora, nº de slides). No sacar conclusiones con menos de ~8 posts por variante; usar comparaciones con intervalos (no "ganó el que tuvo más likes").
- Ajustar tono según datos, sin perder el rigor: el contenido es analítico primero.
