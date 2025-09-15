@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "NODE=%PROJECT_DIR%node\node.exe"
set "DIST=%PROJECT_DIR%Front\digital-human-front\dist"
set "HTTP_SERVER_DIR=%PROJECT_DIR%Front\digital-human-front\node_modules\http-server\bin"

echo ----------------------------------------
echo ?? ????...
echo ----------------------------------------

echo ? Node: %NODE%

REM ?????? http-server.js
if exist "%HTTP_SERVER_DIR%\http-server.js" (
    echo ? ?? http-server.js
    "%NODE%" "%HTTP_SERVER_DIR%\http-server.js" "%DIST%" -p 8080
) else (
    echo ?? ??? http-server.js??? http-server ??
    "%NODE%" "%HTTP_SERVER_DIR%\http-server" "%DIST%" -p 8080
)

echo ----------------------------------------
echo ? ??????: http://127.0.0.1:8080
echo ----------------------------------------

pause