# ADR-001 — Cloud y plataforma CI/CD

- Estado: aceptada.
- Fecha: 2026-08-11.
- Responsable: DevOps.

## Contexto

La consigna permite elegir las tecnologías y exige frontend, backend, base de datos independiente, integración asíncrona, autenticación, pruebas y un despliegue accesible. El proyecto necesita dos ambientes iniciales, costos controlados y una infraestructura reproducible.

## Decisión

- Cloud: Microsoft Azure.
- Región inicial: `Brazil South`.
- Infraestructura como código: Terraform `1.15.8` con AzureRM `~> 4.81`.
- Cómputo inicial: Azure Container Apps Consumption.
- Observabilidad base: Log Analytics por ambiente.
- Estado remoto: Azure Blob Storage mediante Microsoft Entra ID.
- CI/CD: GitHub Actions.
- Autenticación del pipeline: OIDC con credenciales federadas, sin secretos de cliente persistentes.
- Ambientes: `development` y `test`, en resource groups separados.
- Control: cada ambiente de GitHub requiere aprobación de DevOps antes del `terraform apply`.

## Justificación

Azure for Students ofrece crédito académico sin requerir tarjeta de crédito. Container Apps admite contenedores de cualquier stack, plan Consumption y escala a cero, por lo que permite empezar con bajo consumo sin decidir todavía el lenguaje del backend. `Brazil South` reduce distancia respecto del equipo en Argentina y soporta la plataforma elegida.

Terraform permite versionar y revisar la infraestructura. OIDC evita guardar credenciales Azure de larga duración en GitHub.

## Alternativas consideradas

- AWS: ecosistema amplio y hasta USD 200 en créditos para cuentas nuevas, pero el plan gratuito inicial dura hasta seis meses y la plataforma equivalente requiere más decisiones operativas para este TPO.
- Google Cloud: Cloud Run es una alternativa simple y el trial ofrece USD 300 por 90 días, pero el beneficio dura menos que Azure for Students.

## Consecuencias

- El equipo necesita una suscripción Azure activa y un repositorio GitHub antes del primer despliegue real.
- La identidad OIDC y los ambientes protegidos se configuran una sola vez.
- El primer incremento crea la plataforma de ejecución y observabilidad, no la aplicación.
- Base de datos, mensajería, autenticación, registro de contenedores y producción se decidirán cuando el stack y los contratos estén listos.

## Referencias

- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
- [Escalado de Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/scale-app)
- [OIDC desde GitHub Actions hacia Azure](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect)
- [Backend `azurerm` de Terraform](https://developer.hashicorp.com/terraform/language/backend/azurerm)
