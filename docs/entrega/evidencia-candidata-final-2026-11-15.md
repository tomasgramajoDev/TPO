# Evidencia de la candidata final — actualización 15/11/2026

## Revisiones vigentes

- Backend desplegado: `a33873a56e25fb3406c1fcc11dfae5be71c8b0eb`.
- Frontend desplegado: `918ce5d9a3b35f8fec091fe1fbbd0ccfa9af5dc0`.
- Infraestructura desplegada: `00b3b316a60b11fa7256d44dd4ff4dd4473755c0`, release `v2.0-entrega4.7-m7-rfc3339`.
- `compose.yaml` alineado a esas revisiones por PR #77, merge `25d56302320b56ebdf3aae6dc2b90e0bfe5de24b`.

La candidata histórica basada en Back `1f2606e…` y Front `d472da5…` fue reemplazada por correcciones posteriores de integración. Se conserva su evidencia en el historial, pero no se presenta como el estado actual de Azure.

## Azure Test y ACR

| Componente | Revisión | Imagen | Digest ACR |
| --- | --- | --- | --- |
| Backend | `ca-obras-publicas-tst-backend--latest` | `obras-publicas-backend:a33873a56e25fb3406c1fcc11dfae5be71c8b0eb` | `sha256:b58d6fe7cfe3a678a280aef92e093b0bff32fe6bcfbbfc901f1ef9fb85a2a5dd` |
| Frontend | `ca-obras-publicas-tst-frontend--latest` | `obras-publicas-frontend:918ce5d9a3b35f8fec091fe1fbbd0ccfa9af5dc0` | `sha256:3b84fbb1bc07f87562b77dc33659f14dd76cc0c727c2caab7a3d65d3e11adfb6` |

Backend `/api/health` respondió HTTP 200 con base de datos `up`; el Front respondió HTTP 200. Los tags de ACR coinciden con los commits y los digests identifican el contenido inmutable.

## CI vigente

- Backend `43768127963`: 133 pruebas repetidas tres veces, sin fallos; Quality Gate aprobado; JaCoCo, PIT, Gitleaks, Trivy y contenedor aprobados.
- Frontend `43750629674`: 63 pruebas repetidas tres veces, coverage, build, 6 E2E, accesibilidad y contenedor aprobados.
- TPO PR #77 `43779877210`: arranque limpio de la candidata alineada, health/login, Gitleaks, ZAP sin High/Critical y k6 aprobados.

## Métricas y seguridad

- SonarCloud: Quality Gate `OK`, coverage 85,4%, líneas 90,7%, ramas 72,8%, 0 vulnerabilidades y 0 hotspots. Mantiene un bug Major abierto en `EventDispatcher.java:27` y reliability rating C.
- PIT: 53 mutaciones, 32 eliminadas (60%); test strength 82%.
- Trivy Backend: 0 vulnerabilidades en `pom.xml`.
- Front `npm audit`: 0 Critical/High y 3 Moderate en dependencias de desarrollo de Vitest.
- ZAP: 0 High/Critical y cuatro warnings no bloqueantes.
- JWT en Azure: sin token, `alg=none` y firma alterada respondieron 401. El vencimiento está cubierto por prueba automatizada. No se declara prueba de issuer incorrecto porque el Backend no emite ni valida `iss`.
- CORS: el origen real del Front fue aceptado; un origen ajeno fue rechazado con 403.
- QA-14: ocho respuestas API por `/api` en el mismo origen, cero llamadas al Backend directo, cero localhost y cero 4xx/5xx.

## Integraciones incorporadas

- M6 principal, `containerDamaged` y `treeRiskDetected`.
- M1 `approved`, `rejected` y `publicWorksProjectCompleted`.
- M7 `roadAccidentRegistered` y circuito de cortes v1.1 hasta `ENDED`.
- M2: entrada `ticketUpdated` y dos `PROGRESS` confirmados; falta confirmación de `RESOLVED` por M2 y transporte/DLQ por Core.

## Limitaciones honestas

- La deduplicación de `containerDamaged` quedó probada en Core, no en el Inbox de M3.
- El bug Major abierto de Sonar debe asignarse a Backend y verificarse antes de congelar si el equipo decide corregirlo.
- TC-030, TC-031, Jira y usabilidad permanecen en el alcance de QA y no se duplican en esta evidencia DevOps.
