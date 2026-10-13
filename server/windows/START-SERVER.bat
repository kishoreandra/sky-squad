@echo off
title Sky Squad home server (v1.4)
cd /d "%~dp0"
if not exist "Godot_v4.3-stable_win64_console.exe" (
  echo First start: downloading the game engine, about 60 MB. Please wait...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/godotengine/godot-builds/releases/download/4.3-stable/Godot_v4.3-stable_win64.exe.zip' -OutFile 'godot.zip'; Expand-Archive -Force -Path 'godot.zip' -DestinationPath '.'; Remove-Item 'godot.zip'"
  if not exist "Godot_v4.3-stable_win64_console.exe" (
    echo Download failed. Check your internet and run START-SERVER.bat again.
    pause
    exit /b
  )
)
echo ==================================================
echo   Sky Squad home server is running (version 1.4)
echo   Keep this window open while friends play.
echo   Close this window to stop the server.
echo ==================================================
echo.
Godot_v4.3-stable_win64_console.exe --headless --main-pack skysquad.pck -- --dedicated --port=25001 --room=HOME --stay
echo.
echo The server stopped. Press any key to close.
pause > nul
