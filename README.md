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

<br>

> `related_name 옵션` <br>
> ForeignKey를 통해 연결되어 있는 모델들 사이에서 역참조를 할 수 있게끔 필드명을 지정함
> <br>
> ex.) Comment 모델을 ForeignKey를 통해 User 모델로 연결을 했을 때, User의 Comment 들을 불러올 수 있게끔 필드명을 지정해준 것

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

<br>

---

### Django Admin

특정 모델클래스를 admin에 등록하면, 해당 모델을 어드민 계정을 통해 GUI 환경에서 관리 가능함

#### Model Admin 등록방법

1. 기본 ModelAdmin
```python
from django.contrib import admin
from api.models import *

admin.site.register(Post)
```

2. 기본 ModelAdmin 등록 후 커스터마이징
```python
from django.contrib import admin
from api.models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']

admin.site.register(Post, PostAdmin)
```

3. decorator 형태로 ModelAdmin 등록
```python
from django.contrib import admin
from api.models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']
```
<br>

- ModelAdmin 옵션
  - list_display : 보여질 필드 목록
  - list_display_links : 목록 내에서 링크 지정할 필드 목록
  - list_editable : 목록 내에서 수정할 필드 목록
  - list_per_page : 페이지 별로 보여질 최대 갯수
  - list_filter : 필터 옵션

<br>

## 4주차 DRF1: Serializer

---

### Serializer 란

queryset 및 모델 인스턴스와 같은 복잡한 데이터를 JSON, XML 등의 content type 쉽게 변환 가능한 python datatype으로 변환시켜줌

`Deserialize` 는 받은 데이터 (parse -> python datatype)를 validating 한 후에 parsed data를 복잡한 타입으로 다시 변환해주는 것을 말함

생성한 모델을 대상으로 serializing 할 수 있는 `ModelSerializer` 클래스가 존재하며 **create()** 와 **update()** 함수 또한 미리 구현되어 있어 해당 클래스를 사용해주면 편리함
```python
from rest_framework import serializers
from api.models import *

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['id', 'user', 'content', 'like_count', 'comment_count', 'files']
```

### Nested Serializer

다른 모델과 가지고 있는 relationship을 표현해 두 모델을 사용할 수 있음
```python
from rest_framework import serializers
from api.models import *

class FileSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
	files = FileSerializer(many=True, read_only=True)

	class Meta:
		model = Post
		fields = ['id', 'user', 'content', 'like_count', 'comment_count', 'files']
```

### Serializer Method Field

serializer의 필드로 relationship을 가지는 다른 모델의 필드를 가져올 수 있음

```python
from rest_framework import serializers
from api.models import *


class FileSerializer(serializers.ModelSerializer):
	post_id = serializers.SerializerMethodField()

	class Meta:
		model = File
		fields = '__all__'

	def get_post_id(self, obj):
		return obj.post.id
```
<br>

---

### View

- GET<br>
  모델 인스턴스들을 받아 serializing 한 JSON 데이터를 JsonResponse()를 통해 반환함


- POST<br>
  사용자가 입력한 JSON 데이터를 JSONParser()를 통해 parse함<br>
  해당 데이터를 serializing 해준 뒤, is_valid() 를 통해 유효한 데이터임을 알아내면 JsonReponse()를 통해 201 상태코드와 함께 JSON 데이터를 반환해줌
  - 만약 유효하지 않은 데이터임이 드러나면 (is_valid()) 에러와 함께 400 상태코드를 반환해줌

<br>

---

### 데이터 삽입

Post 모델 & File 모델
```python
class Post(DateTime):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
	content = models.TextField()
	like_count = models.PositiveIntegerField(default=0)
	comment_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.content


class File(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
	type = models.PositiveIntegerField() # 0: photo, 1: video
	path = models.CharField(max_length=300)
```

<img width="958" alt="스크린샷 2022-04-28 오전 12 10 39" src="https://user-images.githubusercontent.com/78442839/165579522-9d291e95-0ad7-43b3-8e64-15b23a101508.png">
<img width="957" alt="스크린샷 2022-04-28 오전 12 11 16" src="https://user-images.githubusercontent.com/78442839/165579626-cc0ca748-caa8-4675-beb4-3cae9b9a371b.png">

### 모든 데이터를 가져오는 API

- **URL**: `api/posts/`
- **Method**: `GET`

