# Pipeline de frontend y backend

## Estado

Diseño preparado, implementación bloqueada hasta conocer los repositorios y el stack de las aplicaciones.

El pipeline Terraform crea la plataforma. El pipeline de aplicación deberá construir y desplegar frontend y backend cuando cada repositorio entregue los siguientes datos:

- URL y visibilidad del repositorio;
- lenguaje y versión;
- comando de instalación;
- comando de pruebas;
- comando de build;
- ruta del `Dockerfile` y contexto Docker;
- puerto interno;
- endpoint de health check;
- variables públicas y secretos requeridos.

## Flujo acordado

### Pull request

1. Instalar dependencias con versiones bloqueadas.
2. Ejecutar lint y pruebas.
3. Construir la aplicación.
4. Construir la imagen Docker sin publicarla.
5. Bloquear el merge si falla una validación obligatoria.

### Merge a main

1. Repetir las validaciones.
2. Construir una imagen etiquetada con el SHA del commit.
3. Publicarla en Azure Container Registry.
4. Resolver y registrar su digest inmutable.
5. Esperar autorización de DevOps.
6. Desplegar ese digest en `development`.
7. Ejecutar un smoke test y registrar el resultado.

### Release

1. Seleccionar el digest que ya funcionó en `development`.
2. No reconstruir la imagen.
3. Esperar autorización de DevOps.
4. Promover el mismo digest a `test`.
5. Ejecutar smoke tests y registrar la versión desplegada.

## Responsabilidades

- Frontend/backend mantienen sus pruebas, build, `Dockerfile` y health check.
- DevOps mantiene Azure, Terraform, permisos, environments, workflows, observabilidad, promoción y rollback.
- El PO aprueba funcionalmente la release; esa aprobación no reemplaza la autorización operativa de DevOps.

## Decisiones pendientes

- Repositorios definitivos de frontend y backend.
- Stack y comandos de build/test.
- Base de datos y estrategia de migraciones.
- Servicio de mensajería.
- Gestión de secretos de las aplicaciones.
- Health checks y criterios de rollback.
