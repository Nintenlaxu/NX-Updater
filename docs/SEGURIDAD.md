# Seguridad U10

- Clave privada fuera del repositorio; solo pública oficial en el juego.
- RSA SHA-256 mínimo 2048 bits. No mezclar con el diseño Ed25519 inicial.
- Firma exacta y SHA-256 antes de instalar y de aplicar cada archivo.
- Rutas y enlaces simbólicos restringidos; respaldo, recuperación y rollback.
- HTTPS en hosts GitHub permitidos; HTTP local solo en fixtures.
- Sin tokens en config, JAR o paquetes. El login del publicador reside en GitHub CLI.
- Un repositorio privado no implica distribución anónima. No incluir un PAT global.
- `UPLOAD_FILES.json` limita la subida; no agregar claves, backups o credenciales.

Los controles heredan los límites del cliente recuperado. No equivalen a una
auditoría integral o certificación Windows/Xbox 360.
