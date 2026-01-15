@echo off
REM ============================================================
REM SSH SOCKS5 Tunnel untuk KIOSBANK API
REM VPS: 193.219.97.148
REM User: alwyzon
REM ============================================================

echo ============================================================
echo Starting SSH SOCKS5 Tunnel to VPS
echo ============================================================
echo.
echo VPS IP: 193.219.97.148
echo User: alwyzon
echo Local SOCKS5 Port: 1080
echo.
echo IMPORTANT: Keep this window OPEN while using the proxy!
echo Press Ctrl+C to stop the tunnel.
echo.
echo ============================================================
echo.

REM Start SSH tunnel
REM -D 1080 = SOCKS5 proxy on port 1080
REM -N = No command execution (just tunnel)
REM -v = Verbose (show connection details)

ssh -D 1080 -N -v alwyzon@193.219.97.148

echo.
echo ============================================================
echo SSH Tunnel Stopped
echo ============================================================
pause
