# Study Group Api

## Setting

### 로컬에서 실행

- pipenv 설치

```shell
pip install pipenv
```

- 파이썬3의 가상환경 생성

```
pipenv --three
```

- 만들어진 가상환경으로 이동

```
pipenv shell
```

- 라이브러리 다운로드

```
pipenv install pipfile
```

- 디비 생성 (기본 내장 sqlite3사용)

```
// 마이그레이션 생성하기
python manage.py makemigrations
// 실제 디비에 적용
python manage.py migrate
```

### 배포 시

- 라이브러리 추가

```
pipenv run pipenv_to_requirements
```

- 컨테이너 실행

```
docker-compose up --build
```

### 테스트 데이터 생성

유저 생성

```
python manage.py seed_users --number {count}
```

그룹 생성

```
python manage.py seed_groups --number {count}
```

그룹목표 생성

```
python manage.py seed_subjects --number {count}
```

Todo그룹 생성

```
python manage.py seed_todogroups --number {count}
```

Todo 생성

```
python manage.py seed_todos --number {count}
```