```
[
    {
        "id": 1,
        "content": "post content 1",
        "like_count": 0,
        "comment_count": 0,
        "files": [
            {
                "id": 1,
                "post_id": 1,
                "type": 0,
                "path": "post1.photo.path1",
                "post": 1
            }
        ]
    },
    {
        "id": 2,
        "content": "post content 2",
        "like_count": 0,
        "comment_count": 0,
        "files": [
            {
                "id": 2,
                "post_id": 2,
                "type": 1,
                "path": "post2.video.path1",
                "post": 2
            }
        ]
    },
    {
        "id": 3,
        "content": "post content 3",
        "like_count": 0,
        "comment_count": 0,
        "files": [
            {
                "id": 3,
                "post_id": 3,
                "type": 0,
                "path": "post3.photo.path1",
                "post": 3
            }
        ]
    }
]
```

### 새로운 데이터를 create하도록 요청하는 API

- **URL**: `api/posts/`
- **Method**: `POST`
- **Body**
  ```
  {
      "user": 2,
      "content": "post 4",
      "like_count": 0, 
      "comment_count": 0
  }
  ```

**결과**
```
{
    "id": 4,
    "user": 2,
    "content": "post 4",
    "like_count": 0,
    "comment_count": 0,
    "files": []
}
```
<br>

---

### 회고

Nested Serializer를 공부하면서 생각보다 에러가 나는 부분들이 많아 고생을 조금 했다.
처음에는 욕심을 내서 profile, file, post, comment 까지 전부 중첩해서 가져올 수 있을 것 같다는 생각에 시도를 하였는데 자잘자잘한 오류가 발생하여 Nested Serializer에 대해 조금 더 공부를 해본 뒤, 다시 시도해 보려고 한다.
그리고 views에 safe=False 옵션을 주라는 오류가 몇 번 발생해서 해당 부분을 추가하였더니 잘 작동하였다.
마지막으로 Django Admin을 이번에 나름 적극적으로 활용해봤는데, 정말 편리한 기능인 것 같아서 앞으로 Django를 사용하는 동안 유용하게 활용할 수 있을 것 같다.


<br>

## 5주차 DRF2: API View

---

### Django View

장고에서는 기본적으로 `FBV(함수 기반 뷰)`, `CBV(클래스 기반 뷰)` 2가지의 view 방식을 제공함

**`FBV`**

- 함수 기반 뷰라는 말 그대로 직접 함수를 작성하여 request를 처리하는 view 방식
- if 조건문을 사용해 request 메소드들을 처리해줌

> **장점**
> - 구현이 쉽고 편리함
> - 함수로 정의되어 직관적이고 읽고 이해하기 편함
> - 데코레이터 사용이 간단함
>
> **단점**
> - 코드 확장이나 재사용이 어려움

<br>

**`CBV`**

- django.views.View 클래스를 상속받아 생성함
- request 메소드가 GET이라면 클래스 내의 get() 메소드를 실행하는 방식으로 처리

> **장점**
> - 확장, 재사용이 용이함
> - 다중 상속, Mixin이 가능함
> - 클래스 안에서 HTTP 메소드가 분리되어 처리됨
> - 내장 Generic Class View를 사용할 수 있음
>
> **단점**
> - 코드가 직관적이지 않아 읽고 이해하기 어려움
> - 상속으로 인해 코드를 찾아봐야 함
> - 데코레이터 사용이 어려움

<br>

> 각각 장단점이 존재하기 때문에 코드 재사용이나 확장이 필수적인 상황에서는 CBV를, 빠른 구현이 필요한 상황에서는 FBV를 사용하는 등 적절하게 view를 구현하는 것이 좋음

---

### DFR API View

DRF가 제공하는 `APIView` 클래스는 장고의 View 클래스를 상속받은 클래스

- **`FBV`** 는 `@api_view` 데코레이터를 사용하고, 데코레이터 안에 HTTP 메소드를 명시하여 해당 뷰로 요청이 들어왔을 때 `request.method`로 구분하여 마찬가지로 if문에 따라 생성한 구문을 실행함
- **`CBV`** 는 `APIView`를 상속받아 원하는 클래스를 생성하여 클래스 내에 HTTP 메소드를 처리할 함수를 정의하여 사용함

#### Request 객체

- DRF에서 HTTP 요청을 나타내는 객체로서 HttpRequest 객체를 확장한 Request 객체를 사용함
- `request.data` 속성을 통해 임의의 데이터를 처리하고, POST, PUT, PATCH 메소드에서 동작

#### Response

