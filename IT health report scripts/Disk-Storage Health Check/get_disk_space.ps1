# Script to get disk space information and export to CSV file

# Get the computer name
$ComputerName = $env:COMPUTERNAME

# Get disk information
Get-WmiObject -Class Win32_LogicalDisk |
    Select-Object @{
        Name = "DeviceID";
        Expression = { "$ComputerName $($_.DeviceID)" }
    },
    @{
        Name = "FreeSpace(GB)";
        Expression = { [math]::Round($_.FreeSpace / 1GB, 2) }
    },
    @{
        Name = "TotalSize(GB)";
        Expression = { [math]::Round($_.Size / 1GB, 2) }
    } |
    Export-Csv -Path "C:\Users\MM48\Phibion Pty Ltd\MoTec Log file - MM48 Logged Data\Disk Space Health Check Output\MMXX.csv" -NoTypeInformation