# Publicación compatible con Java

Todavía no hay releases oficiales, clave oficial ni feed activo.

1. Subir el control privado con `tools/upload_to_github.py` tras iniciar sesión.
2. Elegir un repositorio GitHub Releases accesible al cliente para distribución.
   No se crea ni convierte a público ningún repositorio automáticamente.
3. Crear/custodiar fuera del repositorio una clave RSA 3072 bits PKCS#8.
   Entregar solo la pública X.509 como `config/trusted-release-key.pem`, verificando
   su huella por un canal confiable. La rotación no está soportada en el feed actual.
4. Preparar carpetas base y destino reales. El estado recuperado usa SemVer
   `0.1.0`; U09/U10 no son versiones SemVer. El primer parche puede ser `0.1.1`
   si corresponde a esa base real. Crear el delta (OWNER/FEED son marcadores):

```sh
python tools/build_release.py --base BASE --target DESTINO --output PUBLICACION --version 0.1.1 --from-version 0.1.0 --asset-base https://github.com/OWNER/FEED/releases/download/v0.1.1 --notes "Cambios comprobados"
```

Solo se publican `res/`, `lib/`, `runtime/`, el JAR del juego y `version.properties`.
Se excluyen perfiles, config, mods, credenciales y `nx-updater.jar`. Actualizar
el updater requiere instalador completo.

5. Compilar herramientas con `python client-java/build.py`. Firmar fuera de CI:

```sh
java -cp client-java/build/nx-updater.jar nx.updater.ReleaseSigner PRIVATE.pem PUBLICACION/NX_UPDATE_PC_JAVA_DEVELOPMENT.json PUBLICACION/NX_UPDATE_PC_JAVA_DEVELOPMENT.json.sig
java -cp client-java/build/nx-updater.jar nx.updater.ReleaseVerifier PUBLIC.pem PUBLICACION/NX_UPDATE_PC_JAVA_DEVELOPMENT.json PUBLICACION/NX_UPDATE_PC_JAVA_DEVELOPMENT.json.sig 0.1.0 PC_JAVA DEVELOPMENT CB4-LAN-3
```

6. Subir `.bin`, JSON y `.sig` al mismo release elegido. El nombre debe ser
   `NX_UPDATE_PC_JAVA_DEVELOPMENT.json` más `.sig` para la firma. Para RC usar
   `RELEASE_CANDIDATE` en el nombre; STABLE no debe marcarse prerelease.
7. Configurar `distributionRepository=OWNER/FEED` y la pública en una instalación
   de prueba. Probar comprobación, descarga, instalación y restauración antes de entregar.

El control privado no es un CDN anónimo. No se añaden tokens al cliente. La CI
verifica código y fixtures; no contiene secretos de firma ni publica releases.
