import flet as ft
from datetime import datetime, timedelta

# 模擬後端函式：計算特定範圍內的達成率
def get_range_rate(habit_id: str, from_date: str, to_date: str):
    # 這裡目前回傳模擬數據，實際開發時請串接你的資料庫邏輯
    return 0.74  # 例如 74%

def main(page: ft.Page):
    page.title = "Statistics Habit"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    
    # --- 狀態變數 ---
    current_habit = "Running"
    current_streak = 12
    longest_day = 12
    
    # --- UI 元件定義 ---
    
    # 1. 標題列
    header = ft.Container(
        ft.Row(
            controls=[
                ft.Text(current_habit, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"{current_streak}-day streak", size=16, color = ft.Colors.GREY_700, italic=True),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            expand = True
        ),
        border = ft.Border.only(bottom = 1),
        height = 80,
        width = 500
    )

    # 2. 分段切換按鈕
    def handle_segment_change(e):
        custom_row.visible = (e.data == "custom")
        # 根據選擇更新圖表邏輯可寫在此處
        page.update()

    segmented_btn = ft.SegmentedButton(
        selected = ["7"],
        allow_multiple_selection = False,
        # on_change = handle_segment_change,
        segments=[
            ft.Segment(value="7", label=ft.Text("7 days")),
            ft.Segment(value="30", label=ft.Text("30 days")),
            ft.Segment(value="custom", label=ft.Text("Custom")),
        ],
        height = 70,
        width = 500
    )

    # 3. Custom 模式的日期輸入列 (預設隱藏)
    date_from = ft.TextField(label="From", value="2026-03-25", width=150, dense=True, hint_text="YYYY-MM-DD")
    date_to = ft.TextField(label="To", value="2026-04-27", width=150, dense=True, hint_text="YYYY-MM-DD")
    
    custom_row = ft.Row(
        visible=False,
        width = 500,
        height = 60,
        controls = [
            ft.Column([ft.Text("From", size=12), date_from], spacing=2, height = 60),
            ft.Column([ft.Text("To", size=12), date_to], spacing=2, height = 60),
            ft.ElevatedButton("Apply", on_click=lambda _: print("Applying dates..."), 
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))
        ],
        vertical_alignment = ft.CrossAxisAlignment.END,
        
    )

    # 4. 統計資訊卡片
    """def stat_card(title, value, unit=""):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, color=ft.Colors.GREY_700),
                ft.Text(f"{value}{unit}", size=24, weight=ft.FontWeight.W_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15,
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=10,
            expand=True
        )"""

    stats_row = ft.Row(
        controls=[
            ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text("Overall Rate", size = 10),
                        ft.Text("74%", size = 16)
                    ],
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                ),
                padding = 15,
                border = ft.border.all(1, "black12"),
                border_radius = 5,
                expand = True
            ),
            ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text("Complete Days", size = 10),
                        ft.Text("25/34", size = 16)
                    ],
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                ),
                padding = 15,
                border = ft.border.all(1, "black12"),
                border_radius = 5,
                expand = True
            ),
            ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text("Longest Streak", size = 10),
                        # ft.Text(f"{longest_day}-days streak", size = 16)
                        ft.Text("12-days streak", size = 16)
                    ],
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                ),
                padding = 15,
                border = ft.border.all(1, "black12"),
                border_radius = 5,
                expand = True
            ),
            # stat_card("Overall Rate", "74", "%"),
            # stat_card("Complete Days", "25 / 34"),
            # stat_card("Longest Streak", "12", " days"),
        ],
        spacing = 10
    )

    # 5. 統計折線圖
    """chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                points=[
                    ft.LineChartDataPoint(0, 5),
                    ft.LineChartDataPoint(1, 7),
                    ft.LineChartDataPoint(2, 5),
                    ft.LineChartDataPoint(3, 4),
                    ft.LineChartDataPoint(4, 6),
                    ft.LineChartDataPoint(5, 8),
                    ft.LineChartDataPoint(6, 6),
                ],
                color=ft.Colors.GREEN_700,
                stroke_width=3,
                curved=True,
                below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
            )
        ],
        border=ft.border.all(1, ft.Colors.BLACK12),
        left_axis=ft.ChartAxis(labels=[
            ft.ChartAxisLabel(value=0, label=ft.Text("0%")),
            ft.ChartAxisLabel(value=5, label=ft.Text("50%")),
            ft.ChartAxisLabel(value=10, label=ft.Text("100%")),
        ]),
        bottom_axis=ft.ChartAxis(labels=[
            ft.ChartAxisLabel(value=0, label=ft.Text("3/25")),
            ft.ChartAxisLabel(value=3, label=ft.Text("4/8")),
            ft.ChartAxisLabel(value=6, label=ft.Text("4/27")),
        ]),
        expand=True,
        min_y=0,
        max_y=10,
    )

    chart_container = ft.Container(
        content=ft.Column([
            ft.Text("Rate Over Time (Daily Completion Rate)", size=16, weight=ft.FontWeight.W_500),
            ft.Container(chart, height=200)
        ]),
        padding=10
    )"""

    # 主容器封裝所有內容
    main_container = ft.Container(
        content=ft.Column([
            header,
            # ft.Divider(),
            segmented_btn,
            # custom_row,
            # stats_row,
            # chart_container,
        ], spacing=20),
        padding=20,
        border=ft.border.all(1, ft.Colors.BLACK12),
        border_radius=15,
        width=500
    )

    page.add(main_container)

ft.app(target=main)