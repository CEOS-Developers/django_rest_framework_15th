<html>
<head>
  <meta charset = "utf-8">
</head>
  <body>
    <h2><strong>2주차 과제 : Docker를 이용한 배포에 대해 공부하기</h2></strong>
    <ol>
      <li><h3><strong>what is docker?</strong></h3>
      <img src="https://d1.awsstatic.com/acs/characters/Logos/Docker-Logo_Horizontel_279x131.b8a5c41e56b77706656d61080f6a0217a3ba356d.png">
      <p>
      <h4><strong>컨테이너 기반의 오픈소스 가상화 플랫폼</strong></h4>
      이 때, <strong>(1)컨테이너</strong>란 <strong>격리된 공간에서 프로세스가 동작하는 기술. 가상화 기술의 하나</strong>
      기존 가상화는 호스트 OS 위의 게스트 OS 전체를 가상화하는 방식(VMware or VirtualBox), 사용법이 간단하지만 무겁고 느림
      그 후 CPU의 HVM을 이용해 KVM(Kernal Virtual Machine)과 반가상화 방식의 Xen 등장, 그러나 이것도 결국 추가적인 os설치를 이용한 가상화로써 성능 하락
      <br>
      이를 개선하기 위해 <strong>프로세스를 격리하는 방식</strong>이 등장, 이 방식을 리눅스에서 <strong>리눅스 컨테이너</strong> 라고 부름.
      단순히 프로세스를 격리함으로 가볍고 빠름. 성능적으로도 거의 손실 없음
      컨테이너 실행에 필요한 모든 파일과 설정값을 포함하는 파일이 <strong>이미지</strong>로 무상태성, 불변성을 가짐
      같은 이미지에서 여러개의 컨테이너 생성 가능, 컨테이너가 바뀌거나 삭제되어도 이미지는 변하지 않음.
      docker는 layer의 개념 사용. 유니온 파일 시스템을 이용하여 여러개의 레이어를 하나의 파일 시스템으로 사용할 수 있게 해줌.
      </p></li>
    
      <li><h3><strong>how to use Docker</strong></h3></li>
    
    </ol>
  </body>
  
</html>
