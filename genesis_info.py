import asyncio
import os

from aiohttp import ClientSession
from datetime import datetime

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("genesis_info")

load_dotenv()

GENESIS_SECRET_KEY = os.getenv("GENESIS_SECRET_KEY", 'MmIzNzRiZmMtNjczZi00NTgwLTkxZTctNmFhMjZmOGJhZWEzOnZuSnlWTDlTUWJhOHAyMFdNNFJ6Y2dWa3EybTBKakVoSXc3WkRYT1VlUHpRUDNjWA==')
GENESIS_REFRESH_TOKEN = os.getenv("GENESIS_REFRESH_TOKEN", '')
GENESIS_REDIRECT_URL = os.getenv("GENESIS_REDIRECT_URL", '')

speed_unit_mapping = {0: 'feet', 1: 'km', 2: 'meter', 3: 'miles'}
time_unit_mapping = {0: '시간', 1: '분', 2: '밀리초', 3: '초'}
battery_plugin_unit_mapping = {0: '충전 대기', 1: '급속 충전', 2: '일반 충전'}

async def generate_access_token() -> dict:
    response = dict()

    async with ClientSession(headers={
                'Authorization': f'Basic {GENESIS_SECRET_KEY}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }) as session:
        async with session.post(
            url='https://accounts.genesis.com/api/account/ccsp/user/oauth2/token',
            data={
                'grant_type': 'authorization_code',
                'redirect_uri': 'https://clauzewitz.com',
                'code': GENESIS_REFRESH_TOKEN
        }) as resp:
            print(resp.status)
            print(await resp.text())

    return response

@mcp.tool()
async def refresh_access_token() -> str:
    """액세스 토큰을 갱신합니다.
    """
    result = ''

    try:
        async with ClientSession() as session:
            async with session.post('https://accounts.genesis.com/api/account/ccsp/user/oauth2/token',
                headers={
                    'Authorization': f'Basic {GENESIS_SECRET_KEY}',
                },
                data={
                    'grant_type': 'refresh_token',
                    'redirect_uri': GENESIS_REDIRECT_URL,
                    'refresh_token': GENESIS_REFRESH_TOKEN
            }) as resp:
                response = await resp.json()

                if resp.status == 200:
                    result = response['access_token']
                else:
                    result = '토큰 갱신에 실패하였습니다.'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result

@mcp.tool()
async def get_cars(access_token: str) -> str:
    """소유하고 있는 차량 리스트를 조회합니다.
    """
    result = list()

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url='https://dev-kr-ccapi.genesis.com:8081/api/v1/car/profile/carlist') as resp:
                response = await resp.json()

                if resp.status == 200:
                    if response['cars']:
                        for idx, car in enumerate(response['cars']):
                            result.append(f'{idx + 1} 차량명 - {car["carNickname"]}({car["carSellname"]})\n')
                else:
                    result.append('차량 정보 조회에 실패하였습니다.')

    except ValueError:
        result.append('오류가 발생하였습니다.')

    return "".join(result) if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_connected_service_info(access_token: str, car_id: str) -> str:
    """차량의 커넥티드 서비스(GCS) 가입일과 무료 서비스 종료일 정보를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/profile/{car_id}/contract') as resp:
                response = await resp.json()

                if resp.status == 200:
                    subscribe_date = datetime.strptime(response["subscribeDate"], "%Y%m%d")
                    end_date = datetime.strptime(response["endDate"], "%Y%m%d")
                    result = f'차량 커넥티드 서비스 가입일은 {subscribe_date.strftime("%Y-%m-%d")} 이며, 서비스 종료일은 {end_date.strftime("%Y-%m-%d")} 입니다.'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_dte(access_token: str, car_id: str) -> str:
    """차량의 주행 가능 거리를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/{car_id}/dte') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'현재 기준 {response["value"]}{speed_unit_mapping.get(response["unit"], "unknown")} 주행이 가능합니다.(갱신일: {dt.strftime("%Y-%m-%d")})'
                else:
                    result = '차량 정보 조회에 실패하였습니다.'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_odometer(access_token: str, car_id: str) -> str:
    """차량의 누적 주행 거리를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/{car_id}/odometer') as resp:
                response = await resp.json()
                odometers = response.get("odometers", list())

                if resp.status == 200 and odometers:
                    odometer = odometers.sort(key=lambda x: x["timestamp"], reverse=True).first()
                    dt = datetime.strptime(odometer["timestamp"], "%Y%m%d%H%M%S")
                    result = f'현재 기준 {odometer["value"]}{speed_unit_mapping.get(odometer["unit"], "unknown")} 주행하였습니다.(갱신일: {dt.strftime("%Y-%m-%d")})'
                else:
                    result = '차량 정보 조회에 실패하였습니다.'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_ev_charging(access_token: str, car_id: str) -> str:
    """차량의 충전 상태를 조회합니다.
    """
    results = list()

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/{car_id}/ev/charging') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    battery_status = battery_plugin_unit_mapping.get(response["batteryPlugin"], '대기') if response["batteryCharge"] else '대기'
                    results.append(f'현재 배터리 잔량은 {response["soc"]}% 이며, {battery_status} 상태입니다.\n')
                    if response["batteryCharge"] and response["remainTime"]:
                        remain_time = response["remainTime"]
                        results.append(f'{response["targetSOClevel"]}% 충전까지 {time_unit_mapping.get(remain_time["unit"])} 소요 예정입니다.\n')
                else:
                    results.append('차량 정보 조회에 실패하였습니다.')

    except ValueError:
        results.append('오류가 발생하였습니다.')

    return "".join(results) if results else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_ev_battery(access_token: str, car_id: str) -> str:
    """차량의 배터리 잔량을 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/{car_id}/ev/battery') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'현재 배터리 잔량은 {response["soc"]}% 입니다.(갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_low_fuel(access_token: str, car_id: str) -> str:
    """차량의 주유 경고등 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/lowFuel') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'주유량 {"양호" if response["status"] else "낮음"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_tire_pressure(access_token: str, car_id: str) -> str:
    """차량의 타이어 공기압 경고등 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/tirePressure') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'타이어 공기압 {"양호" if response["status"] else "경고"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_lamp_wire(access_token: str, car_id: str) -> str:
    """차량의 Lamp wire 경고등 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/lampWire') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'Lamp wire {"양호" if response["status"] else "경고"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_smart_key_battery(access_token: str, car_id: str) -> str:
    """차량의 스마트키 배터리 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/smartKeyBattery') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'스마트키의 배터리 {"양호" if response["status"] else "낮음"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_washer_fluid(access_token: str, car_id: str) -> str:
    """차량의 워셔액 경고등 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/washerFluid') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'워셔액 {"양호" if response["status"] else "부족"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_break_oil(access_token: str, car_id: str) -> str:
    """차량의 브레이크 오일 경고등 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/breakOil') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'브레이크 오일 {"양호" if response["status"] else "부족"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

@mcp.tool()
async def get_car_warning_engine_oil(access_token: str, car_id: str) -> str:
    """차량의 엔진 오일 경고등 상태를 조회합니다.
    """
    result = ''

    try:
        async with ClientSession(headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }) as session:
            async with session.get(url=f'https://dev-kr-ccapi.genesis.com:8081/api/v1/car/status/warning/{car_id}/engineOil') as resp:
                response = await resp.json()

                if resp.status == 200:
                    dt = datetime.strptime(response["timestamp"], "%Y%m%d%H%M%S")
                    result = f'엔진 오일 {"양호" if response["status"] else "부족"} (갱신일: {dt.strftime("%Y-%m-%d")})'

    except ValueError:
        result = '오류가 발생하였습니다.'

    return result if result else '차량 정보가 존재하지 않습니다.'

async def main():
    print(await get_car_warning_engine_oil('asdf', 'asdfa'))

if __name__ == "__main__":
    # mcp.run(transport="stdio")
    asyncio.run(main())
