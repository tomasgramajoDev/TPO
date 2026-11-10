# API, OpenAPI y SOAP — Entrega 4

- El Back publica OpenAPI en `/v3/api-docs` y Swagger UI en `/swagger-ui.html` cuando la configuración del ambiente los habilita.
- El contrato REST incluye JWT Bearer, códigos HTTP, `Idempotency-Key`, `ETag`/`If-Match` y errores `application/problem+json`.
- La API se consume desde el Front mediante rutas relativas `/api/...` a través del proxy.
- M3 no utiliza SOAP en su alcance vigente; por lo tanto no existe WSDL propio. La consigna indica que WSDL solo aplica a los módulos que usan SOAP.
- Los eventos asincrónicos se documentan mediante envelope de Core y JSON Schema, no mediante WSDL.
