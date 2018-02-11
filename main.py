# coding=utf-8
from Tkinter import *


class WidgetsDemo:
    def __init__(self):
        window = Tk()  # 创建一个窗口
        window.title("Experiment")  # 设置标题

        frame1 = Frame(window)  # 创建一个框架
        frame1.pack()  # 将框架frame1放置在window中

        self.v2 = IntVar()
        # 创建两个单选按钮，放置在frame1中，按钮文本是分别是Red和Yellow，背景色分别是红色和黄色，
        # 当rbRed按钮被选中时self.v2为1,当rbYellow按钮被选中时，self.v2为2，按钮被点击时触发processRadiobutto函数
        rbRed = Radiobutton(frame1, text="Red", bg="red",
                            variable=self.v2, value=1,
                            command=self.processRadiobutton)

        rbYellow = Radiobutton(frame1, text="Yellow", bg="yellow",
                               variable=self.v2, value=2,
                               command=self.processRadiobutton)
        # grid布局
        rbRed.grid(row=1, column=2)
        rbYellow.grid(row=1, column=3)

        frame2 = Frame(window)  # 创建框架frame2
        frame2.pack()  # 将frame2放置在window中

        label = Label(frame2, text="Enter your name: ")  # 创建标签

        self.name = StringVar()
        # 创建Entry，内容是与self.name关联
        entryName = Entry(frame2, textvariable=self.name)
        # 创建按钮，点击按钮时触发processButton函数
        btGetName = Button(frame2, text="Get Name",
                           command=self.processButton)
        # 创建消息
        message = Message(frame2, text=self.name)

        # grid布局
        label.grid(row=1, column=1)
        message.grid(row=1, column=4)

        # 创建格式化文本，并放置在window中
        text = Text(window)
        text.pack()


        # 监测事件直到window被关闭
        window.mainloop()

    def processRadiobutton(self):
        print (("Red" if self.v2.get() == 1 else "Yellow")
               + " is selected.")

        # Get Name按钮点击函数

    def processButton(self):
        print ("Your name is " + self.name.get())


if "__main__":
    WidgetsDemo()