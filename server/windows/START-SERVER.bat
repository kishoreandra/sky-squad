@echo off
title Sky Squad home server (v1.3)
cd /d "%~dp0"
echo ==================================================
echo   Sky Squad home server is running (version 1.3)
echo   Keep this window open while friends play.
echo   Close this window to stop the server.
echo ==================================================
echo.
Godot_v4.3-stable_win64_console.exe --headless --main-pack skysquad.pck -- --dedicated --port=25001 --room=HOME --stay
echo.
echo The server stopped. Press any key to close.
pause > nul
