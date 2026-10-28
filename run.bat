@echo off
chcp 65001 > nul
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%CD%\src;%CD%

echo.


python -u tests\stage3\run_demos.py
if errorlevel 1 (
    echo.
    echo Stage 3 finished with an error.
    exit /b 1
)

echo.
echo Stage 3 finished successfully.
exit /b 0
