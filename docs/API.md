# DrakesCraft Builds API

Base URL: `https://pack.drakescraft.cl/builds/api`

The request and response format follows [Blob Builds](https://blob.build/docs/): every response is
`{"success": bool, "message"|"data"|"error", "code"}`. Send a descriptive `User-Agent` header.

## Getting a token

Tokens are issued per user by the maintainers (`saori_builds_server.py user-add <name>`). The token is shown once and
stored hashed. A user can create up to 25 projects and can only change their own projects. Tokens can be revoked at any
time. Send it as `Authorization: Bearer <token>`.

## Read endpoints (no token)

| Method | Path | Description |
| --- | --- | --- |
| GET | `/projects` | List projects with their latest build |
| GET | `/project/<name>` | One project |
| GET | `/builds/<project>[?channel=release]` | Build history |
| GET | `/builds/<project>/latest` | Latest build |
| GET | `/builds/<project>/latest/download` | Download the latest jar |

## Create a project

```bash
curl -X POST https://pack.drakescraft.cl/builds/api/projects/MyAddon/new \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name": "MyAddon",
    "description": "My Slimefun addon",
    "repoLink": "https://github.com/Example/MyAddon",
    "releaseChannels": [{"name": "Release", "supportedVersions": "26.2", "dependencies": ["Slimefun"]}]
  }'
```

- Name: 2-40 characters, letters, numbers, `.` `_` `-`. Names are unique and case-insensitive.
- `repoLink` must be a GitHub or GitLab repository URL.
- The project appears in the public list after its first upload.

## Update a project or channel

```bash
curl -X PATCH https://pack.drakescraft.cl/builds/api/projects/MyAddon \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"description": "New description", "repoLink": "https://github.com/Example/MyAddon"}'

curl -X PATCH https://pack.drakescraft.cl/builds/api/projects/MyAddon/release \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"supportedVersions": "26.2", "dependencies": ["Slimefun"]}'
```

## Upload a build

```bash
SHA=$(sha256sum MyAddon.jar | cut -d' ' -f1)
curl -X POST https://pack.drakescraft.cl/builds/api/projects/MyAddon/release/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@MyAddon.jar" \
  --form-string "metadata={\"checksum\":\"$SHA\",\"releaseNotes\":\"Fix a crash\",\"commitHash\":\"<sha>\"}"
```

- Channels: `dev`, `rc`, `release`, `experimental`. Maximum size: 80 MB.
- `checksum` is the SHA-256 of the jar and must match.
- Every jar goes through the ABI gate before it is published: Java class version up to 69 (Java 25), a `plugin.yml`
  or `paper-plugin.yml`, and no references to the legacy Slimefun 4 package. A jar that fails is rejected with the reasons.

## Errors

| Code | Meaning |
| --- | --- |
| 401 | Missing, invalid or revoked token |
| 403 | The project belongs to someone else |
| 404 / 4000 | Project not found |
| 409 / 1003 | Project name already exists |
| 1001 | Invalid project name or channel |
| 1002 | `repoLink` is not a GitHub or GitLab repository |
| 1004 | `metadata` is not valid JSON |
| 1005 | Project limit reached |
| 1006 | Checksum does not match the file |

## GitHub Actions

Use the reusable workflow described in the [README](../README.md#publishing-from-an-addon-repository) to publish on every
push. It uploads to Blob Builds and to this mirror.
