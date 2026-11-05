#!/usr/bin/env python3
"""NX Updater: validación estricta (sin dependencias de terceros)."""
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

APP_ID = "street-cbtis4-fighters"
PLATFORMS = {"pc-java-windows", "pc-cpp-windows", "xbox360"}
RELEASE_FIELDS = {"version", "url", "sha256", "size_bytes", "notes", "minimum_updater_version"}
SEMVER = re.compile(r"\A(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[a-zA-Z0-9.-]+)?\Z")
STRICT_VERSION = re.compile(r"\A(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\Z")
HEX64 = re.compile(r"\A[0-9a-f]{64}\Z")
FIELDS = {"schema_version", "app_id", "publisher", "channel", "generated_at", "releases"}


class ManifestError(ValueError):
    pass


def must(condition, error):
    if not condition:
        raise ManifestError(error)


def validate(data, expected_channel=None):
    must(type(data) is dict, "raíz: debe ser un objeto JSON")
    must(set(data) == FIELDS, f"raíz: campos esperados {sorted(FIELDS)}")
    must(type(data["schema_version"]) is int and data["schema_version"] == 1, "schema_version no soportada")
    must(data["app_id"] == APP_ID, "app_id inesperado")
    must(data["publisher"] == "NX GAMES", "publisher inesperado")
    must(data["channel"] in ("stable", "beta"), "canal no válido")
    if expected_channel:
        must(data["channel"] == expected_channel, "canal no coincide con el archivo")
    generated = data["generated_at"]
    must(generated is None or isinstance(generated, str), "generated_at debe ser null o ISO 8601")
    if generated is not None:
        try:
            parsed = dt.datetime.fromisoformat(generated.replace("Z", "+00:00"))
            must(parsed.tzinfo is not None, "generated_at necesita zona horaria")
        except ValueError as e:
            raise ManifestError("generated_at no es fecha ISO 8601 válida") from e
    releases = data["releases"]
    must(type(releases) is dict, "releases debe ser objeto")
    must(set(releases) <= PLATFORMS, "plataforma desconocida")
    if releases:
        must(generated is not None, "releases poblados exigen generated_at")
    for platform, release in releases.items():
        must(type(release) is dict, f"{platform}: debe ser objeto")
        must(set(release) == RELEASE_FIELDS, f"{platform}: campos inválidos o faltantes")
        must(type(release["version"]) is str and SEMVER.fullmatch(release["version"]), f"{platform}: version inválida")
        must(type(release["minimum_updater_version"]) is str and STRICT_VERSION.fullmatch(release["minimum_updater_version"]), f"{platform}: minimum_updater_version inválida")
        must(type(release["sha256"]) is str and HEX64.fullmatch(release["sha256"]), f"{platform}: SHA-256 inválido")
        must(type(release["size_bytes"]) is int and release["size_bytes"] > 0, f"{platform}: tamaño inválido")
        must(type(release["notes"]) is str and len(release["notes"]) <= 4000, f"{platform}: notas inválidas")
        url = release["url"]
        must(type(url) is str and len(url) < 2048, f"{platform}: URL inválida")
        parsed = urlparse(url)
        must(parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password and not parsed.fragment,
             f"{platform}: HTTPS requerido, sin credenciales ni fragmento")
    return True


def main(argv):
    if not argv:
        print("Uso: python tools/validate_manifest.py manifests/stable.json [manifests/beta.json]", file=sys.stderr)
        return 2
    failed = False
    for arg in argv:
        try:
            path = Path(arg)
            data = json.loads(path.read_text(encoding="utf-8"))
            expected = path.stem if path.stem in ("stable", "beta") else None
            validate(data, expected)
            print(f"PASS {path}")
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            failed = True
            print(f"FAIL {arg}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
