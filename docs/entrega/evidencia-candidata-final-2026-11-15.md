# Evidencia de la candidata final — 2026-11-15

## Alcance y revisiones

- Backend: `1f2606e216ca6d9c59507b110a8f0647eee6e8a2`.
- Frontend: `d472da55fa5dca8f6c351a01805d35495f611486`.
- Infraestructura base auditada: `49a5a0d79a5191a62dd93a5588eb912fa24cf57f`.
- La candidata corrige `compose.yaml` para usar las mismas revisiones inmutables que Azure Test.

## Azure Test verificado el 2026-11-15

La consulta de solo lectura a Azure Container Apps y ACR confirmó:

| Componente | Revisión activa | Imagen | Digest ACR | Estado |
| --- | --- | --- | --- | --- |
| Backend | `ca-obras-publicas-tst-backend--latest` | `obras-publicas-backend:1f2606e216ca6d9c59507b110a8f0647eee6e8a2` | `sha256:86462cd76e05bcd4b9479e235e90045b0bd336b1b2cf188bfa16ec0e05d7a5f2` | `Provisioned`, `Healthy`, 100% del tráfico |
| Frontend | `ca-obras-publicas-tst-frontend--latest` | `obras-publicas-frontend:d472da55fa5dca8f6c351a01805d35495f611486` | `sha256:03d3d87ab84081a64a14ed45f1b655cfa890c7e988244b5f91342337d7e35247` | `Running`, 1 réplica al verificar, 100% del tráfico |

El health público del Backend y la raíz pública del Frontend respondieron HTTP 200. Los tags de las imágenes coinciden exactamente con los commits finales; ACR aporta el vínculo inmutable mediante sus digests.

## CI de las revisiones desplegadas

- Backend CI `43415380427`: `success` sobre `1f2606e216ca6d9c59507b110a8f0647eee6e8a2`. Incluyó Maven, SonarCloud, repetición anti-flakiness, PIT, Gitleaks, Trivy y construcción del contenedor.
- Frontend CI `43130876805`: `success` sobre `d472da55fa5dca8f6c351a01805d35495f611486`. Incluyó auditoría, lint, cobertura, repetición, build, Playwright, accesibilidad y construcción del contenedor.

## Backend local

Comando ejecutado desde un worktree limpio y desacoplado:

```powershell
.\mvnw.cmd clean verify
```

Resultado observado:

- 132 pruebas ejecutadas.
- 0 fallos, 0 errores y 0 omitidas.
- Las pruebas con Testcontainers detectaron Docker Desktop y levantaron PostgreSQL 17 real; las 12 migraciones Flyway se aplicaron correctamente.
- JAR generado correctamente.
- JaCoCo: 90,56% de líneas y 72,24% de ramas.
- Todos los controles de cobertura configurados en Maven fueron aprobados.

Esta repetición local elimina la limitación que existía durante la construcción aislada de la imagen, donde el socket de Docker no estaba expuesto. El gate remoto de la candidata conserva la evidencia autoritativa de CI.

## Frontend local

Comandos ejecutados desde un worktree limpio y desacoplado:

```powershell
npm ci
npm run test:coverage
npm run build
```

Resultado observado:

- 7 archivos de prueba aprobados.
- 63 pruebas aprobadas.
- 85,55% de líneas, 85,34% de sentencias y 75,84% de ramas.
- Build Vite de producción aprobado.
- Lint aprobado.
- 6 pruebas E2E Playwright aprobadas, incluida accesibilidad sin hallazgos serios o críticos.
- Lighthouse local sobre la imagen candidata: Performance 100, Accessibility 100, Best Practices 100 y SEO 82.
- Capturas verificadas a 360, 768 y 1280 px sin desbordes ni cortes visibles en la pantalla de ingreso.
- `npm audit` informó tres vulnerabilidades moderadas en dependencias de desarrollo y ninguna vulnerabilidad de producción con `npm audit --omit=dev`. Se conservan como riesgo conocido; no hay CVE crítica observada.

## Arranque reproducible

Se instaló Ubuntu 24.04 LTS sobre WSL 2, se reinició Docker Desktop y se verificó el daemon con `hello-world`. Después se ejecutó localmente, desde esta candidata:

```powershell
docker compose up --build -d --wait
```

Resultado observado:

- Frontend, Backend, PostgreSQL y RabbitMQ quedaron `Healthy`.
- Front respondió HTTP 200 en `/health`.
- Back respondió HTTP 200 en `/api/health`, con `database=up`.
- El build del Backend ejecutó 132 pruebas sin fallos; la repetición directa posterior ejecutó también las pruebas Testcontainers sin omisiones.
- El login real de `personal.obras` respondió correctamente con rol `PERSONAL_OBRAS` y access token presente.
- El `.env` utilizado es local, está ignorado por Git y no contiene credenciales de Azure/Core.

El workflow `Testing release gates` ejecuta en Ubuntu:

1. Gitleaks sobre todo el historial.
2. Configuración efímera sin secretos persistidos.
3. `docker compose up --build -d --wait` desde un checkout limpio.
4. Health de Front, Back, PostgreSQL y login.
5. ZAP y rechazo de hallazgos High/Critical.
6. k6 con 50 usuarios durante cinco minutos en el tag de entrega.
7. Artefactos de diagnóstico y resultados.

El gate final del tag `v2.0-entrega4`, ejecución `43737147567`, quedó en `success`. La repetición local confirma además el arranque reproducible en Windows/WSL 2.

## Integraciones incorporadas a la evidencia

- M6 principal: confirmado E2E.
- M6 `containerDamaged` y `treeRiskDetected`: entrega y procesamiento confirmados; el duplicado fue descartado por Core antes de llegar al Inbox de M3.
- M1 `approved`: confirmado E2E.
- M1 `rejected`: confirmado E2E, sin DLQ y procesado por M3.
- M1 `publicWorksProjectCompleted`: confirmado E2E para `OBRA-3`.
- M7 solicitud: entregada y procesada; respuesta y finalización pendientes.
- M7 `roadAccidentRegistered`: publicado por M7; faltan confirmación de Core y procesamiento de M3.
- M2: pendiente de identificadores y confirmación bilateral.

## Limitaciones honestas

- La etapa interna del Dockerfile no expone el socket Docker, pero la repetición directa con Docker Desktop ejecutó las 132 pruebas, incluidos los smoke Testcontainers, sin omisiones.
- La deduplicación probada para `containerDamaged` corresponde a Core, no al Inbox de M3, porque Core descartó el duplicado antes de una segunda entrega.
- Las confirmaciones funcionales de M2, M7 respuesta/cierre y `roadAccidentRegistered` dependen de otros equipos.
- BOLA/IDOR y la demostración presencial continúan siendo actividades humanas.
