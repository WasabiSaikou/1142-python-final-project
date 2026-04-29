import flet as ft
from backend.habit_manager import get_all_habits

class StatisticView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

        # right side : detail of statistics
        self.stat_detail = ft.Container(
            padding = 15,
            expand = True,
            content = ft.Text("Select a habit to see details", size = 20, color = "grey"),
            alignment = ft.Alignment.TOP_LEFT
        )

        # left side : sidebar of statistics
        self.stat_sidebar = ft.Container(
            width = 250,
            alignment = ft.Alignment.TOP_LEFT,
            # expand = True,
            padding = 0,
            bgcolor = "#F5F1EB", # 參考手繪質感的米色
            border = ft.border.only(right = ft.BorderSide(1, "#807E7C")), # 右側線條邊框
            content = ft.Column(
                scroll = ft.ScrollMode.AUTO,
                expand = True,
                controls = [
                    # SELECT HABIT
                    ft.Container(                        
                        content = ft.Text("SELECT HABIT", size = 13, weight = "bold", color = "#807E7C"),
                        padding = ft.padding.only(top = 20, bottom = 10, left = 10)
                    ),
                    
                    # habits list (need to import the data)
                    self.stat_nav_item("Running"),
                    self.stat_nav_item("Play games"),
                    self.stat_nav_item("Sleep for 8 hours"),
                    self.stat_nav_item("Get up early"),
                    self.stat_nav_item("Clean the house"),
                    self.stat_nav_item("Drink 6 bottles of water"),
                    self.stat_nav_item("Water the flowers"),
                    self.stat_nav_item("Reading"),
                    self.stat_nav_item("Exercise"),
                    self.stat_nav_item("Learning Python for 10 hours every day to build a great project") # 測試長名稱
                ]
            )
        )

        # all contents of Statistics
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls=[
                # Title : Statistics
                ft.Container(
                    width = 1200,
                    padding = ft.padding.only(left = 25, top = 20, bottom = 20),
                    # 使用 Container 的邊框來取代 Divider，這樣線條才會 100% 延伸
                    border = ft.border.only(bottom = ft.BorderSide(1, "#807E7C")),
                    content = ft.Column([
                        ft.Text("Statistics", size = 30, weight = "bold"),
                        ft.Text("Track your progress and stay motivated!", size = 15),
                    ], spacing = 5)
                ),

                # Content (left -> sidebar ; right -> analysis of the chosen habit)
                ft.Row(
                    expand = True,
                    spacing = 0,
                    vertical_alignment = ft.CrossAxisAlignment.START,
                    controls = [
                        self.stat_sidebar,
                        self.stat_detail
                    ]
                )
            ]
        )


    def stat_nav_item(self, label):
        """產生單個習慣條目，支援文字自動換行與懸停變色"""

        # 內建 hover 處理
        def handle_hover(e):
            e.control.bgcolor = "black12" if e.data == "true" else None
            e.control.update()

        return ft.Container(
            on_click = self.stat_on_nav_change,
            on_hover = handle_hover,
            data = label,
            padding = ft.padding.symmetric(horizontal = 10, vertical = 12), # 增加上下間距
            border_radius = 8,
            content = ft.Row(
                vertical_alignment = ft.CrossAxisAlignment.START,
                controls = [
                    ft.Icon(ft.Icons.EVENT, size = 20, color = "#807E7C"),
                    # 使用 Expanded 強制文字佔滿剩餘寬度並觸發換行
                    ft.Text(
                        value = label,
                        size = 16,
                        color = "black87",
                        no_wrap = False,
                        # wrap = ft.TextWrap.WRAP,
                        # soft_wrap = True,      # 允許自動換行
                        overflow = ft.TextOverflow.VISIBLE, # 確保換行文字不會被截斷
                        expand = True
                    )    
                    
                ]
            )
        )

    def stat_on_nav_change(self, e):
        # 當左側習慣被點擊時，更新右側顯示區
        clicked_data = e.control.data
        self.stat_detail.content = ft.Text(f"{clicked_data}", size = 20, weight = "bold")  # 根據點擊的 data 更新右側內容
        self.stat_detail.update()  # 重新渲染畫面

        # ==============================
        #         輸入圖表套件
        # ==============================

        
        

    '''def stat_card(self, title, value, color):
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
        )'''