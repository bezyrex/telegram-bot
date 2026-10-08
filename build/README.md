# Build & publish

Scripts for building the Docker image and pushing it to Docker Hub and GHCR.

## Prerequisites

- Docker daemon running, logged in to the target registries:
  ```bash
  docker login
  docker login ghcr.io
  ```
- Build variables in the repo root `.env` (copy from `.env.example`):

  | Variable | Example | Description |
  |---|---|---|
  | `VERSION` | `v1.0` | Tag appended after `latest` |
  | `DOCKERHUB_PROJECT_NAME` | `myname/tlgram-bt` | Docker Hub image name |
  | `DOCKERHUB_PROJECT_BUILD` | `true` | `true` = push to Docker Hub |
  | `GHCR_PROJECT_NAME` | `ghcr.io/myname/tlgram-bt` | GHCR image name |
  | `GHCR_PROJECT_BUILD` | `true` | `true` = push to GHCR |

## Run from repo root

Scripts resolve `.env` and `./dist/` relative to the current directory. Always run them from the repository root:

```bash
./build/setup.sh
./build/build.sh
./build/publish.sh
```

## Steps

### 1. `setup.sh`

Validates that `DOCKERHUB_PROJECT_NAME`, `GHCR_PROJECT_NAME`, `DOCKERHUB_PROJECT_BUILD` and `GHCR_PROJECT_BUILD` exist and are non-empty in `.env`. Creates `dist/` and marks success with `dist/.setuped`.

- Refuses to run if `dist/.setuped` already exists. To re-run, delete it first:
  ```bash
  rm dist/.setuped
  ```

### 2. `build.sh`

Requires `dist/.setuped`. Builds the image:

```bash
docker build -t $DOCKERHUB_PROJECT_NAME .
```

Marks success with `dist/.builded`.

### 3. `publish.sh`

Requires `dist/.builded`. Pushes, depending on the `_BUILD` flags:

- **Docker Hub**: `$DOCKERHUB_PROJECT_NAME:latest` and `:$VERSION`
- **GHCR**: `$GHCR_PROJECT_NAME:latest` and `:$VERSION` (tagged from the Docker Hub image)

A failed push prints an error but does not stop the remaining pushes.

## Full cycle

```bash
rm -f dist/.setuped dist/.builded   # optional clean start
./build/setup.sh
./build/build.sh
./build/publish.sh
```

## Notes

- `dist/.setuped` and `dist/.builded` are state flags only, no artifacts land in `dist/`.
- The image is defined by the root `Dockerfile`; it installs `requirements.txt`, copies the bot source and uses `python bot.py` as entrypoint.
- Deploy the published image with the root `compose.yaml` (see main [README.md](../README.md)).
