<!-- credits:start -->
> **Credits & license.** Port and maintenance by [JackStar6677-1](https://github.com/JackStar6677-1) and [DrakesCraft Labs](https://github.com/SlimefunNewHorizons). Original authors: [noreply](https://github.com/noreply). Upstream license: **no LICENSE file detected, see the org policy** (see [LICENSE](LICENSE)). Details: [docs/UPSTREAM_ATTRIBUTION.md](docs/UPSTREAM_ATTRIBUTION.md) · Policy: [Rights & Attribution](https://github.com/SlimefunNewHorizons/.github/blob/main/RIGHTS_AND_ATTRIBUTION.md). Independent community project, not affiliated with or endorsed by the original authors or the official Slimefun team.
>
> **Créditos y licencia.** Port y mantenimiento por [JackStar6677-1](https://github.com/JackStar6677-1) y [DrakesCraft Labs](https://github.com/SlimefunNewHorizons). Autores originales: [noreply](https://github.com/noreply). Licencia original: **sin archivo LICENSE detectado, ver la política de la organización**. Detalle en [docs/UPSTREAM_ATTRIBUTION.md](docs/UPSTREAM_ATTRIBUTION.md).
<!-- credits:end -->

# Slimefun 6 addons

Catalog of every addon DrakesCraft Labs maintains and runs on Minecraft 26.2 together with [Slimefun 6](https://github.com/SlimefunNewHorizons/Slimefun6).

- **All addons on one page:** https://slimefunnewhorizons.github.io/addons/
- **Mirror with ABI gate and history:** https://pack.drakescraft.cl/builds/
- **Maven dependencies:** https://maven.drakescraft.cl
- **Upload API (per-user tokens):** [docs/API.md](docs/API.md)

`addons.json` is the single source of truth. Each entry points to the addon's own repository, which stays independent
(history, issues and original authorship are kept). Builds are published to a Blob Builds project, one project per addon,
channel `Release`, Minecraft 26.2.

## Publishing from an addon repository

Add this workflow to the addon repository (replace `project`):

```yaml
name: Publish
on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  publish:
    uses: SlimefunNewHorizons/.github/.github/workflows/publish-blob.yml@main
    with:
      project: MyAddon-Drake
      file: target/MyAddon.jar
    secrets: inherit
```

The reusable workflow uploads the jar to Blob Builds with the commit message as release notes. The organization needs
the `BLOB_BUILDS_API_TOKEN` secret.

## Adding an addon

1. Create its Blob Builds project (or reuse an existing one you own).
2. Add an entry to `addons.json`.
3. Push to `main`; the page is rebuilt automatically.

Entries marked `pending` are built for Minecraft 26.2 but not published yet.

## Credits

Several addons are community projects maintained here as forks. The `author` field in `addons.json` keeps the original
credit, and each repository keeps its original license.
