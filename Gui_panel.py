import tkinter as tk
from tkinter import simpledialog

class Gui_panel:
    def __init__(self, master):
        self.master = master
        master.title("量化交易策略回测————对韭当割")
        master.geometry("500x600")
        #设置主窗口的背景颜色
        master.configure(bg='white')
        # 创建一个标签，显示欢迎信息
        self.label_welcome1 = tk.Label(master, text="欢迎使用",font=("宋体", 25),bg='white')
        self.label_welcome1.place(x=180, y=50)
        self.label_welcome2 = tk.Label(master, text="\"对韭当割\"",font=("宋体", 25),bg='white')
        self.label_welcome2.place(x=160, y=110)
        self.label_welcome3 = tk.Label(master, text="量化交易策略回测系统",font=("宋体", 25),bg='white')
        self.label_welcome3.place(x=80, y=170)

        # 创建两个按钮
        self.btn_reversal = tk.Button(master, text="反转因子设置与回测", command=self.open_reversal_window,font=("宋体", 20))
        self.btn_reversal.place(x=100, y=300, width=300, height=60)

        self.btn_strategy = tk.Button(master, text="高阶策略代码编写与回测", command=self.open_strategy_window,font=("宋体", 20))
        self.btn_strategy.place(x=75, y=400, width=350, height=60)

        

    def open_strategy_window(self):
        # 这里可以添加打开高阶策略界面的逻辑
        pass

    def open_reversal_window(self):
        # 打开反转因子设置界面
        reversal_window = tk.Toplevel(self.master)
        reversal_window.geometry("500x500")
        reversal_window.title("反转因子参数设置")

        # 创建标签和输入框
        tk.Label(reversal_window, text="开始时间").pack()
        self.start_time = tk.Entry(reversal_window)
        self.start_time.pack()

        tk.Label(reversal_window, text="结束时间").pack()
        self.end_time = tk.Entry(reversal_window)
        self.end_time.pack()

        tk.Label(reversal_window, text="初始金额").pack()
        self.initial_amount = tk.Entry(reversal_window)
        self.initial_amount.pack()

        # 添加其他输入框...

        # 创建提交按钮
        self.submit_button = tk.Button(reversal_window, text="提交", command=self.submit_reversal_settings)
        self.submit_button.pack()

    def submit_reversal_settings(self):
        # 获取用户输入的值
        start_time = self.start_time.get()
        end_time = self.end_time.get()
        initial_amount = self.initial_amount.get()
        # 获取其他输入的值...

        # 这里可以添加处理这些值的逻辑
        print("开始时间:", start_time)
        print("结束时间:", end_time)
        print("初始金额:", initial_amount)
        # 打印其他输入的值...

def main():
    root = tk.Tk()
    gui = Gui_panel(root)
    root.mainloop()

if __name__ == "__main__":
    main()