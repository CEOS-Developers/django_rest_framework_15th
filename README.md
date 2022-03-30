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

## Github Actions

> Github Actions란 워크플로우를 자동화하도록 도와주는 Github에서 제공하는 도구.
> > 테스트, 빌드, 배포 등 다양한 작업들을 자동화하여 처리해줌.

> .github/workflows 폴더 내에 .yml 파일을 추가하여 등록하거나 Github 저장소에서 등록 가능(워크플로우 템플릿을 추천해줌)

```
name: Deploy to EC2
on: [push]
jobs:

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
    - name: checkout
      uses: actions/checkout@master

    - name: create env file
      run: |
        touch .env
        echo "${{ secrets.ENV_VARS }}" >> .env     
```        

* Evnets: on: [push] => 워크 플로우를 실행하는 특정 활동이나 규칙. 이 코드에선 커밋이 push 될 때마다 워크플로우 실행
* 워크플로우는 하나 이상의 jobs, 그보다 작은단위인 steps, actions로 이루어져 있으며 각 jobs들은 새로운 가상 환경에서 실행.

> 워크플로우를 실행 시 중요한 정보들은 Github secret으로 저장하여 환경 변수로 사용 가능 

## 실행 플로우

![스크린샷 2022-03-24 오전 1 46 35](https://user-images.githubusercontent.com/59060780/159752231-c6d619f0-70b2-421c-97b8-3920f1cee1f2.png)

> 로컬환경에서 작성된 코드를 깃에 푸쉬 -> Github actions가 푸쉬된 코드를 서버에 띄우고 deploy.sh 실행 -> 실행된 deploy.sh가 docker-compose.prod.yml 파일을 통해 web, nginx 컨테이너를 빌드 후 실행

### git에 푸쉬 후 Github actions가 빌드

![스크린샷 2022-03-24 오전 1 57 09](https://user-images.githubusercontent.com/59060780/159754281-77cd98b7-51c4-4d1d-b88c-05071ad8d00a.png)

### 빌드 후 실행 (Ec2 DNS 주소로 접속)

![스크린샷 2022-03-24 오전 2 01 33](https://user-images.githubusercontent.com/59060780/159755075-c4675ec6-4993-4269-8a9b-bac88865f52e.png)


---------

## 인스타그램 모델링

### mysql 세팅 및 Django와 연동

![image](https://user-images.githubusercontent.com/59060780/160875221-57b03d71-56c4-41f0-a249-736d927a8627.png)

> mysql 설치 및 CEOS DB 생성
>> settings/dev.py에서 생성한 데이터베이스 정보로 설정 변경(보안을 위해 .env 파일에 작성)

* mysqlclient를 설치하려 했지만 오류발생 => homebrew에서 mysql 재설치 후 다시 설치하니 성공


### 모델링 (ERD 설계)

#### ERD 설계

![image](https://user-images.githubusercontent.com/59060780/160880621-9b794f28-08cb-416d-b663-3f5ee05f8950.png)

> 유저, 게시물 (사진, 동영상) 중심으로 ERD를 설계했다.

* User: Django에서 기본으로 제공하는 유저 모델 사용
* Profile: User 테이블과 OnetoOne으로 연결, 인스타그램 개인 프로필에 필요한 정보들
* Following, Follower: 기존에는 한 테이블로 팔로워, 팔로잉 두 컬럼을 한 번에 관리하려 했으나 Django에서 migrate시 오류 발생 => 각각의 테이블로 나눠서 구현 (User 테이블과 일대다 관계)
* Post: 인스타그램에서 사용자가 올리는 릴스와 포스팅하는 게시글 테이블. Image, Movie 테이블을 생성하여 각각의 테이블에 게시물 식별번호를 외래키로 주어 연걸 (User:Post = 1:N, Post:(Image,Movie) = 1:N)
* Liking, Comment, Location: Post 테이블에 필요한 추가 테이블들. Location 테이블은 Post 테이블과 1:1관계로 Lcation의 pk를 Post 테이블에 외래키로 저장. Liking, Comment 테이블은 Post와 User의 중간 테이블로 각각의 pk들을 외래키로 가짐
* Story, ViewingStory: 인스타그램의 스토리는 게시글과는 다른 메커니즘을 갖고있는 것으로 판단해서 새로운 테이블로 생성. 따로 스토리 조회 데이터를 저장하는 ViewingStory 테이블을 만들어 User 테이블과 연결하고 컬럼으로 좋아요 여부까지 저장.


#### models.py 작성

* 예시

```
#api/models.py

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=30)
    profile_scripts = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성 시 현재 시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신 시 현재 시간 자동 저장
    status = models.CharField(max_length=20, default='valid')
    
```

#### migrate 파일 생성

```
$ python manage.py makemigrations api
$ python manage.py migrate api
```
> python manage.py makemigrations --name {지정할 이름} {앱 이름} 명령어를 사용하면 migration 파일 이름을 바꿔서 저장 가능

* migration이란? : 모델의 변경 내역을 DB 스키마에 저장하는 방법. => DB 스키마를 git처럼 버전을 나누어서 관리를 용이하게 해주는 시스템

#### ORM 사용해보기
> User 테이블의 인스턴스 3개 생성

![image](https://user-images.githubusercontent.com/59060780/160882149-3c19ad46-5fb9-40c7-8d49-57c10c47d11b.png)

> User 테이블 인스턴스 3개를 각각 외래키로 갖는 Post 테이블 인스턴스 3개 생성


![image](https://user-images.githubusercontent.com/59060780/160882359-b5049a21-ec82-4072-8f6f-154d0ba64fe4.png)

> 삽입한 Post 테이블 인스턴스들 조회

![image](https://user-images.githubusercontent.com/59060780/160882636-e35875f4-c44c-4188-889c-7a9e2a15d0e1.png)

![image](https://user-images.githubusercontent.com/59060780/160882653-bc06f979-2476-4478-9419-748fa37fa7ce.png)

> filter 사용해서 조회

![image](https://user-images.githubusercontent.com/59060780/160882713-1a0562c4-50a4-433f-b8c7-3b3afc108e25.png)

