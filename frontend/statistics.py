import flet as ft
from backend.habit_manager import get_all_habits

class StatisticView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

        # save all visited Container
        self.stat_items_list = []

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
            padding = 0,
            bgcolor = "#F5F1EB",
            border = ft.border.only(right = ft.BorderSide(0.5, "black12")), # 右側線條邊框
            content = ft.Column(
                # scroll = ft.ScrollMode.AUTO,
                spacing = 0,
                controls = [
                    # SELECT HABIT
                    ft.Container(                        
                        content = ft.Text("SELECT HABIT", size = 13, weight = "bold", color = "#807E7C"),
                        padding = ft.padding.only(top = 20, bottom = 10, left = 10)
                    ),
                    ft.Container(
                        expand = True,
                        padding = ft.padding.only(left = 5, right = 5),
                        content = ft.Column(
                            controls = [
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
                            ],  
                            scroll = ft.ScrollMode.AUTO,
                            spacing = 5
                        )    
                    ),
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
                    width = 1400,
                    padding = ft.padding.only(left = 25, top = 20, bottom = 20),
                    # 使用 Container 的邊框來取代 Divider，這樣線條才會 100% 延伸
                    border = ft.border.only(bottom = ft.BorderSide(0.5, "black12")),
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
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()

        nav_item = ft.Container(
            on_click = self.stat_on_nav_change,
            on_hover = handle_hover,
            data = label,
            padding = ft.padding.symmetric(horizontal = 10, vertical = 12), # 增加上下間距
            border_radius = 8,
            
            ink = True,  # 啟用 Material 水波紋回饋
            ink_color = "black12", # 點擊時的水波紋顏色
            
            content = ft.Row(
                vertical_alignment = ft.CrossAxisAlignment.START,
                controls = [
                    ft.Icon(ft.Icons.EVENT, size = 20, color = "#807E7C"),
                    # 使用 Expanded 強制文字佔滿剩餘寬度並觸發換行
                    ft.Text(
                        value = label,
                        size = 16,
                        color = "black87",
                        overflow = ft.TextOverflow.VISIBLE, # 確保換行文字不會被截斷
                        no_wrap = False,
                        expand = True
                    )    
                ]
            )
        )
        # 將物件存入清單，供後續遍歷更新
        self.stat_items_list.append(nav_item)
        return nav_item
    

    def stat_on_nav_change(self, e):
        # 獲取點擊的資料
        clicked_label = e.control.data

        # 1. 遍歷清單，更新所有條目的背景色
        for item in self.stat_items_list:
            if item.data == clicked_label:
                item.bgcolor = "black12"
            else:
                item.bgcolor = None
            item.update()

        # 2. 更新右側詳細內容
        self.stat_detail.content = ft.Text(f"{clicked_label}", size = 20, weight = "bold")  # 根據點擊的 data 更新右側內容
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