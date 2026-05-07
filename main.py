import sys
import flet as ft
from frontend.layout import AppLayout


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    # hide the titlebar
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    page.window.resizable = True
    # minimize size of the window
    page.window.min_width = 600
    page.window.min_height = 400
    # initial size of the window
    page.window.width = 1000
    page.window.height = 600
    # fonts
    page.fonts = {
        "CustomQuicksand": "/fonts/Quicksand-VariableFont_wght.ttf" # 路徑相對於 assets
    }
    page.theme = ft.Theme(font_family = "CustomQuicksand")
    # create layout instance
    app_layout = AppLayout(page)
    
    # close window
    def handle_close(e):
        try:
            page.window.close()
        except:
            pass
        sys.exit()
    # mazimize
    def handle_maximize(e):
        page.window.maximized = not page.window.maximized
        page.update()

    # create a custom header row
    title_bar = ft.WindowDragArea(
        content = ft.Container(
            bgcolor = "#F1E9DC",
            height = 30,
            padding = ft.padding.only(left = 5),
            border = ft.Border.only(bottom = ft.BorderSide(0.35, "#D3CFC8")),
            content = ft.Row([
                # ft.Text(" Habit Tracker", size = 15, color = "#423621", weight = "W500"),
                ft.Text(" Habit Tracker", size = 15, color = "#7D673F", weight = "W500"),
                ft.Row([
                    ft.IconButton(  # minimize button
                        icon = ft.Icons.REMOVE, 
                        icon_color = "#7D673F",
                        icon_size = 16,
                        on_click = lambda _: setattr(page.window, "minimized", True) or page.update()
                    ),
                    ft.IconButton(  # maximize button
                        icon = ft.Icons.CHECK_BOX_OUTLINE_BLANK, 
                        icon_color = "#7D673F",
                        icon_size = 12,
                        on_click = handle_maximize
                    ),
                    ft.IconButton(  # close window button
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

# launch the application
if __name__ == "__main__":
    ft.app(target = main, assets_dir="assets")