- DRF에서 요청에 대한 응답을 나타내는 객체로서 Response 클래스를 상속받아 사용 가능함
- 렌더링 되지 않은 내용을 읽어서 클라이언트가 요청한 content-type으로 자동 렌더링해줌

#### HTTP Status Code

- 뷰에서 HTTP 상태코드를 단순 숫자로 적는 것은 가독성이 떨어지고, 찾아내기 쉽지 않다는 불편함이 존재함
- DRF에서 status 라는 모듈을 통해 `HTTP_400_BAD_REQUEST`와 같이 상태코드 400을 나타내면서 가독성을 높이고 실수를 줄일 수 있음

---

### API

#### 모든 데이터를 가져오는 API

- **URL**: `api/posts/`
- **Method**: `GET`

```
[
    {
        "id": 1,
        "user": 1,
        "user_name": "세오스",
        "content": "'세오스'가 쓴 글입니다..!",
        "like_count": 1,
        "comment_count": 2,
        "created_at": "2022-05-06T09:16:33.294686+09:00",
        "updated_at": "2022-05-06T09:45:03.791325+09:00",
        "files": [
            {
                "id": 1,
                "type": 0,
                "path": "path/file/photo/ceos",
                "post": 1
            }
        ],
        "comments": [
            {
                "id": 1,
                "post": 1,
                "user": 2,
                "user_name": "강아지",
                "content": "좋아요",
                "created_at": "2022-05-06T09:21:03.163971+09:00",
                "updated_at": "2022-05-06T09:21:03.164031+09:00"
            },
            {
                "id": 2,
                "post": 1,
                "user": 3,
                "user_name": "사람",
                "content": "good",
                "created_at": "2022-05-06T09:21:12.157263+09:00",
                "updated_at": "2022-05-06T09:21:21.801101+09:00"
            }
        ],
        "likes": [
            {
                "id": 1,
                "post": 1,
                "user": 3,
                "user_name": "사람",
                "created_at": "2022-05-06T09:24:06.153134+09:00",
                "updated_at": "2022-05-06T09:24:06.153156+09:00"
            }
        ]
    },
    {
        "id": 2,
        "user": 2,
        "user_name": "강아지",
        "content": "'강아지'가 쓴 글입니다..!",
        "like_count": 2,
        "comment_count": 1,
        "created_at": "2022-05-06T09:16:45.769622+09:00",
        "updated_at": "2022-05-06T09:45:08.696673+09:00",
        "files": [
            {
                "id": 2,
                "type": 1,
                "path": "path/file/video/dog_1",
                "post": 2
            },
            {
                "id": 3,
                "type": 1,
                "path": "path/file/video/dog_2",
                "post": 2
            }
        ],
        "comments": [
            {
                "id": 3,
                "post": 2,
                "user": 3,
                "user_name": "사람",
                "content": "귀여워요",
                "created_at": "2022-05-06T09:23:27.272324+09:00",
                "updated_at": "2022-05-06T09:23:27.272374+09:00"
            }
        ],
        "likes": [
            {
                "id": 2,
                "post": 2,
                "user": 1,
                "user_name": "세오스",
                "created_at": "2022-05-06T09:24:12.020690+09:00",
                "updated_at": "2022-05-06T09:24:12.020771+09:00"
            },
            {
                "id": 3,
                "post": 2,
                "user": 3,
                "user_name": "사람",
                "created_at": "2022-05-06T09:24:17.886407+09:00",
                "updated_at": "2022-05-06T09:24:17.886430+09:00"
            }
        ]
    },
    {
        "id": 3,
        "user": 3,
        "user_name": "사람",
        "content": "'사람'이 쓴 글입니다..!",
        "like_count": 0,
        "comment_count": 0,
        "created_at": "2022-05-06T09:16:57.585530+09:00",
        "updated_at": "2022-05-06T09:16:57.585625+09:00",
        "files": [
            {
                "id": 4,
                "type": 0,
                "path": "path/file/photo/person",
                "post": 3
            }
        ],
        "comments": [],
        "likes": []
    }
]
```

<br>

#### 특정 데이터를 가져오는 API

- **URL**: `api/posts/<int:pk>/`
- **Method**: `GET`

