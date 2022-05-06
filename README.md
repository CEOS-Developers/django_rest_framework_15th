#### CEOS 15기 백엔드 스터디 (2) 모델링 및 drf 연습을 위한 레포


---
# 2. Docker

<details>
<summary> </summary>
<div markdown="1">       

## Docker

## 'Docker file', 'Docker-image', 'Docker-container' 
  ![92180EDC-95C4-4CAF-B9E1-13307D9AE09A](https://user-images.githubusercontent.com/77188666/160082911-846ce296-23c1-4351-a0e7-de671be024ae.jpeg)

### (1) Dockerfile 이란?
- 필요한 최소한의 패키지를 설치하고 동작하기 위한 자신만의 설정을 담은 파일.
- 이 파일로 이미지를 생성(빌드)함

**존재이유**
- 매번 애플리케이션을 동작하는 환경을 구성하기 위해 -> `패키지 설치`,  `환경설정 과정`을 반복하는 것이 불편
- `컨테이너`에 설치하는 `패키지`,`소스코드`,`명령어`,`환경변수설정` 등을 기록한 하나의 파일 `Dockerfile`을 통해 `환경변수 및 셋팅 값 명시화`
- `Dockerfile` 빌드-> 자동`Dockerimage` 생성 -> 애플리케이션 빌드/배포 자동화

.

### (2) Docker Image 란?
- 도커 컨테이너를 구성하는 파일 시스템과 실행한 애플리케이션 설정을 하나로 합친 것  
(Docker container를 생성하는 템플릿)
- 도커 이미지는 도커 컨테이너를 생성하기 위해 반드시 필요한 파일!
- 파일명을 `Dockerfile`로 저장하면, - docker가 호출한 디렉토리 내 `Dockerfile`로 저장되어 있는 파일로 컨테이너를 생성함
- 도커 이미지는 `레이어 저장방식`으로 컨테이너를 실행하기 위한 모든 정보를 가지고 있어 용량이 큼

.

## Docker의 장점
- **쉬운 컨트롤**
- **경량화**
- **CI/CD**

#### 경량화
- VM처럼 하드웨어 emulation 기반 virtualization 과 달리 `커널을 직접 컨트롤`하는 `container`기반 `Docker`는 리소스와 기능이 제한되어 있는 환경에서도 배포 가능하도록 경량화된 application 제공

#### CI/CD
- 지속적인 통합과 자동 배포를 진행하기 위해서 서비스 운영 환경을 패키징 하는 것

### Docker Compose ?
- `다중 컨테이너` 도커 애플리케이션을 정의하고 동작하게 해주는 툴.
- 'YAML`파일로 작성( 작성된 yaml 파일로 모든 서비스들을 생성하고 시작을 하나의 명령어로 실행 )

#### docker-compose.yml
![A2C3D26E-1D1A-4068-9462-C8719AA225A4](https://user-images.githubusercontent.com/77188666/160082978-dfc08651-c3e5-471d-b4e0-8ba07daf7b45.jpeg)
  
---

</div>
</details>

---
# 3. Instagram Data Modeling

<details>
<summary> </summary>
<div markdown="1">     
  
### Django-MySQL(local) Connect

- Django project 에서 `.env` 파일 수정
```
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
DATABASE_SECRET_KEY=
```
- Django Project 에서 shell `python manage.py migrate`  
- MySQl 8.0 Command Line Client
```
show databases;         # DB 목록
use `database_name`;    # DB 사용
show tables;            # 전체 Table 조회
```
- [X] MySQL Query에 `;`을 꼭 사용
- 실행 결과
![mysql2](https://user-images.githubusercontent.com/77188666/161371240-8400acac-c893-4953-8a2c-b55463a1f95a.PNG)

---
### Makemigrations, Migrate

1. models.py 수정 

2. makemigrations file 생성  
    `python manage.py makemigrations app_name --name migration_tag_name`

3. makemigrations file 로 migrate  
    `python manage.py migrate app_name {number_of_migration}`
---
### ERD (using ERDCloud)
- ERD Diagram
![CEOS15](https://user-images.githubusercontent.com/77188666/160993717-d5db4812-5d7c-400d-9075-8b9d77481bb1.png)


#### DB Model ( [api/model.py](https://github.com/yourzinc/django_rest_framework_15th/blob/yourzinc/api/models.py) 주석 참고 )
 
1. Post 게시글  
2. Comment  댓글  
3. File  이미지 파일  
4. Tag  이미지 태그  
5. Alttext  대치 텍스트  
6. Hashtag  해시태그  
7. PostLike  게시글 좋아요  
8. CommentLike  댓글 좋아요  
9. User  사용자  
10. ~~Follow  팔로우/팔로잉~~ 
---
## Relationship 
### 1:1 Relationship  
X

### 1:N Relationship  

- `User : Post`, `User : Comment`, `User : Tag`, `User : PostLike`, `User : CommentLike`  
- `Post : Comment`, `Post : File`, `Post : Hashtag`, `Post : PostLike`  
- `File : Tag`, `File : Alttext`  
- `Comment : CommentLike`  

### N:M Relationship
- `Follow : User`

---

### Django Model Data Type

####
|Data type|Django model type|MySQL DDL|
|---|---|---|
|Boolean|models.BooleanField()|bool NOT NULL|
|Date/time|models.DateField()|date NOT NULL|
|Date/time|models.DateTimeField()|datetime NOT NULL|
|Number|models.AutoField()|integer AUTO_INCREMENT NOT NULL|
|Number|models.IntegerField()|integer NOT NULL|
|Number|models.DecimalField(decimal_places=X,max_digits=Y)|numeric(X, Y) NOT NULL|
|Text|models.CharField(max_length=N)|varchar(50) NOT NULL|
|Text (Specialized)|models.FileField()|varchar(100) NOT NULL|

---
### Image File Upload with Django  

1. `POST` method => `request.FILES`

2. Django 의  model fields : `FileField`, `ImageField`  
   - `database`가 아닌 `filesystem`에 저장
   - `actual file`의 `reference`를 가지고 있는 `string field`
   - `FileField`나 `ImageField`를 지우면 `physical file`은 지우지 않고, `reference` 만 지워짐  

3. DB 에는 `FileField`, `ImageField`의 `reference url`을 저장 `[ TYPE = VARCHAR ]`   

##### Reference : https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html  

---

#### Model 의 Primary Key 설정
```
id = models.BigIntegerField()               # type 1
id = models.AutoField(primary_key=True)     # type 2 ( Automatic primary key )
```
---
## ORM Query
Django Terminal > `python manage.py shell`  
`>>> from api.models import *`

### 1. CREATE  
- Type 1
```
>>> u = User(username="yourzinc", password="password", name="Kim Ayeon", contact="01000000000", birth="0000-00-00")
>>> u.save()
>>> p = Post(user=u, caption="hello_world", location="Seoul")
>>> p.save()
```

- Type 2
```
>>> User.objects.create(username="myzinc", password="password", name="Kim Ayeon", contact="01000000000", birth="0000-00-00")
>>> Post.objects.create(user=User.objects.get(username="myzinc"), caption="goodbye_world_again", location="Seoul")
```
  
### 2. GET -all  

```
>>> User.objects.all()
>>> Post.objects.all()
```

- result
![user objects all()](https://user-images.githubusercontent.com/77188666/161371328-9ca50cbc-7901-4dac-b09f-f00e98a3a5b8.PNG)  
  
### 3. GET

```
>>> User.objects.get(id=0)      # ERROR (doesn't exist)
>>> User.objects.get(id=1)
>>> User.objects.get(id=2)
>>> User.objects.get(id=3)      # ERROR (doesn't exist)
```
- `id(primary key index)`는 1부터 count

- result
![user objects get(id)](https://user-images.githubusercontent.com/77188666/161371294-3cee271c-5f65-4842-ae35-bf7a79064e1c.PNG)

### 4. FILTER

```
>>> User.objects.filter(name="Kim Ayeon")
>>> User.objects.filter(name="Kim Ayeon").exclude(username="yourzinc")

>>> Post.objects.filter(location="Seoul").exclude(user=User.objects.get(id=1))
>>> Post.objects.filter(location="Seoul").exclude(user=User.objects.get(id=1)).exclude(caption="goodbye_world_again")
```
- exclude, include 의 연쇄적 사용
- result
![queryset exercise](https://user-images.githubusercontent.com/77188666/161371388-47721a98-be40-41d4-9ace-f2cdfb4b50c1.PNG)
  

#### Extra : Python return format

Post
```
    def __str__(self):
        return "{} {} {}".format(self.created_at, self.user.username, self.caption)
        # 출력 형식 = 생성일 + user_id + 내용
```

User
```
    def __str__(self):
        return "{} {}".format(self.id, self.username)
        # 출력 형식 = id + user_id
```

### 회고
```
MySQL은 RDBMS으로 Model을 만들 때, Fields와 Key에 대해 명확히 정의해야 한다는 것을 알게 되었다. 

Model을 정의한 후 Relation을 정의할 때 1:1, 1:N, N:M로 나눌 때 다시 Model을 수정하기도 했다.
Model은 한번에 완벽하게 정의 할 수 없는 것을 깨닫고, 새로운 Model이 추가될 때마다 기존의 Model과의 관계성을
고려해야 함을 알게 되었다.

Django에서, SQl문을 대신한 ORM Query들이 편하게 느껴졌다

이전에는 user가 upload한 file이 DB에 바로 저장이 된다고 알았는데,
그게 아닌, file의 위치가 VARCHAR type으로 DB에 저장되는 것을 알게 되었다.

PC와 mobile app으로 Instagram을 들어가 service가 어떻게 작동하는지 분석하고, 실제 DB를 구현하는 과정에서
1. 생각보다 엄청나게 많은 정보를 너무나 빠르게 처리하고 있다는 것,
2. DB의 Size가 가늠이 되지 않을 정도로 크다는 것,
3. 보기엔 단순하지만 실제 완벽한 모델링으로 구현하기 어렵다는 것을
을 알게 되었다.

특히 게시글에 첨부하는 사진 파일과 동영상 파일을 
1. 하나의 Model로 정의하려고 했고,
2. 따로 구분하여 Model을 정의하려고 했지만,

두 방법에 모두 난항을 겪어 결국 사진 파일 모델만 작성했다.

-1 하나의 model로 정의하려고 할 때 어려운 점은 video 항목만 가지고 있는 `is_muted`, `init_image`, `is_reels` 등의 설정 때문이다
-2 따로 구분하여 Model로 정의하려고 할 때 어려운 점은 하나의 post에는 반드시 하나 이상의 file이 첨부되어야 한다는 점이다.
image file과 video file 중 하나 이상의 file을 첨부해야 한다는 것에 설계에 어려움을 겪었다.
```
</div>
</details>

---
# 4. DRF1: Serializer

<details>
<summary> </summary>
<div markdown="1">      

## DRF
Django REST Framework

## Serializer

Serializers allow complex data such as `querysets and model instances` to be converted to `native Python datatypes` that can then be easily rendered into `JSON`, `XML` or `other content types`.  
Serializers also provide `deserialization`, allowing parsed data to be converted back into complex types, after first validating the incoming data.

## Tutorial 1: Serialization
https://www.django-rest-framework.org/tutorial/1-serialization/#tutorial-1-serialization

### 1. model : DB 모델 인스턴스 만들기
- snippets/models.py

```
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']
```  

### 2. ModelSerializers : ModelSerializers 만들기 
- snippets/serializers.py

```
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

```  

### 3. Views : View 만들기 
- snippets/views.py

```
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```
```
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
```

### 4. Urlconf : Url 설정하기
- snippets/urls.py : snippets -> local url
```
urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]
```
- tutorial/urls.py : tutorial -> snippets
```
urlpatterns = [
    path('', include('snippets.urls')),
]
```

## HW 1 : INSERT Data

### Django Admin Page

1. 관리자 계정 설정
`python manage.py createsuperuser`

2. `admin.py` 수정
```
class PostAdmin(admin.ModelAdmin):
    list_display = ('profile', 'caption', 'count_like', 'count_comment')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'number_follower', 'number_following')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
```


2-1 `models.py` 수정
```
class Post(CommonInfo):                                             # 게시글
    ...

    class Meta:
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
class Profile(CommonInfo):                                          # 프로필                
    ...
    
    class Meta:
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
```
3. `127.0.0.1:8000/admin` admin login

![may2](https://user-images.githubusercontent.com/77188666/166111205-890a2f06-657a-41dc-94c5-231cf18bbc11.PNG)

### Profile Model
```
class Profile(CommonInfo):                                              # 프로필
    user = models.OneToOneField(User, on_delete=models.CASCADE)         # FK (user_id)
    name = models.CharField(max_length=30)                              # 이름
    photo = models.FileField(upload_to='file/profile/', null=True)      # 프로필 사진 저장 위치
    website = models.CharField(max_length=320)                          # Website
    bio = models.CharField(max_length=150)                              # Bio
    public_flag = models.BooleanField(default=False)                    # 공개 계정
    number_follower = models.IntegerField(default=0)                    # 팔로워 수
    number_following = models.IntegerField(default=0)                   # 팔로잉 수
    number_posts = models.IntegerField(default=0)                       # 게시글 수

    class Meta:
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
```

![may1](https://user-images.githubusercontent.com/77188666/166110989-e5eadf12-102a-46d7-96ce-0a68f5e8de93.PNG)


## HW 2 : /GET/ API 
```
def profile_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data)
    ...
```


## HW 3 : /POST/ API 
```
def profile_list(request):
    
    ...
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```

</div>
</details>

---

# 5. DRF2: API View

---

### 모든 list를 가져오는 API
#### [GET] api/profiles
- 모든 `Profile`의 list를 가져오는 API
- response
```
[
    {
        "user": 2,
        "name": "oats",
        "photo": "/media/file/profile/1.PNG",
        "website": "none",
        "bio": "none",
        "public_flag": false,
        "number_follower": 100,
        "number_following": 1,
        "number_posts": 0
    },
    {
        "user": 3,
        "name": "serial",
        "photo": "/media/file/profile/1_VyZJzaF.PNG",
        "website": "none",
        "bio": "none",
        "public_flag": false,
        "number_follower": 150,
        "number_following": 150,
        "number_posts": 0
    },
    {
        "user": 4,
        "name": "croffle",
        "photo": "/media/file/profile/1_dFcpKvA.PNG",
        "website": "none",
        "bio": "none",
        "public_flag": true,
        "number_follower": 200,
        "number_following": 1,
        "number_posts": 0
    }
]
```

---

### 특정 데이터를 가져오는 API
#### [GET] api/profiles/1
- `PK=1` 인 `Profile`을 가져오는 API
- response
```
{
    "user": 2,
    "name": "oats",
    "photo": "/media/file/profile/1.PNG",
    "website": "none",
    "bio": "none",
    "public_flag": false,
    "number_follower": 100,
    "number_following": 1,
    "number_posts": 0
}
```

---

### 새로운 데이터를 생성하는 API
#### [POST] api/profiles
- `Profile`을 추가하는 API
- request.body
```

```
- response
```

```
---

### 특정 데이터를 업데이트하는 API
#### [PUT] api/profiles/1
- `PK=1` 인 `Profile`을 수정하는 API
- request.body
```

```
- response
```

```
---

### 특정 데이터를 삭제하는 API
#### [DELETE] api/profiles/1
- `PK=1` 인 `Profile`을 삭제하는 API
- response
```
{
    "detail": "찾을 수 없습니다."
}
```

사진 첨부

---

### Django MVT
사진첨부 - MVT Pattern

Django의 MVT : client request 처리 과정

1. `client`로 `request`를 받으면 `URLconf`를 이용하여 `URL`을 분석한다
2. URL 분석 결과를 통해 해당 `URL에 대한 처리`를 담당할 `View`를 결정한다
3. `View`는 `view의 로직`을 실행한다
   ( DB 처리가 필요하면 `Model`을 통해 처리하고 그 결과를 반환받는다 )
4. `View`는 로직 처리가 끝나면 `Template`을 사용하여 `client`에 전송할 `HTML` 파일을 생성한다
5. `View`는 `client`에 `response`(HTML 파일) 한다

..

---

### 간단한 회고

Django의 CBV에 대해 알게 되었다. 스터디 내용 이외에도 공식문서의 튜토리얼을 통해서
mixins 을 알게 되었다. 또한 이것을 View에서 편하게 사용할 수 있는 generic class-based views도 있다는 것을 알게 되었다.
API 설계가 까다롭게 느껴지지 않았으나, 1) 모델과 모델 사이의 관계가 있다는 것을 놓쳐 중간에 살짝 꼬인 부분이 있었다. 2) Postman으로 DELETE API를 사용하는데, 데이터가 삭제되지만, 원하는 응답이 나오지 않는 부분이 있었다.


---