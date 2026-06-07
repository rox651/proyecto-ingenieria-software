# Despliegue del Software Journey (GitHub Pages)

## URL esperada

https://rox651.github.io/proyecto-ingenieria-software/

## Configuración en GitHub (una sola vez)

1. Abre **Settings → Pages** del repositorio.
2. En **Build and deployment → Source**, elige **Deploy from a branch**.
3. **Branch:** `gh-pages` · **Folder:** `/ (root)`
4. Guarda.

El workflow `.github/workflows/pages.yml` construye VitePress y publica en la rama `gh-pages` en cada push a `main`.

## Si el deploy falló con 404 (Actions)

El error `Failed to create deployment (status: 404)` ocurre cuando Pages está en modo **GitHub Actions** pero el entorno no está listo. Este proyecto usa **peaceiris/actions-gh-pages** (rama `gh-pages`) para evitar ese problema.

Tras configurar Pages como arriba, re-ejecuta el workflow en **Actions → Deploy Software Journey → Re-run all jobs**.

## Verificación local

```bash
npm ci
npm run docs:build
npm run docs:preview
```
