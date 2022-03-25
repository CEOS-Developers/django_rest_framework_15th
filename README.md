<html>
<head>
  <meta charset = "utf-8">
</head>
  <body>
    <h2><strong>2주차 과제 : Docker를 이용한 배포에 대해 공부하기</h2></strong>
    <ol>
      <li><h2><strong>what is docker?</strong></h2></li>
      <img src="https://d1.awsstatic.com/acs/characters/Logos/Docker-Logo_Horizontel_279x131.b8a5c41e56b77706656d61080f6a0217a3ba356d.png">
      <p>
      <h4><strong>컨테이너 기반의 오픈소스 가상화 플랫폼</strong></h4>
      이 때, <strong>(1)컨테이너</strong>란 <strong>격리된 공간에서 프로세스가 동작하는 기술. 가상화 기술의 하나</strong>
      기존 가상화는 호스트 OS 위의 게스트 OS 전체를 가상화하는 방식(VMware or VirtualBox), 사용법이 간단하지만 무겁고 느림
      그 후 CPU의 HVM을 이용해 KVM(Kernal Virtual Machine)과 반가상화 방식의 Xen 등장, 그러나 이것도 결국 추가적인 os설치를 이용한 가상화로써 성능 하락
      <br><br>
      이를 개선하기 위해 <strong>프로세스를 격리하는 방식</strong>이 등장, 이 방식을 리눅스에서 <strong>리눅스 컨테이너</strong> 라고 부름.
      (현재의 docker는 lxc(linux container가 아닌  libcontainer라는 자체 컨테이너 사용함)
      단순히 프로세스를 격리함으로 가볍고 빠름. 성능적으로도 거의 손실 없음
      컨테이너 실행에 필요한 모든 파일과 설정값을 포함하는 파일이 <strong>이미지</strong>로 무상태성, 불변성을 가짐
      같은 이미지에서 여러개의 컨테이너 생성 가능, 컨테이너가 바뀌거나 삭제되어도 이미지는 변하지 않음.
      docker는 layer의 개념 사용. 유니온 파일 시스템을 이용하여 여러개의 레이어를 하나의 파일 시스템으로 사용할 수 있게 해줌.
      </p>
      <li><h2><strong>What is benefit and weakness of using docker</strong></h2></li>
    <p><h5><strong>benefit</strong></h5><ul>
        <li>구성 단순화 - 하나의 Configuration으로 모든 플랫폼에서 실행할 수 있음. 하나의 docker 이미지를 다른 곳에서도 사용 가능</li>
        <li>코드 관리 - 일관된 환경 제공(docker 이미지의 불변성!)</li?
        <li>개발 생산성 향상 - 개발 환경과 운영 환경의 차이점 최소화. Vm에 비해 사용 자원이 적어 여러가지 서비스 실행 가능</li>
        <li>애플리케이션 격리</li>
        <li>빠른 배포</li>
      </ul></p>
  </p><h5><strong>weaknesses of Docker</strong></h5>
  수많은 컨테이너와 컨테이너화 된 앱들의 관리 및 오케스트레이션(컴퓨터 시스템과 애플리케이션, 서비스의 자동화된 설정, 관리, 조정)이 어려워짐
  -> 컨테이너의 그룹화가 필요함 -> <strong><a href = "https://www.redhat.com/ko/topics/containers/what-is-kubernetes", title="kubernetes">쿠버네티스</a></strong>
  <h2><li><strong>about 2nd seminar - docker & docker-compose, github action</strong></li></h2>
      <strong>Docker</strong> -> Dockerfile을 실행시켜줌, Dockerfile은 하나의 이미지를 만들기 위한 과정(이미지에 대해서는 위에서 이미 설명한 대로 !)<br>
      <strong>docker-compose</strong> -> docker-compose.yml을 실행시켜줌 , 이미지를 여러개 띄워서 서로 네트워크도 만들어주고 컨테이너의 밖의 호스트와도 어떻게 연결할지, 파일 시스템은 어떻게 공유할지(volumes) 제어해주는것이 docker-compose<br>
  <h4>github action이 해주는 일 - <strong>Workflow의 자동화</strong></h4>
  Workflow의 종류    
    <ul>
        <li>Test code</li>
        <li>배포 - 서버에 새로운 버전, 기능 등 배포</li>
        <li>자동화 하고싶은 스크립트</li>
      </ul>
      <strong>github action 사용 예시</strong><br><a href="https://fe-developers.kakaoent.com/2022/220106-github-actions/",target="__blank", title="usage of github action">카카오웹툰의 깃허브 액션 사용예</a>
      <br>
    이번 세미나에서 진행한 배포의 흐름
    <img src="Users\jihoo\OneDrive\바탕 화면\ceos15">
    </ol>
  </body>
  
</html>
