import tkinter as tk
from tkinter import ttk
from datetime import timedelta

from main import Maincontrol,Task

class TimerAppWithPercentage(Maincontrol):
    def __init__(self, root):
        # 调用父类的初始化方法
        super().__init__(root)
        # 添加百分比显示标签（在倒计时区域扩展）
        self.percentage_label = ttk.Label(self.timer_frame, text="剩余：100%", font=("Arial", 12))
        self.percentage_label.pack(pady=5)  # 放在倒计时下方

    def calculate_percentage(self, task):
        """计算剩余时间百分比"""
        if task.duration == 0:
            return 0
        return round((task.last / task.duration) * 100, 1)

    def update_timer(self):
        """重写父类的 update_timer 方法，添加百分比更新"""
        if not self.timer_running or self.current_task_index is None:
            return

        task = self.tasks[self.current_task_index]
        task.last -= 1

        if task.last <= 0:
            task.last = 0
            task.status = "completed"
            self.timer_running = False
            self.timer_label.config(text="00:00:00")
            self.percentage_label.config(text="剩余：0%")  # 完成时显示0%
            tk.messagebox.showinfo("提示", f"任务 '{task.name}' 已完成！")
        else:
            # 更新倒计时和百分比
            time_str = str(timedelta(seconds=task.last))
            self.timer_label.config(text=time_str)
            percentage = self.calculate_percentage(task)
            self.percentage_label.config(text=f"{percentage}%")
            # 继续计时
            self.timer_id = self.root.after(1000, self.update_timer)

        # 调用父类的任务列表更新
        self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerAppWithPercentage(root)
    root.mainloop()