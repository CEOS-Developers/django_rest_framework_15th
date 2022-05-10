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
<img width=75% src="https://user-images.githubusercontent.com/63996052/161687278-706d227f-684d-465e-98e4-71421a39d731.png">

**[Profile]**
- 장고에서 기본으로 제공하는 auth_user와 OneToOne Link with User Model (OneToOneField)
- 이름, 사용자 이름(아이디), 비밀번호 등의 정보는 User 테이블 참조
- 휴대전화 번호, 웹사이트, 소개 컬럼
- 사진, 영상 업로드 기능에만 집중하기 위해 유저의 다른 정보들은 생략

**[Post]**
- User와 1:N 관계, user_id (Foreignkey)
- 내용 컬럼, 생성 날짜, 삭제 여부

**[File]**
- Post와 1:N 관계, post_id (Foreignkey)
- 타입(이미지/비디오), 해당 파일의 url 주소 컬럼

**[Like]**
- User와 N:M, Post와 N:M 관계 (ManyToManyField)
- 생성 날짜, 삭제 여부

**[Comment]**
- User와 N:M, Post와 N:M 관계 (ManyToManyField)
- 내용 컬럼, 생성 날짜, 삭제 여부 

### ORM 적용해보기
임의의 User를 하나 생성하고, 해당 유저를 ForeignKey 필드로 포함하는 Post 모델을 선택하여 진행
  
