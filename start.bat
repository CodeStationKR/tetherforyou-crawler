@REM git pull first
git pull
@REM get input from user
@REM in order to select mode
@REM 1 for all
@REM 2 for specific
@REM 3 for none

set /p mode=크롤러 번호를 선택해주세요 (1 전체, 2 바이낸스, 3 빙엑스, 4 비트겟, 5 비트마트, 6 게이트아이오):
@REM if mode is 1
if %mode%==1 (
    @REM run all
    python main_server.py
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
