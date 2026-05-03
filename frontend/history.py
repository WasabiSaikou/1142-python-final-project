import flet as ft
import calendar
import datetime as dt
from backend.habit_manager import get_all_habits
from frontend.calender import HistoryCalendar

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)
        
        # save all visited Container
        self.hist_items_list = []

        # right side : detail of history
        self.hist_detail = ft.Container(
            padding = 15,
            expand = True,
            # content = self.create_detail_content("Running"), # 預設顯示 Running
            content = ft.Text("Select a habit to see details", size = 20, color = "grey"),
            alignment = ft.Alignment.TOP_CENTER
        )

        # left side : sidebar of hostory
        self.hist_sidebar = ft.Container(
            width = 250,
            alignment = ft.Alignment.TOP_LEFT,
            padding = 0,
            bgcolor = "#F5F1EB", # 參考手繪質感的米色
            border = ft.border.only(right = ft.BorderSide(0.5, "black12")), # 右側線條邊框
            content = ft.Column(
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
                                self.hist_nav_item("Running"),
                                self.hist_nav_item("Play games"),
                                self.hist_nav_item("Reading")
                            ],
                            scroll = ft.ScrollMode.AUTO,
                            spacing = 5
                        )
                    ) 
                ]
            )
        )

        # all contents of History
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls=[
                # Title : History
                ft.Container(
                    width = 1400,
                    bgcolor = "#F6EFE5",
                    padding = ft.padding.only(left = 25, top = 20, bottom = 20),
                    border = ft.border.only(bottom = ft.BorderSide(0.5, "black12")),
                    content = ft.Column([
                        ft.Text("History", size = 30, weight = "bold"),
                        ft.Text("Review your daily progress.", size = 15),
                    ], spacing = 5)
                ),

                # Content (left -> sidebar ; right -> history of the chosen habit)
                ft.Row(
                    expand = True,
                    spacing = 0,
                    vertical_alignment = ft.CrossAxisAlignment.START,
                    controls = [
                        self.hist_sidebar,
                        self.hist_detail
                    ]
                )
            ]
        )

    def create_detail_content(self, habit_name):
        """封裝右側內容的生成邏輯"""
        return ft.Column(
            controls = [HistoryCalendar(habit_name = habit_name)], 
            scroll = ft.ScrollMode.AUTO, 
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )


    def hist_nav_item(self, label):
        """產生單個習慣條目，支援文字自動換行與懸停變色"""

        # 內建 hover 處理
        def handle_hover(e):
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()

        nav_item = ft.Container(
            on_click = self.hist_on_nav_change,
            on_hover = handle_hover,
            data = label,
            padding = ft.padding.symmetric(horizontal = 10, vertical = 12), # 增加上下間距
            border_radius = 5,
            ink = True,
            ink_color = "black12",

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
        self.hist_items_list.append(nav_item)
        return nav_item

    def hist_on_nav_change(self, e):
        # 獲取點擊的資料
        clicked_label = e.control.data

        # 1. 遍歷清單，更新所有條目的背景色
        for item in self.hist_items_list:
            item.bgcolor = "black12" if item.data == clicked_label else None
            item.update()

        """# 2. 重新建構右側內容
        # 重點：將 HistoryCalendar 包在一個 Column 裡並給它 expand=True
        self.hist_detail.content = ft.Column(
            controls=[
                ft.Text(f"{clicked_label} - 2026 May", size=28, weight="bold"),
                ft.Divider(height=20, color="transparent"),
                # 這裡直接呼叫你的日曆類別
                HistoryCalendar(habit_name=clicked_label) 
            ],
            expand=True, # 確保佔滿右側
            scroll=ft.ScrollMode.AUTO # 如果日曆太長可以滾動
        )"""

        # 2. **核心銜接點**：更換右側 Detail 內容
        # 我們直接重新建立整個 Column，並傳入新的 habit_name 給 HistoryCalendar
        self.hist_detail.content = self.create_detail_content(clicked_label)

        self.hist_detail.update()