1. 데이터베이스에 해당 모델 객체 3개 넣기

 **ORM 쿼리**
 ```
 one = Post.objects.create(content="첫번째 게시글", user_id=1)
 two = Post.objects.create(content="두번째 게시글", user_id=1)
 thr = Post.objects.create(content="세번째 게시글", user_id=1)
 ```
 **결과화면**
 ![image](https://user-images.githubusercontent.com/63996052/160549121-7526685d-f6ee-4687-b943-50aefb88db65.png)

  
2. 삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)

 **ORM 쿼리**
 ```
 Post.objects.all()
 ```
 **결과화면**
 ![image](https://user-images.githubusercontent.com/63996052/160549260-11b31257-cc3a-49a9-b90f-8fdb0e66d3bf.png)

  
3. filter 함수 사용해보기

 **ORM 쿼리**
 ```
 Post.objects.filter(id=2)
 Post.objects.filter(user_id=1)
 Post.objects.filter(content="첫번째 게시글")
 ```
**결과화면**
  ![image](https://user-images.githubusercontent.com/63996052/160549484-dbe25899-da79-474b-92ea-f07cfda51ae8.png)


### 회고
장고와 같이 모델링하는 환경을 처음 접해보기 때문에, 데이터베이스를 설계하는 과정에서 다양한 고민이 있었다.

이전에 해오던 대로 soft delete를 사용하는 것이 맞는지, CharField, TextField를 되도록이면 null=true 상태로 작성하지 않는 것이 맞는지 고민했다.

또 인스타그램의 사진, 영상 등록이라는 주요 기능만을 고려하기 위해 많은 컬럼을 쳐내는 과정이 있었다.

예를 들면 수정 시점은 기록할 필요가 없다고 느껴 updated_at과 같은 값을 사용하지 않았는데, 유의미한 데이터만 남았기를 바란다.

마지막으로 깃허브 액션 확인 결과 제대로 배포되지 않음을 확인하여 이를 해결해야할 것 같다.

-> 깃허브 액션 문제를 해결했다. 공부하는 과정에서 멋대로 pip freeze > requirements.txt를 실행했는데, 이 과정에서 기존에 사용했던 opencv를 포함한 다양한 라이브러리들이 포함되었다. 이로 인해 timeout이 나면서 자동 배포가 되지 않았음을 알게 되었다.

-> 피드백 반영
erd에 기본 유저 컬럼도 추가, post에 좋아요 카운트 추가, is_deleted 삭제, created updated 상속
null=True, blank=True는 장고 컨벤션에 따라 blank

<hr>

## Week 4: DRF1-Serializer
### 데이터 삽입
사용 모델: File

관련 모델: Post 
```
class Post(DatetimeModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_count = models.PositiveIntegerField(default=0)


class File(models.Model):
    post = models.ForeignKey(Post, related_name='files', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
```
![image](https://user-images.githubusercontent.com/63996052/161798869-103985c9-5be7-4067-8c41-9ba3c6f4838e.png)

### 모든 데이터를 가져오는 API 만들기
- URL : `api/files/`
- Method : `GET`
- 모든 'File'의 list를 가져오는 API 요청 결과 : 
```
[
    ...,
    {
        "id": 5,
        "post_content": "여섯번째 게시글",
        "type": "image",
        "url": "image1",
        "post": 7
    },
    {
        "id": 6,
        "post_content": "여섯번째 게시글",
        "type": "image",
        "url": "image2",
        "post": 7
    },
    {
        "id": 7,
        "post_content": "여섯번째 게시글",
        "type": "image",
        "url": "image3",
        "post": 7
    },
    ...
]
```

### 새로운 데이터를 create하도록 요청하는 API 만들기
- URL : `api/files/`
- Method : `POST`
- Body : `{"post": 3, "type": "video", "url": "new-video"}`
- Post를 추가하는 API 요청 결과 :  
```
{
    "id": 11,
    "post_content": "세번째 게시글",
    "type": "video",
    "url": "new-video",
    "post": 3
}
```

### 회고
![serializer](https://user-images.githubusercontent.com/63996052/161801617-70829f94-9aad-4075-8409-d117e6f8a423.PNG)
위와 같이 Nested Serializer를 연습하는 과정이 가장 어려웠다.

DatetimeModel을 상속하는 형태로 변경하면서 오류가 났는지 의심해 보았지만, 다른 사람들의 코드를 찾아보니 문제 없음을 알 수 있었다.

다음으로 api.models에 속하지 않아 django의 auth_user 테이블을 상속하면 접근이 되지 않는건가 싶어 User 대신 Profile과 ForeignKey 관계에 놓이도록 코드를 변경하였다.

마찬가지로 해결되지 않아 검색 결과 `related_name='files'`와 같이 Serializer에서 접근할 명칭을 지정해주면 된다는 것을 확인하여 수정하였고, 이후 잘 작동하였다.

<hr>

## Week 5: DRF2-API View
### 모든 list를 가져오는 API
- API 요청한 URL: http://127.0.0.1:8000/posts/ `GET`
- 결과 데이터: 
```
[
    {
        "id": 1,
        "content": "수정 post",
        "like_count": 0,
        "files": [
            {
                "id": 1,
                "post_content": "수정 post",
                "type": "image",
                "url": "hi"
            },
            {
                "id": 8,
                "post_content": "수정 post",
                "type": "image",
                "url": "fileurl"
            }
        ],
        "profile": {
            "id": 1,
            "mobile_number": "",
            "website": "",
            "bio": "",
            "user": 1
        }
    },
    {
        "id": 2,
        "content": "두번째 게시글",
        "like_count": 0,
        "files": [
            {
                "id": 9,
                "post_content": "두번째 게시글",
                "type": "image",
                "url": "url"
            },
            {
                "id": 10,
                "post_content": "두번째 게시글",
                "type": "image",
                "url": "imageurl"
            }
        ],
        "profile": {
            "id": 1,
            "mobile_number": "",
            "website": "",
            "bio": "",
            "user": 1
        }
    },
    {
        "id": 3,
        "content": "세번째 게시글",
        "like_count": 0,
        "files": [
            {
                "id": 11,
                "post_content": "세번째 게시글",
                "type": "video",
                "url": "new-video"
            }
        ],
        "profile": {
            "id": 1,
            "mobile_number": "",
            "website": "",
            "bio": "",
            "user": 1
        }
    },
    {
        "id": 6,
        "content": "여섯번째 게시글",
        "like_count": 0,
        "files": [
            {
                "id": 2,
                "post_content": "여섯번째 게시글",
                "type": "image",
                "url": "image1"
            },
            {
                "id": 3,
                "post_content": "여섯번째 게시글",
                "type": "image",
                "url": "image2"
            },
            {
                "id": 4,
                "post_content": "여섯번째 게시글",
                "type": "image",
                "url": "image3"
            }
        ],
        "profile": {
            "id": 1,
            "mobile_number": "",
            "website": "",
            "bio": "",
            "user": 1
        }
    },
    {
        "id": 7,
        "content": "여섯번째 게시글",
        "like_count": 0,
        "files": [
            {
                "id": 5,
                "post_content": "여섯번째 게시글",
                "type": "image",
                "url": "image1"
            },
            {
                "id": 6,
                "post_content": "여섯번째 게시글",
                "type": "image",
                "url": "image2"
            },
            {
                "id": 7,
                "post_content": "여섯번째 게시글",
                "type": "image",
                "url": "image3"
            }
        ],
        "profile": {
            "id": 1,
            "mobile_number": "",
            "website": "",
            "bio": "",
            "user": 1
        }
    }
]
```

### 특정 데이터를 가져오는 API
- API 요청한 URL: http://127.0.0.1:8000/posts/1 `GET`
- 결과 데이터: 
```
{
    "id": 1,
    "content": "수정 post",
    "like_count": 0,
    "files": [
        {
            "id": 1,
            "post_content": "수정 post",
            "type": "image",
            "url": "hi"
        },
        {
            "id": 8,
            "post_content": "수정 post",
            "type": "image",
            "url": "fileurl"
        }
    ],
    "profile": {
        "id": 1,
        "mobile_number": "",
        "website": "",
        "bio": "",
        "user": 1
    }
}
```

### 새로운 데이터를 생성하는 API
- 요청 URL: http://127.0.0.1:8000/posts/ `POST`
- body 데이터의 내용:
```
{
    "profile": "1",
    "id": 4,
    "content": "삽입 post",
    "like_content": 0
}
```
- create된 결과:
```
{
    "id": 8,
    "content": "삽입 post",
    "like_count": 0,
    "files": [],
    "profile": 1
}
```

### 특정 데이터를 업데이트하는 API
- 요청 URL: http://127.0.0.1:8000/posts/1 `PUT`
- body 데이터의 내용:
```
{
    "id": 4,
    "content": "수정 post"
}
```
- update된 결과:
```
{
    "id": 1,
    "content": "수정 post",
    "like_count": 0,
    "files": [
        {
            "id": 1,
            "post_content": "수정 post",
            "type": "image",
            "url": "hi"
        },
        {
            "id": 8,
            "post_content": "수정 post",
            "type": "image",
            "url": "fileurl"
        }
    ],
    "profile": {
        "id": 1,
        "mobile_number": "",
        "website": "",
        "bio": "",
        "user": 1
    }
}
```

### 특정 데이터를 삭제하는 API
- 요청 URL: http://127.0.0.1:8000/posts/3 `DELETE`
- delete된 결과:
```
{
    "status": 204,
    "message": "SUCCESS"
}
```

### 공부한 내용 정리
이번 주차 내용 중 POST api를 생성하는데에 있어서 가장 어려움을 겪었다.

저번 주 피드백을 통해 fields를 일일이 지정해주어야 한다는 점을 알게 되었고, Post에서도 마찬가지로 하고자 시도하였다.

다만 `profile = ProfileSerializer(read_only=True)` 구문을 PostSerializer 안에서 다시 작성하면서, 원래 존재하는 필드인 profile을 덮어 씌워 정상적인 접근이 불가능해지며 삽입이 되지 않은 것 같다.

특정 컬럼 값을 원하거나 여러개의 리스트를 가져올 때만, 그에 일치하는 변수명을 만들고 따로 선언하여 사용하면 될 것 같다.

### 간단한 회고
저번에 겪었던 related_name 문제로 인해 사용하고자 하는 class에서 related_name들을 미리 지정을 해주고 migrate한뒤 코드를 작성하였다. 그럼에도 불구하고 이번 주차 과제를 하다보니 여전히 related_name과 Serializer에 대한 완전한 이해가 되지 않은 것 같아 아쉬웠다. 공부가 더 필요할 것 같다.

<hr>

## Week 6: DRF3-ViewSet & Filter & Permission & Validation
### ViewSet Refactoring
- ViewSet으로 리팩토팅
- Router 사용해 url 매핑

![image](https://user-images.githubusercontent.com/63996052/167603147-7d87e4dd-6934-4ff2-bbdc-8a85cfdc8198.png)

### Filter
```url = filters.CharFilter(field_name='url', lookup_expr='icontains')```

http://127.0.0.1:8000/files?url=hi `GET`

![image](https://user-images.githubusercontent.com/63996052/167616156-0ec754b1-436d-4842-a116-b11be979928e.png)

#### method 사용
```
type = filters.CharFilter(method='filter_by_type')

def filter_by_type(self, queryset, name, value):
    filtered_queryset = queryset.filter(type=value)
    return filtered_queryset
 ```
 
http://127.0.0.1:8000/files?type=video `GET`

![image](https://user-images.githubusercontent.com/63996052/167617892-6b92d391-08a4-43e5-873e-843d12d7c18b.png)


http://127.0.0.1:8000/files?type=image `GET`

![image](https://user-images.githubusercontent.com/63996052/167618086-1ed5703a-d12c-4034-a20d-c6aeabc9554d.png) 

### Permission
```
class PostUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_authenticated
          
          
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [PostUpdatePermission,]
```
➡️ 게시글 조회는 누구나 가능하도록 하였지만, 새 게시글 등록은 인증된 사용자에 한해 가능하도록 함.


http://127.0.0.1:8000/posts/ `GET`

![image](https://user-images.githubusercontent.com/63996052/167647222-3f2aa731-0393-4971-ae7e-20ed875b4a45.png)

http://127.0.0.1:8000/posts/ `POST`

```
{
    "content": "권한 테스트",
    "like_count": 0,
    "files": [],
    "profile": 1
}
```

![image](https://user-images.githubusercontent.com/63996052/167647106-ba1f372f-b524-4105-89dc-9149d40dfa24.png)

### Validation
```
from django.core.validators import MinLengthValidator

class Post(DatetimeModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    content = models.TextField(blank=True, validators=[MinLengthValidator(2, '2글자 이상 입력하세요.')])
    like_count = models.PositiveIntegerField(default=0)
```
➡️ Built-in validator를 사용해서 포스트를 생성할 때 최소 2글자 이상이여야 유효하도록 검사하고, 조건을 만족할 경우에만 새 post를 등록할 수 있도록 제한한다.

http://127.0.0.1:8000/posts/ `POST`

```
{
    "content": "앗",
    "like_count": 0,
    "files": [],
    "profile": 1
}
```

![image](https://user-images.githubusercontent.com/63996052/167667684-63d78894-722b-4584-a25d-e8b2088702aa.png)

### 공부한 내용 정리
**유효성을 검사하는 다양한 방법**

- **Field-level Validation**: db로 따지면 테이블의 컬럼 단위의 value에 대하여 유효성 검사
- **Object-level Validation**: db로 따지면 테이블 단위의 object에 대하여 유효성 검사
- **Validator 함수를 통한 Validation**: 함수의 파라미터가 조건에 맞지 않을 때 에러 발생
- **클래스 내 clean 등 멤버 함수로 유효성 검사 및 값 변경**: 리턴 값을 통해 값을 반환
- 다양한 유효성 검사가 필요한 경우 validators.py에 따로 작성하여 사용하는 것이 좋을 듯 하다.

위처럼 다양한 방법들 중 해당 과제에서는 Validator 함수 중 Built-in Validator 함수인 `MinLengthValidator`를 사용했다.
이 함수를 models.py의 content에 적용하여, 게시글(post)의 내용(content)이 두 글자 이상일 때만 생성이 가능하도록 하였다.
뿐만 아니라, Permission을 통해 인증된 사용자만 접근할 수 있도록 구현되었다.

따라서, 로그인한 사용자가 2글자 이상의 글을 작성했을 때만 게시글이 등록되어 무작위로 의미 없는 게시글들이 등록되는 현상을 방지할 수 있다.

### 간단한 회고
이번 주차 과제를 통해 장고가 제공하는 여러 기능들이 서버 구현의 비용을 엄청나게 줄여준다는 점을 깨달았다. 이전까지는 조금 비효율적이라고 생각했던 부분들이 많이 해결 되었다는 느낌이 들었다.

다만 Permission을 사용함으로 인해서, 게시글에 대하여 조회 외의 다른 기능들이 제대로 작동하는지 포스트맨에서 직접 확인하기 어려웠다. 인증되지 않은 사용자에 대해 에러 메시지를 뱉기는 하지만, 반대로 인증이 되었을 때도 post, put, delete 같은 기능들이 잘 작동하는지 확인하고 싶다는 생각이 들었고, postman에 직접 auth를 주입하는 방법에 대한 공부가 필요하다고 느꼈다.
