import flet as ft
import datetime
import calendar
from backend.habit_manager import get_all_habits, add_habit, delete_habit
from backend.stats_engine import get_week_range, get_current_streak, get_range_rate
from backend import log_manager

class DashboardView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)

        # 1. 初始資料與狀態
        self.habit_list = get_all_habits()

        # date information
        self.today = datetime.datetime.now()
        self.weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.state = {
            "year": self.today.year,
            "month": self.today.month,
            "day" :self.today.day
        }
        

        # 2. 定義 dashboard 的 content
        self.habit_items_column = ft.Column(
            expand = True,
            spacing = 10,
            scroll = ft.ScrollMode.AUTO,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )

        
        # 3. 建立彈出輸入框 (AlertDialog)
        self.new_habit_name_tf = ft.TextField(label = "Habit Name", autofocus = True)
        self.add_habit_dialog = ft.AlertDialog(
            title = ft.Text("Add New Habit"),
            content = ft.Container(
                expand = True,
                padding = ft.padding.only(left = 10, right = 10),
                width = 350,
                height = 200,
                content = ft.Column(
                    controls = [
                        ft.Text("Please enter your new habit name in the input box below."),
                        self.new_habit_name_tf
                    ]
                )
            ),       
            actions = [
                ft.TextButton("Cancel", on_click = self.close_dialog),
                ft.TextButton("Confirm", on_click = self.confirm_add_habit),
            ],
            open = True,
            bgcolor = "#F6EFE5",
            content_padding = ft.Padding.only(left = 20, right = 20, top = 20),
        )

        # 4. 初始化佈局
        self.build_dashboard()


    def build_dashboard(self):
        # Title
        year = self.today.year
        month = self.today.month
        day = self.today.day
        weekday_name = self.weekday[calendar.weekday(year, month, day)]
        month_name = calendar.month_name[month]

        def handle_hover(e):
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()

        title_row = ft.Container(
            padding = ft.padding.only(left = 25, top = 20, bottom = 20, right = 25),
            border=ft.border.only(bottom = ft.BorderSide(0.5, "black12")),
            bgcolor = "#F6EFE5",
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    ft.Column([
                        ft.Text("Dashboard", size = 30, weight = "bold"),
                        ft.Text(f"{weekday_name}, {month_name} {day}, {year}", size = 15, color = "black54", weight = "bold")
                    ], spacing=5),
                    # 改用 ElevatedButton 比較符合草圖按鈕樣式
                    ft.Container(
                        content = ft.Row([
                            ft.Icon(ft.Icons.ADD, size = 20),
                            ft.Text("New Habit", size = 18, weight = "w500")
                        ], spacing = 10),
                        padding = ft.padding.all(10),
                        border = ft.border.all(1, "black12"),
                        bgcolor = None,
                        border_radius = 8,
                        ink = True,
                        ink_color = "black12",
                        on_click = lambda e: self.page.show_dialog(self.add_habit_dialog),
                        on_hover = handle_hover,
                    )
                ]
            )
        )

        # --- 習慣列表內容區域 ---
        self.refresh_habit_list()

        self.dashboard_content = ft.Container(
            content = self.habit_items_column,
            padding = ft.padding.all(25),
            expand = True
        )

        # 組合
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls = [
                title_row,
                self.dashboard_content
                
            ]
        )

    # 建立習慣框框
    def create_habit_dashboard(self, habit_list):
        weekday = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

        for habit_data in habit_list:
            habit_id = habit_data.get("id")
            habit_name = habit_data.get("name")
            current_streak = get_current_streak(habit_id)

            habit_card = ft.Container(
                padding = 5,
                border = ft.border.all(1, "black26"),
                border_radius = 5,
                bgcolor = "#F7F4EF",
                content = ft.Column(
                    spacing = 3,
                    expand = True,
                    controls = [
                        ft.Row(
                            controls = [
                                ft.Text(habit_name, size = 20, weight = "bold"),
                                ft.Row([
                                    ft.Text(f"{current_streak}-day streak", color = "black54"),
                                    ft.IconButton(ft.Icons.DELETE, icon_color = "black54", 
                                                  on_click = lambda e: self.handle_delete(habit_data))
                                ])
                            ],
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.ProgressBar(
                                        value = self.get_progress(habit_id),    # 帶入你的進度數據 (0.0 ~ 1.0)
                                        color = "#7BA753",
                                        bgcolor = None,      #"black12",
                                        height = 8,
                                        border_radius = 4,
                                    ),
                                    expand=True, # 關鍵：讓進度條佔滿左邊剩餘的所有空間
                                ),
                                # 顯示百分比文字
                                ft.Text(f"{self.get_progress(habit_id) * 100} %", size = 16, weight = "bold", color = "black87"),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            vertical_alignment = ft.CrossAxisAlignment.CENTER,
                            spacing = 15, # 進度條與百分比之間的間距
                        ),
                        ft.Row(
                            controls=[self.build_card(d) for d in weekday],
                            spacing=10, 
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]
                )
            )
            self.habit_items_column.controls.append(habit_card)
        return 
    

    def build_card(self, day):
        return ft.Container(
            content = ft.Text(day, size = 16),
            width = 60, height = 45,
            border = ft.border.all(1, "black38"),
            border_radius = 5,
            alignment = ft.Alignment.CENTER,
        )
    

    # --- 建立「習慣框框」元件 (對應草圖中的 Habit 1, 2, 3) ---
    def create_habit_card(self, habit_data):
        name = habit_data.get("id", "name")
        streak = habit_data.get("streak", 0)
        progress = habit_data.get("progress", 0.0)

        # 星期幾的按鈕 (Mon, Tue...)
        days = ["Mon.", "Tue.", "Wed.", "Thr.", "Fri.", "Sat.", "Sun."]
        day_controls = []
        for d in days:
            day_controls.append(
                ft.Container(
                    content=ft.Text(d, size=16),
                    width=60, height=45,
                    border=ft.border.all(1, "black38"),
                    border_radius=5,
                    alignment = ft.Alignment.CENTER,
                )
            )

        return ft.Container(
            padding = 20,
            border = ft.border.all(1, "black26"),
            border_radius = 15,
            bgcolor = "white",
            content = ft.Column([
                # 第一排：名稱、Streak、百分比、垃圾桶
                ft.Row([
                    ft.Text(name, size = 22, weight = "bold"),
                    ft.Row([
                        ft.Icon(ft.Icons.CIRCLE, color = "red", size = 10),
                        ft.Text(f"{streak}-day streak", color = "black54")
                    ], spacing = 5),
                    ft.Text(f"{int(progress*100)}%", size = 16),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color = "black54", on_click = lambda _: self.handle_delete(habit_data))
                ], alignment = ft.MainAxisAlignment.SPACE_BETWEEN),
                
                # 第二排：星期按鈕列與打勾按鈕
                ft.Row([
                    ft.Row(day_controls, spacing=10, expand=True),
                    ft.Container(
                        content=ft.Icon(ft.Icons.CHECK, color="green", size=30),
                        width=50, height=50,
                        border=ft.border.all(2, "green"),
                        border_radius=10,
                        bgcolor="#E8F5E9"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )


    def close_dialog(self, e):
        self.add_habit_dialog.open = False
        self.new_habit_name_tf.value = ""
        self.page.update()

    def confirm_add_habit(self, e):
        new_name = self.new_habit_name_tf.value.strip()
        add_habit(new_name)
        print(self.habit_list)
        self.close_dialog(e)

    def handle_delete(self, habit_data):
        self.habit_list.remove(habit_data)
        delete_habit(habit_data['id'])
        self.refresh_habit_list()

    def get_progress(self, habit_id):
        week_range = get_week_range(str(self.today))
        return get_range_rate(habit_id, week_range["start"], week_range["end"])


    
    # --- 邏輯功能 ---
    def refresh_habit_list(self):
        self.habit_items_column.controls.clear()
        for h in self.habit_list:
            self.habit_items_column.controls.append(self.create_habit_card(h))
        self.update()
    

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
        self.update()
