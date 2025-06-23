import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import time
from datetime import datetime
import win32file
import win32con
import pywintypes

class FileTimeModifier:
    def __init__(self, root):
        self.root = root
        self.root.title("文件时间修改器")
        self.root.geometry("600x400")
        
        # 文件选择部分
        self.file_frame = ttk.LabelFrame(root, text="文件选择", padding="10")
        self.file_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path, width=50)
        self.file_entry.pack(side="left", padx=5)
        
        self.browse_button = ttk.Button(self.file_frame, text="浏览", command=self.browse_file)
        self.browse_button.pack(side="left", padx=5)
        
        # 时间设置部分
        self.time_frame = ttk.LabelFrame(root, text="时间设置", padding="10")
        self.time_frame.pack(fill="x", padx=10, pady=5)
        
        # 创建时间
        self.create_frame = ttk.Frame(self.time_frame)
        self.create_frame.pack(fill="x", pady=5)
        ttk.Label(self.create_frame, text="创建时间：").pack(side="left")
        self.create_entry = ttk.Entry(self.create_frame, width=20)
        self.create_entry.pack(side="left", padx=5)
        ttk.Button(self.create_frame, text="获取当前时间", 
                   command=lambda: self.set_current_time(self.create_entry)).pack(side="left")
        
        # 修改时间
        self.modify_frame = ttk.Frame(self.time_frame)
        self.modify_frame.pack(fill="x", pady=5)
        ttk.Label(self.modify_frame, text="修改时间：").pack(side="left")
        self.modify_entry = ttk.Entry(self.modify_frame, width=20)
        self.modify_entry.pack(side="left", padx=5)
        ttk.Button(self.modify_frame, text="获取当前时间", 
                   command=lambda: self.set_current_time(self.modify_entry)).pack(side="left")
        
        # 访问时间
        self.access_frame = ttk.Frame(self.time_frame)
        self.access_frame.pack(fill="x", pady=5)
        ttk.Label(self.access_frame, text="访问时间：").pack(side="left")
        self.access_entry = ttk.Entry(self.access_frame, width=20)
        self.access_entry.pack(side="left", padx=5)
        ttk.Button(self.access_frame, text="获取当前时间", 
                   command=lambda: self.set_current_time(self.access_entry)).pack(side="left")
        
        # 说明标签
        ttk.Label(self.time_frame, 
                 text="时间格式：YYYY-MM-DD HH:MM:SS，例如：2023-12-31 23:59:59").pack(pady=5)
        
        # 操作按钮
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.modify_button = ttk.Button(self.button_frame, text="修改时间", command=self.modify_times)
        self.modify_button.pack(side="left", padx=5)
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(root, textvariable=self.status_var)
        self.status_label.pack(pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_path.set(filename)
            self.update_current_times()

    def set_current_time(self, entry):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry.delete(0, tk.END)
        entry.insert(0, current_time)

    def update_current_times(self):
        try:
            filepath = self.file_path.get()
            if not os.path.exists(filepath):
                return

            # 获取文件时间
            handle = win32file.CreateFile(
                filepath,
                win32con.GENERIC_READ,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_ATTRIBUTE_NORMAL,
                None
            )
            
            times = win32file.GetFileTime(handle)
            handle.Close()

            # 更新输入框
            def filetime_to_str(filetime):
                return datetime.fromtimestamp(filetime.timestamp()).strftime("%Y-%m-%d %H:%M:%S")

            self.create_entry.delete(0, tk.END)
            self.create_entry.insert(0, filetime_to_str(times[0]))
            
            self.modify_entry.delete(0, tk.END)
            self.modify_entry.insert(0, filetime_to_str(times[1]))
            
            self.access_entry.delete(0, tk.END)
            self.access_entry.insert(0, filetime_to_str(times[2]))

        except Exception as e:
            messagebox.showerror("错误", f"获取文件时间失败：{str(e)}")

    def modify_times(self):
        try:
            filepath = self.file_path.get()
            if not filepath:
                messagebox.showerror("错误", "请先选择文件！")
                return
            
            if not os.path.exists(filepath):
                messagebox.showerror("错误", "文件不存在！")
                return

            # 转换时间字符串为 PyWin32 时间格式
            def str_to_filetime(time_str):
                dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                return pywintypes.Time(dt.timestamp())

            create_time = str_to_filetime(self.create_entry.get())
            modify_time = str_to_filetime(self.modify_entry.get())
            access_time = str_to_filetime(self.access_entry.get())

            # 修改文件时间
            handle = win32file.CreateFile(
                filepath,
                win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_ATTRIBUTE_NORMAL,
                None
            )
            
            win32file.SetFileTime(handle, create_time, access_time, modify_time)
            handle.Close()

            self.status_var.set("文件时间修改成功！")
            messagebox.showinfo("成功", "文件时间修改成功！")

        except ValueError as e:
            messagebox.showerror("错误", "时间格式错误！请使用正确的格式：YYYY-MM-DD HH:MM:SS")
        except Exception as e:
            messagebox.showerror("错误", f"修改文件时间失败：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTimeModifier(root)
    root.mainloop()
