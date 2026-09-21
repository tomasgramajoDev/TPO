# Operación DevOps

## Ambientes

El flujo GitFlow siguiente corresponde a los futuros pipelines de frontend y backend. Los workflows existentes en este repositorio administran la plataforma Terraform y conservan sus disparadores actuales hasta que se diseñe una estrategia de ramas específica para infraestructura.

| Ambiente | Disparador de aplicación acordado | Control de DevOps | Estado Terraform |
| --- | --- | --- | --- |
| `development` | Pull request de aplicación fusionado en `develop` | Autorización del despliegue y revisión de smoke tests | `development.terraform.tfstate` |
| `test` | Rama `release/vX.Y.Z` creada o actualizada al cerrar el sprint | Autorización del despliegue y revisión de smoke tests | `test.terraform.tfstate` |

La versión candidata se prueba en `test`; luego el Product Owner la aprueba funcionalmente. Esa aprobación no reemplaza el control operativo de DevOps. Al finalizar, la rama de release se fusiona en `main` y se etiqueta. `main` representa una versión aprobada, pero no despliega a producción mientras ese ambiente no exista.

Estado operativo al 2026-09-15:

- `development` ejecuta frontend, backend, PostgreSQL 16 y Event Grid en `Chile Central`;
- `test` ejecuta la release `v0.1.0` con las mismas imágenes inmutables verificadas en `development`;
- ambos ambientes tienen health checks y proxy `/api` verificados;
- los endpoints de consulta responden HTTP `200` con la base inicialmente vacía;
- después de las pruebas, PostgreSQL quedó intencionalmente `Stopped` en ambos ambientes para ahorrar crédito; debe iniciarse antes del próximo uso;
- la aceptación funcional del Product Owner y las suscripciones de eventos continúan pendientes.

## Recursos del primer incremento

Cada ambiente contiene:

- un resource group propio;
- un workspace de Log Analytics;
- un entorno Azure Container Apps con plan Consumption.

El bootstrap compartido crea:

- el resource group, Storage Account y contenedor privado para el estado remoto;
- los resource groups de `development` y `test`;
- un Azure Container Registry compartido;
- una identidad administrada para GitHub Actions;
- las credenciales federadas OIDC y los roles mínimos necesarios.

## Configuración requerida en GitHub

Crear los ambientes `development` y `test`, agregar al DevOps como revisor obligatorio y definir estas variables en cada ambiente o en el repositorio. Cada job que referencia el ambiente debe superar sus reglas, por lo que DevOps controla por separado el plan y el `apply`:

| Variable | Contenido |
| --- | --- |
| `AZURE_CLIENT_ID` | Client ID de la aplicación o identidad usada por GitHub Actions. |
| `AZURE_TENANT_ID` | Tenant ID de Microsoft Entra. |
| `AZURE_SUBSCRIPTION_ID` | Subscription ID de Azure. |
| `TF_STATE_RESOURCE_GROUP` | Resource group devuelto por el bootstrap. |
| `TF_STATE_STORAGE_ACCOUNT` | Storage account devuelto por el bootstrap. |
| `TF_STATE_CONTAINER` | Contenedor devuelto por el bootstrap; valor predeterminado `tfstate`. |
| `AZURE_CONTAINER_REGISTRY` | Login server del registro compartido, reservado para el pipeline de aplicaciones. |

`ENABLE_AUTOMATIC_DEPLOYMENTS` está configurada en `true` para los workflows Terraform actuales. Un merge a `main` o una release publicada pueden iniciar el flujo de plataforma, pero los jobs de plan y `apply` permanecen bloqueados por la aprobación del environment y conservan la autoridad operativa de DevOps. Esto no define los disparadores de las aplicaciones: al recibir frontend y backend se implementarán con `develop` para `development` y `release/*` para `test`.

Estos identificadores no son contraseñas. No se debe crear `AZURE_CLIENT_SECRET`.

Los revisores obligatorios de ambientes privados requieren un plan GitHub compatible; en GitHub Free están disponibles para repositorios públicos. Si DevOps es la única persona autorizada, no se debe activar `Prevent self-review`.

## Identidad federada

El bootstrap crea una identidad administrada y una credencial federada por environment de GitHub. El subject debe corresponder exactamente a cada ambiente:

- `repo:tomasgramajoDev/TPO:environment:development`
- `repo:tomasgramajoDev/TPO:environment:test`

