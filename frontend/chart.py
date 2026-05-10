import flet as ft
import datetime
import re
from backend.stats_engine import get_current_streak, get_longest_streak, get_range_rate, get_range_status, get_week_range, get_month_range

class StatisticalChart(ft.Container):
    def __init__(self, habit_id, habit_name):
        super().__init__(padding = 10, alignment = ft.Alignment.TOP_CENTER)
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.cur_streak = get_current_streak(self.habit_id)
        self.longest_streak = get_longest_streak(self.habit_id)
        self.today = datetime.datetime.now()

        # 建立一個「內容掛載點」，之後所有的內容都塞進這裡
        self.main_layout = ft.Column(scroll = ft.ScrollMode.ADAPTIVE,spacing = 20)
        self.content = self.main_layout
        self.stats_row_area = ft.Row(spacing = 10, alignment = ft.MainAxisAlignment.CENTER)

        # 建立自定義日期輸入 Row (預設不顯示)
        self.build_custom_date_row()
        self.build_ui_structure()
        # initialize
        self.initial_load()



    def initial_load(self):
        date_range = get_week_range(self.today.strftime("%Y-%m-%d"))
        rate = get_range_rate(self.habit_id, date_range["start"], date_range["end"])
        statuses = get_range_status(self.habit_id, date_range["start"], date_range["end"])
        
        completed = sum(1 for s in statuses if s is True)
        total = sum(1 for s in statuses if s is not None)

        self.stats_row_area.controls = self.create_stat_card_controls(rate, completed, total)


    def validate_dates(self):
        """驗證日期格式與合法性"""
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        MIN_DATE = datetime.datetime(2020, 1, 1)  # 假設 App 從 2020 開始
        MAX_DATE = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        
        def get_date_obj(date_str):
            if not re.match(date_pattern, date_str):
                return None
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return None

        from_date_obj = get_date_obj(self.from_input.value)
        to_date_obj = get_date_obj(self.to_input.value)

        is_valid = False

        if from_date_obj and to_date_obj:
            if from_date_obj <= to_date_obj:
                if (from_date_obj <= MAX_DATE) and (from_date_obj >= MIN_DATE):
                    if (to_date_obj <= MAX_DATE) and (to_date_obj >= MIN_DATE):
                        is_valid = True
        
        self.apply_btn.disabled = not is_valid
        
        if self.page:
            self.update()


    def build_custom_date_row(self):
        # start date input
        self.from_input = ft.TextField(
                label = "Started date", 
                value = (self.today - datetime.timedelta(days = 7)).strftime("%Y-%m-%d"),
                dense = True, hint_text = "YYYY-MM-DD", expand = True,
                on_change = lambda _: self.validate_dates()
            )
        self.from_input_column = ft.Column(
            controls = [
                ft.Text("From", size = 12, weight = "bold"),
                self.from_input
            ],
            spacing = 2, expand = True
        )
        
        # end date input
        self.to_input = ft.TextField(
            label = "End date", 
            value = self.today.strftime("%Y-%m-%d"),
            dense = True, hint_text = "YYYY-MM-DD", expand = True,
            on_change = lambda _: self.validate_dates()
        )
        self.to_input_column = ft.Column(
            controls = [
                ft.Text("To", size = 12, weight = "bold"),
                self.to_input
            ],
            spacing = 2, expand = True
        )

        self.apply_btn = ft.ElevatedButton(
            "Apply", 
            on_click = self.handle_apply_click,
            expand = True,
            style = ft.ButtonStyle(
                shape = ft.RoundedRectangleBorder(radius = 5),
                # 設定背景顏色：正常時為淡紅色 (Red 100/200)，禁用時為灰色
                color = {
                    ft.ControlState.DEFAULT: ft.Colors.RED_700,
                    ft.ControlState.DISABLED: ft.Colors.GREY_400,
                },
                bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.RED_100,
                    ft.ControlState.DISABLED: ft.Colors.GREY_200,
                }
            )            
        )
        
        # 包裝成一個 Row 並設定預設隱藏
        self.custom_date_area = ft.Row(
            controls = [
                ft.Container(content = self.from_input_column, padding = ft.padding.only(left = 10, right = 10),expand = 1, alignment = ft.Alignment.CENTER),
                ft.Container(content = self.to_input_column, padding = ft.padding.only(left = 10, right = 10), expand = 1, alignment = ft.Alignment.CENTER),
                ft.Container(content = self.apply_btn, padding = ft.padding.only(top = 18, left = 10, right = 10), expand = 1, height = 55),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            visible = False # 初始隱藏
        )
        

    def build_ui_structure(self):
        # Header
        header_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # 確保垂直置中
            controls=[
                # habit name
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Text(
                                self.habit_name, 
                                size = 20, 
                                weight = "bold",
                                no_wrap = True
                            )
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE, 
                    ),
                    expand = True,
                    margin = ft.margin.only(right = 15) 
                ),
                # streak
                ft.Text(
                    f"{self.cur_streak}-day streak", 
                    size = 16, 
                    color = ft.Colors.GREY_700,
                    no_wrap = True
                )
            ]
        )
        header_container = ft.Container(
            content = header_row, 
            border = ft.border.only(bottom = ft.BorderSide(0.5, "black12")), 
            padding = ft.padding.only(bottom = 10, left = 10, right = 10) # 稍微增加 padding 讓比例更好看
        )

        # Segmented Buttons
        self.mode_buttons = ft.SegmentedButton(
            selected = ["this week"],
            on_change = self.handle_mode_change,
            allow_empty_selection = False,
            allow_multiple_selection = False,
            show_selected_icon = False,
            expand = True,
            style = ft.ButtonStyle(
                shape = ft.RoundedRectangleBorder(radius = 5),
            ),
            segments = [
                ft.Segment(value = "this week", label = ft.Text("this week", text_align = ft.TextAlign.CENTER)),
                ft.Segment(value = "this month", label = ft.Text("this month", text_align = ft.TextAlign.CENTER)),
                ft.Segment(value = "Custom", label = ft.Text("Custom", text_align = ft.TextAlign.CENTER)),
            ],
        )
        buttons_row = ft.Row([self.mode_buttons])

        # put all elements into main_layout
        self.main_layout.controls.extend([
            header_container,
            buttons_row,
            self.custom_date_area,  # 自訂日期輸入區
            self.stats_row_area     # 將統計卡片的坑位放在按鈕下方
        ])


    def create_stat_card_controls(self, rate, completed, total):
        def build_single_card(title, value):
            return ft.Container(
                content = ft.Column([
                    ft.Text(title, size = 14, color = ft.Colors.GREY_700),
                    ft.Text(value, size = 24, weight = "bold"),
                ], alignment = "center", horizontal_alignment = "center"),
                border = ft.border.all(1, ft.Colors.GREY_400),
                border_radius = 5,
                padding = ft.padding.only(top = 10, bottom = 10),
                expand = 1
            )
        
        return [
            build_single_card("Overall Rate", f"{rate:.1%}"),
            build_single_card("Completed Days", f"{completed} / {total}"),
            build_single_card("Longest Streak", f"{self.longest_streak} days"),
        ]


    def handle_mode_change(self, e):
        mode = e.data if isinstance(e.data, str) else list(e.data)[0]
        
        # 控制日期輸入框的顯示/隱藏
        self.custom_date_area.visible = (mode == "Custom")

        if mode != "Custom":
            self.load_stats_by_mode(mode)
        else:
            self.from_input.value = ""
            self.to_input.value = ""
            
            self.apply_btn.disabled = True
            
            self.render_custom_initial_stats()
            
            if self.page:
                self.update()


    def handle_apply_click(self, e):
        start_date = self.from_input.value
        end_date = self.to_input.value
        # 這裡可以加一些格式檢查 (例如正則表達式)
        self.render_stats(start_date, end_date)


    def load_stats_by_mode(self, mode):
        if mode == "this week":
            date_range = get_week_range(self.today.strftime("%Y-%m-%d"))
        else: # this month
            date_range = get_month_range(self.today.strftime("%Y-%m-%d"))

        self.render_stats(date_range["start"], date_range["end"])


    def render_stats(self, start_date, end_date):
        """最終執行數據獲取與渲染的函式"""
        rate = get_range_rate(self.habit_id, start_date, end_date)
        statuses = get_range_status(self.habit_id, start_date, end_date)
        
        completed = sum(1 for s in statuses if s is True)
        total = sum(1 for s in statuses if s is not None)

        # 更新卡片內容
        new_cards = self.create_stat_card_controls(rate, completed, total)
        self.stats_row_area.controls = new_cards
        
        if self.page:
            self.update()

    
    def render_custom_initial_stats(self):
        """專門用於 Custom 模式初始化的渲染"""
        # 手動建立一組顯示為 0 的卡片
        def build_single(title, value):
            return ft.Container(
                content = ft.Column([
                    ft.Text(title, size = 14, color = ft.Colors.GREY_700),
                    ft.Text(value, size = 24, weight = "bold"),
                ], alignment="center", horizontal_alignment = "center"),
                border = ft.border.all(1, ft.Colors.GREY_400),
                border_radius = 5,
                expand = 1,
                padding = ft.padding.only(top = 10, bottom = 10)
            )
            
        initial_cards = [
            build_single("Overall Rate", "0.0%"),
            build_single("Completed Days", "0 / 0"),
            build_single("Longest Streak", "0 days"),
        ]
        
        self.stats_row_area.controls = initial_cards


      

    '''
        # --- 4. Statistics Cards Row (Overall Rate, Complete Days, Longest Streak) ---
        self.stat_cards = ft.Row(
            spacing=20,
            controls=[
                self.create_stat_card("Overall Rate", "74 %"),
                self.create_stat_card("Complete Days", "25 / 34"),
                self.create_stat_card("Longest Streak", "12 days"),
            ]
        )

        # --- 5. Chart Section ---
        self.chart_title = ft.Text("Rate Over Time (Daily Completion Rate)", size=16)
        
        # 這裡使用簡單的 Placeholder，你可以之後填入 ft.LineChart
        self.line_chart = ft.Container(
            content=ft.Text("Line Chart Canvas Placeholder", color=ft.Colors.GREY_400),
            height=300,
            alignment=ft.Alignment.CENTER,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10
        )     
    '''