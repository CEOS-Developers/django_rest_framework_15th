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



### ERD (using ERDCloud)
- ERD Diagram
![CEOS15](https://user-images.githubusercontent.com/77188666/160993717-d5db4812-5d7c-400d-9075-8b9d77481bb1.png)


#### DB Model ( `api/model.py` 의 주석 참고 )
 
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
  
### 1. CREATE
  
### 2. GET -all
  - before changing return type
  ![user_object_all_console3](https://user-images.githubusercontent.com/77188666/161371402-597619cb-6777-4ae7-a7aa-b5abacefea28.PNG)
  - after chainging
  ![user objects all()](https://user-images.githubusercontent.com/77188666/161371328-9ca50cbc-7901-4dac-b09f-f00e98a3a5b8.PNG)  
  
### 3. GET
![user objects get(id)](https://user-images.githubusercontent.com/77188666/161371294-3cee271c-5f65-4842-ae35-bf7a79064e1c.PNG)
- id - primary key index는 1부터 증가
  
  
### 4. FILTER
![queryset exercise](https://user-images.githubusercontent.com/77188666/161371388-47721a98-be40-41d4-9ace-f2cdfb4b50c1.PNG)

</div>
</details>
