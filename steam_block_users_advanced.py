import requests
import time
import json
import os
from typing import List, Dict, Any

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
                'success': response.status_code == 200,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'steam_id': steam_id,
                'status_code': None,
                'response_text': str(e),
                'success': False,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
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
        print("=" * 60)
        
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

def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """
    설정 파일 로드
    
    Args:
        config_file: 설정 파일 경로
        
    Returns:
        설정 데이터
    """
    if not os.path.exists(config_file):
        print(f"설정 파일 {config_file}을 찾을 수 없습니다.")
        return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"설정 파일 로드 중 오류 발생: {e}")
        return {}

def save_results(results: List[dict], filename: str = None):
    """
    결과를 파일로 저장
    
    Args:
        results: 차단 결과 리스트
        filename: 저장할 파일명 (기본값: 현재 시간)
    """
    if filename is None:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"block_results_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"결과가 {filename}에 저장되었습니다.")
    except Exception as e:
        print(f"결과 저장 중 오류 발생: {e}")

def main():
    # 설정 파일 로드
    config = load_config()
    
    if not config:
        print("설정 파일을 찾을 수 없거나 로드할 수 없습니다.")
        print("config.json 파일을 확인해주세요.")
        return
    
    # 설정값 추출
    session_id = config.get('session_id')
    steam_login_secure = config.get('steam_login_secure')
    steam_ids_to_block = config.get('steam_ids_to_block', [])
    delay_seconds = config.get('delay_seconds', 1)
    
    # 필수 설정 확인
    if not session_id or not steam_login_secure:
        print("session_id와 steam_login_secure가 설정되지 않았습니다.")
        return
    
    if not steam_ids_to_block:
        print("차단할 Steam ID가 설정되지 않았습니다.")
        return
    
    print("=== Steam 사용자 차단 도구 ===")
    print(f"세션 ID: {session_id[:10]}...")
    print(f"차단할 사용자 수: {len(steam_ids_to_block)}명")
    print(f"요청 간격: {delay_seconds}초")
    print()
    
    # 사용자 확인
    confirm = input("계속하시겠습니까? (y/N): ").strip().lower()
    if confirm != 'y':
        print("작업이 취소되었습니다.")
        return
    
    # 차단기 초기화
    blocker = SteamUserBlocker(session_id, steam_login_secure)
    
    # 사용자 차단 실행
    results = blocker.block_multiple_users(steam_ids_to_block, delay_seconds)
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("=== 차단 결과 요약 ===")
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
    
    # 결과 저장
    save_results(results)

if __name__ == "__main__":
    main() 