La identidad recibe `Contributor` solamente en los resource groups de ambos ambientes, `Storage Blob Data Contributor` sobre el Storage Account de estado y `AcrPush` sobre el registro de contenedores. No recibe permisos generales sobre toda la suscripción.

## Secuencia de puesta en marcha

1. Activar Azure for Students o una suscripción equivalente.
2. Crear el repositorio GitHub y subir esta base.
3. Definir `github_repository` y ejecutar una vez `infra/terraform/bootstrap` con una sesión Azure administrativa.
4. Migrar el estado local del bootstrap al backend Azure creado.
5. Configurar variables y revisores de los ambientes GitHub con los outputs del bootstrap.
6. Ejecutar el workflow de desarrollo para verificar acceso y desplegar la plataforma inicial. Completado el 2026-08-13.
7. Publicar las imágenes inmutables de las aplicaciones y desplegarlas en `development`. Completado el 2026-09-15.
8. Crear `release/v0.1.0`, integrar la versión en `main`, publicar la release de infraestructura y ejecutar el workflow de `test`. Completado el 2026-09-15.
9. Obtener la aceptación funcional del Product Owner antes de considerar cerrada la release.

## Reglas operativas

### Cuentas de demostración de Test

El environment `test` de GitHub conserva el secreto `TEST_BOOTSTRAP_USERS` con un array JSON de seis cuentas, que se entrega a Terraform como variable sensible y a Container Apps como `AUTH_BOOTSTRAP_USERS`. El archivo privado de origen no se sube a Git. El backend con Flyway V4 crea solamente cuentas faltantes: cambiar este secreto no modifica contraseñas ni roles persistidos. El workflow intenta reiniciar la revisión activa; Azure puede rechazar ese reinicio con un error interno, por lo que el criterio definitivo es el health y los seis logins a través del frontend. En la ejecución `35615302917` del 2026-09-21 los seis ingresaron: las cinco cuentas ya persistidas con la contraseña anterior de `TEST_DEMO_PASSWORD` y la nueva `ingeniero.arquitecto` con la contraseña de `users.json`. No se debe entregar una contraseña única del JSON para las seis cuentas: las existentes no se rotaron.

Esos seis logins fueron solicitudes `curl` a través del proxy del Front, **no** sesiones abiertas desde el navegador. La prueba exploratoria posterior detectó que el navegador envía `Origin` y recibía HTTP 403. Terraform fija `CORS_ALLOWED_ORIGINS` al origen público exacto del Front de Test; si cambia el FQDN, se debe actualizar ese valor. El smoke test del pipeline ahora envía el encabezado `Origin` para detectar este fallo, pero la aceptación funcional sigue requiriendo probar las pantallas.

- Revisar el archivo de plan generado antes de aprobar el job `apply`.
- No ejecutar `terraform apply` simultáneamente sobre el mismo ambiente.
- No guardar `.tfstate`, `.tfvars` reales, tokens ni contraseñas en Git.
- Los cambios manuales de emergencia deben documentarse y reconciliarse de inmediato en Terraform.
- Destruir recursos es una acción excepcional y requiere revisar el plan y el ambiente objetivo.
- Al terminar una sesión de pruebas, detener PostgreSQL en `development` y `test`; Container Apps mantiene mínimo de cero réplicas. Volver a iniciar las bases antes del próximo uso. Azure inicia automáticamente cada Flexible Server después de siete días detenido, por lo que DevOps debe volver a apagarlo si aún no se usa.

## Definition of Done DevOps propuesta

La Clase 2 presenta una Definition of Done general y otra estricta. Para este proyecto se propone que una historia solo pueda promoverse cuando:

- cumple sus criterios de aceptación;
- las pruebas unitarias, funcionales y de integración aplicables están aprobadas;
- el cambio fue revisado por pares mediante pull request;
- se cumplieron los requisitos no funcionales definidos;
- la documentación técnica fue actualizada;
- cualquier configuración manual posterior al despliegue está identificada;
- el release incluye notas de versión cuando corresponda;
- el Product Owner aceptó la historia.

Estos criterios están `PROPOSED` hasta que el equipo adopte formalmente su Definition of Done. El ejemplo docente de desplegar a producción con el feature toggle desactivado no se aplica todavía: el ambiente de producción y la estrategia de feature flags continúan pendientes.
