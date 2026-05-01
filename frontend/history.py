import flet as ft
from backend.habit_manager import get_all_habits

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

        # save all visited Container
        self.hist_items_list = []

        # right side : detail of history
        self.hist_detail = ft.Container(
            padding = 15,
            expand = True,
            content = ft.Text("Select a habit to see details", size = 20, color = "grey"),
            alignment = ft.Alignment.TOP_LEFT
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
                                self.hist_nav_item("Sleep for 8 hours"),
                                self.hist_nav_item("Get up early"),
                                self.hist_nav_item("Clean the house"),
                                self.hist_nav_item("Drink 6 bottles of water"),
                                self.hist_nav_item("Water the flowers"),
                                self.hist_nav_item("Reading"),
                                self.hist_nav_item("Exercise"),
                                self.hist_nav_item("Learning Python for 10 hours every day to build a great project") # 測試長名稱
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
                    # 使用 Container 的邊框來取代 Divider，這樣線條才會 100% 延伸
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
            border_radius = 8,
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
            if item.data == clicked_label:
                item.bgcolor = "black12"
            else:
                item.bgcolor = None
            item.update()

        # 2. 更新右側詳細內容
        self.hist_detail.content = ft.Text(f"{clicked_label}", size = 20, weight = "bold")  # 根據點擊的 data 更新右側內容
        self.hist_detail.update()  # 重新渲染畫面

        # ==============================
        #         輸入圖表套件
        # ==============================

        
  