## Week 2: 도커-깃허브 액션을 이용한 자동배포

### 도커
리눅스 컨테이너에 프로세스 격리 기술을 사용해 컨테이너로서 더 쉽게 사용할 수 있게 만들어진 오픈소스 프로젝트

<img width=50% src="https://user-images.githubusercontent.com/63996052/159634175-7b3176fe-9a2f-409f-b5fd-4516807a826a.png">

<b>기존 가상화 기술</b>
  - 여러 개의 게스트 OS를 하나의 호스트 OS 위에 생성
  - 하이퍼바이저를 거쳐 성능 저하
  - 게스트 OS 사용을 위한 라이브러리, 커널 등의 포함으로 이미지 사이즈 증가 
 
<b>도커 컨테이너</b>
  - 프로세스 단위의 격리 환경으로 매우 적은 성능 손실
  - 라이브러리 및 실행파일만 포함하여 이미지 용량 저하
  - 이미지 용량 저하에 따른 배포 시간 단축

도커 사용 시 => 개발 및 배포 과정의 편리성! 애플리케이션의 독립성과 확장성!

### 깃허브 액션
깃허브 저장소를 기반으로 소프트웨어 개발 Workflow를 자동화 하는 CI/CD 도구

<img width=50% src="https://user-images.githubusercontent.com/63996052/159648278-84730dda-4f44-4881-951e-c279131ed90e.png">

- build, test, package, release, deploy 등 다양한 이벤트 기반 Workflow 생성
- Runners라고 불리는 환경에서 직접 구동 가능
- 저장소마다 최대 20개의 Workflow 등록 가능
- 각 Workflow의 Job마다 최대 6시간 동안 실행, 초과시 자동 중지
- Job에서 Github API 호출시 1시간 동안 최대 1,000번 가능

<b>장점</b>
- 다른 CI 툴과 달리 복잡하지 않은 절차, 별도 설치 필요 없음
- Workflow 복제 용이
- Github와의 통합
- 여러 OS 및 런타임 버전 동시 테스트 가능
- 모든 언어 어플리케이션 빌드, 테스트 및 배포 가능
- 설정 자체에 많은 시간을 쏟지 않아도 가능 -> 작은 규모의 프로젝트에 용이

<b>단점</b>
- 문서 부족
- 개별 Workflow 삭제 불가능
- Workflow에서 단일 Job만 실행 불가능
- 큰 규모의 프로젝트의 경우 완전하지 못한 제어

### 도커-깃허브 액션
깃허브 액션을 이용한 Docker Image Build 및 Push

![image](https://user-images.githubusercontent.com/63996052/159630360-6123b537-83fe-48f5-9406-caf8ad833e4c.png)

<b>환경</b>
```
docker
docker-compose
nginx
gunicorn
mysql
python3.8
django(>=3.0)
```

nginx는 동시접속 처리에 특화된 웹 서버 프로그램으로, Apache보다 동작이 단순하고 전달자 역할만 한다.
gunicorn은 Python WSGI(Web Server Gateway Interface)로 python으로 작성된 웹 어플리케이션과 서버 사이의 인터페이스 또는 규칙이다.


![image](https://user-images.githubusercontent.com/63996052/159658230-65687557-bd2e-42ca-aee1-25ee5168d02b.png)


nginx는 여러개의 요청을 동시에 받았을 때, 정적 파일은 클라이언트에게 바로 돌려주고 동적 파일은 gunicorn을 거쳐 django에게 요청을 넘긴다.


<b>과정</b>

`.env` 파일에 임의의 장고 시크릿 키를 생성해 입력한다.

`Dockerfile` 파일을 통해 도커 이미지를 생성한다. 이를 통해 손쉽게 동일한 이미지를 반복해서 만들 수 있다.

`docker-compose.yml` 파일로 독립된 컨테이너의 실행 옵션을 정의한다.

`docker-compose up` 커맨드를 통해 컨테이너를 개시한다.

`.env.prod` 파일에 데이터베이스(RDS) 및 EC2 ip 주소, 장고 시크릿 키 등을 입력한다.

Github Secrets-Actions에 `.env.prod`, EC2 서버 퍼블릭 DNS(IPv4) 주소, ssh key (.pem) 전문을 설정한다.

Actions 탭에서 실행하거나 master에 push 한 뒤 잠시 기다리면 다음과 같이 Github Actions 또는 EC2 DNS 주소에서 배포가 완료되었음을 확인할 수 있다.


![image](https://user-images.githubusercontent.com/63996052/159650798-0bd37772-1692-47e0-9d96-3698023c1da7.png)

![image](https://user-images.githubusercontent.com/63996052/159661427-7a280fee-1dfc-4225-9aca-c92dfe7c541d.png)

<hr>

## Week 3: 인스타그램 데이터 모델링
### 인스타그램 서비스 설명 ('사진, 영상 업로드' 기능만)
모든 서비스는 유저 로그인 기반으로 동작
- 게시글에 사진, 동영상 등록 (1개 이상)
- 게시글에 댓글 (0개 이상)
- 게시글에 좋아요 (0개 이상)
- 게시글 삭제
- 댓글 삭제
- 좋아요 취소

### 모델 설명
<img width=75% src="https://user-images.githubusercontent.com/63996052/160384055-0edaa6fa-ed15-4afc-98e9-82f3982fc34a.png">

**[User]**
- 장고에서 기본으로 제공하는 auth_user와 OneToOne Link with User Model (Profile) (OneToOneField)
- 이름, 사용자 이름(아이디), 비밀번호, 웹사이트, 소개 컬럼
- 생성 날짜, 업데이트 날짜, 삭제 여부
- 사진, 영상 업로드 기능에만 집중하기 위해 유저의 다른 정보들은 생략

**[Post]**
- User와 1:N 관계, user_id (Foreignkey)
- 내용 컬럼, 생성 날짜, 업데이트 날짜, 삭제 여부

**[File]**
- Post와 1:N 관계, post_id (Foreignkey)
- 타입(이미지/비디오), 해당 파일의 url 주소 컬럼
- 생성 날짜, 업데이트 날짜, 삭제 여부

**[Like]**
- User와 N:M, Post와 N:M 관계 (ManyToManyField)
- 삭제 여부

**[Comment]**
- User와 N:M, Post와 N:M 관계 (ManyToManyField)
- 생성 날짜, 업데이트 날짜, 삭제 여부 

### ORM 적용해보기
1. 데이터베이스에 해당 모델 객체 3개 넣기
2. 삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)
3. filter 함수 사용해보기


### 회고
