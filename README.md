CEOS 14기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## 2주차 Docker와 Github Action

---

### 컨테이너 (Container)

- 운영체제 수준의 가상화 기술로 리눅스 커널을 공유하면서 각 프로세스를 격리된 환경에서 실행하는 기술
- 다양한 프로그램, 실행 환경을 컨테이너를 통해 쉽게 관리, 공유, 재사용할 수 있음

### 이미지 (Image)

- 컨테이너 실행에 필요한 환경 (프로그램, 파일, 설정값 등)을 포함하고 있는 것
- 내가 구축한 환경을 그대로 찍어둔 것이라고 생각하면 됨
- 이미지를 통해 컨테이너를 생성할 수 있고, 이미지만 있으면 다른 컴퓨어에서도 똑같은 환경을 만들 수 있음

---

### Docker

- 컨테이너 기반의 오픈소스 가상화 플랫폼<br>

> 💡 **도커의 특징**
- 도커가 설치되어 있으면 어디서든 컨테이너를 실행할 수 있음
- Dockerfile을 이용하여 이미지를 만들고 처음부터 재현 가능함
  - 빌드 서버에서 이미지를 만들면 해당 이미지를 이미지 저장소에 저장하고 운영서버에서 이미지를 불러와 사용
- 이미지가 환경변수에 따라 동적으로 설정파일을 생성하도록 만들어져야 함
- 컨테이너는 삭제 후 새로 만들면 모든 데이터가 초기화되어 제거가 쉬움
  - 저장이 필요하다면, 업로드 파일을 외부 스토리지 S3와 같은 별도의 저장소가 필요함
  - 세션이나 캐시를 redis와 같은 외부로 분리

### Dockerfile

- 하나의 이미지를 만들기 위한 과정

### Docker Compose

- 여러 컨테이너를 한 번에 작동시키고 관리할 수 있는 툴

```docker-compose.yml```

- db, web 두 개의 컨테이너 정의
  - web 이라는 컨테이너에서 db라는 컨테이너로 연결
  - _두 컨테이너 서로 소통 가능_

<br>

```docker-compose.prod.yml```

- docker-compose.yml 과 달리 db 컨테이너 없이 web, nginx 컨테이너 정의
  - 서버에서 데이터가 모두 삭제될 위험이나 보안 상의 위험이 있고, 인스턴스 자원(메로리, cpu 등)을 서버와 DB가 함께 쓰게 되어 효율적이지 못하게 되는 문제가 생기기 때문에 production의 docker-compose에는 db 컨테이너가 없음

---

### .env

- 환경변수룰 env 파일에 저장하여 관리

### Nginx

- 경량 웹 서버
- 클라이언트로부터 요청을 받았을 때 정적 파일을 응답해주는 HTTP Web Server로 활용
- WAS 서버의 부하를 줄일 수 있는 로드 밸런서로 활용
  - WAS란 DB 조회나 다양한 로직 처리를 요구하는 dynamic 컨텐츠를 제공하기 위해 만들어진 Application Server 이다

---

### Github Action

- Github Action은 Github에서 공식적으로 제공하는 CI/CD 툴, 즉 개발의 workflow를 자동화할 수 있게 도와주는 툴

> **Workflow**<br>
> 자동화된 전체 프로세스로, Github Repository의 ```./github/workflows``` 폴더 아래에 저장됨.
> Github에게 YAML 파일로 정의한 자동화 동작을 전달하면, Github Actions는 해당 파일을 기반으로 그대로 실행시킴.

### Deploy

1. Github Actions로 ```deploy.yml``` 실행하여 ```deploy.sh``` 실행
2. ```deploy.sh```가 docker-compose 실행
3. docker-compose가 컨테이너 빌드하고 실행

### deploy.yml

- 배포 스크립트
- ```on: [push]```
  - push 될 때마다 해당 workflow 수행
- ```- name: create env file```
  - Github 설정에 복사해놓은 ENV_VARS의 값을 모두 .env file로 만듬
- ```- name: create remote directory```
  - ec2 서버에 디렉토리 생성
- ```- name: copy source via ssh key```
  - ssh key를 이용하여 현재 push된 소스를 서버에 복사
- ```- name: executing remote ssh commands using password```
  - 서버에 접속하여 ```deploy.sh``` 실행

### deploy.sh

- ```if ! type docker > /dev/null```로 시작하는 코드 블록은 docker가 깔려있지 않을 때 설치해주는 코드
- ```if ! type docker-compose > /dev/null```로 시작하는 코드 블록은 docker-compose가 깔려있지 않을 때 설치해주는 코드
  
  ```
  sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d
  ```
  - 위의 맨 마지막 코드가 최종 실행 코드로 해당 command에 의해 서버가 빌드되고 실행됨
  <br><br>
  
  - ```up``` : docker-compose(여기서는 -f 파라미터가 가리키는 docker-compose.prod)에 정의된 모든 컨테이너를 띄우는 명령어
  - ```--build``` : up할 때마다 새로 build 수행하도록 하는 파라미터
  - ```-d``` : daemon 실행, background로 docker-compose 돌릴 수 있음

<br>

## 3주차 DB 모델링 및 Django ORM

---

### 인스타그램 데이터 모델링

<img width="550" alt="스크린샷 2022-04-02 오전 4 46 09" src="https://user-images.githubusercontent.com/78442839/161331948-0c0659dc-0b64-43a4-a8ca-1202b0787996.png">

