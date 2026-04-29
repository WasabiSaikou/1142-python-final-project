import flet as ft

class StatisticView(ft.Container): # 繼承 Container 方便設定邊距和背景
    def __init__(self):
        super().__init__(expand = True, padding = 15)
        
        # 這裡放入你 Statistic 頁面的所有內容
        self.content = ft.Column(
            controls=[
                ft.Text("統計數據概覽", size=30, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                
                # 這裡可以先放一些簡單的卡片或是文字作為示意
                ft.Row([
                    self.stat_card("今日完成", "5", ft.Colors.BLUE),
                    self.stat_card("本週達成", "28", ft.Colors.GREEN),
                    self.stat_card("剩餘任務", "3", ft.Colors.ORANGE),
                ]),
                
                # 之後你可以在這裡加入圖表 (ft.LineChart 等)
                ft.Text("數據圖表區 (開發中...)", size=20, color="grey"),
            ]
        )

    def stat_card(self, title, value, color):
        """這是一個簡單的統計卡片輔助函式"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, color="black"),
                ft.Text(value, size=24, weight="bold", color=color),
            ]),
            width=150,
            height=100,
            bgcolor="#F9F9F9",
            border=ft.border.all(1, "black12"),
            border_radius=10,
            padding=15
        )