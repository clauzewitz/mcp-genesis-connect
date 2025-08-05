# Genesis MCP

이 프로젝트는 Genesis 차량의 다양한 정보를 조회할 수 있는 MCP 입니다. 이를 활용하여 차량 정보, 상태 등을 쉽게 조회할 수 있습니다.

## 기능

- 차량 목록 조회
- 커넥티드 서비스 계약 정보 조회
- 주행 가능 거리 조회
- 누적 운행 거리 조회
- 전기차 충전 상태 및 배터리 정보 조회
- 다양한 경고등 상태 정보 조회
  - 연료 부족
  - 타이어 공기압
  - 램프 와이어
  - 스마트키 배터리
  - 워셔액
  - 브레이크 오일
  - 엔진 오일

## 사용 방법

python 직접 실행
```
{
    "servers": {
        "genesis-connect": {
            "command": "python",
            "args": ["-m", "src.genesis_connect.server.py"],
            "env": {
                "GENESIS_API_KEY": "Enter your Genesis API Key here.",
            }
        }
    }
}
```

Docker를 이용한 실행
```
{
    "servers": {
        "genesis-connect": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "GENESIS_API_KEY",
                "genesis-connect:latest"
            ],
            "env": {
                "GENESIS_API_KEY": "Enter your Genesis API Key here.",
            }
        }
    }
}
```

## 라이선스

이 프로젝트는 [MIT](LICENSE) 라이선스에 따라 배포됩니다.

## 참고

- 이 프로젝트는 Genesis의 공식 API를 사용합니다.
- API 사용에 대한 자세한 정보는 Genesis 개발자 포털을 참조하세요.