#!/usr/bin/env python3
"""Comprobar SHA-256 de un archivo ya descargado."""
import hashlib
import re
import sys
from pathlib import Path


def verify(path, expected):
    if not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
        raise ValueError("Hash esperado debe tener 64 caracteres hexadecimales")
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    actual = digest.hexdigest()
    return actual.lower() == expected.lower(), actual


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python tools/check_sha256.py ARCHIVO HASH_SHA256", file=sys.stderr)
        sys.exit(2)
    try:
        valid, actual = verify(sys.argv[1], sys.argv[2])
        print(("PASS" if valid else "FAIL") + " SHA256=" + actual)
        sys.exit(0 if valid else 1)
    except (ValueError, OSError) as exc:
        print("FAIL " + str(exc), file=sys.stderr)
        sys.exit(1)
