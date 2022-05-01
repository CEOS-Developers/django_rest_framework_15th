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


### 과제하면서 느낀 점

> 사용해봤던 ERD 툴이였고 Mysql 이였지만 생각보다 많은 오류에 부딪히게 되어 당황하고 많이 배운 과제였다. 
> 인스타그램을 뜯어보면서 생각보다 많이 어렵다고 생각했고 정말 인스타그램 개발자들은 천재인가 싶었다.
> 처음 mysql을 homebrew로 설치하는데 경로 오류가 지속적으로 발생하여 많이 당황했고 로컬 환경에서 mysqlclient 설치에도 어려움을 겪어 많이 당황했었다.
> 또, 처음 장고를 사용하면서 테이블들을 models.py에 객체로써 구현하는게 어색했고 많이 어려웠지만 오히려 많은 공부가 되었던 것 같아 좋은 경험이라 생각한다.
> 위의 문제들은 구글링을 통해 간단히 해결했지만, ORM을 사용하면서 부딪힌 문제는 쉽게 해결이 되지 않았다.
> User 생성에 계속 실패하여 (last_login 컬럼 문제) 검색해봤지만 전부 영어 문서여서 제일 믿음직한 스택 오버플로우에서 시키는대로 mysql에 접속 후, 
> 생성 db를 삭제하고 migrations 파일들을 전부 삭제 후 다시 진행하는 방법을 택했다. (배포 후에는 사용하면 안된다고 함) 
> 장고뿐만 아니라 데이터베이스, erd 설계 공부 등이 더 필요하다고 생각하게 되는 과제였다.


## Serializer를 이용하여 Views.py 작성

### models.py 수정

> 과제 발표할 때 들었던 수정사항들과 Serializer를 사용하면서 발생한 문제점들에 대해 수정

```
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성 시 현재 시간 자동 저장
    updated_at = models.DateTimeField(auto_now=True)  # 해당 레코드 갱신 시 현재 시간 자동 저장
    status = models.CharField(max_length=20, default='valid')

    class Meta:
        abstract = True
        
```

* created_at, updated_at, status 같은 중복 컬럼들은 따로 클래스로 선언 후 상속

```
class Post(BaseModel):
  ...
    liking_count = models.PositiveIntegerField(default=0)
    
```

* 좋아요 카운트를 하나의 컬럼으로 생성

```
class Following(BaseModel):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followerUser')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followingUser')

    def __str__(self):
        return '{} : {}'.format(self.follower.nickname, self.following.nickname)

```

* 팔로잉 테이블 생성 시 related_name을 지정하여 한 테이블이 동시에 참조 가능하게 설정


### 데이터 삽입

> django shell을 통해 Profile 데이터 3개 삽입

