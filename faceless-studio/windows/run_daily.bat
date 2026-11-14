@echo off
REM Faceless Studio daily run. Windows Task Scheduler starts this every morning.
REM It asks Claude Code to follow tasks\DAILY_TASK.md, and logs to logs\<date>.txt.
setlocal
cd /d "%~dp0.."
if not exist logs mkdir logs
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%i
echo ==== Daily run started %date% %time% ==== >> "logs\%TODAY%.txt"

REM The flags below were checked against "claude --help" during setup (see SETUP_PC.md).
claude -p "Follow tasks/DAILY_TASK.md exactly for today. Work only in this folder and the Google Drive folder in settings.json." --permission-mode acceptEdits >> "logs\%TODAY%.txt" 2>&1

if errorlevel 1 (
  echo ==== Daily run FAILED %time% ==== >> "logs\%TODAY%.txt"
  python make.py notify "Daily run hit an error. See logs\%TODAY%.txt"
) else (
  echo ==== Daily run finished %time% ==== >> "logs\%TODAY%.txt"
)
endlocal
