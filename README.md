CEOS 14기 백엔드 스터디 모델링 및 drf 연습을 위한 레포

## Docker와 Github Action

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