import pandas as pd
import os
import sys
# 상위 폴더(루트)의 config를 불러오기 위해 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class DataProcessor:
    def __init__(self):
        self.raw_path = config.RAW_DATA_DIR
        self.save_path = config.PROCESSED_DATA_DIR

    def load_and_merge(self):
        """
        개별 CSV를 로드하여 날짜 기준 병합 및 결측치 처리
        """
        print("[Info] 데이터 전처리 시작...")
        
        try:
            # 1. 데이터 로드 (CSV 읽기)
            # index_col=0: 첫 번째 열을 날짜로 간주
            df_krw = pd.read_csv(os.path.join(self.raw_path, 'USDKRW.csv'), index_col=0)
            df_jpy = pd.read_csv(os.path.join(self.raw_path, 'USDJPY.csv'), index_col=0)

            # 2. [핵심 수정] 강제 형변환 (Data Cleaning)
            # 날짜 인덱스를 표준 datetime 형식으로 강제 변환 (에러 발생 시 무시하고 NaT 처리)
            df_krw.index = pd.to_datetime(df_krw.index, errors='coerce')
            df_jpy.index = pd.to_datetime(df_jpy.index, errors='coerce')
            
            # 날짜가 아닌 행(헤더가 잘못 들어간 경우 등) 제거
            df_krw = df_krw.dropna(axis=0, how='any') # 인덱스가 NaT인 행 제거
            df_jpy = df_jpy.dropna(axis=0, how='any')

            # 데이터를 강제로 숫자로 변환 (문자가 섞여 있으면 NaN으로 처리)
            # yfinance 저장 방식에 따라 컬럼명이 'Close', 'Adj Close', 'USDKRW' 등으로 다를 수 있음
            # 첫 번째 컬럼을 무조건 가져와서 숫자로 바꿈
            col_krw = df_krw.columns[0]
            col_jpy = df_jpy.columns[0]

            df_krw[col_krw] = pd.to_numeric(df_krw[col_krw], errors='coerce')
            df_jpy[col_jpy] = pd.to_numeric(df_jpy[col_jpy], errors='coerce')

        except FileNotFoundError:
            print("[Error] 데이터 파일이 없습니다. collector.py를 먼저 실행하세요.")
            return None
        except Exception as e:
            print(f"[Error] 데이터 로드 중 치명적 오류: {e}")
            return None

        # 3. 컬럼명 변경 및 병합
        df_krw.rename(columns={col_krw: 'KRW'}, inplace=True)
        df_jpy.rename(columns={col_jpy: 'JPY'}, inplace=True)

        # Outer Join (날짜 기준 병합)
        df_merged = df_krw.join(df_jpy, how='outer').sort_index()

        # 4. 결측치 처리 (중요: 앞의 값으로 채우기 전에, 아예 빈 값은 제거)
        df_merged.ffill(inplace=True)
        df_merged.dropna(inplace=True)

        if df_merged.empty:
            print("[Error] 병합 후 유효한 데이터가 없습니다. CSV 파일을 확인해주세요.")
            return None

        # 5. 파생 변수 생성 (여기서 에러가 났었음 -> 이제 숫자로 변환했으니 안전함)
        try:
            df_merged['KRW_Ret'] = df_merged['KRW'].pct_change()
            df_merged['JPY_Ret'] = df_merged['JPY'].pct_change()

            df_merged['KRW_MA20'] = df_merged['KRW'].rolling(window=20).mean()
            df_merged['KRW_MA60'] = df_merged['KRW'].rolling(window=60).mean()
        except Exception as e:
            print(f"[Error] 지표 계산 중 오류: {e}")
            print("데이터 샘플:\n", df_merged.head())
            return None

        # 6. 저장
        save_file = os.path.join(self.save_path, 'merged_market_data.csv')
        df_merged.to_csv(save_file)
        print(f"[Info] 전처리 완료 및 저장: {save_file}")
        print(f" > 데이터 기간: {df_merged.index.min().date()} ~ {df_merged.index.max().date()}")
        print(f" > 총 데이터 수: {len(df_merged)} rows")
        
        return df_merged

if __name__ == "__main__":
    processor = DataProcessor()
    processor.load_and_merge()