# 2주차 과제
## Docker란?
도커는 컨테이너를 기반으로 하여 독립적으로 애플리케이션을 실행할 수 있도록 컨테이너를 만들고 관리하는 것을 도와주는 도구입니다.

### VM 과의 차이점
![docker.com](https://images.velog.io/images/offsujin/post/5958876c-6eef-4aaf-9d62-c0cd227df6e1/VMdocker.png)

오른쪽에 보이는 VM은 호스트 OS 위에 게스트 OS를 가상화하여 사용하기 때문에 오버헤드가 많아지고 속도문제가 발생하게 됩니다.

하지만 왼쪽과 같은 Docker는 호스트 OS 위에 게스트 OS를 분리하는 것이 아니라, 프로세스를 분리하여 사용합니다.

따라서 VM 처럼 완전히 분리된 환경을 이루면서도 오버헤드를 줄일 수 있습니다.

## image와 container
![생활코딩](https://images.velog.io/images/offsujin/post/2676d4dd-074c-4884-afe2-8682c058247d/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.04.01.png)

**docker hub**는 우리가 사용하는 app store처럼 다양한 프로그램들을 다운로드, 업로드 할 수 있는 공간입니다.

**image**는 app store에서 다운받는 프로그램과 같은 의미입니다.

**container**는 프로그램에서 실행하는 프로세스라고 볼 수 있습니다.

하나의 이미지에서 여러 개의 컨테이너를 생성할 수 있고, 각각의 컨테이너는 독립된 환경을 가지고 있기 때문에 서로 영향을 받지 않습니다.

## image pull
docker hub에서 이미지를 다운받는 것을 pull이라고 합니다.

https://hub.docker.com/
위의 docker hub 사이트에 접속하면 다양한 이미지들을 확인할 수 있습니다.

![](https://images.velog.io/images/offsujin/post/46c17bd9-ed2c-4002-9a88-db856f92ab92/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.30.16.png)

`docker pull httpd` 명령어를 사용해서 아파치 웹 서버 이미지를 pull 해보겠습니다.

`docker images` 로 아래처럼 이미지가 잘 받아졌는지 확인할 수 있습니다.

![](https://images.velog.io/images/offsujin/post/62a117c6-a040-497e-85a3-0c73d082a82b/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.36.58.png)

## container
### 생성
![](https://images.velog.io/images/offsujin/post/dbd8b65d-b376-4629-a5d3-dbbd0c61159d/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.40.19.png)

`docker run httpd`

### 실행 중인 container
컨테이너가 제대로 만들어졌는지 확인하려면 ps 라는 명령어를 이용합니다.
![](https://images.velog.io/images/offsujin/post/31d0ab1c-d02f-417f-ba33-078d756dad5c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.41.19.png)
위의 결과처럼 httpd 이미지로 컨테이너가 하나 만들어진 것을 확인할 수 있습니다.

### 이름 지정
docs에서 option 카테고리에 가보면 다양한 옵션을 찾을 수 있습니다.
![](https://images.velog.io/images/offsujin/post/8972ed5e-7f17-40c0-a757-ac759d19f54c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.43.24.png)
그 중 --name 이라는 옵션을 주면 컨테이너의 이름을 지정할 수 있습니다.

만약 컨테이너 이름을 web-server라고 하고싶다면 명령어는 다음과 같습니다.

`docker run --name web-server httpd`

### 실행 중지
`docker stop web-server`를 이용해서 컨테이너를 끌 수 있습니다.

`ps` 명령어를 이용해서 컨테이너가 실행되고 있는지 확인합니다.

![](https://images.velog.io/images/offsujin/post/b91e4180-221a-401d-b92d-bf425ac77552/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.52.00.png)

컨테이너 리스트에서 ws1 컨테이너가 사라진 것을 확인했습니다.

### 재실행
이미 만들어놓은 컨테이너를 다시 시작하고 싶다면 `start` 를 사용합니다.

`docker start web-server`

`ps` 명령어에 `-a` 옵션을 지정하면 지금까지 만들어둔 사용가능한 컨테이너를 확인할 수 있습니다.
![](https://images.velog.io/images/offsujin/post/e28db155-4c18-409c-97b5-4d342dfd0951/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.55.22.png)

제가 stop시킨 ws1도 있습니다.

### 삭제
컨테이너를 지우고 싶다면 `rm`을 사용합니다.

`docker rm ws1`

간혹 에러가 뜨고 제대로 삭제되지 않는 경우가 있습니다.

이럴 때에는 `--force` 옵션을 주면 강제로 삭제할 수 있습니다.

### images 삭제

이미지는 `rmi` 라는 명령어로 삭제할 수 있습니다.

`docker rmi httpd`

## 명령어 정리

`docker pull IMAGE` : IMAGE pull

`docker rmi IMAGE` : IMAGE 삭제

`docker images` : IMAGE 리스트 보기

`docker run --name CNAME IMAGE` : IMAGE를 CNAME이라는 이름으로 컨테이너 생성

`docker ps -a` : 존재하는 컨테이너 리스트 보기

`docker ps` : 실행 중인 컨테이너 리스트 보기

`docker stop CONTAINER` : 컨테이너 실행 중지

`docker start CONTAINER` : 컨테이너 실행

***

# 3주차 과제
⚒️ refactoring: 중복되는 필드인 생성 시간, 수정 시간을 timestamp 추상 클래스로 만들어서 상속관계로 구현
## 데이터베이스 
<img width="770" alt="ERD" src="https://user-images.githubusercontent.com/88263178/161997711-49c05ae8-7f4b-4979-87b3-8d31424e7e17.png">

- profile
  - 인스타그램 프로필
  - name, 상태 메세지
  - user와 일대일 관계

- user
  - 사용자 모델
  - 장고의 기본 User 모델 사용
  
- timestamp
  - 생성 시간, 수정 시간을 가지는 추상 클래스

- comment
  - 게시글에 달리는 댓글 모델
  - 댓글은 게시글에 여러 개 달릴 수 있으므로, 일대다 관계
  - 댓글은 사용자와 일대다 관계
  - 댓글 내용, 생성시간, 수정시간(timestamp를 상속)
  
- post
  - 게시글 모델
  - 게시글은 한 유저가 여러 개 작성할 수 있으므로, 일대다 관계
  - 게시글 내용, 생성시간, 수정시간(timestamp를 상속), 좋아요 개수

- like
  - 좋아요 모델
  - 좋아요는 유저와 일대다 관계
  - 좋아요는 게시글이 여러 개 가질 수 있으므로 일대다 관계

- file
  - 게시글에 포함되는 사진이나 동영상 모델
  - 게시글은 여러 사진이나 동영상을 포함할 수 있으므로 일대다 관계
  - 파일의 이름, url path

👉 **DATETIME과 TIMESTAMP의 차이**

생성시간과 수정시간을 작성하다가 DATETIME과 TIMESTAMP 둘 중 어떤 타입을 써야할지 고민했습니다.

둘의 차이를 찾아보니 DATETIME은 입력된 날짜와 시간 그대로 데이터를 저장하지만, TIMESTAMP는 time_zone 시스템 변수로 값을 지정한다고 합니다.

TIMESTAMP는 데이터 입출력시 time_zone 시스템 변수 값을 체크해 그 기반으로 변환하여 처리하기 때문에 time_zone이 바뀌면 모든 데이터가 그 시간대에 맞게 바뀝니다.

따라서 해외에 나가는 사이트라면 TIMESTAMP를 고려해야할 것 같습니다.

저는 이번 인스타그램 프로젝트는 한국에서만 사용하는 것으로 판단하고 DATETIME으로 지정하였습니다.

## ORM 적용

### 객체 생성

<img width="1523" alt="ORM_객체생성" src="https://user-images.githubusercontent.com/88263178/161998117-22b8edba-de7d-400c-a5a2-b765e25107d8.png">


## 객체 조회
<img width="725" alt="ORM_객체조회" src="https://user-images.githubusercontent.com/88263178/161998291-48e2dcff-f71c-4012-8fc8-b9a6c91a221f.png">

## filter 사용 

<img width="1519" alt="ORM_filter1" src="https://user-images.githubusercontent.com/88263178/161998335-5f473f76-3b2c-4a67-8949-3e47ca99ce86.png">

<img width="1542" alt="ORM_filter2" src="https://user-images.githubusercontent.com/88263178/161998346-1d086b9e-0f65-4ed9-9922-3e8213b8be91.png">

***

# 4주차 과제

## 데이터 삽입
### Post, Comment 모델
Comment가 Post를 fk로 가지고 있습니다.
<img width="864" alt="스크린샷 2022-04-07 오후 3 28 04" src="https://user-images.githubusercontent.com/88263178/162134254-68a754aa-445d-4c23-bb6c-46edd437d4fe.png">

### Serializer
Nested Serializer로 구현했습니다.

<img width="618" alt="스크린샷 2022-04-07 오후 3 30 51" src="https://user-images.githubusercontent.com/88263178/162134654-4485a6c3-a2ed-4a84-851c-23a14ca102fa.png">

그런데 shell에서 데이터를 넣고 출력해보면 아래의 사진처럼 comments가 보이지 않는 오류가 발생했습니다.
<img width="676" alt="nested_serializer_error" src="https://user-images.githubusercontent.com/88263178/162134864-9e5501a8-b5ef-4506-9502-c0777740175b.png">

원인을 찾아보니 model에서 related_name이라는 필드가 있는 것을 발견하고 추가해주니 정상적으로 comments가 출력되는 것을 볼 수 있었습니다.
<img width="862" alt="ns_error_모델변경" src="https://user-images.githubusercontent.com/88263178/162134937-395dc3bc-a614-465c-8af0-653999a63477.png">
<img width="1383" alt="ns_error_해결코드" src="https://user-images.githubusercontent.com/88263178/162135082-d8ef1e0c-a97a-40fe-ba0a-a4679f23bd8b.png">

그리고 장고 admin 페이지에서 Post와 Comment를 확인해보았습니다.
<img width="804" alt="post" src="https://user-images.githubusercontent.com/88263178/162135398-9804aa92-513b-4c3e-9b5a-672735ece4be.png">

<img width="793" alt="comment" src="https://user-images.githubusercontent.com/88263178/162135408-c32e9c79-598c-4f99-83a8-1c0cd82b90cc.png">

## 모든 데이터를 가져오는 API
모든 'Post'의 list를 가져오는 API 요청 결과

url : api/post/ GET

<img width="404" alt="GET api:post" src="https://user-images.githubusercontent.com/88263178/162135599-3e599cb9-36e2-4321-a0c2-957d769059b1.png">

## 새로운 데이터를 create하도록 요청하는 API
Post를 추가하는 API 요청 결과

url : api/post/ POST

<img width="637" alt="POST api:post:" src="https://user-images.githubusercontent.com/88263178/162135684-c3b45f91-8ab3-4189-801c-99907d1acb47.png">

## 회고

