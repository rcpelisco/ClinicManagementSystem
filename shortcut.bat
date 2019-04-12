start cmd.exe @cmd /k "python ."
echo %time%
timeout 5 > NUL
echo %time%
start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http:\\localhost:5000"