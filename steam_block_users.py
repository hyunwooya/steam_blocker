import requests
import time
import json
from typing import List

class SteamUserBlocker:
    def __init__(self, session_id: str, steam_login_secure: str):
        """
        Steam 사용자 차단 클래스 초기화
        
        Args:
            session_id: Steam 세션 ID
            steam_login_secure: Steam 로그인 보안 토큰
        """
        self.session_id = session_id
        self.steam_login_secure = steam_login_secure
        self.base_url = "https://steamcommunity.com"
        
        # 세션 설정
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://steamcommunity.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        })
        
        # 쿠키 설정
        self.cookies = {
            'timezoneOffset': '32400,0',
            'Steam_Language': 'koreana',
            'browserid': '181938084950144526',
            'sessionid': self.session_id,
            'steamCountry': 'KR%7Cdfc519408d201aa2c016d8767f6cc734',
            'steamLoginSecure': self.steam_login_secure
        }
        
    def block_user(self, steam_id: str) -> dict:
        """
        특정 Steam 사용자를 차단
        
        Args:
            steam_id: 차단할 사용자의 Steam ID
            
        Returns:
            API 응답 결과
        """
        url = f"{self.base_url}/actions/BlockUserAjax"
        
        data = {
            'sessionID': self.session_id,
            'steamid': steam_id,
            'block': '1'
        }
        
        headers = {
            'Referer': f'https://steamcommunity.com/profiles/{steam_id}/'
        }
        
        try:
            response = self.session.post(
                url,
                data=data,
                cookies=self.cookies,
                headers=headers,
                timeout=10
            )
            
            return {
                'steam_id': steam_id,
                'status_code': response.status_code,
                'response_text': response.text,
                'success': response.status_code == 200
            }
            
        except Exception as e:
            return {
                'steam_id': steam_id,
                'status_code': None,
                'response_text': str(e),
                'success': False
            }
    
    def block_multiple_users(self, steam_ids: List[str], delay_seconds: int = 1) -> List[dict]:
        """
        여러 Steam 사용자를 순차적으로 차단
        
        Args:
            steam_ids: 차단할 사용자들의 Steam ID 리스트
            delay_seconds: 각 요청 사이의 대기 시간 (초)
            
        Returns:
            각 사용자별 차단 결과 리스트
        """
        results = []
        
        print(f"총 {len(steam_ids)}명의 사용자를 차단합니다. 각 요청 사이에 {delay_seconds}초 대기합니다.")
        
        for i, steam_id in enumerate(steam_ids, 1):
            print(f"[{i}/{len(steam_ids)}] Steam ID {steam_id} 차단 중...")
            
            result = self.block_user(steam_id)
            results.append(result)
            
            # 결과 출력
            if result['success']:
                print(f"  ✓ 성공: {steam_id}")
            else:
                print(f"  ✗ 실패: {steam_id} - {result['response_text']}")
            
            # 마지막 요청이 아니면 대기
            if i < len(steam_ids):
                print(f"  {delay_seconds}초 대기 중...")
                time.sleep(delay_seconds)
        
        return results

def main():
    # 설정값 (실제 값으로 변경하세요)
    SESSION_ID = "f9f9836f9b2998f5a368f613"  # 실제 세션 ID로 변경
    STEAM_LOGIN_SECURE = "76561198151886439%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAxNF8yNjgwQTA4Rl8wRkRBQSIsICJzdWIiOiAiNzY1NjExOTgxNTE4ODY0MzkiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3NTA2OTA5NzMsICJuYmYiOiAxNzQxOTYzMjU5LCAiaWF0IjogMTc1MDYwMzI1OSwgImp0aSI6ICIwMDBDXzI2N0I4RjhEX0U2QzdBIiwgIm9hdCI6IDE3NTA2MDMyNTksICJydF9leHAiOiAxNzY4ODkzODI3LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNjEuODUuMTAwLjE5NiIsICJpcF9jb25maXJtZXIiOiAiNjEuODUuMTAwLjE5NiIgfQ.ghOzrH_LWL1gqmbmAded_COwUNoB435m0qiIZAY58O9KgPieKX9Qvl0_Hnk5kivQY0hmbh4AoWB8QEEmkTmXDw"
    
    # 차단할 Steam ID 리스트 (실제 Steam ID로 변경하세요)
    STEAM_IDS_TO_BLOCK = [
        "76561198211548375",
        # 여기에 더 많은 Steam ID를 추가하세요
    ]
    
    # 차단기 초기화
    blocker = SteamUserBlocker(SESSION_ID, STEAM_LOGIN_SECURE)
    
    # 사용자 차단 실행
    results = blocker.block_multiple_users(STEAM_IDS_TO_BLOCK, delay_seconds=1)
    
    # 결과 요약
    print("\n=== 차단 결과 요약 ===")
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"성공: {successful}명")
    print(f"실패: {failed}명")
    
    # 실패한 경우 상세 정보 출력
    if failed > 0:
        print("\n=== 실패한 사용자들 ===")
        for result in results:
            if not result['success']:
                print(f"Steam ID: {result['steam_id']}")
                print(f"오류: {result['response_text']}")
                print()

if __name__ == "__main__":
    main() 