from tkinter import *
from tkinter import ttk
from tkinter import Canvas
from datetime import datetime
from tkinter import messagebox
import uuid
import random

# ================== THEME ==================
BG_COLOR = "#021D29"
SIDEBAR_COLOR = "#232527"
PRIMARY_COLOR = "#2563EB"
TEXT_COLOR = "#FFFFFF"
primary_colour = BG_COLOR

STATUS_OPTIONS = ["Pending", "Awaiting Vendor Quote", "In Progress", "Resolved"]
TEAMS = ["Plumbing", "Electrical", "Groundskeeping", "Vendor"]

DATA_FILE = "data.json"

# ================== MAIN APP ==================
class CMMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Condominium Maintenance Management System")
        self.root.state("zoomed")
        self.root.configure(bg=BG_COLOR)

        # Load data if exists
        self.records = []
        self.daily_updates = []
        self.vendor_notifications = []

        self.setup_style()
        self.create_layout()
        self.show_mainmenu()

    # ================== STYLE ==================
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_COLOR,
                        fieldbackground=BG_COLOR,
                        foreground="#93C5FD",
                        rowheight=32,
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background="#60A5FA",
                        foreground="white",
                        font=("Segoe UI", 12, "bold"))
        style.configure("Primary.TButton",
                        background=PRIMARY_COLOR,
                        foreground="white",
                        padding=8)

    # ================== LAYOUT ==================
    def create_layout(self):
        # Sidebar
        self.sidebar = Frame(self.root, bg=SIDEBAR_COLOR, width=240)
        self.sidebar.pack(side="left", fill="y")

        # Main area
        self.main_area = Frame(self.root, bg=BG_COLOR)
        self.main_area.pack(side="right", expand=True, fill="both")

        # Sidebar content
        Label(self.sidebar, text="CAMC",
                 fg="white", bg=SIDEBAR_COLOR,
                 font=("Segoe UI", 18, "bold")).pack(pady=30)

        # Navigation buttons
        self.nav_button("Main Menu", self.show_mainmenu)
        self.nav_button("Report Issue", self.show_repeat_issue)
        self.nav_button("View Requests", self.show_requests)
        self.nav_button("Incident / Defect Status", self.show_check_problem)

    def nav_button(self, text, command):
        Button(self.sidebar, text=text,
                  font=("Segoe UI", 11),
                  bg=SIDEBAR_COLOR, fg="white",
                  bd=0, anchor="w",
                  padx=20, pady=12,
                  command=command).pack(fill="x")

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ================== SEARCH FUNCTIONALITY ==================
    def create_search_frame(self, tree, data_source="records"):
        """Create search frame for filtering records"""
        search_frame = Frame(self.main_area, bg=primary_colour)
        search_frame.pack(side=TOP, fill=X, padx=20, pady=(0, 10))

        searchTitle = Label(search_frame, text="Search:", bg=primary_colour, fg="#AAAAAA", font=("Arial", 10))
        searchTitle.pack(side=LEFT)
        
        search_var = StringVar()
        search_var.trace("w", lambda *args: self.on_search(search_var, tree, data_source))

        searchEntry = Entry(search_frame, textvariable=search_var, width=32, font=("Arial", 11),
              bg="#333333", fg="white", relief=FLAT, insertbackground="white")
        searchEntry.pack(side=LEFT, padx=(10, 0))
        
        # Add clear button
        Button(search_frame, text="Clear", font=("Arial", 10),
               bg="#555555", fg="white", relief=FLAT,
               command=lambda: self.clear_search(search_var, tree, data_source)).pack(side=LEFT, padx=(10, 0))

    def on_search(self, search_var, tree, data_source="records"):
        """Filter treeview based on search text"""
        search_text = search_var.get().lower()
        
        # Clear tree
        for item in tree.get_children():
            tree.delete(item)
        
        # Get data based on source
        if data_source == "records":
            data = self.records
        elif data_source == "daily_updates":
            data = self.daily_updates
        elif data_source == "vendor_notifications":
            data = self.vendor_notifications
        
        # Filter and display records
        for record in data:
            # Convert all values to string and search
            all_text = ' '.join(str(value).lower() for value in record.values())
            if search_text in all_text:
                # Insert based on what columns the tree expects
                if len(tree['columns']) == 6:
                    tree.insert("", "end", values=(
                        record.get('date', ''),
                        record.get('unit_number', ''),
                        record.get('title', ''),
                        record.get('location', ''),
                        record.get('assigned', ''),
                        record.get('status', '')
                    ))
                elif len(tree['columns']) == 5:
                    tree.insert("", "end", values=(
                        record.get('date', ''),
                        record.get('unit_number', ''),
                        record.get('title', ''),
                        record.get('location', ''),
                        record.get('severity', '')
                    ))
                elif len(tree['columns']) == 4:
                    tree.insert("", "end", values=(
                        record.get('id', ''),
                        record.get('title', ''),
                        record.get('status', ''),
                        record.get('date', '')
                    ))

    def clear_search(self, search_var, tree, data_source="records"):
        """Clear search and reset treeview"""
        search_var.set("")
        # Reset tree with all records
        self.update_treeview(tree, data_source)

    def update_treeview(self, tree, data_source="records"):
        """Update treeview with given records"""
        # Clear tree
        for item in tree.get_children():
            tree.delete(item)
        
        # Get data based on source
        if data_source == "records":
            data = self.records
        elif data_source == "daily_updates":
            data = self.daily_updates
        elif data_source == "vendor_notifications":
            data = self.vendor_notifications
        
        # Insert all records
        for record in data:
            if len(tree['columns']) == 6:
                tree.insert("", "end", values=(
                    record.get('date', ''),
                    record.get('unit_number', ''),
                    record.get('title', ''),
                    record.get('location', ''),
                    record.get('assigned', ''),
                    record.get('status', '')
                ))
            elif len(tree['columns']) == 5:
                tree.insert("", "end", values=(
                    record.get('date', ''),
                    record.get('unit_number', ''),
                    record.get('title', ''),
                    record.get('location', ''),
                    record.get('severity', '')
                ))
            elif len(tree['columns']) == 4:
                tree.insert("", "end", values=(
                    record.get('id', ''),
                    record.get('title', ''),
                    record.get('status', ''),
                    record.get('date', '')
                ))

    # ================== MAIN MENU ==================
    def show_mainmenu(self):
        self.clear_main()

        canvas = Canvas(self.main_area, bg=primary_colour, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)
        canvas.update()
        w, h = canvas.winfo_width(), canvas.winfo_height()

        class Particle:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.x = random.randint(0, width)
                self.y = random.randint(0, height)
                self.size = random.randint(1, 4)
                self.speed = random.uniform(1.0, 3.0)

            def move(self):
                self.x += self.speed
                if self.x > self.width:
                    self.x = 0
                    self.y = random.randint(0, self.height)

        particles = [Particle(w, h) for _ in range(150)]
        text_id = canvas.create_text(
            w // 2, h // 2,
            text="Welcome to Condominium A Management Committee",
            font=("Arial", 32, "bold"),
            fill="white"
        )

        # ================== Live Pending/Complete Label ==================
        self.status_var = StringVar()
        self.status_label = Label(self.main_area, textvariable=self.status_var,
                                     font=("Segoe UI", 12, "bold"),
                                     bg="#1F2933", fg="#FBBF24", padx=10, pady=5)
        self.status_label.place(relx=0.98, rely=0.98, anchor="se")

        def update_status_label():
            pending = len([r for r in self.records if r["status"] not in ["Resolved", "Complete"]])
            complete = len([r for r in self.records if r["status"] in ["Resolved", "Complete"]])
            self.status_var.set(f"Pending: {pending}  |  Complete: {complete}")
            self.main_area.after(1000, update_status_label)

        update_status_label()

        # ================== Particle animation ==================
        def animate():
            nonlocal w, h
            w, h = canvas.winfo_width(), canvas.winfo_height()
            canvas.coords(text_id, w // 2, h // 2)
            canvas.delete("particles")
            for p in particles:
                p.width = w
                p.height = h
                canvas.create_oval(p.x, p.y, p.x + p.size, p.y + p.size,
                                   fill="white", outline="", tags="particles")
                p.move()
            self.main_area.after(30, animate)

        animate()

        close_btn = Button(self.main_area, text="✕",
                              font=("Segoe UI", 14, "bold"),
                              bg="#EF4444", fg="white",
                              activebackground="#DC2626",
                              bd=0, padx=10, pady=5,
                              command=self.root.destroy)
        close_btn.place(relx=0.98, rely=0.02, anchor="ne")
        close_btn.lift()

    # ================== Incident / Defect Status ==================
    def show_check_problem(self):
        self.clear_main()
        
        # ========== 标题和搜索框在同一行 ==========
        header_frame = Frame(self.main_area, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=30, pady=20)
        
        # 标题在左边
        Label(header_frame, text="Incident / Defect Status",
              font=("Segoe UI", 28, "bold"),
              bg=BG_COLOR, fg="white").pack(side="left", anchor="w")
        
        # 搜索框在右边
        search_frame = Frame(header_frame, bg=BG_COLOR)
        search_frame.pack(side="right", anchor="e")
        
        searchTitle = Label(search_frame, text="Search:", bg=BG_COLOR, fg="#AAAAAA", font=("Arial", 10))
        searchTitle.pack(side="left")
        
        self.search_var_check = StringVar()
        self.search_var_check.trace("w", lambda *args: self.on_search_treeview())
        
        searchEntry = Entry(search_frame, textvariable=self.search_var_check, width=32, font=("Arial", 11),
              bg="#333333", fg="white", relief=FLAT, insertbackground="white")
        searchEntry.pack(side="left", padx=(10, 0))
        # ===========================================

        # List frame
        list_frame = Frame(self.main_area, bg=BG_COLOR)
        list_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # 使用Treeview而不是Listbox以显示更多信息
        columns = ("Date", "Unit Number", "Incident / Defect", "Location","Assign To","Issues Status")
        self.tree_check = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        scrollbar = Scrollbar(list_frame, orient="vertical", command=self.tree_check.yview)
        self.tree_check.configure(yscrollcommand=scrollbar.set)
        
        for col in columns:
            self.tree_check.heading(col, text=col)
            self.tree_check.column(col, width=150, anchor="center")
        
        self.tree_check.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 填充数据
        for record in self.records:
            self.tree_check.insert("", "end", 
                       values=(
                           record.get('date', ''),
                           record.get('unit_number', ''),
                           record.get('title', ''),
                           record.get('location', ''),
                           record.get('assigned', ''),
                           record.get('status', '')
                       ))

        # ========== 状态更新区域 ==========
        update_frame = Frame(self.main_area, bg="#1F2933")
        update_frame.pack(padx=30, pady=20, fill="x")
        
        Label(update_frame, text="Update Status",
                 font=("Segoe UI", 16, "bold"),
                 bg="#1F2933", fg="white").pack(anchor="w", padx=20, pady=(15, 10))

        # 状态选择区域
        status_select_frame = Frame(update_frame, bg="#1F2933")
        status_select_frame.pack(padx=20, pady=10, fill="x")
        
        Label(status_select_frame, text="Select New Status:",
                 font=("Segoe UI", 12),
                 bg="#1F2933", fg="white").pack(side="left", padx=(0, 20))
        
        # 状态选项
        self.status_var_check = StringVar(value="Pending")
        status_options = ["Pending", "Awaiting Vendor Quote", "In Progress", "Resolved"]
        
        status_combo = ttk.Combobox(status_select_frame, textvariable=self.status_var_check,
                                    values=status_options, state="readonly",
                                    font=("Segoe UI", 11), width=20)
        status_combo.pack(side="left", padx=10)
        
        # 显示当前选中问题的状态
        self.current_status_label = Label(status_select_frame, text="Current: None",
                                        font=("Segoe UI", 11, "italic"),
                                        bg="#1F2933", fg="#93C5FD")
        self.current_status_label.pack(side="left", padx=(30, 0))

        # 按钮框架
        button_frame = Frame(self.main_area, bg=BG_COLOR)
        button_frame.pack(pady=20)

        # ========== 更新状态按钮 ==========
        def update_selected_status():
            selected = self.tree_check.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a problem first.")
                return
            
            values = self.tree_check.item(selected)["values"]
            new_status = self.status_var_check.get()
            
            # 找到并更新记录
            for record in self.records:
                if (record.get('unit_number') == values[1] and 
                    record.get('title') == values[2] and
                    record.get('date') == values[0]):
                    old_status = record["status"]
                    record["status"] = new_status
                    
                    # 记录状态变更
                    self.daily_updates.append(datetime.now().date())
                    
                    # 显示成功消息
                    messagebox.showinfo("Success", 
                                       f"Status updated from '{old_status}' to '{new_status}'")
                    
                    # 刷新显示
                    self.show_check_problem()
                    self.check_daily_updates()
                    break

        Button(button_frame, text="Update Status",
                  bg="#10B981", fg="white",
                  font=("Segoe UI", 12, "bold"),
                  bd=0, padx=30, pady=10,
                  command=update_selected_status).pack(side="left", padx=10)

        # ========== 检查状态按钮 ==========
        def check_selected_status():
            selected = self.tree_check.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a problem first.")
                return
            
            values = self.tree_check.item(selected)["values"]
            
            # 找到记录
            record = next((r for r in self.records if 
                          r.get('unit_number') == values[1] and 
                          r.get('title') == values[2] and
                          r.get('date') == values[0]), None)
            if record:
                if record["status"] in ["Resolved", "Complete"]:
                    status_msg = "Complete"
                else:
                    status_msg = record["status"]
                
                details = (f"Problem ID: {record.get('id', 'N/A')}\n"
                          f"Title: {record.get('title', 'N/A')}\n"
                          f"Location: {record.get('location', 'N/A')}\n"
                          f"Current Status: {status_msg}\n"
                          f"Date Reported: {record.get('date', 'N/A')}")
                
                if 'assigned' in record:
                    details += f"\nAssigned To: {record['assigned']}"
                
                messagebox.showinfo("Status Details", details)

        Button(button_frame, text="Check Status Details",
                  bg=PRIMARY_COLOR, fg="white",
                  font=("Segoe UI", 12, "bold"),
                  bd=0, padx=30, pady=10,
                  command=check_selected_status).pack(side="left", padx=10)

        # ========== 返回主菜单按钮 ==========
        Button(button_frame, text="✕ Return to Main Menu",
                  bg="#6B7280", fg="white",
                  font=("Segoe UI", 12),
                  bd=0, padx=30, pady=10,
                  command=self.show_mainmenu).pack(side="left", padx=10)

        # ========== 选中事件 - 更新状态选择框 ==========
        def on_tree_select(event):
            selected = self.tree_check.focus()
            if selected:
                values = self.tree_check.item(selected)["values"]
                for record in self.records:
                    if (record.get('unit_number') == values[1] and 
                        record.get('title') == values[2] and
                        record.get('date') == values[0]):
                        # 更新当前状态标签
                        self.current_status_label.config(text=f"Current: {record['status']}")
                        # 设置下拉框为当前状态
                        self.status_var_check.set(record['status'])
                        break
        
        self.tree_check.bind("<<TreeviewSelect>>", on_tree_select)

        # 搜索功能
        def on_search_treeview():
            search_text = self.search_var_check.get().lower()
            
            # 清除当前显示
            for item in self.tree_check.get_children():
                self.tree_check.delete(item)
            
            # 过滤和显示记录
            for record in self.records:
                all_text = ' '.join(str(value).lower() for value in record.values())
                if search_text in all_text:
                    self.tree_check.insert("", "end", values=(
                        record.get('date', ''),
                        record.get('unit_number', ''),
                        record.get('title', ''),
                        record.get('location', ''),
                        record.get('assigned', ''),
                        record.get('status', '')
                    ))

    # ================== REPEAT ISSUE ==================
    def show_repeat_issue(self):
        self.clear_main()
        
        # ========== 标题和搜索框在同一行 ==========
        header_frame = Frame(self.main_area, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=30, pady=20)
        
        # 标题在左边
        Label(header_frame, text="Report Issue",
              font=("Segoe UI", 28, "bold"),
              bg=BG_COLOR, fg="white").pack(side="left", anchor="w")
        
        # 搜索框在右边
        search_frame = Frame(header_frame, bg=BG_COLOR)
        search_frame.pack(side="right", anchor="e")
        
        searchTitle = Label(search_frame, text="Search:", bg=BG_COLOR, fg="#AAAAAA", font=("Arial", 10))
        searchTitle.pack(side="left")
        
        self.search_var_repeat = StringVar()
        self.search_var_repeat.trace("w", lambda *args: self.on_search_treeview_repeat())
        
        searchEntry = Entry(search_frame, textvariable=self.search_var_repeat, width=32, font=("Arial", 11),
              bg="#333333", fg="white", relief=FLAT, insertbackground="white")
        searchEntry.pack(side="left", padx=(10, 0))
        # ===========================================

        # Create treeview
        list_frame = Frame(self.main_area, bg=BG_COLOR)
        list_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("Date", "Unit Number", "Incident / Defect", "Location", "Severity")
        self.tree_repeat = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        scrollbar = Scrollbar(list_frame, orient="vertical", command=self.tree_repeat.yview)
        self.tree_repeat.configure(yscrollcommand=scrollbar.set)
        self.tree_repeat.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for col in columns:
            self.tree_repeat.heading(col, text=col)
            self.tree_repeat.column(col, width=150, anchor="center")

        for r in self.records:
            self.tree_repeat.insert("", "end", values=(
                r.get('date', ''),
                r.get('unit_number', ''),
                r.get('title', ''),
                r.get('location', ''),
                r.get('severity', '')
            ))

        button_frame = Frame(self.main_area, bg=BG_COLOR)
        button_frame.pack(pady=30)

        def repeat_selected_issue():
            selected = self.tree_repeat.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select an issue to repeat.")
                return

            values = self.tree_repeat.item(selected)["values"]
            original_record = next((r for r in self.records if 
                                  r.get('unit_number') == values[1] and 
                                  r.get('title') == values[2] and
                                  r.get('date') == values[0]), None)

            if original_record:
                repeated_record = original_record.copy()
                repeated_record["id"] = str(uuid.uuid4())[:8]
                repeated_record["title"] = f"REPEAT: {original_record['title']}"
                repeated_record["status"] = "Pending"
                repeated_record["date"] = datetime.now().strftime("%Y-%m-%d")
                self.records.append(repeated_record)

                vendor_msg = f"Repeated issue: {repeated_record['title']}"
                self.vendor_notifications.append({
                    'report_id': repeated_record['id'],
                    'message': vendor_msg,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'notified': True
                })

                messagebox.showinfo("Success", "Issue repeated successfully!\nVendor has been notified.")
                self.check_daily_updates()

        Button(button_frame, text="Report Selected Issue",
                  bg=PRIMARY_COLOR, fg="white",
                  font=("Segoe UI", 12, "bold"),
                  bd=0, padx=30, pady=10,
                  command=repeat_selected_issue).pack(side="left", padx=10)

        Button(button_frame, text="✕ Return to Main Menu",
                  bg="#6B7280", fg="white",
                  font=("Segoe UI", 12),
                  bd=0, padx=30, pady=10,
                  command=self.show_mainmenu).pack(side="left", padx=10)

        # 搜索功能
        def on_search_treeview_repeat():
            search_text = self.search_var_repeat.get().lower()
            
            # 清除当前显示
            for item in self.tree_repeat.get_children():
                self.tree_repeat.delete(item)
            
            # 过滤和显示记录
            for record in self.records:
                all_text = ' '.join(str(value).lower() for value in record.values())
                if search_text in all_text:
                    self.tree_repeat.insert("", "end", values=(
                        record.get('date', ''),
                        record.get('unit_number', ''),
                        record.get('title', ''),
                        record.get('location', ''),
                        record.get('severity', '')
                    ))

    # ================== VIEW REQUESTS ==================
    def show_requests(self):
        self.clear_main()
        
        # ========== 标题和搜索框在同一行 ==========
        header_frame = Frame(self.main_area, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=30, pady=20)
        
        # 标题在左边
        Label(header_frame, text="View Requests",
              font=("Segoe UI", 28, "bold"),
              bg=BG_COLOR, fg="white").pack(side="left", anchor="w")
        
        # 搜索框在右边
        search_frame = Frame(header_frame, bg=BG_COLOR)
        search_frame.pack(side="right", anchor="e")
        
        searchTitle = Label(search_frame, text="Search:", bg=BG_COLOR, fg="#AAAAAA", font=("Arial", 10))
        searchTitle.pack(side="left")
        
        self.search_var_requests = StringVar()
        self.search_var_requests.trace("w", lambda *args: self.on_search_treeview_requests())
        
        searchEntry = Entry(search_frame, textvariable=self.search_var_requests, width=32, font=("Arial", 11),
              bg="#333333", fg="white", relief=FLAT, insertbackground="white")
        searchEntry.pack(side="left", padx=(10, 0))
        # ===========================================

        table_frame = Frame(self.main_area, bg=BG_COLOR)
        table_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("Date", "Unit Number", "Incident / Defect", "Location", "Assign To", "Issues Status")
        self.tree_requests = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        scrollbar = Scrollbar(table_frame, orient="vertical", command=self.tree_requests.yview)
        self.tree_requests.configure(yscrollcommand=scrollbar.set)
        self.tree_requests.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for col in columns:
            self.tree_requests.heading(col, text=col)
            self.tree_requests.column(col, width=150, anchor="center")

        for r in self.records:
            self.tree_requests.insert("", "end",
                        values=(
                            r.get('date', ''),
                            r.get('unit_number', ''),
                            r.get('title', ''),
                            r.get('location', ''),
                            r.get('assigned', ''),
                            r.get('status', '')
                        ))

        detail_frame = Frame(self.main_area, bg="#1F2933")
        detail_frame.pack(padx=30, pady=20, fill="x")

        Label(detail_frame, text="Issue Details",
                 font=("Segoe UI", 14, "bold"),
                 bg="#1F2933", fg="white").pack(anchor="w", padx=20, pady=(20, 10))

        details_text = Text(detail_frame, height=6, bg="#374151", fg="white",
                               font=("Segoe UI", 11), wrap="word")
        details_text.pack(padx=20, pady=(0, 20), fill="x")

        def show_selected_details(event):
            selected = self.tree_requests.focus()
            if selected:
                values = self.tree_requests.item(selected)["values"]
                for r in self.records:
                    if (r.get('unit_number') == values[1] and 
                        r.get('title') == values[2] and
                        r.get('date') == values[0]):
                        details_text.delete(1.0, END)
                        details_text.insert(END, f"Title: {r['title']}\n")
                        details_text.insert(END, f"Location: {r['location']}\n")
                        details_text.insert(END, f"Description: {r.get('description', 'N/A')}\n")
                        details_text.insert(END, f"Status: {r['status']}\n")
                        details_text.insert(END, f"Assigned: {r.get('assigned', 'N/A')}\n")
                        details_text.insert(END, f"Date: {r['date']}")
                        if 'additional_notes' in r:
                            details_text.insert(END, "\nAdditional Notes:\n")
                            for note in r['additional_notes']:
                                details_text.insert(END, f"- {note['note']} ({note['timestamp']})\n")
                        break

        self.tree_requests.bind("<<TreeviewSelect>>", show_selected_details)

        add_frame = Frame(self.main_area, bg="#1F2933")
        add_frame.pack(padx=30, pady=10, fill="x")

        Label(add_frame, text="Add more entry into the directory:",
                 font=("Segoe UI", 12, "bold"),
                 bg="#1F2933", fg="white").pack(anchor="w", padx=20, pady=(10, 5))

        add_entry_frame = Frame(add_frame, bg="#1F2933")
        add_entry_frame.pack(padx=20, pady=10, fill="x")

        entry_label = Label(add_entry_frame, text="Additional Notes:",
                               bg="#1F2933", fg="white", font=("Segoe UI", 11))
        entry_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        additional_entry = ttk.Entry(add_entry_frame, width=50)
        additional_entry.grid(row=0, column=1, padx=10)

        btns = Frame(self.main_area, bg=BG_COLOR)
        btns.pack(pady=20)

        def submit_process():
            selected = self.tree_requests.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a request first.")
                return

            values = self.tree_requests.item(selected)["values"]
            additional_text = additional_entry.get().strip()

            for r in self.records:
                if (r.get('unit_number') == values[1] and 
                    r.get('title') == values[2] and
                    r.get('date') == values[0]):
                    if r["status"] == "In Progress":
                        messagebox.showinfo("Process Status", "Process is currently in progress.")
                    else:
                        messagebox.showinfo("Process Status", "Process is not in progress.")

                    if additional_text:
                        if 'additional_notes' not in r:
                            r['additional_notes'] = []
                        r['additional_notes'].append({
                            'note': additional_text,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        messagebox.showinfo("Success", "Additional note added to directory.")
                        additional_entry.delete(0, END)
                    break

        Button(btns, text="Submit Process",
                  bg=PRIMARY_COLOR, fg="white",
                  font=("Segoe UI", 11),
                  bd=0, padx=20, pady=8,
                  command=submit_process).pack(side="left", padx=10)

        Button(btns, text="✕ Return to Main Menu",
                  bg="#6B7280", fg="white",
                  font=("Segoe UI", 11),
                  bd=0, padx=20, pady=8,
                  command=self.show_mainmenu).pack(side="left", padx=10)

        # 搜索功能
        def on_search_treeview_requests():
            search_text = self.search_var_requests.get().lower()
            
            # 清除当前显示
            for item in self.tree_requests.get_children():
                self.tree_requests.delete(item)
            
            # 过滤和显示记录
            for record in self.records:
                all_text = ' '.join(str(value).lower() for value in record.values())
                if search_text in all_text:
                    self.tree_requests.insert("", "end", values=(
                        record.get('date', ''),
                        record.get('unit_number', ''),
                        record.get('title', ''),
                        record.get('location', ''),
                        record.get('assigned', ''),
                        record.get('status', '')
                    ))

    # ================== DAILY UPDATES ==================
    def check_daily_updates(self):
        today = datetime.now().date()
        today_count = self.daily_updates.count(today)
        if today_count > 10:
            self.generate_summary_report()

    def generate_summary_report(self):
        today = datetime.now().date()
        today_records = [r for r in self.records
                         if datetime.strptime(r['date'], "%Y-%m-%d").date() == today]

        summary = f"=== DAILY SUMMARY REPORT ===\n"
        summary += f"Date: {today}\n"
        summary += f"Total Updates Today: {len(self.daily_updates)}\n"
        summary += f"New Requests Today: {len(today_records)}\n\n"
        summary += "Today's Requests:\n"
        for r in today_records:
            summary += f"- {r['id']}: {r['title']} ({r['status']})\n"

        summary += f"\nVendor Notifications Sent: {len([n for n in self.vendor_notifications if datetime.strptime(n['timestamp'][:10], '%Y-%m-%d').date() == today])}"

        messagebox.showinfo("Auto Summary Report",
                            f"More than 10 updates today.\nSummary report generated.\n\n{summary}")

    # ================== ASSIGN/UPDATE STATUS ==================
    def assign(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request first.")
            return
        values = tree.item(selected)["values"]
        for r in self.records:
            if (r.get('unit_number') == values[1] and 
                r.get('title') == values[2] and
                r.get('date') == values[0]):
                r["assigned"] = random.choice(TEAMS)
                messagebox.showinfo("Success", f"Assigned to {r['assigned']} team.")
                break
        self.show_requests()

    def update_status(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request first.")
            return
        values = tree.item(selected)["values"]
        for r in self.records:
            if (r.get('unit_number') == values[1] and 
                r.get('title') == values[2] and
                r.get('date') == values[0]):
                current_index = STATUS_OPTIONS.index(r["status"])
                next_index = (current_index + 1) % len(STATUS_OPTIONS)
                r["status"] = STATUS_OPTIONS[next_index]
                self.daily_updates.append(datetime.now().date())
                messagebox.showinfo("Success", f"Status updated to {r['status']}.")
                break
        self.show_requests()
    
    def save_data(self):
        # 这里应该实现数据保存到文件的功能
        # 目前是占位函数
        pass

# ================== RUN ==================
if __name__ == "__main__":
    root = Tk()
    CMMSApp(root)
    root.mainloop()