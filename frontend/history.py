import flet as ft
from backend.habit_manager import get_all_habits

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

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
                    width = 1200,
                    padding = ft.padding.only(left = 25, top = 20, bottom = 20),
                    # 使用 Container 的邊框來取代 Divider，這樣線條才會 100% 延伸
                    border = ft.border.only(bottom = ft.BorderSide(1, "#807E7C")),
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
            e.control.bgcolor = "black12" if e.data == "true" else None
            e.control.update()

        return ft.Container(
            on_click = self.hist_on_nav_change,
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
                        overflow = ft.TextOverflow.VISIBLE, # 確保換行文字不會被截斷
                        expand = True
                    )    
                ]
            )
        )

    def hist_on_nav_change(self, e):
        # 當左側習慣被點擊時，更新右側顯示區
        clicked_data = e.control.data
        self.hist_detail.content = ft.Text(f"{clicked_data}", size = 20, weight = "bold")  # 根據點擊的 data 更新右側內容
        self.hist_detail.update()  # 重新渲染畫面

        # ==============================
        #         輸入圖表套件
        # ==============================

        
  