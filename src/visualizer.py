import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import platform
import sys
from matplotlib import font_manager, rc

# 상위 폴더(루트) config 임포트
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class PortfolioVisualizer:
    def __init__(self):
        self.data_path = os.path.join(config.PROCESSED_DATA_DIR, 'merged_market_data.csv')
        self.result_path = os.path.join(config.PROCESSED_DATA_DIR, 'event_impact_result.csv')
        self.save_dir = os.path.join(config.DATA_DIR, 'charts')
        os.makedirs(self.save_dir, exist_ok=True)
        
        self._set_style()

    def _set_style(self):
        sns.set_style("darkgrid")
        # 운영체제별 한글 폰트 자동 설정
        system_name = platform.system()
        try:
            if system_name == 'Windows':
                font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
                rc('font', family=font_name)
            elif system_name == 'Darwin': # Mac
                rc('font', family='AppleGothic')
            else:
                # 리눅스 등 폰트가 없을 경우 영문 기본 폰트 사용 (깨짐 방지)
                print("[Warning] 한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
                plt.rcParams['font.family'] = 'sans-serif'
        except:
            plt.rcParams['font.family'] = 'sans-serif'
        
        plt.rcParams['axes.unicode_minus'] = False 

    def load_data(self):
        # [수정 포인트] index_col=0 으로 변경
        if not os.path.exists(self.data_path):
             print("[Error] 시각화할 데이터가 없습니다.")
             return False
             
        self.df = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        
        if os.path.exists(self.result_path):
            self.res_df = pd.read_csv(self.result_path)
        else:
            self.res_df = None
            print("[Warning] 분석 결과 파일이 없어 일부 차트가 스킵됩니다.")
        return True

    def plot_market_trend_with_events(self):
        print(" > Drawing: Market Trend with Events...")
        plt.figure(figsize=(14, 7))
        
        ax1 = sns.lineplot(data=self.df, x=self.df.index, y='KRW', label='USD/KRW', color='navy', linewidth=1.5)
        ax1.set_ylabel('USD/KRW Rate')
        
        colors = {'RATE_CHECK': 'red', 'NPS_MEETING': 'green'}
        
        for event_type, dates in config.MARKET_EVENTS.items():
            color = colors.get(event_type, 'gray')
            for date_str in dates:
                try:
                    d = pd.to_datetime(date_str)
                    if d >= self.df.index.min() and d <= self.df.index.max():
                        plt.axvline(x=d, color=color, linestyle='--', alpha=0.7)
                        # 텍스트 위치 조정
                        y_pos = self.df['KRW'].max()
                        plt.text(d, y_pos, f' {event_type}', rotation=90, verticalalignment='top', fontsize=9, color=color, fontweight='bold')
                except:
                    continue

        plt.title('Impact of Policy Events on USD/KRW Exchange Rate', fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_dir, '1_trend_with_events.png'))
        plt.close()

    def plot_correlation_change(self):
        if self.res_df is None or self.res_df.empty: return
        
        print(" > Drawing: Correlation Change...")
        plt.figure(figsize=(10, 6))
        
        try:
            plot_df = self.res_df.melt(id_vars=['Date', 'Event_Type'], value_vars=['Pre_Corr', 'Post_Corr'], 
                                       var_name='Period', value_name='Correlation')
            
            sns.barplot(data=plot_df, x='Date', y='Correlation', hue='Period', palette='coolwarm')
            plt.title('Changes in KRW-JPY Correlation (Pre vs Post Event)', fontsize=14)
            plt.ylim(-1.0, 1.0)
            plt.axhline(0, color='black', linewidth=0.8)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(self.save_dir, '2_correlation_change.png'))
        except Exception as e:
            print(f" [Error] 상관관계 차트 그리기 실패: {e}")
        plt.close()

    def plot_bollinger_band(self, window=20):
        print(" > Drawing: Bollinger Bands...")
        
        temp_df = self.df.copy()
        temp_df['MA'] = temp_df['KRW'].rolling(window=window).mean()
        temp_df['STD'] = temp_df['KRW'].rolling(window=window).std()
        temp_df['Upper'] = temp_df['MA'] + (temp_df['STD'] * 2)
        temp_df['Lower'] = temp_df['MA'] - (temp_df['STD'] * 2)
        
        plt.figure(figsize=(14, 7))
        plt.plot(temp_df.index, temp_df['Upper'], 'r--', label='Upper Band', alpha=0.3)
        plt.plot(temp_df.index, temp_df['Lower'], 'r--', label='Lower Band', alpha=0.3)
        plt.plot(temp_df.index, temp_df['KRW'], label='USD/KRW', color='navy')
        plt.fill_between(temp_df.index, temp_df['Upper'], temp_df['Lower'], color='gray', alpha=0.1)
        
        plt.title(f'Bollinger Bands ({window} Days) - Volatility Check', fontsize=14)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_dir, '3_bollinger_bands.png'))
        plt.close()

    def run(self):
        if self.load_data():
            self.plot_market_trend_with_events()
            self.plot_correlation_change()
            self.plot_bollinger_band()
            print(f"[Info] 모든 차트가 저장되었습니다: {self.save_dir}")

if __name__ == "__main__":
    viz = PortfolioVisualizer()
    viz.run()