import logging
import os
from typing import Final, Annotated

import aiohttp
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import Field

from models.car import Car, CarDistance, CarOdometer, CarChargeStatus, CarBatteryStatus, CarWarning, CarConnectedService

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BASE_API_URL: Final = 'https://dev-kr-ccapi.genesis.com:8081/api/v1/car'

if not os.getenv("GENESIS_API_KEY"):
    load_dotenv()

GENESIS_API_KEY: Final = str(os.getenv("GENESIS_API_KEY") or '').strip()

mcp: Final = FastMCP("genesis-connect")

headers: Final = {
    'Authorization': f'Bearer {GENESIS_API_KEY}',
    'Content-Type': 'application/json'
}


@mcp.tool("get_cars")
async def get_cars() -> list[Car] | str:
    """
    차량 목록 정보를 가져옵니다.

    Returns:
        list[CarInfo]: 성공 시 CarInfo 객체 목록을 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://developers.genesis.com/web/v1/genesis/data/carprofile_carlist') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return [Car(**car) for car in response.get('cars', [])]
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_contract")
async def get_car_contract(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarConnectedService | str:
    """
    차량의 커넥티드 서비스 가입일과 무료 서비스 종료일 정보를 가져옵니다.

    Returns:
        CarConnectedService: 성공 시 커넥티드 서비스 가입일과 무료 서비스 종료일 정보를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/profile/{car_id}/contract') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarConnectedService(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_dte")
async def get_car_dte(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarDistance | str:
    """
    특정 차량의 주행 가능 거리 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarDistance: 성공 시 차량 주행 가능 거리 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/dte') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarDistance(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_odometer")
async def get_car_odometer(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> list[CarOdometer] | str:
    """
    특정 차량의 누적 운행 거리 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        List[CarOdometer]: 성공 시 차량 누적 운행 거리 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/odometer') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return [CarOdometer(**odometer) for odometer in response.get('odometers', [])]
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_ev_charging")
async def get_car_ev_charging(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarChargeStatus | str:
    """
    전기차 차량의 충전 중 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarChargeStatus: 성공 시 충전 중 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/ev/charging') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarChargeStatus(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_ev_battery")
async def get_car_ev_battery(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarBatteryStatus | str:
    """
    전기차 차량의 배터리 잔량 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarBatteryStatus: 성공 시 배터리 잔량 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/{car_id}/ev/battery') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarBatteryStatus(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_low_fuel")
async def get_car_warning_low_fuel(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 연료 부족 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 연료 부족 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/lowFuel') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_tire_pressure")
async def get_car_warning_tire_pressure(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 타이어 공기압 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 타이어 공기압 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/tirePressure') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_lamp_wire")
async def get_car_warning_lamp_wire(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 Lamp wire 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 Lamp wire 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/lampWire') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_smart_key_battery")
async def get_car_warning_smart_key_battery(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 스마트키 배터리 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 스마트키 배터리 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/smartKeyBattery') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_washer_fluid")
async def get_car_warning_washer_fluid(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 워셔액 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 워셔액 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/washerFluid') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_break_oil")
async def get_car_warning_break_oil(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 브레이크 오일 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 브레이크 오일 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/breakOil') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

@mcp.tool("get_car_warning_engine_oil")
async def get_car_warning_engine_oil(car_id: Annotated[str, Field(description="vehicle unique identifier")]) -> CarWarning | str:
    """
    차량의 엔진 오일 경고등 상태 정보를 가져옵니다.

    Args:
        car_id (str): 차량 ID

    Returns:
        CarWarning: 성공 시 엔진 오일 경고등 상태 정보를 담은 객체를 반환합니다.
        str: 오류 발생 시 오류 메시지를 반환합니다.
    """
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{BASE_API_URL}/status/warning/{car_id}/engineOil') as resp:
                resp.raise_for_status()
                response = await resp.json()
                return CarWarning(**response)
    except Exception as e:
        return f'차량 정보를 가져올 수 없습니다. 오류: {str(e)}'

if __name__ == "__main__":
    mcp.run(transport="stdio")