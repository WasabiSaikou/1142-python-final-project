import sys
import flet as ft
from frontend.layout import AppLayout


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    # 隱藏標題列
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    page.window.resizable = True
    # 設定視窗的最小寬度與高度
    page.window.min_width = 600
    page.window.min_height = 400
    # 設定視窗起始大小
    page.window.width = 1000
    page.window.height = 600
    
    # 建立佈局實例
    app_layout = AppLayout(page)
    
    # 關閉視窗
    def handle_close(e):
        try:
            page.window.close()
        except:
            pass
        sys.exit()
    # 最大化
    def handle_maximize(e):
        page.window.maximized = not page.window.maximized
        page.update()

    # 建立自定義標題列
    title_bar = ft.WindowDragArea(
        content = ft.Container(
            bgcolor = "#F9EBCA",
            padding = ft.padding.only(left = 5),
            content = ft.Row([
                ft.Text(" Habit Tracker", size = 15, color = "#7D673F", weight = "bold"),
                ft.Row([
                    ft.IconButton(  # 最小化按鈕
                        icon = ft.Icons.REMOVE, 
                        icon_color = "#7D673F",
                        icon_size = 16,
                        on_click = lambda _: setattr(page.window, "minimized", True) or page.update()
                    ),
                    ft.IconButton(  # 最大化按鈕
                        icon = ft.Icons.CHECK_BOX_OUTLINE_BLANK, 
                        icon_color = "#7D673F",
                        icon_size = 12,
                        on_click = handle_maximize
                    ),
                    ft.IconButton(  # 關閉視窗按鈕
                        icon = ft.Icons.CLOSE, 
                        icon_color = "#7D673F", 
                        icon_size = 16,
                        on_click = handle_close
                    ),
                ], spacing = 0)
            ],  alignment = ft.MainAxisAlignment.SPACE_BETWEEN)
        )
    )

    page.add(title_bar, app_layout)
    page.update()

# 啟動應用程式
if __name__ == "__main__":
    ft.app(target = main)
