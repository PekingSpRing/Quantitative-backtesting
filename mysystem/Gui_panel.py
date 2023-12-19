import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import pandas as pd
import time
from tkcalendar import Calendar
from tkinter import messagebox
from mysystem.backtesting import Backtesting
from mysystem.strategy import My_Strategy
from mysystem.data_reader import DataReader
import threading
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

class Gui_panel:
    def __init__(self, master):
        #基本参数设置
        self.mode='easy'                     #easy表示简单模式，hard表示高阶模式
        self.timemode='start'                #start表示开始时间，end表示结束时间
        self.start_time='2020-02-19'         #开始时间，默认为'2020-02-19'
        self.end_time='2022-12-30'           #结束时间，默认为'2022-12-30'
        self.start_money=100000000           #初始金额，默认为1个小目标
        self.yongjin_rate=0.001              #佣金费率，默认为0.001
        self.yinhua_tax_rate=0.001           #印花税率，默认为0.001
        self.guohu_tax_rate=0.002            #过户费率，默认为0.002
        self.nodanger_rate=0.03              #无风险利率，默认为0.03
        self.benchmark_rate=0.1              #基准收益率，默认为0.1
        self.all_net_value=[]                #所有股票的净值曲线，key为股票代码，value为该股票的净值曲线
        self.all_day=[]                      #所有股票的信号，key为股票代码，value为该股票的信号
        self.performance={}                  #回测指标
        self.signal_path='null'              #信号文件的路径

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
        # 打开基本因子设置界面
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
        initial_amount_label=tk.Label(basic_info_window, text="初始资产",font=("宋体", 14),bg='white')
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
        #设置输入框默认值是0.05
        self.benchmark_rate_entry.insert(0, '0.05')
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
        self.submit_button.place(x=200, y=560, width=400, height=50)
           
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
        selected_dates = event.widget.selection_get()
        selected_date=selected_dates.strftime('%Y-%m-%d')
        if self.timemode=='start':
            self.start_time=selected_date
            messagebox.showinfo(title='开始时间', message='开始时间为'+selected_date)
            event.widget.master.destroy()
        elif self.timemode=='end':
            self.end_time=selected_date
            messagebox.showinfo(title='结束时间', message='结束时间为'+selected_date)
            event.widget.master.destroy()

    def submit_basic_settings(self):
        # 获取用户输入的值
        self.start_money=float(self.initial_amount_entry.get())           #初始金额，默认为1个小目标
        self.yongjin_rate=float(self.yongjin_rate_entry.get())            #佣金费率，默认为0.001
        self.yinhua_tax_rate=float(self.yinhua_tax_rate_entry.get())      #印花税率，默认为0.001
        self.guohu_tax_rate=float(self.guohu_tax_rate_entry.get())        #过户费率，默认为0.002
        self.nodanger_rate=float(self.nodanger_rate_entry.get())          #无风险利率，默认为0.03
        self.benchmark_rate=float(self.benchmark_rate_entry.get())        #基准收益率，默认为0.1
        #不将窗口关闭

        if self.mode=='easy':
            self.easy_backtest_window()
        elif self.mode=='hard':
            self.hard_backtest_window()
    
    def easy_backtest_window(self):
        #简单模式下的回测
        # 打开反转因子设置界面
        reverse_window = tk.Toplevel(self.master)
        reverse_window.geometry("500x550")
        reverse_window.title("反转因子参数设置")
        reverse_window.configure(bg='white')

        #反转因子参数设置
        self.reverse_time=22                 #反转因子的时间窗口,默认为22天
        self.reverse_rate=0.05               #反转因子的阈值,默认为0.05

        # 创建标签和输入框
        label_welcome_reverse = tk.Label(reverse_window, text="反转策略回测",font=("宋体", 23),bg='white')
        label_welcome_reverse.place(x=50, y=30,width=400, height=60)

        #设置反转因子的时间窗口
        reverse_time_label=tk.Label(reverse_window, text="均值窗口",font=("宋体", 14),bg='white')
        reverse_time_label.place(x=150, y=120, width=200, height=40)
        self.reverse_time__entry = tk.Entry(reverse_window,font=("times new roman", 12))
        #设置输入框默认值是22
        self.reverse_time__entry.insert(0, '22')
        self.reverse_time__entry.place(x=150, y=170, width=200, height=40)

        #设置反转因子的阈值
        reverse_rate_label=tk.Label(reverse_window, text="反转因子阈值",font=("宋体", 14),bg='white')
        reverse_rate_label.place(x=150, y=240, width=200, height=40)
        self.reverse_rate_entry = tk.Entry(reverse_window,font=("times new roman", 12))
        #设置输入框默认值是0.001
        self.reverse_rate_entry.insert(0, '0.05')
        self.reverse_rate_entry.place(x=150, y=290, width=200, height=40)


        #放置进度条
        self.progressbar=ttk.Progressbar(reverse_window,orient="horizontal",length=380,mode="determinate")
        self.progressbar.place(x=50, y=400,width=400, height=30)
        self.progressbar["maximum"]=100
        self.progressbar["value"]=0
        reverse_window.update_idletasks()#更新一下进度条

        #放置进度条的标签
        self.process_text=tk.StringVar(value='回测进度')
        self.label_process=tk.Label(reverse_window, textvariable=self.process_text,font=("宋体", 8),bg='white')
        self.label_process.place(x=50, y=370,width=400, height=30)

        # 创建提交按钮
        self.begin_test = tk.Button(reverse_window, text="开始回测", command=self.submit_reverse_settings,font=("宋体", 15))
        self.begin_test.place(x=150, y=450, width=200, height=50)
    
    def hard_backtest_window(self):
        #高阶模式下的回测
        reverse_window = tk.Toplevel(self.master)
        reverse_window.geometry("500x500")
        reverse_window.title("自定义策略回测")
        reverse_window.configure(bg='white')

        # 创建标签和输入框
        label_welcome_reverse = tk.Label(reverse_window, text="自定义策略回测",font=("宋体", 23),bg='white')
        label_welcome_reverse.place(x=50, y=30,width=400, height=60)

        # 创建选取信号文件按钮
        self.choose_file = tk.Button(reverse_window, text="选取信号文件", command=self.select_signal_file,font=("宋体", 15))
        self.choose_file.place(x=150, y=120, width=200, height=50)

        # 创建自定义代码按钮
        self.begin_test_hard = tk.Button(reverse_window, text="创建自定义代码", command=self.design_strategy,font=("宋体", 15))
        self.begin_test_hard.place(x=150, y=190, width=200, height=50)

        #放置进度条的标签
        self.process_text_hard=tk.StringVar(value='回测进度')
        self.label_process_hard=tk.Label(reverse_window, textvariable=self.process_text_hard,font=("宋体", 8),bg='white')
        self.label_process_hard.place(x=50, y=270,width=400, height=30)

        #放置进度条
        self.progressbar_hard=ttk.Progressbar(reverse_window,orient="horizontal",length=380,mode="determinate")
        self.progressbar_hard.place(x=50, y=300,width=400, height=30)
        self.progressbar_hard["maximum"]=100
        self.progressbar_hard["value"]=0
        reverse_window.update_idletasks()#更新一下进度条

        # 创建提交按钮
        self.begin_test_hard = tk.Button(reverse_window, text="开始回测", command=self.submit_reverse_settings,font=("宋体", 15))
        self.begin_test_hard.place(x=150, y=350, width=200, height=50)
    
    def select_signal_file(self):
        filepath = filedialog.askopenfilename(
        title="选择文件",
        filetypes=(("信号文件", "*.json"),("所有文件", "*.*"))
        )
        if filepath:
            self.signal_path=filepath

    def design_strategy(self):
        messagebox.showinfo(title='自定义方法', 
                            message='请按照ReadMe文档在design_strategy.py中补全Your_strategy类中的Your_get_stock_money和Your_get_signal方法')

    def submit_reverse_settings(self):
        def on_complete():
            self.plot_results()

        def thread_target():
            self.run_reverse()
            self.master.after(0, on_complete)

        backtest_thread = threading.Thread(target=thread_target)
        backtest_thread.start()

    def plot_results(self):
            # 创建一个顶层窗口
        tree_windows = tk.Toplevel(self.master)
        tree_windows.geometry("1000x600")
        tree_windows.title("回测结果")

        # 创建 Treeview 部分
        col = ('回测指标', '数值')
        tree = ttk.Treeview(tree_windows, columns=col, show='headings')
        
        # 配置列和插入数据
        for i in col:
            tree.heading(i, text=i)
            tree.column(i, width=100, anchor='center')
        for key, value in self.performance.items():
            tree.insert('', 'end', values=(key, value))

        # 布局 Treeview
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 绘图部分
        self.all_day = [date for date in self.all_day if date != 'before start']
        self.all_day = pd.to_datetime(self.all_day, errors='coerce')

        fig, ax = plt.subplots()
        ax.plot(self.all_day, self.all_net_value[1:])
        ax.set_title("Net Worth Curve")
        ax.set_xlabel("Date")
        ax.set_ylabel("Net Worth")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=int(len(self.all_day)/8)))
        fig.autofmt_xdate()

        # 将图形嵌入到 Tkinter 窗口
        canvas = FigureCanvasTkAgg(fig, master=tree_windows)  # 注意指定 master 为 tree_windows
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        canvas.draw()

    def run_reverse(self):
        if self.mode=='easy':
            reverse_window=self.progressbar.master
            temp_bar=self.progressbar
            temp_text=self.process_text
            self.reverse_time=int(self.reverse_time__entry.get())
            self.reverse_rate=float(self.reverse_rate_entry.get())
        elif self.mode=='hard':
            reverse_window=self.progressbar_hard.master
            temp_bar=self.progressbar_hard
            temp_text=self.process_text_hard
        
        temp_text.set('正在读取数据')

        data_reader=DataReader('../data/stk_daily.feather')
        temp_bar["value"]=20
        reverse_window.update_idletasks()#更新一下进度条

        temp_text.set('正在读取数据')
        all_stocks,all_days=data_reader.drop_discrete_data()
        temp_bar["value"]=40
        reverse_window.update_idletasks()#更新一下进度条

        temp_text.set('正在生成信号,此过程约5min,还请耐心等待')
        my_strategy=My_Strategy(data_reader.data_new,all_stocks,all_days,self.start_money)
        my_strategy.set_time_block(self.start_time,self.end_time)#设置回测时间段
        if self.signal_path!='null' and self.mode=='hard':
            my_strategy.run_Strategy(self.start_time,self.end_time,signal_choices='fromfiles',signal_path=self.signal_path)
        elif self.signal_path=='null' and self.mode=='hard':
            #说明这是自定义模型
            my_strategy.run_Strategy(self.start_time,self.end_time,signal_choices='design')
        elif self.mode=='easy':
            #说明这是简单模式
            my_strategy.run_Strategy(self.start_time,self.end_time)
            #my_strategy.run_Strategy(self.start_time,self.end_time,signal_choices='fromfiles',signal_path='signal.json')
        temp_bar["value"]=60
        reverse_window.update_idletasks()#更新一下进度条

        temp_text.set('正在回测,此过程约2min,还请耐心等待')
        backtest=Backtesting(data_reader.data_new,self.start_money,
                             all_stocks,all_days,my_strategy.start_stock_money,
                             my_strategy.signal,self.start_time,self.end_time)
        backtest.set_fee_rate(self.yongjin_rate,self.yinhua_tax_rate,self.guohu_tax_rate,
                              self.nodanger_rate,self.benchmark_rate)
        temp_bar["value"]=70
        reverse_window.update_idletasks()#更新一下进度条

        backtest.trade_by_signal()
        temp_bar["value"]=90
        reverse_window.update_idletasks()

        temp_text.set('正在计算回测指标')
        self.performance=backtest.calculate_performance_metrics()
        temp_bar["value"]=98
        reverse_window.update_idletasks()

        temp_text.set('正在生成净值曲线')
        self.all_net_value,self.all_day=backtest.draw_net_value()
        temp_bar["value"]=100
        reverse_window.update_idletasks()

        temp_text.set('回测完成！')

def main():
    root = tk.Tk()
    gui = Gui_panel(root)
    root.mainloop()

if __name__ == "__main__":
    main()