사진, 영상 업로드 기능

#### User
```django.contrib.auth.models import User```
- django에서 제공하는 User 모델
  - 사용자의 이름(username), 이메일(email), 비밀번호(password) 필드 등
  - 사용자의 이름을 인스타그램의 사용자 계정 이름으로 사용할 예정

#### Profile
- User 모델과 OneToOne 관계를 통해 구현
- 이름(프로필 이름), 웹사이트, 자기소개, 프로필 이미지

#### Post
- 게시글 모델로, 업로드된 파일은 File 모델에 저장하여 관리
- User 모델과의 OneToMany 관계를 이용해 Foreign Key 사용
- 내용, 생성시간, 좋아요 개수, 댓글 개수

#### File
- 게시글에서 업로드된 사진, 영상 파일 모델
- Post 모델과의 OneToMany 관계를 이용해 Foreign Key 사용

#### Comment
- 게시글에 달린 댓글 모델
- Post 모델과의 OneToMany 관계를 이용해 Foreign Key 사용
  - 댓글이 작성된 Post
- User 모델과의 OneToMany 관계를 이용해 Foreign Key 사용
  - 댓글을 작성한 User
- 내용, 생성 시간, 수정 시간

#### Like
- 게시글에 등록된 좋아요 모델
- Post 모델과의 OneToMany 관계를 이용해 Foreign Key 사용
  - 좋아요가 등록된 Post
- User 모델과의 OneToMany 관계를 이용해 Foreign Key 사용
  - 좋아요를 등록한 User

<br>

> ```CharField() vs TextField()```<br>
> RDBMS에서 CharField()는 작은 문자열(최대 길이 명시), TextField()는 큰 문자열에 사용함<br><br>
> ```DateTimeField()의 auto_now=True vs auto_now_add=True```<br>
> auto_now는 django model이 save 될 때마다 현재 시간으로 갱신<br>
> auto_now_add는 django model이 최초 저장(insert, create)될 때만 현재 시간으로 적용

---

### ORM 적용

데이터베이스에 User 모델 객체 생성
##### ORM 쿼리
```django
from django.contrib.auth.models import User

User.objects.create_user("user1", "user1@test.com", "password1")
User.objects.create_user("user2", "user2@test.com", "password2")
```
##### 결과 화면
<img width="578" alt="스크린샷 2022-04-02 오전 4 31 53" src="https://user-images.githubusercontent.com/78442839/161335060-084fb003-2161-4844-8cd0-d1144667a53f.png">
<br>

1. 데이터베이스에 Post 모델 객체 3개 넣기
##### ORM 쿼리
```django
from api.models import *

Post.objects.create(user_id=1, content="post1", like_count=0, comment_count=0)
Post.objects.create(user_id=1, content="post2", like_count=0, comment_count=0)
Post.objects.create(user_id=2, content="post3", like_count=0, comment_count=0)
```
##### 결과 화면
<img width="672" alt="스크린샷 2022-04-02 오전 4 35 38" src="https://user-images.githubusercontent.com/78442839/161335855-1b01be67-b5a9-4b94-80bb-772ba79492db.png">
<img width="669" alt="스크린샷 2022-04-02 오전 5 21 42" src="https://user-images.githubusercontent.com/78442839/161335996-a12ca91e-c97e-46b5-bee4-acf0254dbd55.png">
<br>

2. 삽입한 객체들을 쿼리셋으로 조회
##### ORM 쿼리
```django
Post.objects.all()

Post.objects.get(content="post1")
Post.objects.get(content="post2")
Post.objects.get(user_id=2)
```
##### 결과 화면
<img width="721" alt="스크린샷 2022-04-02 오전 4 37 44" src="https://user-images.githubusercontent.com/78442839/161336234-6509d709-ebdc-4ef1-b294-d5a5c25e826b.png">
<br>

3. filter 함수 사용해 조회
##### ORM 쿼리
```django
Post.objects.filter(user_id=1)
Post.objects.filter(like_count=0)
```
##### 결과 화면
<img width="699" alt="스크린샷 2022-04-02 오전 4 38 58" src="https://user-images.githubusercontent.com/78442839/161336501-ffa72eab-de3e-4baa-ab59-3754f9306bc4.png">

---

### 회고

장고에서 모델링과 ORM 적용이 처음이어서 models.py 코드를 작성하고 이를 migrate 하는 모든 과정이 익숙하지 않아 조금 헤맸지만 역시 직접 설계하고 구현해보니 훨씬 더 많은 공부가 되었던 것 같다.<br>
인스타그램 데이터 모델링을 할 때 사진, 영상 업로드 기능이라는 핵심 기능에만 초점을 맞춰야 했기 때문에 어떤 기능들을 제거하고 ERD를 만드는 게 좋을지 고민이 있었던 것 같다. 결과적으로 핵심 기능에만 집중하기 위해 팔로우, 스토리, 대댓글 등의 기능들은 과감하게 고려하지 않고 설계했다.<br>
CharField, TextField, ImageField, FileField 등 알지 못했던 부분들도 공부해보며 적용했다.<br>
이번에 장고를 통해 모델링을 해보며 가장 편리했던 점은 User 모델이 자체적으로 존재했다는 것이다. User 모델에 대해 더 자세하게 공부해보고 싶은 생각이 들어 개인적으로 Django의 User 모델에 대해 더 공부해볼 생각이다.