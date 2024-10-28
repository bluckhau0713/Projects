
$credential = (New-Object System.Management.Automation.PSCredential("secretUsername", (ConvertTo-SecureString "secretPassword" -AsPlainText -Force)))
$tenantDomainName = 'secretTenant'
  

Write-Verbose "Getting token"

$body = @{
    Grant_Type    = "client_credentials"
    Scope         = "https://graph.microsoft.com/.default"
    Client_Id     = $credential.username
    Client_Secret = $credential.GetNetworkCredential().password
}

$connectGraph = Invoke-RestMethod -Uri "https://login.microsoftonline.com/$tenantDomainName/oauth2/v2.0/token" -Method POST -Body $body

$token = $connectGraph.access_token

if ($token) {
    Write-Host "Bearer $($token)"
    $header = @{ Authorization = "Bearer $($token)" }

} else {
    throw "Unable to obtain token"
}
$body = @{
    reportName = "Devices"
    format     = "csv"
}

$result = Invoke-RestMethod -Headers $header -Uri "https://graph.microsoft.com/v1.0/deviceManagement/reports/exportJobs" -Body $body -Method Post

Write-Warning "Waiting for the report to finish generating"
do {
    $export = Invoke-RestMethod -Headers $header -Uri "https://graph.microsoft.com/v1.0/deviceManagement/reports/exportJobs('$($result.id)')" -Method Get
    Write-Host $result.id
    Start-Sleep 5
} while ($export.status -eq "inProgress")
#endregion wait for generating of the report to finish

#region download generated report
if ($export.status -eq "completed") {
    $originalFileName = $export.id + ".csv"
    $reportArchive = "C:\Users\luckhbr\Desktop\Devices.zip"
    Write-Host $reportArchive
    Write-Warning "Downloading the report to $reportArchive"
    $null = Invoke-WebRequest -Uri $export.url -Method Get -OutFile $reportArchive
}