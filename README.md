# CEOS 15기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## 도커란? 

* 도커는 컨테이너 기반의 오픈소스 가상화 플랫폼이다.

다양한 프로그램, 실행환경(백엔드 프로그램, DB서버, 메시지 큐 등)을 컨테이너로 추상화하고 동일한 인터페이스를 제공 => 프로그램의 배포 및 관리를 단순하게 만들어준다.

### 컨테이너: 가상화 기술의 한 종류로 격리된 공간에서 프로세스가 동작하는 기술

#### 가상화 방식의 변화

> OS를 가상화: 가상머신을 이용하여 호스트 OS위에 게스트 OS를 띄우는 방식 => 사용법은 간단하지만 무겁고 느림 

> 전가상화, 반가상화: 전체 OS를 가상화하는 방식이 아니기 때문에 성능 향상

> 프로세스 격리 방식: 단순히 프로세스를 격리시키면서 CPU, 메모리는 딱 프로세스가 필요한 만큼만 추가로 사용하고 성능적으로도 손실 X => 한 개의 서버에 여러 컨테이너를 실행해도 격리된 채 실행되기 때문에 서로 영향을 미치지 않고 독립적으로 실행

<img width="616" alt="스크린샷 2022-03-23 오후 1 28 38" src="https://user-images.githubusercontent.com/59060780/159624151-8333c7ec-3758-421e-bce8-b31b728652a8.png"> 출처: https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html

### 이미지(Image): 특정 프로세스(컨테이너)를 실행하기 위한 모든 파일과 설정값(환경)을 묶은 것 (상태값을 가지지 않고 불변 == Immutable)

> 즉, 컨테이너는 이미지를 실행한 상태라 할 수 있다.

### 레이어(Layer): 기존 이미지에 추가적인 파일이 필요할 때 모든 파일을 다시 다운로드 받지 않고 해당 파일을 추가하기 위한 개념

> 이미지는 여러 개의 읽기 전용 Layer로 구성된다.

> 새로운 파일이 추가되면 새로운 Layer가 생성되고 도커는 여러 개의 Layer를 묶어서 하나의 파일시스템으로 만들어줌.
>> EX. nginx 이미지가 A + nginx의 집합이라면 WebApp 이미지는 A + nginx의 집합에 soruce 이미지를 추가한 A + nginx + source Layer로 구성된다.  

## Docker-compose과 Dockerfile

> Dockerfile: 하나의 이미지를 만들기 위한 과정 (docker가 실행)

```
FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app/
```

> docker-compose: 이미지를 여러개 띄워서 서로 연결해주고 컨테이너 외부의 호스트와의 연결 방법 그리고 파일 시스템을 어떻게 공유할지 제어해주는 것

```
version: '3'
services:

  db:
    container_name: db
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_HOST: '%'
      MYSQL_ROOT_PASSWORD: mysql
    expose:
      - 3306
    ports:
      - "3307:3306"
    env_file:
      - .env
    volumes:
      - dbdata:/var/lib/mysql

  web:
    container_name: web
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    environment:
      MYSQL_ROOT_PASSWORD: mysql
      DATABASE_NAME: mysql
      DATABASE_USER: 'root'
      DATABASE_PASSWORD: mysql
      DATABASE_PORT: 3306
      DATABASE_HOST: db
      DJANGO_SETTINGS_MODULE: django_docker.settings.dev
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - db
volumes:
  app:
  dbdata:
  ```
  
  * imgae: 컨테이너가 실행될때 필요한 이미지를 정의 => db컨테이너가 실행 될 때 mysql:5.7 이미지를 사용
  * command: 컨테이너 실행 후 실행할 명령어들을 정의.
  * environment: 각 컨테이너에서 쓸 환경변수들을 지정
  * ports: 컨테이너에서 사용되는 포트와 호스트의 포트를 매핑 (외부로 노출할 포트를 지정) HOST_PORT:CONTAINER_PORT
  * volumes: 호스트 디렉토리와 컨테이너 디렉토리를 매핑 => 컨테이너의 해당 디렉토리에서 호스트의 디렉토리를 참조 할 수 있게된다. (EX. 호스트 디렉토리의 dbdata 디렉토리를 컨테이너의 /var/lib/mysql 디렉토리에서 참조 가능)




