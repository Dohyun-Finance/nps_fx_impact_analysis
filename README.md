# 📉 Policy-Driven FX Analysis: 국민연금 및 외환 당국 개입 효과 분석

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) 
![Financial Analysis](https://img.shields.io/badge/Finance-Quant%20Analysis-green) 
![Status](https://img.shields.io/badge/Status-Completed-success)

> **"시장 데이터로 검증하는 정책의 유효성: 2022-2024 원·달러 환율 분석"**

## 1. 프로젝트 개요 (Overview)
본 프로젝트는 **국민연금(NPS)의 환헤지 정책 변화** 와 **외환 당국의 구두 개입(Rate Check)** 이 원·달러 환율(USDKRW)의 변동성 및 엔·달러(USDJPY)와의 상관관계에 미치는 영향을 정량적으로 분석했습니다.

단순한 가격 모니터링을 넘어, 주요 정책 이벤트 전후의 **통계적 유의성(Pearson Correlation, Volatility Change)** 을 검증하여, 향후 유사한 고환율 국면(1,350~1,400원) 발생 시 **리스크 관리 및 헷지(Hedge) 전략** 수립의 근거를 마련하는 것을 목표로 합니다.

## 2. 핵심 가설 (Hypothesis)
1.  **변동성 제어:** 외환 당국의 구두 개입(Rate Check)은 과열된 환율 상승 압력을 억제하고, 단기 변동성을 유의미하게 축소시킬 것이다.
2.  **디커플링(Decoupling):** 강력한 정책 공조(예: 한·미·일 재무장관 회의) 이후, 원화는 엔화의 약세 흐름과 동조화(Correlation)가 약해지며 독자적인 안정세를 찾을 것이다.

## 3. 기술 스택 (Tech Stack)
* **Language:** Python 3.10+
* **Data Collection:** `yfinance` (Yahoo Finance API v0.2.40+)
* **Data Processing:** `pandas`, `numpy` (Time-series Merging, Returns Calculation)
* **Statistical Analysis:** `scipy` (Pearson Correlation, Volatility Modeling)
* **Visualization:** `matplotlib`, `seaborn` (Event Highlighting, Bollinger Bands)

## 4. 프로젝트 구조 (Directory Structure)
유지보수와 확장성을 고려하여 소스 코드(`src`)와 설정(`root`)을 분리한 **모듈형 구조(Modular Architecture)** 로 설계되었습니다.

```bash
nps_fx_impact_analysis/
├── config.py             # [Configuration] 분석 기간 및 주요 이벤트 날짜 관리
├── main.py               # [Entry Point] 전체 파이프라인(수집-분석-시각화)통합 실행
├── requirements.txt      # [Dependency] 필수 라이브러리 목록
├── data/                 # [Data Storage] (Git 제외 설정됨)
│   ├── raw/              # 수집된 원본 CSV
│   ├── processed/        # 전처리 및 병합된 데이터
│   └── charts/           # 최종 분석 결과 이미지 (png)
└── src/                  # [Source Code]
    ├── collector.py      # 데이터 수집 모듈 (yfinance 연동)
    ├── processor.py      # 데이터 정제 및 파생변수 생성
    ├── analyzer.py       # 통계 분석 및 가설 검정 엔진
    └── visualizer.py     # 시각화 및 리포팅 모듈
```

## 5. 분석 대상 및 기간
* **Period:** 2022.10.01 ~ 2024.05.31 (주요 정책 전환기 및 고환율 구간 포함)
* **Assets:** USDKRW(원/달러), USDJPY(엔/달러)
* **Key Events (Source: News & Public Disclosure):**
    * **RATE_CHECK:** 한은 총재 구두 경고(23.10), 기재부-한은 공동 개입(24.04), 한미일 공동선언(24.04)
    * **NPS_MEETING:** 국민연금 환헤지 비율 상향(22.12), 한은-국민연금 외환스왑(23.04)

## 6. 실행 방법 (How to Run)
### 1) 환경 설정
``` bash
# 저장소 클론
git clone [https://github.com/YOUR_USERNAME/nps-fx-impact-analysis.git](https://github.com/YOUR_USERNAME/nps-fx-impact-analysis.git)

# 가상환경 생성 (권장) 및 필수 라이브러리 설치
pip install -r requirements.txt
```
### 2) 분석 파이프라인 실행
main.py를 실행하면 데이터 수집 → 전처리 → 분석 → 시각화 전 과정이 순차적으로 수행됩니다.
```bash
python main.py
```
실행 완료 후 data/charts/ 폴더에서 결과 이미지를 확인할 수 있습니다.

## 7. 분석 결과 및 인사이트 (Results)
### 📊 1. 정책 개입과 환율 추이 (Trend with Events)

* **분석:** 2024년 4월, 환율이 1,400원에 육박했을 때 단행된 **'기재부-한은 공동 구두 개입'** 직후 환율이 즉각적인 저항(Resistance)을 맞고 하락 전환(Peak-out)하는 패턴이 확인되었습니다.

* **인사이트:** 당국의 개입은 심리적 저지선 역할을 효과적으로 수행했습니다.

### 📉 2. 상관관계 변화 (Correlation Change)
* **분석:** 2024년 4월 17일 이벤트(한미일 공동선언) 전후를 비교했을 때, 엔화와의 상관계수가 **1.0(완전 동조)** 에 가까운 수준에서 **급격히 하락(Decoupling)** 했습니다.

* **인사이트:** 정책적 공조가 원화만의 독자적인 가치 방어에 기여했음을 통계적으로 입증했습니다.

### 〰️ 3. 변동성 분석 (Bollinger Bands)
* **분석:** 주요 이벤트 발생 구간에서 볼린저 밴드의 폭이 일시적으로 축소(Squeeze)되거나, 상단을 이탈한 후 회귀하는 모습이 관찰되었습니다.

## 8. 결론 (Conclusion)
과거 데이터(2022-2024) 백테스팅 결과, **환율 1,350원~1,400원 구간에서의 적극적인 정책 개입은 시장 안정화에 유의미한 효과(변동성 축소, 쏠림 완화)** 가 있음을 확인했습니다. 이는 향후 유사한 고환율 위기 발생 시, 당국 개입 시점을 포착하여 포트폴리오 헷지 비율을 조절하는 전략이 유효함을 시사합니다.
