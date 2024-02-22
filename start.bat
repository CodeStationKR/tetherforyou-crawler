@REM git pull first
git pull
@REM get input from user
@REM in order to select mode
@REM 1 for all
@REM 2 for specific
@REM 3 for none

set /p mode=Select Crawler (1 ALL, 2 BINANCE, 3 BINGX, 4 BITGET, 5 BITMART, 6 GATE.IO):
@REM if mode is 1
if %mode%==1 (
    @REM run all
    python main_v2_server.py
    @REM after main server is done run gateio
    python only_gateio_server.py
)

@REM if mode is 2
if %mode%==2 (
    @REM run binance
    python only_binance_v2_server.py
)

@REM if mode is 3
if %mode%==3 (
    @REM run bithumb
    python only_bingx_v2_server.py
)

@REM if mode is 4
if %mode%==4 (
    @REM run bitget
    python only_bitget_v2_server.py
)

@REM if mode is 5
if %mode%==5 (
    @REM run bitmart
    python only_bitmart_v2_server.py
)

@REM if mode is 6
if %mode%==6 (
    @REM run gateio
    python only_gateio_server.py
)
