import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import calendar

# 检查是否为Windows系统，如果是则导入win32相关模块
is_windows = os.name == 'nt'
if is_windows:
    try:
        from win32file import SetFileTime, CreateFile, CloseHandle
        from win32file import GENERIC_WRITE, FILE_SHARE_WRITE
        from win32file import OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL
        from pywintypes import Time
        win32_available = True
    except ImportError:
        win32_available = False
else:
    win32_available = False

class FileTimeModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件时间修改工具")
        self.root.geometry("600x450")
        self.root.resizable(False, False)  # 设置窗口大小固定
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("TLabel", padding=5)
        self.style.configure("TFrame", padding=10)
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件选择部分
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding=10)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="浏览...", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        # 时间设置部分
        time_frame = ttk.LabelFrame(main_frame, text="时间设置", padding=10)
        time_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # 创建时间
        created_frame = ttk.Frame(time_frame)
        created_frame.pack(fill=tk.X, pady=5)
        
        self.created_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(created_frame, text="修改创建时间", variable=self.created_enabled, 
                        command=self.toggle_created).pack(side=tk.LEFT, padx=5)
        
        if not win32_available:
            ttk.Label(created_frame, text="(仅Windows系统支持，需安装pywin32)", 
                     foreground="red").pack(side=tk.LEFT, padx=5)
            self.created_enabled.set(False)
        
        self.created_date_frame = ttk.Frame(time_frame)
        self.created_date_frame.pack(fill=tk.X, pady=2)
        ttk.Label(self.created_date_frame, text="日期:").pack(side=tk.LEFT, padx=5)
        # 获取当前日期作为默认值
        current_date = datetime.now()
        self.created_date = DateEntry(self.created_date_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, state='disabled',
                                    year=current_date.year, month=current_date.month, day=current_date.day)
        self.created_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.created_date_frame, text="时间:").pack(side=tk.LEFT, padx=5)
        
        # 获取当前时间作为默认值
        current_time = datetime.now()
        self.created_hour = ttk.Spinbox(self.created_date_frame, from_=0, to=23, width=3, state='disabled')
        self.created_hour.set(current_time.hour)
        self.created_hour.pack(side=tk.LEFT)
        ttk.Label(self.created_date_frame, text=":").pack(side=tk.LEFT)
        self.created_minute = ttk.Spinbox(self.created_date_frame, from_=0, to=59, width=3, state='disabled')
        self.created_minute.set(current_time.minute)
        self.created_minute.pack(side=tk.LEFT)
        ttk.Label(self.created_date_frame, text=":").pack(side=tk.LEFT)
        self.created_second = ttk.Spinbox(self.created_date_frame, from_=0, to=59, width=3, state='disabled')
        self.created_second.set(current_time.second)
        self.created_second.pack(side=tk.LEFT)
        
        # 修改时间
        modified_frame = ttk.Frame(time_frame)
        modified_frame.pack(fill=tk.X, pady=5)
        
        self.modified_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(modified_frame, text="修改修改时间", variable=self.modified_enabled, 
                        command=self.toggle_modified).pack(side=tk.LEFT, padx=5)
        
        self.modified_date_frame = ttk.Frame(time_frame)
        self.modified_date_frame.pack(fill=tk.X, pady=2)
        ttk.Label(self.modified_date_frame, text="日期:").pack(side=tk.LEFT, padx=5)
        # 获取当前日期作为默认值
        current_date = datetime.now()
        self.modified_date = DateEntry(self.modified_date_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, state='disabled',
                                     year=current_date.year, month=current_date.month, day=current_date.day)
        self.modified_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.modified_date_frame, text="时间:").pack(side=tk.LEFT, padx=5)
        
        # 获取当前时间作为默认值
        current_time = datetime.now()
        self.modified_hour = ttk.Spinbox(self.modified_date_frame, from_=0, to=23, width=3, state='disabled')
        self.modified_hour.set(current_time.hour)
        self.modified_hour.pack(side=tk.LEFT)
        ttk.Label(self.modified_date_frame, text=":").pack(side=tk.LEFT)
        self.modified_minute = ttk.Spinbox(self.modified_date_frame, from_=0, to=59, width=3, state='disabled')
        self.modified_minute.set(current_time.minute)
        self.modified_minute.pack(side=tk.LEFT)
        ttk.Label(self.modified_date_frame, text=":").pack(side=tk.LEFT)
        self.modified_second = ttk.Spinbox(self.modified_date_frame, from_=0, to=59, width=3, state='disabled')
        self.modified_second.set(current_time.second)
        self.modified_second.pack(side=tk.LEFT)
        
        # 访问时间
        accessed_frame = ttk.Frame(time_frame)
        accessed_frame.pack(fill=tk.X, pady=5)
        
        self.accessed_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(accessed_frame, text="修改访问时间", variable=self.accessed_enabled, 
                        command=self.toggle_accessed).pack(side=tk.LEFT, padx=5)
        
        self.accessed_date_frame = ttk.Frame(time_frame)
        self.accessed_date_frame.pack(fill=tk.X, pady=2)
        ttk.Label(self.accessed_date_frame, text="日期:").pack(side=tk.LEFT, padx=5)
        # 获取当前日期作为默认值
        current_date = datetime.now()
        self.accessed_date = DateEntry(self.accessed_date_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, state='disabled',
                                     year=current_date.year, month=current_date.month, day=current_date.day)
        self.accessed_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.accessed_date_frame, text="时间:").pack(side=tk.LEFT, padx=5)
        
        # 获取当前时间作为默认值
        current_time = datetime.now()
        self.accessed_hour = ttk.Spinbox(self.accessed_date_frame, from_=0, to=23, width=3, state='disabled')
        self.accessed_hour.set(current_time.hour)
        self.accessed_hour.pack(side=tk.LEFT)
        ttk.Label(self.accessed_date_frame, text=":").pack(side=tk.LEFT)
        self.accessed_minute = ttk.Spinbox(self.accessed_date_frame, from_=0, to=59, width=3, state='disabled')
        self.accessed_minute.set(current_time.minute)
        self.accessed_minute.pack(side=tk.LEFT)
        ttk.Label(self.accessed_date_frame, text=":").pack(side=tk.LEFT)
        self.accessed_second = ttk.Spinbox(self.accessed_date_frame, from_=0, to=59, width=3, state='disabled')
        self.accessed_second.set(current_time.second)
        self.accessed_second.pack(side=tk.LEFT)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="应用修改", command=self.apply_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="显示当前时间", command=self.show_current_times).pack(side=tk.RIGHT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var.set("就绪")
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.file_path.set(file_path)
            self.status_var.set(f"已选择文件: {file_path}")
            # 自动加载文件的当前时间
            self.load_file_times(file_path)
    
    def load_file_times(self, file_path):
        """加载文件的当前时间并设置到控件中"""
        try:
            # 获取文件时间
            stat_info = os.stat(file_path)
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            accessed_time = datetime.fromtimestamp(stat_info.st_atime)
            
            # 在Windows上获取创建时间
            if is_windows:
                created_time = datetime.fromtimestamp(stat_info.st_ctime)
                # 设置创建时间控件
                self.created_date.set_date(created_time)
                self.created_hour.set(created_time.hour)
                self.created_minute.set(created_time.minute)
                self.created_second.set(created_time.second)
            
            # 设置修改时间控件
            self.modified_date.set_date(modified_time)
            self.modified_hour.set(modified_time.hour)
            self.modified_minute.set(modified_time.minute)
            self.modified_second.set(modified_time.second)
            
            # 设置访问时间控件
            self.accessed_date.set_date(accessed_time)
            self.accessed_hour.set(accessed_time.hour)
            self.accessed_minute.set(accessed_time.minute)
            self.accessed_second.set(accessed_time.second)
            
        except Exception as e:
            self.status_var.set(f"加载文件时间失败: {str(e)}")
    
    def toggle_created(self):
        state = 'normal' if self.created_enabled.get() else 'disabled'
        self.created_date.config(state=state)
        self.created_hour.config(state=state)
        self.created_minute.config(state=state)
        self.created_second.config(state=state)
    
    def toggle_modified(self):
        state = 'normal' if self.modified_enabled.get() else 'disabled'
        self.modified_date.config(state=state)
        self.modified_hour.config(state=state)
        self.modified_minute.config(state=state)
        self.modified_second.config(state=state)
    
    def toggle_accessed(self):
        state = 'normal' if self.accessed_enabled.get() else 'disabled'
        self.accessed_date.config(state=state)
        self.accessed_hour.config(state=state)
        self.accessed_minute.config(state=state)
        self.accessed_second.config(state=state)
    
    def get_datetime_str(self, date_widget, hour_widget, minute_widget, second_widget):
        date_obj = date_widget.get_date()
        hour = int(hour_widget.get())
        minute = int(minute_widget.get())
        second = int(second_widget.get())
        
        dt = datetime(date_obj.year, date_obj.month, date_obj.day, hour, minute, second)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def show_current_times(self):
        file_path = self.file_path.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("错误", "请选择一个有效的文件")
            return
        
        try:
            # 获取文件时间
            stat_info = os.stat(file_path)
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            accessed_time = datetime.fromtimestamp(stat_info.st_atime)
            
            # 在Windows上获取创建时间
            if is_windows:
                created_time = datetime.fromtimestamp(stat_info.st_ctime)
                created_info = f"创建时间: {created_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            else:
                created_info = "创建时间: 不支持在此系统上查看\n"
            
            info = (f"文件: {file_path}\n"
                   f"{created_info}"
                   f"修改时间: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                   f"访问时间: {accessed_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            messagebox.showinfo("文件时间信息", info)
            
            # 更新控件显示当前时间
            if is_windows:
                self.created_date.set_date(created_time)
                self.created_hour.set(created_time.hour)
                self.created_minute.set(created_time.minute)
                self.created_second.set(created_time.second)
            
            self.modified_date.set_date(modified_time)
            self.modified_hour.set(modified_time.hour)
            self.modified_minute.set(modified_time.minute)
            self.modified_second.set(modified_time.second)
            
            self.accessed_date.set_date(accessed_time)
            self.accessed_hour.set(accessed_time.hour)
            self.accessed_minute.set(accessed_time.minute)
            self.accessed_second.set(accessed_time.second)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取文件时间信息失败: {str(e)}")
    
    def apply_changes(self):
        file_path = self.file_path.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("错误", "请选择一个有效的文件")
            return
        
        try:
            # 检查是否至少启用了一个时间修改选项
            if not (self.created_enabled.get() or self.modified_enabled.get() or self.accessed_enabled.get()):
                messagebox.showwarning("警告", "请至少选择一个要修改的时间属性")
                return
            
            # 获取时间字符串
            created_time_str = None
            modified_time_str = None
            accessed_time_str = None
            
            if self.created_enabled.get():
                created_time_str = self.get_datetime_str(
                    self.created_date, self.created_hour, self.created_minute, self.created_second
                )
            
            if self.modified_enabled.get():
                modified_time_str = self.get_datetime_str(
                    self.modified_date, self.modified_hour, self.modified_minute, self.modified_second
                )
            
            if self.accessed_enabled.get():
                accessed_time_str = self.get_datetime_str(
                    self.accessed_date, self.accessed_hour, self.accessed_minute, self.accessed_second
                )
            
            # 修改文件时间
            self.modify_file_times(file_path, created_time_str, modified_time_str, accessed_time_str)
            
        except Exception as e:
            messagebox.showerror("错误", f"修改文件时间失败: {str(e)}")
    
    def modify_file_times(self, file_path, created=None, modified=None, accessed=None):
        """
        修改文件的创建时间、修改时间和访问时间
        
        参数:
            file_path: 文件路径
            created: 创建时间 (格式: "YYYY-MM-DD HH:MM:SS")
            modified: 修改时间 (格式: "YYYY-MM-DD HH:MM:SS")
            accessed: 访问时间 (格式: "YYYY-MM-DD HH:MM:SS")
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            # 将时间字符串转换为时间戳
            def str_to_timestamp(time_str):
                if time_str:
                    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    return time.mktime(dt.timetuple())
                return None

            # 转换时间
            created_time = str_to_timestamp(created)
            modified_time = str_to_timestamp(modified)
            accessed_time = str_to_timestamp(accessed)

            # 获取当前时间作为默认值
            current_time = time.time()
            
            # 设置访问时间和修改时间
            if modified_time is not None or accessed_time is not None:
                os.utime(file_path, (
                    accessed_time if accessed_time is not None else os.stat(file_path).st_atime,
                    modified_time if modified_time is not None else os.stat(file_path).st_mtime
                ))

            # 在Windows系统上设置创建时间
            if is_windows and win32_available and created_time is not None:
                handle = CreateFile(
                    file_path,
                    GENERIC_WRITE,
                    FILE_SHARE_WRITE,
                    None,
                    OPEN_EXISTING,
                    FILE_ATTRIBUTE_NORMAL,
                    None
                )
                
                # 直接从datetime对象创建Windows时间对象，避免使用时间戳
                if created:
                    dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
                    # 创建一个兼容PyInstaller打包环境的Windows时间对象
                    created_win32_time = Time(dt.year, dt.month, dt.day, 
                                             dt.hour, dt.minute, dt.second, 0)
                    SetFileTime(handle, created_win32_time, None, None)
                
                CloseHandle(handle)

            self.status_var.set(f"成功修改文件时间属性: {file_path}")
            messagebox.showinfo("成功", "文件时间属性已成功修改")
            
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            raise e

def main():
    # 检查依赖
    missing_deps = []
    try:
        import tkcalendar
    except ImportError:
        missing_deps.append("tkcalendar")
    
    if is_windows and not win32_available:
        missing_deps.append("pywin32")
    
    # 如果缺少依赖，显示安装提示
    if missing_deps:
        print("缺少以下依赖库，请安装：")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n可以使用以下命令安装：")
        print(f"pip install {' '.join(missing_deps)}")
        
        if tk._default_root is None:
            root = tk.Tk()
            root.withdraw()
        
        messagebox.showwarning(
            "缺少依赖", 
            f"缺少以下依赖库，请安装：\n{', '.join(missing_deps)}\n\n"
            f"可以使用以下命令安装：\npip install {' '.join(missing_deps)}"
        )
    
    root = tk.Tk()
    app = FileTimeModifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
