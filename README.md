# NCOF API Server

데이터모델과 API 스켈레톤은 [OpenAPI Generator](https://openapi-generator.tech) 를 사용 하였다.

- API version: 1.0.0
- Generator version: 7.13.0-SNAPSHOT
- Build package: org.openapitools.codegen.languages.PythonFastAPIServerCodegen

## Requirements.

Python >= 3.12

## Installation & Usage

uv 가 없다면 다음 명령을 사용해서 설치한다.

```sh
pip install uv

# 또는 다음 명령으로도 설치가 가능하다.
# curl -LsSf https://astral.sh/uv/install.sh | sh

```

프로젝트 루트 디렉토리에서 다음 명령을 사용해서 프로젝트 의존성을 동기화 한다.

```sh
uv sync
```

서버를 시작하려면 프로젝트 루트 디렉토리에서 다음 명령을 실행한다.

```sh
sh run.sh
```

run.sh 의 옵션은 다음과 같다.

- PYTHONPATH=src

  - Python 모듈 검색 경로에 src 디렉토리를 추가 (즉, src 폴더 내의 모듈을 import할 수 있도록 환경 설정)

- uv run

  - uv(uvicorn의 빠른 실행 래퍼 등)로 명령을 실행 (uv는 uvicorn을 포함한 여러 개발 도구를 통합적으로 실행할 수 있게 해주는 도구)

- uvicorn openapi_server.main:app

  - uvicorn으로 ASGI 앱 실행
  - openapi_server.main:app은 openapi_server/main.py 파일의 app 객체를 지정 (즉, FastAPI 인스턴스가 app 변수에 할당되어 있어야 함).

- --host 0.0.0.0

  - 모든 네트워크 인터페이스(외부 포함)에서 접속 가능하도록 바인딩

- --port 8080

  - 8080번 포트에서 서버 실행

- --reload

  - 코드 변경 시 서버가 자동으로 재시작 (개발 환경에서 편리하게 사용, 운영 환경에서는 비권장).

- --log-config log_config.ini
  - 로그 설정을 log_config.ini 파일에서 불러와 적용(로그 포맷, 핸들러 등 커스텀 가능).

확인을 위해서 웹 브라우저로 `http://localhost:8080/docs/` 접속한다.

## Tests

To run the tests:

```bash
uv add pytest
PYTHONPATH=src uv run pytest tests
```
