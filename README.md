# NX Updater — Java U10

Control de publicaciones de STREET CBTIS4 FIGHTERS, NX GAMES.
Destino: **Nintenlaxu/NX-Updater, PRIVATE**.

El cliente recuperado de U09 usa **RSA SHA-256**, clave pública RSA mínima 2048
bits, JSON `schemaVersion: 1`, plataforma `PC_JAVA`, protocolo `CB4-LAN-3` y
canales `DEVELOPMENT`, `RELEASE CANDIDATE`, `STABLE`. No se cambió a Ed25519.

## Estado comprobado

- Cliente Java compilado; 63 pruebas de actualización y 6 de repositorios PASS.
- Publicador delta compatible con pruebas Python.
- U10 identifica Nintenlaxu/NX-Updater como control privado previsto.
- Repositorio privado creado: https://github.com/Nintenlaxu/NX-Updater.
- Código y pruebas preparados para el commit inicial U10.
- Sin feed accesible, clave pública oficial ni releases publicados.
- C++ y Xbox 360 no se modifican ni se certifican.

## Subir a GitHub

Instala Git, Python 3.9+ y GitHub CLI. Inicia sesión como Nintenlaxu con `gh auth login`.
Después, desde esta carpeta:

```sh
python tools/upload_to_github.py
```

El script usa `UPLOAD_FILES.json`, confirma la cuenta, crea el repositorio
**privado** si falta, conserva archivos remotos adicionales y sube un commit
sin force push. Si existe público, se detiene. No sube el instalador, claves
o credenciales. La lista se revisó al empaquetar; no la regeneres con secretos.

## Comprobar

```sh
python -m unittest discover -s tests -v
python tools/validate_manifest.py manifests/stable.json manifests/beta.json
python client-java/build.py
```

Build: JDK 17+; bytecode 8, probado en Java 21. Certificación Java 8 y Windows pendiente.
`docs/DISTRIBUCION.md` explica preparación, firma y verificación.

`manifests/stable.json`, `manifests/beta.json` y su esquema conservan el catálogo
administrativo inicial: **no son el formato que consume el juego**.
El contrato autoritativo es `client-java/src/nx/updater/UpdateManifest.java`.

© 2026 NX GAMES. Se conserva NOTICE.md. No se otorga licencia de código abierto.
