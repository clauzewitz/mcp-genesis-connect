from pydantic import BaseModel, Field

from genesis_connect.models.type import VehicleType, DistanceUnit, PlugType, TimeUnit, PlugStatus


class Car(BaseModel):
    car_id: str = Field(description="unique identifier for the car")
    car_nickname: str = Field(description="nickname of the car, used for personalization")
    car_type: VehicleType = Field(description="type of the car, such as SUV, sedan, etc.")
    car_name: str = Field(description="name of the car model")
    car_sellname: str = Field(description="name of the car model in the market")

class CarConnectedService(BaseModel):
    subscribeDate: str = Field(description="date of connected service subscription: YYYYMMDD")
    endDate: str = Field(description="end date of free service: YYYYMMDD")

class BaseDistance(BaseModel):
    timestamp: str = Field(description="timestamp of the car status update: YYYYMMDDHHmmSS")
    value: int = Field(description="distance to empty (DTE) value in kilometers")
    unit: DistanceUnit = Field(description="distance to empty (DTE) unit in kilometers")

class CarDistance(BaseDistance):
    phev_total_value: int = Field(description="total distance to empty (DTE) value for PHEV in kilometers")
    phev_total_unit: DistanceUnit = Field(description="total distance to empty (DTE) unit in kilometers")

class CarOdometer(BaseDistance):
    date: str = Field(description="date of the car status update: YYYYMMDDHHmmSS")

class CarTargetCharge(BaseModel):
    plug_type: PlugType = Field(description="type of charge, such as SUV, sedan, etc.")
    target_soc_level: int = Field(description="target soc level in battery percentage")

class CarTargetChargeTime(BaseModel):
    value: int = Field(description="target charge time value")
    unit: TimeUnit = Field(description="target charge time unit")

class CarChargeStatus(BaseModel):
    battery_plugin: PlugStatus = Field(description="battery plugin status")
    battery_charge: bool = Field(description="battery charge status")
    soc: int = Field(description="state of charge (SOC) percentage of the battery")
    target_soc: CarTargetCharge = Field(description="target soc status")
    remainTime: CarTargetChargeTime = Field(description="remaining time for target charge")
    timestamp: int = Field(description="timestamp of the car status update: YYYYMMDDHHmmSS")

class CarBatteryStatus(BaseModel):
    soc: int = Field(description="state of charge (SOC) percentage of the battery")
    timestamp: int = Field(description="timestamp of the car status update: YYYYMMDDHHmmSS")

class CarWarning(BaseModel):
    status: bool = Field(description="indicates if the warning is active")