![스크린샷 2022-04-08 오후 10 07 13](https://user-images.githubusercontent.com/59060780/162441746-1035fa6f-e67c-4318-b1da-a679f3994cce.png)


### API 만들기

#### ModelSerializer 사용

```
# api.serializers.py

from rest_framework import serializers
from api.models import *


class LikeSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Liking
        fields = '__all__'

    def get_user_nickname(self, obj):
        return obj.user.nickname


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user_nickname(self, obj):
        return obj.user.nickname


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    liked_post = LikeSerializer(many=True, read_only=True, source='liking_set')
    comment_post = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Post
        fields = '__all__'

    def get_author_nickname(self, obj):
        return obj.author.nickname


class ProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True, read_only=True, source='post_set')
    user_like_posting = LikeSerializer(many=True, read_only=True, source='liking_set')
    user_add_comment = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Profile
        fields = '__all__'

```

#### FBV (함수 기반으로 뷰 작성)
```
# api.views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import *
from api.serializers import *
from rest_framework import viewsets

@csrf_exempt
def post_api(request):
    if request.method == 'GET':
        post_list = Post.objects.all()
        serializer = PostSerializer(post_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def post_detail(request, pk):
    try:
        get_post = Post.objects.get(pk=pk)
        serializer = PostSerializer(get_post)
        return JsonResponse(serializer.data)
    except Post.DoesNotExist:
        return JsonResponse(status=404)


@csrf_exempt
def profile_api(request):
    if request.method == 'GET':
        profile_list = Profile.objects.all()
        serializer = ProfileSerializer(profile_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def profile_detail(request, pk):
    try:
        get_profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(get_profile)
        return JsonResponse(serializer.data)
    except Profile.DoesNotExist:
        return JsonResponse(status=404)


```

#### Url 연결

```
# api.urls.py

urlpatterns = [
    path('api/post/', views.post_api),
    path('api/post/<int:pk>', views.post_detail),
    path('api/profile', views.profile_api),
    path('api/profile/<int:pk>', views.profile_detail),
]

```

#### API 결과 

> 모든 Profile 가져오기
> > URI: api/profile/
> > Method : GET

```
# JSON
[
    {
        "id": 1,
        "created_at": "2022-04-08T17:57:14.213173+09:00",
        "updated_at": "2022-04-08T17:57:14.213301+09:00",
        "status": "valid",
        "name": "test1",
        "nickname": "sanbonai06",
        "profile_scripts": "",
        "profile_image": "",
        "user": 1
    },
    {
        "id": 2,
        "created_at": "2022-04-08T21:42:28.206798+09:00",
        "updated_at": "2022-04-08T21:42:28.206819+09:00",
        "status": "valid",
        "name": "",
        "nickname": "고스락키보드",
        "profile_scripts": "",
        "profile_image": "",
        "user": 2
    },
    {
        "id": 3,
        "created_at": "2022-04-08T21:45:58.555640+09:00",
        "updated_at": "2022-04-08T21:45:58.555664+09:00",
        "status": "valid",
        "name": "",
        "nickname": "min_zzoni",
        "profile_scripts": "",
        "profile_image": "",
        "user": 3
    }
]

```

> Profile 생성
> > URI: api/profile/
> > Method : POST

![스크린샷 2022-04-08 오후 10 13 22](https://user-images.githubusercontent.com/59060780/162442795-911a0529-ada9-4c4c-b99b-a2d6c4c3d35e.png)


> Profile을 통해 새로운 게시글(Post) 생성 API
> > URI: api/post
> > Method: POST

![스크린샷 2022-04-08 오후 10 14 46](https://user-images.githubusercontent.com/59060780/162443017-73db9c4f-15a4-4959-885f-e7b57ab681cd.png)


> 모든 Post 가져오기
> > URI: api/post
> > Method: GET

```
# JSON
[
    {
        "id": 1,
        "author_nickname": "sanbonai06",
        "created_at": "2022-04-08T18:10:15.875153+09:00",
        "updated_at": "2022-04-08T18:10:15.875196+09:00",
        "status": "valid",
        "script": "test1",
        "type": "Posting",
        "liking_count": 0,
        "author": 1,
        "location": 1
    },
    {
        "id": 2,
        "author_nickname": "sanbonai06",
        "created_at": "2022-04-08T21:00:01.300981+09:00",
        "updated_at": "2022-04-08T21:00:01.301034+09:00",
        "status": "valid",
        "script": "test2",
        "type": "Posting",
        "liking_count": 0,
        "author": 1,
        "location": 1
    },
    {
        "id": 3,
        "author_nickname": "sanbonai06",
        "created_at": "2022-04-08T22:14:40.392765+09:00",
        "updated_at": "2022-04-08T22:14:40.392801+09:00",
        "status": "valid",
        "script": "test2",
        "type": "Posting",
        "liking_count": 0,
        "author": 1,
        "location": 1
    }
]

```


### 과제하면서 느낀 점

> API 단 두개만 만들면 된다 생각한 과제였지만 호되게 당해버렸다... 그동안 프로젝트를 쿼리문을 이용해서 만들었었는데 ORM을 직접 사용해보니 생각보다 어려운 점이 많았던 것 같다.
> Serializer를 선언하면서 테이블 끼리의 참조관계에 대해 굉장히 헷갈렸고 어려움을 겪었다. 실제 쿼리문 작성처럼 생각하면 안된다는 것을 깨달았다. 그리고 처음엔 User 테이블 자체를 참조하려 했지만 여러 오류를 겪고 Profile 테이블 참조로 바꾸었다.
> Views.py를 작성할 때도 마찬가지였다. Serializer부터 오류가 발생하니 모든게 엉망이였다. 결국 여러 정보들을 찾아보며 해결하였지만 여러 API들을 구현하려면 더 많은 공부가 필요하다는 것을 깨달았다.