# Steam 사용자 차단 도구

Steam 커뮤니티에서 여러 사용자를 자동으로 차단하는 Python 도구입니다.

## 기능

- 여러 Steam 사용자를 순차적으로 차단
- 설정 가능한 요청 간격 (기본: 1초)
- 차단 결과 로깅 및 저장
- 설정 파일을 통한 쉬운 관리
- **파일에서 Steam ID 자동 추출** (새로운 기능!)

## 설치

1. Python 3.6 이상이 필요합니다.
2. 필요한 패키지를 설치합니다:

```bash
pip install requirements
```

## 사용법

### 방법 1: 설정 파일에서 Steam ID 직접 입력

`config.json` 파일을 편집하여 다음 정보를 입력하세요:

### 방법 : 파일에서 Steam ID 자동 추출 (권장)

1. `block_code.txt` 파일에 Steam 프로필 URL을 한 줄씩 입력하세요: 
   중간에 빈 줄이 있어도 되고 없어도 됩니다.
```
https://steamcommunity.com/profiles/#################/


https://steamcommunity.com/profiles/#################/
```

2. `config.json` 파일에서 세션 정보만 설정:

이 값들은 **스팀 웹사이트에 로그인할 때 사용되는 브라우저의 쿠키(Cookie) 값**입니다. 쉽게 말해, 이 프로그램이 사용자 본인인 것처럼 스팀에 접속하기 위해 필요한 '인증 티켓'입니다.

이 값들은 **절대로 다른 사람에게 노출해서는 안 됩니다.** 비밀번호와 동일하게 취급해야 합니다.

---

## 🍪 쿠키 값 찾는 방법 (Chrome 기준)

다른 브라우저(Edge, Firefox 등)도 F12 개발자 도구를 이용하는 방식은 거의 동일합니다.

1.  **스팀 커뮤니티 사이트 접속 및 로그인**
    * [https://steamcommunity.com/](https://steamcommunity.com/)
    * 여기에 먼저 로그인합니다.

2.  **개발자 도구 열기**
    * 사이트에 접속된 상태에서 키보드에서 **F12** 키를 누릅니다. (또는 마우스 오른쪽 클릭 > '검사')

3.  **Application (애플리케이션) 탭 이동**
    * 개발자 도구 상단 탭에서 **Application**을 클릭합니다. (만약 보이지 않으면 `>>` 화살표를 눌러 찾아보세요.)
    * (Firefox의 경우 'Storage'(저장소) 탭일 수 있습니다.)

4.  **쿠키 값 확인**
    * 왼쪽 메뉴에서 **Storage** (저장소) > **Cookies** (쿠키)를 차례대로 펼칩니다.
    * `https://steamcommunity.com`을 클릭합니다.
    * 오른쪽에 쿠키 목록이 나타납니다.

5.  **값 찾기 및 복사**
    * **`sessionid` 찾기:** 'Name' 열에서 `sessionid`를 찾아 'Value' 열에 있는 값을 복사합니다. 이 값을 `config.json`의 `"session_id"`에 붙여넣습니다.
    * **`steamLoginSecure` 찾기:** 'Name' 열에서 `steamLoginSecure`를 찾아 'Value' 열에 있는 값을 복사합니다. 이 값을 `config.json`의 `"steam_login_secure"`에 붙여넣습니다.



이 두 값을 `config.json` 파일에 정확히 입력하면 프로그램이 사용자의 계정으로 로그인하여 작동할 수 있게 됩니다.


```json
{
    "session_id": "여기에_실제_세션_ID_입력",
    "steam_login_secure": "여기에_실제_steamLoginSecure_값_입력",
    "delay_seconds": 1
}
```

3. 실행:
```bash
python steam_block_users_from_file.py
```

### 세션 정보 얻기

1. 브라우저에서 Steam 커뮤니티에 로그인합니다.
2. 개발자 도구(F12)를 열고 Network 탭을 확인합니다.
3. 아무 페이지나 새로고침하고 요청을 찾습니다.
4. 요청 헤더에서 다음 정보를 복사합니다:
   - `sessionid` 쿠키 값
   - `steamLoginSecure` 쿠키 값

## 파일 설명

- `steam_block_users.py`: 기본 버전의 차단 스크립트
- `steam_block_users_advanced.py`: 설정 파일을 사용하는 고급 버전
- `steam_block_users_from_file.py`: **파일에서 Steam ID를 자동 추출하는 버전 (권장)**
- `config.json`: 설정 파일
- `block_code.txt`: Steam 프로필 URL 목록 파일
- `README.md`: 이 파일

## 주의사항

⚠️ **중요**: 이 도구는 개인적인 용도로만 사용하세요. Steam의 이용약관을 준수하고, 과도한 요청으로 서버에 부하를 주지 않도록 주의하세요.

- 요청 간격을 너무 짧게 설정하지 마세요 (최소 1초 권장)
- 대량의 사용자를 한 번에 차단하지 마세요
- Steam의 정책을 위반하는 용도로 사용하지 마세요

## 결과

차단 작업이 완료되면 다음과 같은 정보를 확인할 수 있습니다:

- 각 사용자별 차단 성공/실패 여부
- 실패한 경우 오류 메시지
- 전체 결과 요약
- 결과 파일 저장 (JSON 형식)

## 문제 해결

### 세션 만료
세션이 만료되면 다시 로그인하여 새로운 세션 정보를 얻으세요.

### 권한 오류
차단하려는 사용자가 이미 차단되었거나 권한이 없는 경우 오류가 발생할 수 있습니다.

### 네트워크 오류
네트워크 연결을 확인하고 다시 시도하세요.

### 파일 읽기 오류
`block_code.txt` 파일이 올바른 형식으로 작성되었는지 확인하세요. Steam 프로필 URL이 한 줄씩 있어야 합니다.

## 라이선스

이 도구는 교육 및 개인적인 용도로만 제공됩니다. 