from enum import StrEnum, IntEnum

class VehicleType(StrEnum):
    GN = 'GN' ##내연기관
    EV = 'EV' ##전기
    HEV = 'HEV' ##하이브리드
    PHEV = 'PHEV' ##플러그인하이브리드
    FCEV = 'FCEV' ## 수소전기

class DistanceUnit(IntEnum):
    FEET = 0 ## feet
    KM = 1 ## km
    METER = 2 ## meter
    MILES = 3 ## miles

class PlugType(IntEnum):
    DC = 0  ## DC fast charger
    AC_240V = 1  ## AC charger with 240V
    AC_120V = 2  ## AC charger with 120V

class TimeUnit(IntEnum):
    HOUR = 0  ## seconds
    MINUTE = 1  ## minutes
    MSEC = 2  ## hours
    SEC = 3  ## days

class PlugStatus(IntEnum):
    NOT_CONNECTED = 0  ## 플러그 연결 안됨
    DC_FAST_CHARGER = 1  ## 급속 충전기 연결
    AC_CHARGER = 2  ## 일반 충전기 연결