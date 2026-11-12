# Cierre Git de la Entrega 4

**Fecha:** 12/11/2026  
**Alcance:** referencias inmutables de la versión desplegada y evidencia de cierre. No contiene secretos.

## Tags

El tag académico histórico `v1.0-testing` se conserva sin reescribir. Como la aplicación evolucionó después de su creación, se agregó `v1.0-testing-final` en cada repositorio para identificar los commits finales efectivamente usados por la entrega.

La cátedra exige además `v2.0-entrega4` en `main` y no considera commits posteriores. El 12/11 se actualizó esa referencia al cierre vigente, antes de la clase. El destino anterior no se perdió: quedó preservado como `v2.0-entrega4-original-2026-11-10`.

| Repositorio | Rama estable | Tag final | Commit |
| --- | --- | --- | --- |
| Backend | `develop` | `v1.0-testing-final` | `89524a530b946590c490e2d0d5d001f74a4f2d6e` |
| Frontend | `main` | `v1.0-testing-final` | `307f3eec55358be7b10f57878304c4996312fdf2` |
| Infraestructura | release desplegada | `v1.0-testing-final` | `21a55f796e511a19dc622c551aa6733fe471e8a9` |

No se movió ni eliminó ningún tag anterior. Esto conserva la auditoría y evita presentar un tag reescrito como si fuera histórico.

## Release y despliegue

- Release: `v2.0-entrega4.3-gemini`.
- Backend desplegado: imagen inmutable `89524a530b946590c490e2d0d5d001f74a4f2d6e`.
- Frontend final: `307f3eec55358be7b10f57878304c4996312fdf2`.
- Workflow de despliegue: `43146512964`.
- Terraform: `0` altas, `2` cambios en sitio y `0` bajas.
- Mensajería Core: habilitada; `module_obras` reconectó por AMQPS al vhost `/core`.
- Gemini: activo en Azure Test mediante secreto protegido, sin almacenar la clave en Git.

## Controles aprobados

- CI de Frontend, Backend e Infraestructura.
- SonarCloud y umbrales JaCoCo.
- Análisis de secretos y dependencias.
- Pruebas unitarias, integración, E2E, accesibilidad y responsive.
- Smoke test, seis logins y health de PostgreSQL.
- Verificación live de Gemini, autorización por roles y entrada adversarial sin PII en la salida.
- Integraciones E2E M6-M3-Core y M1-M3-Core para el escenario `approved`.

## Trabajo externo o manual pendiente

- Cierre documental y evidencias finales a cargo de Testing.
- Variante M1 `rejected`.
- Pruebas bilaterales M2 y M7.
- TC-022 y TC-024 coordinados con Core.
- BOLA/IDOR en vivo o aclaración pública de la cátedra.
- JWT firmado/validado con M1 y catálogo final de eventos de Core.
- Carga en Teams y demo/defensa en vivo.

El detalle vigente está en `docs/decisiones/decisiones-pendientes.md`.
