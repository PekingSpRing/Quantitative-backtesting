import tkinter as tk
from tkinter import simpledialog
import tkinter.ttk as ttk
from tkcalendar import Calendar

class Gui_panel:
    def __init__(self, master):
        #基本参数设置
        self.mode='easy'                     #easy表示简单模式，hard表示高阶模式
        self.timemode='start'                #start表示开始时间，end表示结束时间
        self.start_time='2010-01-01'         #开始时间，默认为2010-01-01
        self.end_time='2019-12-31'           #结束时间，默认为2019-12-31
        self.start_money=100000000           #初始金额，默认为1个小目标
        self.yongjin_rate=0.001              #佣金费率，默认为0.001
        self.yinhua_tax_rate=0.001           #印花税率，默认为0.001
        self.guohu_tax_rate=0.002            #过户费率，默认为0.002
        self.nodanger_rate=0.03              #无风险利率，默认为0.03
        self.benchmark_rate=0.1              #基准收益率，默认为0.1

        #反转因子参数设置
        self.reverse_time=22                 #反转因子的时间窗口,默认为22天
        self.reverse_rate=0.05               #反转因子的阈值,默认为0.05

        # 设置主窗口
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
        self.btn_reversal = tk.Button(master, text="反转因子设置与回测", command=self.open_basic_info_window,font=("宋体", 20))
        self.btn_reversal.place(x=100, y=300, width=300, height=60)

        self.btn_strategy = tk.Button(master, text="高阶策略代码编写与回测", command=self.open_strategy_window,font=("宋体", 20))
        self.btn_strategy.place(x=75, y=400, width=350, height=60)

        

    def open_strategy_window(self):
        # 这里可以添加打开高阶策略界面的逻辑
        self.mode='hard'
        self.setting_basic_infowindows()
        pass

    def open_basic_info_window(self):
        self.setting_basic_infowindows()
        self.mode='easy'
        
    def setting_basic_infowindows(self):
        #无论点击哪种模式，都会弹出这个窗口，用来设置基本信息
        #基本信息包括：开始时间、结束时间、初始金额、佣金费率、印花税率、过户费率、基准收益率、无风险利率
        # 打开反转因子设置界面
        basic_info_window = tk.Toplevel(self.master)
        basic_info_window.geometry("800x700")
        basic_info_window.title("基本参数设置")
        basic_info_window.configure(bg='white')

        # 创建标签和输入框
        label_welcome_basic = tk.Label(basic_info_window, text="请设置您的基本参数",font=("宋体", 23),bg='white')
        label_welcome_basic.place(x=200, y=20,width=400, height=60)

        #设置开始时间和结束时间
        timelabel=tk.Label(basic_info_window, text="开始时间-结束时间",font=("宋体", 14),bg='white')
        timelabel.place(x=250, y=80, width=300, height=40)
        start_time_button=tk.Button(basic_info_window, text="设置开始时间", command=self.start_time_button)
        start_time_button.place(x=270, y=130, width=100, height=40)
        end_time_button=tk.Button(basic_info_window, text="设置结束时间", command=self.end_time_button)
        end_time_button.place(x=430, y=130, width=100, height=40)

        #设置初始金额
        initial_amount_label=tk.Label(basic_info_window, text="初始金额",font=("宋体", 14),bg='white')
        initial_amount_label.place(x=150, y=190, width=200, height=40)
        self.initial_amount_entry = tk.Entry(basic_info_window,font=("times new roman", 12))
        #设置输入框默认值是100000000
        self.initial_amount_entry.insert(0, '100000000')
        self.initial_amount_entry.place(x=150, y=240, width=200, height=40)

        #设置佣金费率
        yongjin_rate_label=tk.Label(basic_info_window, text="佣金费率",font=("宋体", 14),bg='white')
        yongjin_rate_label.place(x=450, y=190, width=200, height=40)
        self.yongjin_rate_entry = tk.Entry(basic_info_window,font=("times new roman", 12))
        #设置输入框默认值是0.001
        self.yongjin_rate_entry.insert(0, '0.001')
        self.yongjin_rate_entry.place(x=450, y=240, width=200, height=40)

        #设置印花税率
        yinhua_tax_rate_label=tk.Label(basic_info_window, text="印花税率",font=("宋体", 14),bg='white')
        yinhua_tax_rate_label.place(x=150, y=310, width=200, height=40)
        self.yinhua_tax_rate_entry = tk.Entry(basic_info_window,font=("times new roman", 12))
        #设置输入框默认值是0.001
        self.yinhua_tax_rate_entry.insert(0, '0.001')
        self.yinhua_tax_rate_entry.place(x=150, y=360, width=200, height=40)

        #设置过户费率
        guohu_tax_rate_label=tk.Label(basic_info_window, text="过户费率",font=("宋体", 14),bg='white')
        guohu_tax_rate_label.place(x=450, y=310, width=200, height=40)
        self.guohu_tax_rate_entry = tk.Entry(basic_info_window,font=("times new roman", 12))
        #设置输入框默认值是0.002
        self.guohu_tax_rate_entry.insert(0, '0.002')
        self.guohu_tax_rate_entry.place(x=450, y=360, width=200, height=40)

        #设置基准收益率
        benchmark_rate_label=tk.Label(basic_info_window, text="基准收益率",font=("宋体", 14),bg='white')
        benchmark_rate_label.place(x=150, y=430, width=200, height=40)
        self.benchmark_rate_entry = tk.Entry(basic_info_window,font=("times new roman", 12))
        #设置输入框默认值是0.1
        self.benchmark_rate_entry.insert(0, '0.1')
        self.benchmark_rate_entry.place(x=150, y=480, width=200, height=40)

        #设置无风险利率
        nodanger_rate_label=tk.Label(basic_info_window, text="无风险利率",font=("宋体", 14),bg='white')
        nodanger_rate_label.place(x=450, y=430, width=200, height=40)
        self.nodanger_rate_entry = tk.Entry(basic_info_window,font=("times new roman", 12))
        #设置输入框默认值是0.03
        self.nodanger_rate_entry.insert(0, '0.03')
        self.nodanger_rate_entry.place(x=450, y=480, width=200, height=40)


        # 创建提交按钮
        self.submit_button = tk.Button(basic_info_window, text="提交", command=self.submit_basic_settings,font=("宋体", 15))
        self.submit_button.place(x=200, y=540, width=400, height=50)
        
    
    def start_time_button(self):
        self.timemode='start'
        time_window=tk.Toplevel(self.master)
        cal = Calendar(time_window, selectmode='day')
        cal.pack()
        cal.bind("<<CalendarSelected>>", self.on_date_select)
    
    def end_time_button(self):
        self.timemode='end'
        time_window=tk.Toplevel(self.master)
        cal = Calendar(time_window, selectmode='day')
        cal.pack()
        cal.bind("<<CalendarSelected>>", self.on_date_select)
    
    def on_date_select(self,event):
        #将选中的日期赋值给开始时间或者结束时间
        selected_date = event.widget.selection_get()
        if self.timemode=='start':
            self.start_time=selected_date
        elif self.timemode=='end':
            self.end_time=selected_date
        #将窗口关闭
        event.widget.master.destroy()

    def submit_basic_settings(self):
        # 获取用户输入的值
        self.start_money=float(self.initial_amount_entry.get())           #初始金额，默认为1个小目标
        self.yongjin_rate=float(self.yongjin_rate_entry.get())            #佣金费率，默认为0.001
        self.yinhua_tax_rate=float(self.yinhua_tax_rate_entry.get())      #印花税率，默认为0.001
        self.guohu_tax_rate=float(self.guohu_tax_rate_entry.get())        #过户费率，默认为0.002
        self.nodanger_rate=float(self.nodanger_rate_entry.get())          #无风险利率，默认为0.03
        self.benchmark_rate=float(self.benchmark_rate_entry.get())        #基准收益率，默认为0.1
        #将窗口关闭
        self.submit_button.master.destroy()
        if self.mode=='easy':
            self.easy_backtest_window()
        elif self.mode=='hard':
            self.hard_backtest_window()
    
    def easy_backtest_window(self):
        #简单模式下的回测
        pass
    
    def hard_backtest_window(self):
        #高阶模式下的回测
        pass



def main():
    root = tk.Tk()
    gui = Gui_panel(root)
    root.mainloop()

if __name__ == "__main__":
    main()