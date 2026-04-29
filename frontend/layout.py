import flet as ft
from frontend.statistics import StatisticView
from frontend.history import HistoryView


class AppLayout(ft.Row):
    def __init__(self, page: ft.Page):
        # 初始化父類別 (Row)，讓整個佈局橫向排列
        super().__init__(expand = True, spacing = 0)
        # self.main_page = page
        
        # --- [右側內容區] ---
        # 這是使用者點選選單後，右邊畫面會變動的地方
        self.content_area = ft.Container(
            alignment = ft.Alignment.TOP_LEFT,
            expand = True,
            padding = 0,
            bgcolor = "#F5F1EB",
            content = ft.Column(
                controls = [
                    ft.Text("Dashboard", size = 30, weight = "bold"),
                    ft.Text("date", size = 15)
                ]
            )
        )

        # --- [左側選單區] ---
        self.sidebar = ft.Container(
            width = 210,
            bgcolor = "#F5F1EB", # 參考手繪質感的米色
            border = ft.border.only(right = ft.BorderSide(1, "#807E7C")), # 右側線條邊框
            content = ft.Column(
                controls = [
                    # 1. 頂部標題 MENU
                    ft.Container(                        
                        content = ft.Text("MENU", size = 35, weight = "bold"),
                        padding = ft.padding.only(top = 30, bottom = 30, left = 20)
                    ),
                    
                    # 2. 中間功能列表 (加上 expand=True 會佔滿中間空間，把設定推到底部)
                    ft.Container(
                        width = 210,
                        expand = True,
                        content = ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            expand = True,
                            spacing = 5, # 讓按鈕之間有點間隔
                            controls = [
                                # 改用字串名稱，保證圖示能顯示
                                self.nav_item(ft.Icon(ft.Icons.DASHBOARD), "Dashboard", "dash"),
                                self.nav_item(ft.Icon(ft.Icons.INSERT_CHART), "Statistics", "stat"),
                                self.nav_item(ft.Icon(ft.Icons.HISTORY), "History", "hist"),
                                # self.nav_item(ft.Icon(ft.Icons.PETS), "Pet", "pet")
                            ]
                        ),
                        padding = ft.padding.all(10), # 讓按鈕不要貼邊
                    ),
                    
                    # 3. 底部設定按鈕
                    ft.Container(
                        width = 210,
                        content = self.nav_item(ft.Icon(ft.Icons.SETTINGS), "Settings", "set"),
                        padding = ft.padding.only(bottom = 20, top = 15, left = 10, right = 20),
                        # border = ft.border.only(top = ft.BorderSide(0.8, "#807E7C")), # 設定上方的橫線
                    ),
                ],
                spacing = 0,
            )
        )

        # 將「左側選單」與「右側內容」放入這個 Row 中
        self.controls = [self.sidebar, self.content_area]


    def nav_item(self, icon_name, label, data):

        return ft.ListTile(
            # 直接用字串 "black" 避開 ft.Colors.BLACK87 可能的報錯
            # leading = ft.Icon(icon_name, color="black", size = 24),
            width = 180,
            leading = icon_name,  
            title = ft.Text(
                label, 
                no_wrap = True
            ),
            on_click = self.on_nav_change,
            data = data,
            hover_color = "black12", # 滑鼠移上去有淡淡的灰色
            content_padding = ft.padding.symmetric(horizontal=20, vertical=5)  # 增加上下間距
        )
    
    # 當選單被點擊時觸發此函式
    def on_nav_change(self, e):
        clicked_data = e.control.data
        
        # 根據點擊的 data 更新右側內容
        if clicked_data == "dash":
            self.content_area.content = ft.Text("Dashboard", size = 30)

        elif clicked_data == "stat":
            # self.content_area.content = ft.Text("Statistics", size = 30)
            self.content_area.content = StatisticView()

        elif clicked_data == "hist":
            self.content_area.content = HistoryView()

        # elif clicked_data == "pet":
            # self.content_area.content = ft.Text("Pet", size = 30)

        elif clicked_data == "set":
            self.content_area.content = ft.Text("Settings", size = 30)
            
        # 必須調用 update() 才會重新渲染畫面
        self.content_area.update()