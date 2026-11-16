# Informe de ejecución — candidato Entrega 4

**Corte:** 15 de noviembre de 2026.  
**Regla:** solo se marca PASS con evidencia observada; pendiente no significa aprobado.

## Resultados comprobados

- Back `a33873a56e25fb3406c1fcc11dfae5be71c8b0eb`: CI `43768127963`, 133 pruebas repetidas tres veces, 0 fallos, 0 errores y 0 omitidas.
- SonarCloud: Quality Gate `OK`, coverage 85,4%, líneas 90,7%, ramas 72,8%, 0 vulnerabilidades y 0 hotspots.
- PIT: 53 mutaciones, 32 eliminadas, mutation score 60% y test strength 82%.
- Trivy Backend: 0 vulnerabilidades; Gitleaks: sin secretos.
- Front `918ce5d9a3b35f8fec091fe1fbbd0ccfa9af5dc0`: CI `43750629674`, 63 pruebas repetidas tres veces, 6 E2E, 85,55% de líneas y 75,84% de ramas.
- `npm audit`: 0 Critical/High y tres Moderate en dependencias de desarrollo de Vitest.
- PR TPO #77: gate `43779877210` verde con clean start, health/login, Gitleaks, ZAP y k6 sobre las mismas revisiones de Azure Test.
- QA-14 Azure: ocho respuestas API por `/api` en el mismo origen, cero llamadas al Back directo, cero localhost y cero 4xx/5xx.
- Seguridad en vivo: JWT ausente, `alg=none` y firma alterada respondieron 401; CORS rechazó un origen ajeno con 403.
- Headers Front: CSP, HSTS, `nosniff`, `DENY`, COOP/COEP/CORP, Permissions-Policy y Referrer-Policy presentes.
- Última muestra de 69 líneas de logs Azure: cero tokens JWT, headers Authorization, passwords, DNI, stack traces o nivel ERROR detectados.
- M6–M3–Core: circuito principal, `containerDamaged` y `treeRiskDetected` confirmados.
- M1–M3–Core: `approved`, `rejected` y `publicWorksProjectCompleted` confirmados.
- M3–M7–Core: `roadAccidentRegistered` y circuito de cortes v1.1 hasta `ENDED` confirmados.
- M2–M3: `ticketUpdated` y dos `PROGRESS` aplicados; el cierre completo continúa pendiente.

## Candidata desplegada

| Componente | Imagen | Digest ACR |
| --- | --- | --- |
| Backend | `obras-publicas-backend:a33873a56e25fb3406c1fcc11dfae5be71c8b0eb` | `sha256:b58d6fe7cfe3a678a280aef92e093b0bff32fe6bcfbbfc901f1ef9fb85a2a5dd` |
| Frontend | `obras-publicas-frontend:918ce5d9a3b35f8fec091fe1fbbd0ccfa9af5dc0` | `sha256:3b84fbb1bc07f87562b77dc33659f14dd76cc0c727c2caab7a3d65d3e11adfb6` |

## Riesgos y pendientes reales

| ID | Severidad | Hallazgo | Estado/acción |
| --- | --- | --- | --- |
| E4-01 | Mayor | Sonar mantiene un bug Major en `EventDispatcher.java:27` por posible `NullPointerException`; reliability rating C. | Abierto. Backend debe analizar y corregir o justificar con evidencia. |
| E4-02 | Menor | ZAP reporta cuatro warnings: versión de servidor, cache, `style-src 'unsafe-inline'` y aplicación moderna. | Riesgo documentado; 0 High/Critical. |
| E4-03 | Menor | Tres vulnerabilidades Moderate en herramientas Vitest de desarrollo. | Riesgo documentado; 0 High/Critical y sin dependencia productiva afectada observada. |
| E4-04 | Mayor si la cátedra lo exige | El JWT no emite ni valida claim `iss`. | No declarar issuer incorrecto como PASS; decidir con Backend si se incorpora. |
| E4-05 | Externo | M2 aún debe confirmar `RESOLVED` y Core debe confirmar entrega/DLQ del hilo M2. | Esperar evidencia externa, sin inventar cierre. |
| E4-06 | Operativo | La IP saliente de Azure no es estática y puede exigir cambios de allowlist en Core. | Evaluar VNet/NAT solo con aprobación de costo. |

## Actividades humanas pendientes

1. TC-030, TC-031, carga de Jira y prueba de usabilidad, asignadas a QA.
2. Ensayo manual y exposición en vivo.
3. Confirmación externa restante del circuito M2.
4. Subida final de evidencias a Teams y firma nominal de la declaración de IA.

## Conclusión

Azure Test y el `compose.yaml` reproducible quedaron alineados a las mismas revisiones inmutables mediante PR #77, con gate verde antes del merge. La candidata técnica es reproducible y presentable, pero no se declara “perfecta”: conserva el bug Major de Sonar, el issuer JWT no implementado y actividades QA/humanas pendientes.
