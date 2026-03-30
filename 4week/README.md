# 요구 사항 분석하기
> 1. DummySensor Class 구현하기

내부 변수 : env_values 사전 객체
- 화성 기지 내부 온도 (mars_base_internal_temperature)
- 화성 기지 외부 온도 (mars_base_external_temperature)
- 화성 기지 내부 습도 (mars_base_internal_humidity)
- 회성 기지 외부 광량 (mars_base_external_illuminance)
- 화성 기지 내부 이산화탄소 농도 (mars_base_internal_co2)
- 화성 기지 내부 산소 농도 (mars_base_internal_oxygen)

함수 : set_env()

- set_env : env_values 사전 객체를 초기화 한다
- - 주어진 범위 내부의 값에서 random 값으로 초기화 한다
- - - 화성 기지 내부 온도 (18~30도)
- - - 화성 기지 외부 온도 (0~21도)
- - - 화성 기지 내부 습도 (50~60%)
- - - 화성 기지 외부 광량 (500~715 W/m2)
- - - 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
- - - 화성 기지 내부 산소 농도 (4%~7%)
- get_env() : env_values 사전 객체의 값을 얻는다

> 2. DummySensor test 하기
Dummy Sensor ds instance를 만들고 set_env(), get_env()를 호출하여 값을 확인한다

# 제한 사항
- python 버전은 3.x를 사용한다
- 별도의 라이브러리나 패키지를 사용하지 않는다 (random 제외)
- Python conding style guide를 확인하고 준수한다
- 문자열은 ' 으로 사용하며 부득이한 경우에는 " 을 사용할 수 있다
- foo = (0,) 와 같이 대입문의  = 앞 뒤로는 공백을 준다
- 경고 메시지 없이 모든 코드는 실행 되어야 한다
- 전채 코드를 mars_mission_computer.py 에 작성한다

# 보너스 과제
get_env()함수에 env_values값들을 파일에 log를 남기는 기능을 구현한다

# class 정리
> DummySensor
화성 기지 내부 / 외부 상태값들을 저장한다
__init__(stage : DummySensorStage, log_file : str = '')
set_env() : env_values 사전 객체를 랜덤 값으로 초기화한다
get_env() -> dict : env_values 값을 반환하며 log_env()를 호출한다
log_env() : env_values 값들을 파일에 로그로 남긴다 (보너스 과제)

> DummySensorStage
DummySensor의 random 값들의 범위를 책임지는 class
DEFAULT_MIN = 0, DEFAULT_MAX = 100 (파싱 실패 시 기본값)
__init__(lines : list) : 문자열 리스트를 파싱하여 센서별 범위를 설정한다
내부에서 {'sensorName': (min, max), ... } dict 형식
static cast_value(range_tuple : tuple) -> tuple : 문자열 튜플을 int/float로 캐스팅
get_ranges() -> dict : 센서별 범위 사전을 반환한다

> Random
random 값을 발생시키기 위한 class
static random_float(include_min : float, include_max : float) -> float
static random_int(include_min : int, include_max : int) -> int
static random(a, b) : a, b 타입에 따라 적절한 랜덤 값을 반환한다

> FileReader
파일을 읽는 class
static read(file : str) -> str (FileNotFoundError, PermissionError 처리 포함)

> FileWriter
파일을 쓰는 class
static write(file : str, content : str)

> Main
controller 함수
main(self)
    1. dummy_stage.txt 파일 읽기
    2. DummySensorStage instance 생성
    3. DummySensor instance 생성
    4. DummySensor instance의 set_env() 호출
    5. DummySensor instance의 get_env() 호출
    6. get_env()의 반환값을 출력

# 구현 순서 
1. FileReader / FileWriter 구현
2. Random 구현
3. DummySensorStage 구현
4. DummySensor 구현
5. Main 함수 구현