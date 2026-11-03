# Release candidata de testing — 2026-11-03

## Componentes promovidos

- Backend: `fe7c3370a7d98bddb1769cc47264370fceb8e8e8`.
- Frontend: `aec831cb89bc86f3188aefac8341829967ad7967`.

Las imágenes se construyen desde esos commits y se publican en ACR con etiquetas SHA inmutables. Terraform conserva las referencias exactas en la configuración de Test.

## Controles previos

- Frontend: lint, auditoría de dependencias, 58 pruebas unitarias, cobertura, build, seis E2E/accesibilidad y construcción Docker.
- Backend: 110 pruebas, repetición para detectar inestabilidad, mutation testing, SonarCloud, Gitleaks, Trivy y construcción Docker.
- SonarCloud del backend: sin bugs, vulnerabilidades ni code smells nuevos; Quality Gate aprobado en el PR.
- No se incorporaron secretos al repositorio.

## Cambios incluidos

- Headers HTTP de seguridad en Nginx del frontend.
- Acciones de GitHub fijadas por SHA en Front y Back.
- Validación segura de SQL permitido en migraciones Java.
- Corrección del posible `NullPointerException` del despachador de eventos.
- CSRF habilitado globalmente y omitido solo en la API JWT sin sesión y el health check.
- Eliminación del password generado por Spring de los logs de inicio.

## Validación posterior al despliegue

Después del `terraform apply` deben comprobarse:

1. `/api/health` con backend y PostgreSQL en estado saludable.
2. Login de las seis cuentas de demo.
3. Headers de seguridad servidos por el frontend.
4. ZAP sin hallazgos High o Critical.
5. Casos manuales y bilaterales todavía pendientes en la matriz de QA.
