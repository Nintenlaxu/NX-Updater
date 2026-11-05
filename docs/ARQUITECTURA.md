# Integración U10

`client-java/` contiene el updater recuperado de U09, su pantalla, pruebas y
compilador del parche. Se aplican solo estas clases al JAR U09. Las clases de
combate, menús restantes, LAN y SDL se preservan byte a byte.

`repository=Nintenlaxu/NX-Updater` identifica el control privado previsto.
`distributionRepository=` queda vacío. U10 informa distribución pendiente
y evita consultas anónimas al control privado. Cuando el campo no existe en
instalaciones antiguas se conserva el comportamiento original de `repository`.

El contrato real usa RSA SHA-256. La firma cubre los bytes exactos del manifiesto
y cada archivo lleva SHA-256, tamaño y acción ADD/REPLACE/DELETE. PATCH exige
versión base exacta. Se comprueba plataforma, canal, protocolo y dependencias.

La instalación sigue usando el proceso externo original con respaldo y
recuperación. El juego bloquea instalar mientras hay combate o sala conectada.
Los cambios U10 no alteran ese control ni el protocolo LAN.

Sin clave pública oficial y feed accesible el juego funciona y el updater
informa qué falta. No se incorpora PAT, clave privada o clave de prueba oficial.
C++ y Xbox 360 continúan pendientes de integración específica y validación.
