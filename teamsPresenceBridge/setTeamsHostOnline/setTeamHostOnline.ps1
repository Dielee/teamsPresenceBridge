while ($true)
{
    Invoke-WebRequest "http://192.168.50.2:5557/setOnline"
    Start-Sleep(240)
}
    