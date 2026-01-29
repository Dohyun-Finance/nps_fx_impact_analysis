import yfinance as yf
import pandas as pd
import os
import config

class DataCollector:
    def __init__(self):
        self.tickers = config.TICKERS
        self.start_date = config.START_DATE
        self.end_date = config.END_DATE
        self.save_path = config.RAW_DATA_DIR

    def fetch_market_data(self):
        """
        yfinance를 통해 일간 환율 데이터 수집
        """
        print(f"[Info] 데이터 수집 시작 ({self.start_date} ~ {self.end_date})")
        
        for name, ticker_symbol in self.tickers.items():
            try:
                # 1. 데이터 다운로드
                print(f" > Fetching {name} ({ticker_symbol})...")
                df = yf.download(ticker_symbol, start=self.start_date, end=self.end_date, progress=False)
                
                if df.empty:
                    print(f"[Warning] {name} 데이터가 비어있음.")
                    continue

                # 2. 필요한 컬럼만 선택 (Adj Close 기준)
                # yfinance 버전에 따라 컬럼 구조가 다를 수 있어 'Close' 우선 사용
                target_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
                df_clean = df[[target_col]].rename(columns={target_col: 'Close'})
                
                # 3. 저장
                file_name = f"{name}.csv"
                full_path = os.path.join(self.save_path, file_name)
                df_clean.to_csv(full_path)
                print(f" > Saved to {full_path}")

            except Exception as e:
                print(f"[Error] {name} 수집 중 오류 발생: {e}")

    def run(self):
        self.fetch_market_data()
        print("[Info] 데이터 수집 완료.")

if __name__ == "__main__":
    collector = DataCollector()
    collector.run()