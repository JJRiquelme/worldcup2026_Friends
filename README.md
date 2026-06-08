# ⚽ Mundial 2026 — Pool de amigos

Pool de predicciones para la fase de grupos del Mundial 2026.  
Los 48 equipos, los 72 partidos, clasificación automática diaria.

---

## Cómo funciona

| Quién | Qué hace |
|---|---|
| **Participantes** | Abren `index.html`, rellenan las 72 predicciones (1/X/2) + campeón y envían **una sola vez** |
| **Admin (tú)** | Editas `data/results.json` conforme se juegan los partidos |
| **GitHub Actions** | Recalcula la clasificación cada día a las 10:00 (Madrid) y actualiza `leaderboard.html` |

---

## Setup inicial (5 pasos)

### 1. Crea el repositorio en GitHub
Ya lo tienes: `github.com/JJRiquelme/worldcup2026_Friends`  
Asegúrate de que sea **público** (necesario para que GitHub Pages funcione gratis).

### 2. Sube todos los archivos
```bash
git clone https://github.com/JJRiquelme/worldcup2026_Friends.git
cd worldcup2026_Friends
# copia aquí todos los archivos de este repo
git add .
git commit -m "Initial setup"
git push
```

### 3. Crea el fine-grained Personal Access Token

Este token permite que el formulario escriba los archivos de predicciones directamente en el repo.

1. Ve a **GitHub → Settings → Developer Settings → Personal access tokens → Fine-grained tokens**
2. Haz clic en **"Generate new token"**
3. Configura:
   - **Token name:** `wc2026-pool-write`
   - **Expiration:** 60 days (cubre el torneo entero, 11 Jun – 19 Jul)
   - **Repository access:** Only selected repositories → `worldcup2026_Friends`
   - **Permissions → Repository permissions → Contents:** `Read and Write`
4. Copia el token generado (solo se muestra una vez)

### 4. Pon el token en index.html

Abre `index.html` y busca esta línea cerca del principio del `<script>`:

```js
token: 'ghp_REPLACE_WITH_YOUR_FINE_GRAINED_TOKEN',
```

Reemplaza el valor con el token que acabas de crear. Guarda y haz push.

> ⚠️ **Seguridad:** El token queda visible en el HTML público. Es un riesgo controlado:
> el token solo tiene permisos de escritura en este repo concreto.
> Para un pool entre amigos, es perfectamente aceptable.
> **Revócalo desde GitHub Settings cuando cierre el plazo de envíos.**

### 5. Activa GitHub Pages

1. Ve a **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Guarda

En unos minutos, el pool estará disponible en:  
`https://jjriquelme.github.io/worldcup2026_Friends/`

---

## Uso durante el torneo

### Introducir resultados

Edita `data/results.json` después de cada partido:

```json
"A1": {"home": "Mexico", "away": "South Africa", "result": "1"},
"A2": {"home": "Mexico", "away": "South Korea",  "result": "X"},
```

Valores: `"1"` (gana local) · `"X"` (empate) · `"2"` (gana visitante)

Al terminar el torneo, pon también el campeón:
```json
"champion": "Spain"
```

### Forzar actualización de la clasificación

Sin esperar al cron diario:  
**GitHub → Actions → Update Leaderboard → Run workflow**

---

## Puntuación

| Acierto | Puntos |
|---|---|
| Resultado correcto (1/X/2) | **3 pts** |
| Campeón correcto | **+10 pts** |

---

## Estructura del repo

```
worldcup2026_Friends/
├── index.html                    # Formulario de predicciones
├── leaderboard.html              # Clasificación en tiempo real
├── data/
│   ├── results.json              # Resultados reales (editar manualmente)
│   ├── leaderboard.json          # Generado automáticamente por el script
│   └── predictions/
│       └── {apellido}_{nombre}.json   # Un archivo por participante
├── scripts/
│   └── calc_leaderboard.py       # Lógica de puntuación
└── .github/workflows/
    └── leaderboard.yml           # Cron job diario (10:00 Madrid)
```

---

## FAQ

**¿Pueden los participantes modificar sus predicciones?**  
No. El archivo se crea una sola vez vía GitHub API. Si ya existe, la API devuelve error 422. Además se guarda un flag en localStorage como segunda barrera.

**¿Qué pasa si dos personas tienen el mismo nombre y apellido?**  
El formulario les avisa que ya existe un envío. En ese caso, pídele a uno que añada una inicial o algo al apellido.

**¿Puedo añadir rondas eliminatorias?**  
No está implementado en esta versión, pero es fácil de extender: añade más partidos a `results.json` con IDs tipo `R32_1`, `QF_1`, etc., y actualiza la lógica del formulario.

**¿Cuándo revocar el token?**  
Antes del primer partido (11 de junio). Después de esa fecha nadie debería poder enviar predicciones nuevas.
