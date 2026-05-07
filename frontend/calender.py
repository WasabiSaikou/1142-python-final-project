import flet as ft
import calendar
import datetime
# from backend.stats_engine import get_month_status   ### not yet
from backend.log_manager import get_status # 以 id、日期為參數，輸出該天的完成狀況


class HistoryCalendar(ft.Container):
    def __init__(self, habit_id):
        super().__init__(expand = True, padding = 5)
        self.habit_id = habit_id

        self.today = datetime.datetime.now()
        self.state = {
            "year": self.today.year,
            "month": self.today.month,
        }

        # habits 完成度資料
        #self.habit_history_data = get_month_status(self.habit_id, self.state["year"], self.state["month"])
        # returns {"2026-04-01": "completed", "2026-04-02": "missed", "2026-04-03": "not_started"}

        # 用來放置月曆格子的容器
        self.calendar_content = ft.Column(
            spacing = 0, 
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            width = 560
        )

        # 建立一個支援水平滾動的 Row 來包住內容
        self.content = ft.Row(
            controls = [self.calendar_content],
            scroll = ft.ScrollMode.AUTO,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True
        )

        self.build_calendar()
        

    def get_status_dot(self, date_str):     # 判斷日期狀態並回傳顏色
        check_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today_date = self.today.date()
        
        # 未來日期：不顯示點點
        if check_date > today_date:
            return None
        
        # 2. 直接從字典中根據日期字串 (Key) 取得狀態 (Value)
        # 使用 .get() 避免 Key 不存在時報錯
        status = self.habit_history_data.get(date_str)

        if status == "completed":
            return "#58CD67"  # 綠色
        elif status == "missed":
            return "#F92828"  # 紅色
        else:
            # 過去日子但沒有紀錄，或是狀態為 "not_started"
            return "#888888"  # 灰色

        '''
        # 搜尋對應習慣與日期的紀錄
        record = next((item for item in self.habit_history_data 
                       if item["date"] == date_str and item["habit_id"] == self.habit_id), None)
        if record is not None:
            return "#58CD67" if record["completed"] else "#F92828"  # 根據完成狀態回傳綠色或紅色
        else:
            return "#888888"    # 過去但沒有紀錄：顯示灰色 (Not started)
        '''

    def build_calendar(self):
        self.calendar_content.controls.clear()
        
        year = self.state["year"]
        month = self.state["month"]

        # 取得月份資料
        month_list = calendar.monthcalendar(year, month)

        # 標題與切換按鈕
        month_name = calendar.month_name[month] # 取得英文月份名稱
        header_row = ft.Row(
            controls=[
                ft.Row([
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click = lambda _: self.change_date(y = -1)),
                    ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click = lambda _: self.change_date(m = -1)),
                ], spacing = 0),
                ft.Text(f"{month_name} {year}", size = 30, weight = "bold", width = 250, text_align = "center", expand = True),
                ft.Row([
                    ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click = lambda _: self.change_date(m = 1)),
                    ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click = lambda _: self.change_date(y = 1)),
                ], spacing = 0),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
        )
        self.calendar_content.controls.append(header_row)
        self.calendar_content.controls.append(ft.Container(height = 10)) # 間距


        # 專門包住「格線區」的容器 ---
        grid_body = ft.Column(spacing = 0)

        # 星期表頭 (Mon-Sun)
        # calendar.setfirstweekday(calendar.SUNDAY) # 星期表頭 (Sun-Sat)
        days_header = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
        
        week_head = ft.Row(
            controls=[
                ft.Container(
                    content = ft.Text(day, size = 16, weight = "bold"),
                    width = 80, height = 40, alignment = ft.Alignment.CENTER,
                    border = ft.border.only(
                        bottom = ft.BorderSide(0.5, ft.Colors.BLACK26),
                        right = ft.BorderSide(0.5, ft.Colors.BLACK26))
                ) for day in days_header
            ],
            spacing = 0, 
            alignment = ft.MainAxisAlignment.CENTER
        )
        grid_body.controls.append(week_head)

        # 日期格子
        for week in month_list:
            week_row = ft.Row(spacing = 0, alignment = ft.MainAxisAlignment.CENTER)
            for day in week:
                # 建立格子的基礎內容：日期數字
                content_stack = ft.Column(
                    controls=[ft.Text(str(day) if day != 0 else "", size=16)],
                    alignment = ft.MainAxisAlignment.START,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    spacing = 8
                )

                # 如果當天有日期，檢查是否需要加入小點
                if day != 0:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    dot_color = self.get_status_dot(date_str)
                    
                    if dot_color:
                        content_stack.controls.append(
                            ft.Container(
                                width = 12,
                                height = 12,
                                bgcolor = dot_color,
                                border_radius = 6
                            )
                        )

                day_box = ft.Container(
                    content = content_stack,
                    width = 80, height = 70,
                    border = ft.border.only(
                        bottom = ft.BorderSide(1, "black12"),
                        right = ft.BorderSide(1, "black12")
                    ),
                    padding = 10,
                    alignment = ft.Alignment.TOP_LEFT
                )
                week_row.controls.append(day_box)
            grid_body.controls.append(week_row)

        # 加上最外圈的左邊與上邊線
        grid_container = ft.Container(
            content = grid_body,
            border = ft.border.only(
                left = ft.BorderSide(1, "black12"),
                top = ft.BorderSide(1, "black12")
            )
        )

        # 最後將組好的 grid_container 放入主 Column
        self.calendar_content.controls.append(grid_container) # 修正後的格線區
        self.calendar_content.controls.append(ft.Container(height = 20))
        
        # 圖示點點說明欄 (Legend)
        legend_row = ft.Row(
            controls = [
                ft.Row([ft.Container(width = 14, height = 14, border_radius = 7, bgcolor = "#58CD67"),
                        ft.Text(" : completed", size = 18)], alignment = ft.Alignment.TOP_LEFT),
                ft.Row([ft.Container(width = 14, height = 14, border_radius = 7, bgcolor = "#F92828"),
                        ft.Text(" : missed", size = 18)], alignment = ft.Alignment.TOP_LEFT),
                ft.Row([ft.Container(width = 14, height = 14, border_radius = 7, bgcolor = "#888888"),
                        ft.Text(" : not started", size = 18)], alignment = ft.Alignment.TOP_LEFT)
            ],
            alignment = ft.MainAxisAlignment.CENTER, # 說明欄水平置中
            spacing = 90, # 各個說明項之間的間距
        )
        self.calendar_content.controls.append(legend_row) 


    def change_date(self, y = 0, m = 0):
        self.state["year"] += y
        self.state["month"] += m
        if self.state["month"] > 12: 
            self.state["month"] = 1
            self.state["year"] += 1
        elif self.state["month"] < 1: 
            self.state["month"] = 12
            self.state["year"] -= 1

        # 切換月份後，重新呼叫後端函式取得該月份的資料
        self.habit_history_data = get_month_status(self.habit_id, self.state["year"], self.state["month"])

        self.build_calendar()
        self.update()

