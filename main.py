import flet as ft
from frontend.layout import AppLayout


def main(page: ft.Page):
    # 設定視窗標題
    page.title = "Habit Tracker"
    page.theme_mode = 'light'
    
    # 移除頁面預設邊距，讓選單能貼緊邊緣
    page.padding = 0
    page.spacing = 0
    
    # 設定視窗起始大小
    page.window_width = 1000
    page.window_height = 700
    
    # 建立佈局實例
    app_layout = AppLayout(page)
    
    # 將佈局加到頁面中
    page.add(app_layout)

# 啟動應用程式
if __name__ == "__main__":
    ft.app(target = main)
