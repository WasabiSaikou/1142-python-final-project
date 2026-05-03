import flet as ft
import datetime as dt
import calendar
from backend.habit_manager import get_all_habits, add_habit, delete_habit

class DashboardView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

        # dashboard 的標題那一列
        """ Dashboard -> 如果不會可以去參考我的 statistics 和 history, 但是這邊還是有點不一樣
            日期你可以去研究一下怎麼引用進來
            右邊的 button 記得用 Icon 引入 flet 內建圖像，再加上 label"""
        self.dashboard_title = ft.Container(
            # you need to use ft.Row to put "title, date" and "button of add habit" to a row
            # write your code here

            content = ft.Row(
                controls = [
                    ft.Column(
                        controls = [
                            ft.Text("Dashboard", size = 30, weight = "bold"),
                            # Date
                            ft.Text(str(dt.date.today()), size = 15)
                        ]
                    ),
                    # button : add habit (靠右)

                ]
            )
        )


        # content of dashboard, including every habits and their information
        """ 你可以先自己定義幾個 habits, 做出這些 habits 的框框與一些簡單的布局
            可以多設幾個 habits 測試 scroll
            設定的 habits 可以用函式的方式去定義他們
            不會的話可以參考一下我 statistics 的 stat_nav_item 和 stat_on_nav_change"""
        self.dashboard_content = ft.Container(
            # you need to use ft.Column, and remember to use scroll (頁面滾輪)
            # write your code here
            



            
        ) 


        # all contents of Dashboard
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls=[
                # Title
                self.dashboard_title,
                # Content 
                self.dashboard_content 
            ]
        )

### =============================================================================
###  主要你可以先把 title、date、button 跟下面的 habit 框框弄出來
###  確認可以顯示、按鈕可以點、排版正常就好
###  到時候再去研究如何 add habit 跳出一個輸入框，以及新增這筆 habit 到 dashboard 上
### =============================================================================

""" 定義你需要用到的函式 """

