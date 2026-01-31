@echo off
echo Building Linux Executable using Docker...

REM Check if Docker is available
docker --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Docker is not installed or not in the PATH.
    echo Please install Docker Desktop for Windows to use this script.
    echo Alternatively, push your code to GitHub to use the automated build workflow.
    pause
    exit /b 1
)

REM Build the Docker image
echo Building Docker image...
docker build -f Dockerfile.linux -t fuse-linux-builder .

REM Create a container to copy the artifact
echo Extracting executable...
docker create --name fuse_temp fuse-linux-builder
docker cp fuse_temp:/app/dist/fuse_linux ./fuse_linux
docker rm fuse_temp

echo.
echo Build complete! The executable is located at: %CD%\fuse_linux
pause
