import sys
import os

# 각 모듈 임포트
from src.collector import DataCollector
from src.processor import DataProcessor
from src.analyzer import MarketAnalyzer
from src.visualizer import PortfolioVisualizer

def main():
    print("==================================================")
    print("   [Project] 국민연금 환헤지 및 외환 개입 분석   ")
    print("==================================================\n")

    try:
        # Phase 2: 데이터 수집
        print(">>> [Phase 2] Data Collection")
        collector = DataCollector()
        collector.run()
        print("-" * 50)

        # Phase 3: 데이터 전처리
        print(">>> [Phase 3] Data Processing")
        processor = DataProcessor()
        df_processed = processor.load_and_merge()
        if df_processed is None:
            raise Exception("데이터 전처리 실패")
        print("-" * 50)

        # Phase 4: 데이터 분석
        print(">>> [Phase 4] Statistical Analysis")
        analyzer = MarketAnalyzer()
        analyzer.run()
        print("-" * 50)

        # Phase 6: 시각화
        print(">>> [Phase 6] Visualization")
        visualizer = PortfolioVisualizer()
        visualizer.run()
        print("-" * 50)

        print("\n[Success] 모든 프로세스가 성공적으로 완료되었습니다.")
        print(f"결과 확인 경로: {os.path.abspath('data/charts')}")

    except Exception as e:
        print(f"\n[Fail] 프로세스 실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()