import os
from typing import Final

import aiohttp
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.contrib.mcp_mixin import mcp_tool

from models.car import Car, CarDistance, CarOdometer, CarChargeStatus, CarBatteryStatus, CarWarning, CarConnectedService

BASE_API_URL: Final = 'https://dev-kr-ccapi.genesis.com:8081/api/v1/car'

if not os.getenv("GENESIS_API_KEY"):
    load_dotenv()

GENESIS_API_KEY: Final = str(os.getenv("GENESIS_API_KEY")).strip()

mcp: Final = FastMCP("genesis_info")


async def client_session():
    return aiohttp.ClientSession(
        headers={
            'Authorization': f'Bearer {GENESIS_API_KEY}'
        }
    )


@mcp_tool("getCarList")
async def get_car_list() -> list[Car] | str:
    """
    차량 목록 정보를 가져옵니다.

    Returns:
        list[CarInfo]: 성공 시 CarInfo 객체 목록을 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get('https://developers.genesis.com/web/v1/genesis/data/carprofile_carlist') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return [Car(**car) for car in response.get('cars', [])]
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarContract")
async def get_car_contract(car_id: str) -> CarConnectedService | str:
    """
    차량의 커넥티드 서비스 가입일과 무료 서비스 종료일 정보를 가져옵니다.

    Returns:
        CarConnectedService: 성공 시 커넥티드 서비스 가입일과 무료 서비스 종료일 정보를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/profile/{car_id}/contract') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarConnectedService(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarDte")
async def get_car_dte(car_id: str) -> CarDistance | str:
    """
    특정 차량의 주행 가능 거리 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarDistance: 성공 시 차량 주행 가능 거리 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/dte') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarDistance(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarOdometer")
async def get_car_odometer(car_id: str) -> list[CarOdometer] | str:
    """
    특정 차량의 누적 운행 거리 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        List[CarOdometer]: 성공 시 차량 누적 운행 거리 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/odometer') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return [CarOdometer(**odometer) for odometer in response.get('odometers', [])]
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarEvCharging")
async def get_car_ev_charging(car_id: str) -> CarChargeStatus | str:
    """
    전기차 차량의 충전 중 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarChargeStatus: 성공 시 충전 중 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/ev/charging') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarChargeStatus(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarEvBattery")
async def get_car_ev_battery(car_id: str) -> CarBatteryStatus | str:
    """
    전기차 차량의 배터리 잔량 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarBatteryStatus: 성공 시 배터리 잔량 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/ev/battery') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarBatteryStatus(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningLowFuel")
async def get_car_warning_lowFuel(car_id: str) -> CarWarning | str:
    """
    차량의 연료 부족 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 연료 부족 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/lowFuel') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningTirePressure")
async def get_car_warning_tire_pressure(car_id: str) -> CarWarning | str:
    """
    차량의 타이어 공기압 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 타이어 공기압 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/tirePressure') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningLampWire")
async def get_car_warning_lamp_wire(car_id: str) -> CarWarning | str:
    """
    차량의 Lamp wire 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 Lamp wire 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/lampWire') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningSmartKeyBattery")
async def get_car_warning_smart_key_battery(car_id: str) -> CarWarning | str:
    """
    차량의 스마트키 배터리 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 스마트키 배터리 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/smartKeyBattery') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningWasherFluid")
async def get_car_warning_washer_fluid(car_id: str) -> CarWarning | str:
    """
    차량의 워셔액 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 워셔액 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/washerFluid') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningBreakOil")
async def get_car_warning_break_oil(car_id: str) -> CarWarning | str:
    """
    차량의 브레이크 오일 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 브레이크 오일 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/breakOil') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp_tool("getCarWarningEngineOil")
async def get_car_warning_engine_oil(car_id: str) -> CarWarning | str:
    """
    차량의 엔진 오일 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 엔진 오일 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with client_session() as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/engineOil') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

if __name__ == "__main__":
    mcp.run(transport="stdio")