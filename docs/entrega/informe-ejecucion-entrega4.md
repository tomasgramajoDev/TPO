# Informe de ejecución — candidato Entrega 4

**Corte:** 16 de noviembre de 2026.
**Regla:** solo se marca PASS con evidencia observada; pendiente no significa aprobado.

## Resultados comprobados

- Back `00e0be1167180cf95d678a720915f3057652016c`: CI `43857225056`, 140 pruebas, repetición anti-flakiness, JaCoCo, SonarCloud, PIT, Gitleaks, Trivy y construcción Docker aprobados.
- SonarCloud: Quality Gate `OK`; sin vulnerabilidades ni hotspots abiertos en la candidata final.
- PIT: 53 mutaciones, 32 eliminadas, mutation score 60% y test strength 82%.
- Trivy Backend: 0 vulnerabilidades; Gitleaks: sin secretos.
- Front `4d1a885fe029c991a3f224a036622fae209baa41`: CI `43901973413`, 64 pruebas, cobertura global superior al 85%, lint, build, audit, repetición anti-flakiness, 7 E2E y contenedor aprobados. Incluye la regresión responsive a 768 px.
- `npm audit`: 0 Critical/High y tres Moderate en dependencias de desarrollo de Vitest.
- Tag `v2.0-entrega4`: gate `43890063632` verde sobre `fa1fb579f5a6d374a287fb5cc7bab4ed3e4fb692`, con clean start, health/login, Gitleaks, ZAP y k6.
- QA-14 Azure: ocho respuestas API por `/api` en el mismo origen, cero llamadas al Back directo, cero localhost y cero 4xx/5xx.
- Seguridad en vivo: JWT ausente, `alg=none` y firma alterada respondieron 401; CORS rechazó un origen ajeno con 403.
- Headers Front: CSP, HSTS, `nosniff`, `DENY`, COOP/COEP/CORP, Permissions-Policy y Referrer-Policy presentes.
- Última muestra de 69 líneas de logs Azure: cero tokens JWT, headers Authorization, passwords, DNI, stack traces o nivel ERROR detectados.
- M6–M3–Core: circuito principal, `containerDamaged` y `treeRiskDetected` confirmados.
- M1–M3–Core: `approved`, `rejected` y `publicWorksProjectCompleted` confirmados.
- M3–M7–Core: `roadAccidentRegistered` y circuito de cortes v1.1 hasta `ENDED` confirmados.
- M2–M3–Core: `ticketUpdated`, `STARTED`, dos `PROGRESS` y `RESOLVED` confirmados; el cierre `c889727e-db9e-4bd6-a064-7ff1ad5b32b6` fue aplicado por M2 y auditado por Core en un intento, sin retry ni DLQ.
- M7–M3–Core: además del circuito base y `roadAccidentRegistered`, quedaron confirmadas las variantes `REJECTED`, `ENDED` automático y `EXPIRED` sin `streetClosureEnded`.

## Candidata desplegada

| Componente | Imagen | Digest ACR |
| --- | --- | --- |
| Backend | `obras-publicas-backend:00e0be1167180cf95d678a720915f3057652016c` | `sha256:bae2abbf3e5fdacc7a60c8e5d8d2c39492c28415d7f18d1484e582ddb2e850b3` |
| Frontend | `obras-publicas-frontend:4d1a885fe029c991a3f224a036622fae209baa41` | `sha256:3e54ba11c35d30e761a9a1b436c4ed314241ff656e7d15533a4178f0ab3d418f` |

## Riesgos y pendientes reales

| ID | Severidad | Hallazgo | Estado/acción |
| --- | --- | --- | --- |
| E4-01 | Mayor | Sonar había señalado una posible desreferencia nula en `EventDispatcher`. | Cerrado en Backend PR #29; el CI final y el Quality Gate aprobaron. |
| E4-02 | Menor | ZAP reporta cuatro warnings: versión de servidor, cache, `style-src 'unsafe-inline'` y aplicación moderna. | Riesgo documentado; 0 High/Critical. |
| E4-03 | Menor | Tres vulnerabilidades Moderate en herramientas Vitest de desarrollo. | Riesgo documentado; 0 High/Critical y sin dependencia productiva afectada observada. |
| E4-04 | Mayor si la cátedra lo exige | El JWT no emitía ni validaba claim `iss`. | Cerrado en Backend PR #29; existen regresiones para expirado, firma alterada, `alg=none` e issuer incorrecto. |
| E4-05 | Externo | El cierre M2 y las variantes A/B/C de M7 requerían auditoría de Core. | Cerrado con evidencia de M2/M7/M3 y auditorías de Core del 16/11. |
| E4-06 | Operativo | La IP saliente de Azure no es estática y puede exigir cambios de allowlist en Core. | Evaluar VNet/NAT solo con aprobación de costo. |

## Actividades humanas pendientes

1. Repetir manualmente los casos afectados por la candidata final: corte válido/rango inválido, descripción de 301 y 1001 caracteres, rechazo con y sin motivo, responsive 768 y panel de Integraciones.
2. Actualizar el PDF QA con los SHAs, corridas y cierres externos definitivos; no reutilizar el resultado `55%` calculado sobre la candidata anterior.
3. Ensayo manual y exposición en vivo.
4. Subida final de evidencias a Teams y firma nominal de la declaración de IA.

## Conclusión

La candidata del tag `v2.0-entrega4` es reproducible y presentable. El gate final `43890063632` levantó el sistema desde cero y aprobó seguridad y carga. Las brechas técnicas que el paquete QA del 16/11 todavía presentaba como abiertas —Sonar, issuer JWT, M2 y M7— ya están cerradas; permanecen la reejecución manual sobre la candidata final, la firma/carga documental y la demo en vivo.
