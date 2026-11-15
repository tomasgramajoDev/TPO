# Evidencia de la candidata final — 2026-11-15

## Alcance y revisiones

- Backend: `1f2606e216ca6d9c59507b110a8f0647eee6e8a2`.
- Frontend: `d472da55fa5dca8f6c351a01805d35495f611486`.
- Infraestructura base auditada: `49a5a0d79a5191a62dd93a5588eb912fa24cf57f`.
- La candidata corrige `compose.yaml` para usar las mismas revisiones inmutables que Azure Test.

## Backend local

Comando ejecutado desde un worktree limpio y desacoplado:

```powershell
.\mvnw.cmd clean verify
```

Resultado observado:

- 132 pruebas ejecutadas.
- 0 fallos y 0 errores.
- 2 pruebas Testcontainers omitidas porque esta PC no tiene WSL y Docker Desktop no puede iniciar.
- JAR generado correctamente.
- JaCoCo: 90,56% de líneas y 72,24% de ramas.
- Todos los controles de cobertura configurados en Maven fueron aprobados.

Las dos pruebas omitidas no se presentan como aprobadas localmente. Deben ejecutarse en GitHub Actions, donde Docker está disponible; el gate remoto de la candidata es la evidencia autoritativa para Testcontainers y el arranque Compose.

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
- `npm audit` informó tres vulnerabilidades moderadas y ninguna crítica. Se conservan como riesgo conocido; el criterio eliminatorio prohíbe CVE críticas sin mitigar.

## Arranque reproducible

Se intentó ejecutar localmente `docker compose up --build -d --wait`, pero Docker Desktop devolvió que no podía iniciar. La verificación del host mostró que WSL no está instalado. No se modificó Windows ni se simuló un PASS.

El workflow `Testing release gates` ejecuta en Ubuntu:

1. Gitleaks sobre todo el historial.
2. Configuración efímera sin secretos persistidos.
3. `docker compose up --build -d --wait` desde un checkout limpio.
4. Health de Front, Back, PostgreSQL y login.
5. ZAP y rechazo de hallazgos High/Critical.
6. k6 con 50 usuarios durante cinco minutos en el tag de entrega.
7. Artefactos de diagnóstico y resultados.

La entrega no se considera recongelada hasta que ese workflow quede verde sobre el nuevo `v2.0-entrega4`.

## Integraciones incorporadas a la evidencia

- M6 principal: confirmado E2E.
- M1 `approved`: confirmado E2E.
- M1 `rejected`: confirmado E2E, sin DLQ y procesado por M3.
- M7 solicitud: entregada y procesada; respuesta y finalización pendientes.
- M2: pendiente de identificadores y confirmación bilateral.

## Limitaciones honestas

- La indisponibilidad de Docker local impide repetir Testcontainers y Compose en esta PC.
- Las confirmaciones funcionales de M2, M6 secundarios, M7 respuesta/cierre y M1 `publicWorksProjectCompleted` dependen de otros equipos.
- BOLA/IDOR y la demostración presencial continúan siendo actividades humanas.
