import pandas as pd
import numpy as np
import os
import sys

# 상위 폴더(루트)의 config를 불러오기 위해 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class MarketAnalyzer:
    def __init__(self):
        self.data_path = os.path.join(config.PROCESSED_DATA_DIR, 'merged_market_data.csv')
        self.save_path = os.path.join(config.PROCESSED_DATA_DIR, 'event_impact_result.csv')
        self.events = config.MARKET_EVENTS
        self.df = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError("전처리된 데이터가 없습니다. processor.py를 실행하세요.")
        
        # [수정 포인트] index_col='Date' 대신 index_col=0 사용
        # CSV의 첫 번째 열을 무조건 날짜 인덱스로 인식
        df = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        
        # 인덱스 이름이 비어있을 경우를 대비해 'Date'로 강제 명명
        df.index.name = 'Date'
        return df

    def analyze_event_impact(self, window_days=14):
        """
        이벤트(구두개입, 기금위) 전후 window_days 기간 동안의 지표 변화 분석
        """
        results = []

        print(f"\n[Analysis] 이벤트 영향력 분석 (전후 {window_days}일 비교)")
        
        for event_type, dates in self.events.items():
            for date_str in dates:
                try:
                    event_date = pd.to_datetime(date_str)
                    
                    # 데이터 범위 내에 이벤트가 있는지 확인
                    if event_date < self.df.index.min() or event_date > self.df.index.max():
                        print(f" > [Skip] {date_str}: 분석 기간 범위 밖")
                        continue

                    # 데이터 슬라이싱 (Calendar Day 기준)
                    pre_start = event_date - pd.Timedelta(days=window_days)
                    post_end = event_date + pd.Timedelta(days=window_days)

                    pre_data = self.df.loc[pre_start:event_date]
                    post_data = self.df.loc[event_date:post_end]

                    # 데이터 개수 부족 시 스킵 (휴장일 등 고려하여 최소 5일치)
                    if len(pre_data) < 5 or len(post_data) < 5:
                        print(f" > [Skip] {date_str}: 데이터 부족 (전:{len(pre_data)}, 후:{len(post_data)})")
                        continue

                    # 1. 상관계수 변화 (Pearson Correlation)
                    pre_corr = pre_data['KRW'].corr(pre_data['JPY'])
                    post_corr = post_data['KRW'].corr(post_data['JPY'])

                    # 2. 변동성 변화 (Volatility = Std Dev of Returns)
                    # 연율화 (sqrt(252)) 적용
                    pre_vol = pre_data['KRW_Ret'].std() * np.sqrt(252)
                    post_vol = post_data['KRW_Ret'].std() * np.sqrt(252)

                    results.append({
                        'Event_Type': event_type,
                        'Date': date_str,
                        'Pre_Corr': round(pre_corr, 4),
                        'Post_Corr': round(post_corr, 4),
                        'Corr_Change': round(post_corr - pre_corr, 4),
                        'Pre_Vol': round(pre_vol, 4),
                        'Post_Vol': round(post_vol, 4),
                        'Vol_Change': round(post_vol - pre_vol, 4)
                    })
                except Exception as e:
                    print(f" > [Error] {date_str} 처리 중 오류: {e}")
                    continue

        return pd.DataFrame(results)

    def analyze_lag_correlation(self, max_lag=5):
        """
        교차 상관분석 (Cross-Correlation)
        """
        print(f"\n[Analysis] 엔-원 시차 상관분석 (Lag 0 ~ {max_lag})")
        
        # 데이터가 충분한지 확인
        if len(self.df) < max_lag + 2:
            print(" > [Skip] 데이터가 너무 적어 시차 분석 불가")
            return

        base_corr = self.df['JPY_Ret'].corr(self.df['KRW_Ret'])
        print(f" > Lag 0 (동행): {base_corr:.4f}")

        for lag in range(1, max_lag + 1):
            # JPY를 lag일 만큼 shift (JPY가 선행변수라 가정)
            shifted_jpy = self.df['JPY_Ret'].shift(lag)
            # shift로 인해 생긴 NaN 제거 후 상관계수 계산
            valid_idx = shifted_jpy.dropna().index.intersection(self.df.index)
            
            if len(valid_idx) > 0:
                corr = self.df.loc[valid_idx, 'KRW_Ret'].corr(shifted_jpy.loc[valid_idx])
                print(f" > Lag {lag} (엔화 {lag}일 선행): {corr:.4f}")

    def run(self):
        # 1. 이벤트 영향도 분석
        impact_df = self.analyze_event_impact()
        
        if not impact_df.empty:
            print("\n>>> 이벤트 전후 지표 변화 요약 <<<")
            print(impact_df.to_string(index=False))
            impact_df.to_csv(self.save_path, index=False)
            print(f"\n[Info] 분석 결과 저장 완료: {self.save_path}")
        else:
            print("\n[Warning] 유효한 이벤트 분석 결과가 없습니다.")

        # 2. 시차 분석
        self.analyze_lag_correlation()

if __name__ == "__main__":
    analyzer = MarketAnalyzer()
    analyzer.run()