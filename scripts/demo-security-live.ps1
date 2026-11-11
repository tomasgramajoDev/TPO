param(
    [string]$BaseUrl = $env:TEST_BASE_URL,
    [string]$Username = $env:TEST_LOW_ROLE_USERNAME,
    [string]$Password = $env:TEST_LOW_ROLE_PASSWORD
)

$ErrorActionPreference = 'Stop'

function Require-Value([string]$Name, [string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) {
        throw "Falta $Name. Configurarlo como variable de entorno; no escribir secretos en el script."
    }
}

function Invoke-Status {
    param(
        [ValidateSet('GET', 'POST')][string]$Method,
        [string]$Uri,
        [hashtable]$Headers = @{},
        [string]$Body
    )

    $args = @{
        Uri = $Uri
        Method = $Method
        Headers = $Headers
        SkipHttpErrorCheck = $true
        TimeoutSec = 30
    }
    if ($PSBoundParameters.ContainsKey('Body')) {
        $args.ContentType = 'application/json'
        $args.Body = $Body
    }
    Invoke-WebRequest @args
}

function Assert-Status([string]$Name, $Response, [int[]]$Expected) {
    if ($Expected -notcontains [int]$Response.StatusCode) {
        throw "$Name fallo: HTTP $($Response.StatusCode), esperado $($Expected -join '/')"
    }
    Write-Host "PASS $Name -> HTTP $($Response.StatusCode)"
}

Require-Value 'TEST_BASE_URL' $BaseUrl
Require-Value 'TEST_LOW_ROLE_USERNAME' $Username
Require-Value 'TEST_LOW_ROLE_PASSWORD' $Password
$BaseUrl = $BaseUrl.TrimEnd('/')

Write-Host 'Pruebas seguras y no destructivas de la Entrega 4'

$health = Invoke-Status GET "$BaseUrl/api/health"
Assert-Status 'Health' $health @(200)

$openApi = Invoke-Status GET "$BaseUrl/v3/api-docs"
Assert-Status 'OpenAPI' $openApi @(200)

$withoutSession = Invoke-Status GET "$BaseUrl/api/public-works/projects"
Assert-Status 'Sin sesion' $withoutSession @(401)

$invalidJwt = Invoke-Status GET "$BaseUrl/api/public-works/projects" @{ Authorization = 'Bearer token-invalido' }
Assert-Status 'JWT invalido' $invalidJwt @(401)

$loginBody = @{ username = $Username; password = $Password } | ConvertTo-Json -Compress
$login = Invoke-Status POST "$BaseUrl/api/auth/login" @{} $loginBody
Assert-Status 'Login rol bajo' $login @(200)
$loginJson = $login.Content | ConvertFrom-Json
Require-Value 'accessToken de login' $loginJson.accessToken
$auth = @{ Authorization = "Bearer $($loginJson.accessToken)" }

$bfla = Invoke-Status POST "$BaseUrl/api/public-works/projects" $auth '{}'
Assert-Status 'BFLA: rol bajo no crea proyectos' $bfla @(403)

$encodedInjection = [uri]::EscapeDataString("' OR 1=1 --")
$injection = Invoke-Status GET "$BaseUrl/api/public-works/projects?search=$encodedInjection&page=0&size=5" $auth
Assert-Status 'Busqueda con entrada de inyeccion' $injection @(200)
if ($injection.Content -match '(?i)(sqlstate|syntax error|stack trace|exception)') {
    throw 'La respuesta expuso un error interno ante la entrada de inyeccion.'
}

$randomUser = "qa-$([guid]::NewGuid().ToString('N'))"
$statuses = @()
1..4 | ForEach-Object {
    $body = @{ username = $randomUser; password = 'incorrecta-para-prueba' } | ConvertTo-Json -Compress
    $response = Invoke-Status POST "$BaseUrl/api/auth/login" @{} $body
    $statuses += [int]$response.StatusCode
}
if ($statuses -notcontains 429) {
    throw "Fuerza bruta fallo: no aparecio HTTP 429. Estados: $($statuses -join ',')"
}
Write-Host "PASS Fuerza bruta -> $($statuses -join ',')"

Write-Host ''
Write-Host 'Resultado: controles automatizables aprobados.'
Write-Host 'MANUAL: BOLA/IDOR debe usar dos recursos o identidades reales elegidos para la demo.'
Write-Host 'MANUAL: mass assignment debe ejecutarse con un payload valido controlado y comprobar que no haya mutacion.'
