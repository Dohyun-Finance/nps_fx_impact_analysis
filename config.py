import os
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()

# 2. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# 3. 디렉토리 생성
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# 4. 분석 대상 설정
TICKERS = {
    'USDKRW': 'KRW=X', 
    'USDJPY': 'JPY=X'
}

# 5. 기간 설정 (정책 변화를 모두 포함하도록 2022년 말부터 설정)
START_DATE = "2022-10-01" 
END_DATE = "2024-05-31"

# 6. 주요 이벤트 날짜 (뉴스 기반 업데이트 완료)
MARKET_EVENTS = {
    # 외환 당국 개입 (구두개입, 레이트 체크, 한미일 공동선언)
    'RATE_CHECK': [
        '2023-10-04', # 한은 총재 경고
        '2024-04-16', # 기재부-한은 공동 구두개입 (강력)
        '2024-04-17'  # 한미일 재무장관 공동선언 (국제적 공조)
    ],
    
    # 국민연금(NPS) 환헤지 및 스왑 정책
    'NPS_MEETING': [
        '2022-12-16', # 환헤지 비율 상향 결정 (핵심 정책 변화)
        '2023-04-13', # 한은-국민연금 외환스왑 체결
        '2023-06-21'  # 환헤지 비율 추가 조정
    ]
}