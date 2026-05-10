import flet as ft
from backend.habit_manager import get_all_habits
from frontend.calender import HistoryCalendar

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand = True, padding = 0)
        
        # save all visited Container
        self.hist_items_list = []
        
        self.habit_list = get_all_habits()
        # return [{"id": "abc", "name": "Running", "created_at": "2026-04-28"}, {"id": "efg", "name": "Reading", "created_at": "2026-04-30"}]
        
        # right side : detail of history
        self.hist_detail = ft.Container(
            padding = 15,
            expand = True,
            content = ft.Text("Select a habit to see details", size = 20, color = "grey"),
            alignment = ft.Alignment.TOP_CENTER
        )       
        
        # 沒有習慣資料時顯示提示
        if not self.habit_list:
            self.hist_detail.content = ft.Text("No habits were established.", size = 20, color = "grey")
        else:
            # 建立 Sidebar 項目，傳入整個習慣字典
            sidebar_controls = [self.hist_nav_item(habit) for habit in self.habit_list]
            # 初始化：預設顯示第一個習慣的日曆
            first_habit = self.habit_list[0]
            self.hist_detail.content = self.create_detail_content(first_habit["id"])
            sidebar_controls[0].bgcolor = "black12" # 設定第一個為選取狀態      

        # left side : sidebar of hostory
        self.hist_sidebar = ft.Container(
            width = 250,
            alignment = ft.Alignment.TOP_LEFT,
            padding = 0,
            bgcolor = "#F5EFE6",
            border = ft.border.only(right = ft.BorderSide(0.5, "black12")),
            content = ft.Column(
                spacing = 0,
                controls = [
                    # SELECT HABIT
                    ft.Container(                        
                        content = ft.Text("SELECT HABIT", size = 13, weight = "bold", color = "#807E7C"),
                        padding = ft.padding.only(top = 20, bottom = 10, left = 10)
                    ),
                    ft.Container(
                        expand = True,
                        padding = ft.padding.only(left = 5, right = 5),
                        content = ft.Column(
                            # controls = [self.hist_nav_item(name) for name in habit_info],
                            controls = sidebar_controls,
                            scroll = ft.ScrollMode.AUTO,
                            spacing = 5
                        )
                    ) 
                ]
            )
        )

        # all contents of History
        self.content = ft.Column(
            expand = True,
            spacing = 0,
            controls=[
                # Title : History
                ft.Container(
                    width = 1400,
                    bgcolor = "#F6EFE5",
                    padding = ft.padding.only(left = 25, top = 20, bottom = 20),
                    border = ft.border.only(bottom = ft.BorderSide(0.5, "black12")),
                    content = ft.Column([
                        ft.Text("History", size = 30, weight = "bold"),
                        ft.Text("Review your daily progress.", size = 15),
                    ], spacing = 5)
                ),

                # Content (left -> sidebar ; right -> history of the chosen habit)
                ft.Row(
                    expand = True,
                    spacing = 0,
                    vertical_alignment = ft.CrossAxisAlignment.START,
                    controls = [
                        self.hist_sidebar,
                        self.hist_detail
                    ]
                )
            ]
        )


    def create_detail_content(self, habit_id):
        """傳入 ID 建立日曆元件"""
        return ft.Column(
            controls = [HistoryCalendar(habit_id = habit_id)], 
            scroll = ft.ScrollMode.AUTO, 
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )


    def hist_nav_item(self, habit_dict):
        """產生成員條目，將字典存入 data"""

        # 內建 hover 處理 (懸浮變色)
        def handle_hover(e):
            if e.control.bgcolor != "black12":
                e.control.bgcolor = "black12" if e.data == "true" else None
                e.control.update()

        nav_item = ft.Container(
            on_click = self.hist_on_nav_change,
            on_hover = handle_hover,
            data = habit_dict,  # 這裡存入整個字典 {"id": ..., "name": ...}
            padding = ft.padding.symmetric(horizontal = 10, vertical = 12), # 增加上下間距
            border_radius = 5,
            ink = True,
            ink_color = "black12",

            content = ft.Row(
                vertical_alignment = ft.CrossAxisAlignment.START,
                controls = [
                    ft.Icon(ft.Icons.EVENT, size = 20, color = "#807E7C"),
                    # 使用 Expanded 強制文字佔滿剩餘寬度並觸發換行
                    ft.Text(
                        value = habit_dict["name"], # 顯示習慣名稱
                        size = 16,
                        color = "black87",
                        overflow = ft.TextOverflow.VISIBLE, # 確保換行文字不會被截斷
                        no_wrap = False,
                        expand = True
                    )    
                ]
            )
        )
        # 將物件存入清單，供後續遍歷更新
        self.hist_items_list.append(nav_item)
        return nav_item


    def hist_on_nav_change(self, e):
        # 獲取點擊的習慣字典
        habit_info = e.control.data
        clicked_id = habit_info["id"]

        # 1. 更新側邊欄背景色
        for item in self.hist_items_list:
            item.bgcolor = "black12" if item.data["id"] == clicked_id else None
            item.update()

        # 2. 以 ID 為參數更新右側日曆
        self.hist_detail.content = self.create_detail_content(clicked_id)
        self.hist_detail.update()

        '''
        # 1. 遍歷清單，更新所有條目的背景色
        for item in self.hist_items_list:
            item.bgcolor = "black12" if item.data == clicked_label else None
            item.update()

        # 2. **核心銜接點**：更換右側 Detail 內容
        # 我們直接重新建立整個 Column，並傳入新的 habit_info 給 HistoryCalendar
        self.hist_detail.content = self.create_detail_content(clicked_label)
        self.hist_detail.update()
        '''