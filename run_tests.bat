
@echo off
chcp 65001 > nul
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%CD%\src;%CD%

echo.

python -u src\main.py tests\test2\config_real.toml
if errorlevel 1 exit /b 1

echo.

python -u src\main.py tests\test2\config_test.toml

exit /b %ERRORLEVEL%
