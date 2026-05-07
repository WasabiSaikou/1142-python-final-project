import flet as ft
from backend.stats_engine import get_current_streak, get_longest_streak, get_range_rate

class StatisticalChart(ft.Container):
    def __init__(self, habit_id, habit_name):
        super().__init__(expand = True, padding = 15)
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.selected_mode = "7 days" # 預設模式

        self.cur_streak = get_current_streak(self.habit_id)
        self.longest_streak = get_longest_streak(self.habit_id)

        # 用來放置統計內容的容器
        self.stat_content = ft.Column(
            spacing = 0, 
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        )

        # 建立一個支援水平滾動的 Row 來包住內容
        self.content = ft.Row(
            controls = [self.stat_content],
            scroll = ft.ScrollMode.AUTO,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True
        )

        self.build_chart()


    def build_chart(self):
        # Header Row (習慣名稱 & 連續天數) ---        
        header_row = ft.Row(
            controls = [
                ft.Text(self.habit_name, size = 20, weight = "bold"),
                ft.Text(f"{self.cur_streak}-day streak", size = 16, color = ft.Colors.GREY_700)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # --- 2. Mode Selection Row (7天, 30天, Custom) ---
        self.mode_buttons = ft.SegmentedButton(
            selected = {"7 days"},
            on_change = self.handle_mode_change,
            segments = [
                ft.Segment(value = "7 days", label = ft.Text("7 days")),
                ft.Segment(value = "30 days", label = ft.Text("30 days")),
                ft.Segment(value = "Custom", label = ft.Text("Custom")),
            ],
        )

        # --- 3. Custom Date Range Row (預設隱藏) ---
        self.date_picker_row = ft.Row(
            visible=False, # 只有在 Custom 模式才顯示
            controls=[
                ft.TextField(label="From", value="2026 / 03 / 25", width=180, read_only=True),
                ft.TextField(label="To", value="2026 / 04 / 27", width=180, read_only=True),
                ft.ElevatedButton("Apply", on_click = lambda _: print("Applied!")),
            ],
            spacing=20
        )

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

        # --- 組合成主要佈局 ---
        self.content = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                header_row,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row([self.mode_buttons], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                self.date_picker_row,
                self.stat_cards,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.chart_title,
                self.line_chart
            ]
        )

    def create_stat_card(self, title, value):
        """建立統計方格的輔助函式"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, color=ft.Colors.GREY_700),
                ft.Text(value, size=24, weight="bold"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=180,
            height=120,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            alignment=ft.Alignment.CENTER,
        )

    def handle_mode_change(self, e):
        """處理時間模式切換邏輯"""
        self.selected_mode = list(e.data)[0] if isinstance(e.data, set) else e.selection.pop()
        
        # 判斷是否顯示自訂日期列
        if "Custom" in str(self.selected_mode):
            self.date_picker_row.visible = True
        else:
            self.date_picker_row.visible = False
        
        self.update() # 重新渲染 UI