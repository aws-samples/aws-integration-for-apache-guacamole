$logFile = "C:\log.txt"

$ssmKey = $args[0]
$ssmRegion = $args[1]

$password = & "C:\Program Files\Amazon\AWSCLIV2\aws.exe"  ssm get-parameter --name "$ssmKey" --region "$ssmRegion" --with-decryption --query "Parameter.Value" --output text

$securePass = ConvertTo-SecureString $password -AsPlainText -Force

Function Write-Log {
  param(
      [Parameter(Mandatory = $true)][string] $message,
      [Parameter(Mandatory = $false)]
      [ValidateSet("INFO","WARN","ERROR")]
      [string] $level = "INFO"
  )
  # Create timestamp
  $timestamp = (Get-Date).toString("yyyy/MM/dd HH:mm:ss")
  # Append content to log file
  Add-Content -Path $logFile -Value "$timestamp [$level] - $message"
}

Function Create-LocalAdmin {
    process {
      try {
        New-LocalUser "developer" -Password $securePass -FullName "Developer" -Description "Developer Account"
        Add-LocalGroupMember -Group "Administrators" -Member "developer"
      }catch{
    Write-log -message "Creating local account failed" -level "ERROR"
  }
}
}

Create-LocalAdmin