`api/posts/1/` **결과**
```
{
    "id": 1,
    "user": 1,
    "user_name": "세오스",
    "content": "'세오스'가 쓴 글입니다..!",
    "like_count": 1,
    "comment_count": 2,
    "created_at": "2022-05-06T09:16:33.294686+09:00",
    "updated_at": "2022-05-06T09:45:03.791325+09:00",
    "files": [
        {
            "id": 1,
            "type": 0,
            "path": "path/file/photo/ceos",
            "post": 1
        }
    ],
    "comments": [
        {
            "id": 1,
            "post": 1,
            "user": 2,
            "user_name": "강아지",
            "content": "좋아요",
            "created_at": "2022-05-06T09:21:03.163971+09:00",
            "updated_at": "2022-05-06T09:21:03.164031+09:00"
        },
        {
            "id": 2,
            "post": 1,
            "user": 3,
            "user_name": "사람",
            "content": "good",
            "created_at": "2022-05-06T09:21:12.157263+09:00",
            "updated_at": "2022-05-06T09:21:21.801101+09:00"
        }
    ],
    "likes": [
        {
            "id": 1,
            "post": 1,
            "user": 3,
            "user_name": "사람",
            "created_at": "2022-05-06T09:24:06.153134+09:00",
            "updated_at": "2022-05-06T09:24:06.153156+09:00"
        }
    ]
}
```

<br>

#### 새로운 데이터를 생성하는 API

- **URL**: `api/posts/`
- **Method**: `POST`

- **Body**
  ```
  {
      "user": 2,
      "content": "'강아지'가 쓴 두 번째 글입니다..!",
      "like_count": 0,
      "comment_count": 0
  }
  ```

**결과**
```
{
    "id": 5,
    "user": 2,
    "user_name": "강아지",
    "content": "'강아지'가 쓴 두 번째 글입니다..!",
    "like_count": 0,
    "comment_count": 0,
    "created_at": "2022-05-06T11:09:09.344227+09:00",
    "updated_at": "2022-05-06T11:09:09.344303+09:00",
    "files": [],
    "comments": [],
    "likes": []
}
```

<br>

#### 특정 데이터를 업데이트하는 API

- **URL**: `api/posts/<int:pk>/`
- **Method**: `PUT`

- **Body**
  ```
  {
    "user": 2,
    "content": "'강아지'가 수정한 글",
    "like_count": 1,
    "comment_count": 1
  }
  ```

`api/posts/5/` **결과**
```
{
    "id": 5,
    "user": 2,
    "user_name": "강아지",
    "content": "'강아지'가 수정한 글",
    "like_count": 1,
    "comment_count": 1,
    "created_at": "2022-05-06T11:09:09.344227+09:00",
    "updated_at": "2022-05-06T11:22:42.902466+09:00",
    "files": [],
    "comments": [
        {
            "id": 4,
            "post": 5,
            "user": 1,
            "user_name": "세오스",
            "content": "cute",
            "created_at": "2022-05-06T11:12:53.836951+09:00",
            "updated_at": "2022-05-06T11:12:53.837036+09:00"
        }
    ],
    "likes": [
        {
            "id": 4,
            "post": 5,
            "user": 3,
            "user_name": "사람",
            "created_at": "2022-05-06T11:12:29.682022+09:00",
            "updated_at": "2022-05-06T11:12:29.682128+09:00"
        }
    ]
}
```

<br>

#### 특정 데이터를 삭제하는 API

- **URL**: `api/posts/<int:pk>/`
- **Method**: `DELETE`

`api/posts/5` **결과**

<img width="908" alt="스크린샷 2022-05-06 오전 11 25 48" src="https://user-images.githubusercontent.com/78442839/167059500-06ebd00c-a438-4404-8c98-1139d3e2b4d1.png">

---

### 회고

view 완성하는 것이 메인인 주차였지만 역시나 이번 주차에도 serializer에 더 시간을 많이 투자한 것 같다. 저번 PR에서는 serializer method field를 이용해 id 필드를 가져오기도 했으나 굳이 pk값인 id 필드를 따로 작업해주지 않아도 모델에 등록되어 있는 필드 이름만 serializer에 제대로 넣어주면 알아서 id 값을 가져온다는 것도 알게되어 serializer 코드 리팩토링을 하게 되었다.<br>
좋았던 점은 저번 주차에 이어서 이번 주차까지 FBV와 CBV를 모두 써보면서 장단점을 직접 느낄 수 있었던 것 같아 앞으로 적절하게 사용할 수 있을 것 같다.<br>
작업을 하면서 `def get_object()` 함수의 로직이 스터디 초반에 공부했던 django.shortcuts 모듈의 `get_object_or_404()`와 동일하다는 것이 생각나 해당 함수를 이용해 구현을 해주었다. 
