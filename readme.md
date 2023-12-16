## 欢迎使用“对韭当割”量化交易回测系统
**开发者：曹仁君 北京大学地球与空间科学学院**
### 使用说明
#### 1.入门用法（适合编程基础薄弱的用户）
* 运行test.ipynb中的main()函数，可以进入系统主界面。
* 点击**反转因子设置与回测**进入简易模式。
* 在该模式下，你可以设置有关基本参数，包括回测区间时间，初始资产，佣金费率，印花税率，过户费率，基准收益率，无风险利率。其中，如果不进行特别设置，每个基本参数都设有默认值，可以直接点击提交进入下一界面。                       
* 默认回测区间是2020-02-19到2022-12-30
* 在下一界面，可以对反转策略的因子进行设置，可以设置均值窗口与阈值
* 设置完毕后点击开始回测，系统会自动根据你所设计的参数计算出超额收益，年化收益，年化波动，夏普比率，最大回撤。以及绘制出净值曲线。
* **注：回测过程请勿随意点击或关闭窗口，有可能引发未知错误**

#### 2.进阶用法（适合编程基础较好的用户）
* 运行test.ipynb中的main()函数，可以进入系统主界面。
* 点击**高阶策略代码编写与回测**进入进阶模式。
* 在该模式下的第一个页面与简易模式相同，你可以设置有关基本参数，设置完毕后点击提交进入下一界面
* 在下一界面，有两个选项 **选取信号文件**和**创建自定义代码**。

##### 2.1 选取信号文件
* 这一选项允许你将信号以json的格式输入系统，在mysystem/newdata/signal.json中，有示例信号文件，你可以选择这个信号文件，也可以仿照其创建自己的信号文件。
* 信号文件的格式如下：
* {"000001.SZ": [["2020-02-19", 0, "full"],……],……}
* {"股票名": [["日期", 是否买卖, 买卖数目],……],……}
* 日期必须严格按照 "年-月-日"标准书写。
* 0代表不进行买卖操作，1代表买入，-1代表卖出。
* 数量可以是具体整数，也可以是字符串"full"，"full"代表全仓买卖。
* 选定信号文件后，点击开始回测即可，与前文一致。

##### 2.2 创建自定义代码
* 这部分是为专业编程开发人员设计，通过修改**design_strategy.py**文件中的**Your_strategy**类中的**Your_get_stock_money**和**Your_get_signal**方法，既可将你独有的策略接入系统，实现回测。
* **Your_get_stock_money**方法，是为了实现最初的资产配置策略，默认情况下，会将初始资金等分给每一支股票，通过这个函数，你可以实现你自己定制的资产配置策略，注意，最终返回值一定是一个字典，字典的key为股票代码，value为该股票的初始资产。
* **Your_get_signal**方法，是为了获取交易信号序列，你可以通过自己的量化策略生成一个交易信号序列，注意，最终返回值也是一个字典，字典的key为股票代码，value为该股票的信号，信号为一个嵌套列表,大列表中的每个小列表格式为[日期,交易信号,数量]，日期为'年-月-日格式'，交易信号1为买入，-1为卖出，0为不操作，数量如果是'full'表示全仓买卖，如果是整数就表示按整数买卖，{'stock name':[['2020-02-19',1,300],……],……}。
* 具体信息可参见具体代码中的注释。
* 完成自定义后，直接点击开始回测即可，余下过程与前文一致。

#### 注意事项：
* 每次程序执行只可以使用一种策略进行回测，如果多次反复回测，程序可能会出现数值上的错误
* 在程序执行过程中，如遇执行较慢的情况，请耐心等待，在test.ipynb中的输出框中也会有详细的执行进度细节。
* **报错可能：**假如在数据读取时，出现了找不到文件的情况，请您修改mysystem/Gui_panel.py 中的第343行代码，将路径改为可以在您环境上运行的路径即可。因为在我的环境里，我的相对路径是相对于整个项目工程文件夹的相对路径，在有些编译器中可能会设置为相对Gui_panel.py的路径，这并不是一个bug，只是不同编译器设置不同罢了，如有报错，还请您手动改一下这个地方。

#### 最后，“对韭当割”量化交易回测系统祝您使用愉快！

