param(
    [string]$BaseUrl = "https://ca-obras-publicas-dev-frontend.victoriousground-b333790d.chilecentral.azurecontainerapps.io"
)

$ErrorActionPreference = "Stop"
$apiBase = $BaseUrl.TrimEnd('/') + "/api"

function Invoke-DemoJson {
    param(
        [Parameter(Mandatory = $true)][string]$Method,
        [Parameter(Mandatory = $true)][string]$Uri,
        [object]$Body
    )

    $parameters = @{
        Method     = $Method
        Uri        = $Uri
        TimeoutSec = 120
    }

    if ($null -ne $Body) {
        $parameters.ContentType = "application/json; charset=utf-8"
        $parameters.Body = $Body | ConvertTo-Json -Depth 10
    }

    Invoke-RestMethod @parameters
}

function Show-Step {
    param([string]$Title, [object]$Order)
    Write-Host ("{0,-22} id={1} estado={2}" -f $Title, $Order.id, $Order.status) -ForegroundColor Cyan
}

Write-Host "Demo: ciclo completo de una orden de trabajo" -ForegroundColor Green
Write-Host "Ambiente: $BaseUrl"

$health = Invoke-DemoJson -Method Get -Uri "$apiBase/health"
if ($health.status -ne "ok" -or $health.database -ne "up") {
    throw "El ambiente no esta listo: status=$($health.status), database=$($health.database)"
}
Write-Host "Health comprobado: aplicacion ok, PostgreSQL up" -ForegroundColor Green

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$order = Invoke-DemoJson -Method Post -Uri "$apiBase/public-works/work-orders" -Body @{
    sourceRequestId       = "demo-oral-$stamp"
    origin                = "MANUAL"
    description           = "Reparar bache detectado durante la demo oral"
    interventionType      = "BACHEO"
    location              = "Calle Demo 123"
    priority              = "ALTA"
    estimatedDurationHours = 4
}
Show-Step -Title "Orden creada" -Order $order

$scheduledDate = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
$order = Invoke-DemoJson -Method Patch -Uri "$apiBase/public-works/work-orders/$($order.id)/schedule" -Body @{
    scheduledDate = $scheduledDate
}
Show-Step -Title "Orden programada" -Order $order

$order = Invoke-DemoJson -Method Patch -Uri "$apiBase/public-works/work-orders/$($order.id)/start"
Show-Step -Title "Trabajo iniciado" -Order $order

$order = Invoke-DemoJson -Method Patch -Uri "$apiBase/public-works/work-orders/$($order.id)/complete" -Body @{
    outcome = "Bache reparado y zona liberada"
}
Show-Step -Title "Trabajo completado" -Order $order

$order = Invoke-DemoJson -Method Patch -Uri "$apiBase/public-works/work-orders/$($order.id)/validate" -Body @{
    approved     = $true
    observations = "Conformidad aprobada durante la demo oral"
}
Show-Step -Title "Orden validada" -Order $order

if ($order.status -ne "VALIDADA") {
    throw "La demo termino en un estado inesperado: $($order.status)"
}

Write-Host "Demo finalizada correctamente. La orden $($order.id) queda como evidencia en development." -ForegroundColor Green
