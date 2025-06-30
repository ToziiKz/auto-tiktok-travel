# Auto TikTok Travel

Pipeline GitHub Actions pour générer, monter et publier automatiquement des vidéos de voyage sur TikTok.

## Mise en route rapide

1. **Fork** ou téléverse ce dépôt dans ton propre compte GitHub.
2. Ajoute les *Secrets* dans *Settings → Secrets and variables → Actions* :

   - `OPENAI_KEY`
   - `RUNWAY_KEY`
   - `PEXELS_KEY`
   - `ELEVEN_KEY`
   - `TIKTOK_APP_ID`
   - `TIKTOK_SECRET`

3. (Optionnel) Modifie `config.json` pour changer l’heure de publication (`cron`) ou le mode (`draft` vs `publish`).
4. Active GitHub Actions. Lance le workflow **Auto‑TikTok** une première fois manuellement.
5. Vérifie tes brouillons ou vidéos publiées dans l’appli TikTok et ajuste si besoin.