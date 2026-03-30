import random as _random


class Random:
    '''random 값을 발생시키기 위한 클래스'''

    @staticmethod
    def random_float(include_min: float, include_max: float) -> float:
        '''include_min 이상 include_max 이하의 랜덤 실수를 반환한다'''
        return round(_random.uniform(include_min, include_max), 2)

    @staticmethod
    def random_int(include_min: int, include_max: int) -> int:
        '''include_min 이상 include_max 이하의 랜덤 정수를 반환한다'''
        return _random.randint(include_min, include_max)

    @staticmethod
    def random(a, b):
        '''a, b의 타입에 따라 적절한 랜덤 값을 반환한다'''
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(
                f'Illegal Type {type(a).__name__}, {type(b).__name__}'
            )
        if isinstance(a, int) and isinstance(b, int):
            return Random.random_int(a, b)
        return Random.random_float(float(a), float(b))


class FileReader:
    '''파일을 읽는 클래스'''

    @staticmethod
    def read(file: str) -> str:
        '''파일을 읽어 문자열로 반환한다'''
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다: {file}')
            return ''
        except PermissionError:
            print(f'파일 읽기 권한이 없습니다: {file}')
            return ''


class FileWriter:
    '''파일을 쓰는 클래스'''

    @staticmethod
    def write(file: str, content: str):
        '''파일에 문자열을 쓴다'''
        try:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        except PermissionError:
            print(f'파일 쓰기 권한이 없습니다: {file}')
        except OSError as e:
            print(f'파일 쓰기 오류: {e}')


class DummySensorStage:
    '''DummySensor의 random 값들의 범위를 책임지는 클래스'''

    DEFAULT_MIN = 0
    DEFAULT_MAX = 100

    def __init__(self, lines: list):
        '''문자열 리스트를 파싱하여 센서별 범위를 설정한다'''
        self.ranges = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            name = parts[0]
            try:
                self.ranges[name] = self.cast_value((parts[1], parts[2]))
            except TypeError:
                self.ranges[name] = (
                    DummySensorStage.DEFAULT_MIN,
                    DummySensorStage.DEFAULT_MAX,
                )

    @staticmethod
    def cast_value(range_tuple: tuple) -> tuple:
        '''(min, max) 문자열 튜플을 적절한 타입으로 캐스팅하여 반환한다'''
        min_str, max_str = range_tuple[0], range_tuple[1]
        try:
            return (int(min_str), int(max_str))
        except ValueError:
            pass
        try:
            return (float(min_str), float(max_str))
        except ValueError:
            raise TypeError(
                f'Illegal Type {min_str}, {max_str}'
            )

    def get_ranges(self) -> dict:
        '''센서별 범위 사전을 반환한다'''
        return self.ranges


class DummySensor:
    '''화성 기지 내부 / 외부 상태값들을 저장한다'''

    def __init__(self, stage: DummySensorStage, log_file: str = ''):
        '''DummySensorStage를 받아 초기화한다'''
        self.stage = stage
        self.log_file = log_file
        self.env_values = {}

    def set_env(self):
        '''env_values 사전 객체를 랜덤 값으로 초기화한다'''
        ranges = self.stage.get_ranges()
        for name, (min_val, max_val) in ranges.items():
            self.env_values[name] = Random.random(min_val, max_val)

    def get_env(self) -> dict:
        '''env_values 사전 객체의 값을 반환한다'''
        self.log_env()
        return self.env_values

    def log_env(self):
        '''env_values 값들을 파일에 로그로 남긴다'''
        if not self.log_file:
            return
        lines = []
        for name, value in self.env_values.items():
            lines.append(f'{name}: {value}')
        content = '\n'.join(lines)
        FileWriter.write(self.log_file, content)


class Main:
    '''controller 함수'''

    def main(self):
        '''메인 실행 함수'''
        lines = FileReader.read('dummy_stage.txt').splitlines()
        stage = DummySensorStage(lines)
        ds = DummySensor(stage, 'env_log.txt')
        ds.set_env()
        env = ds.get_env()
        for name, value in env.items():
            print(f'{name}: {value}')


if __name__ == '__main__':
    Main().main()
