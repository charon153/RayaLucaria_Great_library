import time
import csv
from datetime import datetime, timedelta
from tkinter import ttk,messagebox,simpledialog
from tkinter import filedialog
import tkinter as tk

# 储存单个信息任务：
# massion:任务名称；
# duration：任务总时长;
# status:状态；
# last:剩余时间
class Task:
	def __init__(self,massion, duration,status='default',last=None):
		self.massion = massion
		self.duration = int(duration)
		self.status = status
		self.last = int(last) if last else self.duration


#控制器
class Maincontrol:
	def __init__(self,root):
		self.root = root
		self.root.tittle("C'sTimer")
		self.root.geometry("600x400")
		self.tasks=[]
		self.present_task=None
		self.is_running=False
		self.timer_id=None
		self.setup_ui()


#创建框架，父容器为root,内边距为10
#将框架变为整个窗口中，并使得填充整个窗口，框架随窗口大小调整
	def setup_ui(self):
		main_frame=ttk.Frame(self.root,padding=10)
		main_frame.pack(fill='both',expand=True)
		task_frame=ttk.LabelFrame(main_frame,text="任务列表",padding=10)#将任务列表框架放置在主框架中，填充主框架，上下边距为5
		task_frame.pack(fill=tk.BOTH,expand=True,pady=5)

		#列表框
		self.task_listbox=tk.Listbox(task_frame,height=10)
		self.task_listbox.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
		self.update_task_list()
		#按钮
		button_frame=ttk.Frame(task_frame,padding=10)
		button_frame.pack(side=tk.RIGHT,fill=tk.Y)

		ttk.Button(button_frame,text="添加任务",command=self.add_task).pack(fill=tk.X,pady=5)
		ttk.Button(button_frame,text="修改任务",command=self.modify_task).pack(fill=tk.X,pady=5)
		ttk.Button(button_frame, text="删除任务", command=self.delete_task).pack(fill=tk.X, pady=5)

		#倒计时显示区域
		timer_frame=ttk.LabelFrame(main_frame,text='计时器',padding=10)
		timer_frame.pack(fill=tk.X,pady=5)

		#创建倒计时显示标签
		self.timer_label=ttk.Label(timer_frame,text='00:00:00',font=('Arial',20))
		self.timer_label.pack(pady=10)

		#计时器控制按钮框架
		control_frame=ttk.Frame(main_frame,padding=10)
		control_frame.pack(fill=tk.X)

		#创建开始，暂停，停止按钮
		#左侧对齐，左右边距5像素
		ttk.Button(control_frame,text='开始',command=self.start_timer).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)
		ttk.Button(control_frame,text='暂停',command=self.start_timer).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)
		ttk.Button(control_frame,text='停止',command=self.start_timer).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)

		#创建导入导出框架
		io_frame=ttk.Frame(main_frame,padding=10)
		io_frame.pack(fill=tk.X)

		#创建导入导出按钮
		ttk.Button(io_frame,text='导出任务',command=self.export_tasks).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)
		ttk.Button(io_frame,text='导出任务',command=self.export_tasks).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)

	#将秒转化为时分秒格式
	def format_time(self,seconds):
		return str(timedelta(seconds=seconds))

	#及时更新任务列表内容
	def update_task_list(self):
		self.task_listbox.delete(0,tk.END)
		for i,task in enumerate(self.tasks):
			self.task_listbox.insert(tk.END,f'{i+1}.{task.massion} -{self.format_time(task.duration)}-{task.status}')


	#添加新任务的方法
	def add_task(self):
		#弹出输入框获取信息
		massion=simpledialog.askstring('添加任务','请输入任务名称')
		if not massion:
			return

		duration_str=simpledialog.askstring('添加任务','请输入任务时长')
		if not duration_str or not duration_str.isdigit():
			messagebox.showerror('时长无效，请输入有效时长')
			return
		#创建Task实例并添加到self.task列表
		duration=int(duration_str)
		self.tasks.append(Task(massion,duration))
		self.update_task_list()

	#修改选中的任务
	def modify_task(self):
		selected=self.task_listbox.curselection()
		if not selected:
			messagebox.showwarning('注意','选择一个任务')
			return

		index=selected[0]
		task=self.tasks[index]

		massion=simpledialog.askstring('修改任务','请输入新的任务名称',initialvalue=task.massion)
		if not massion:
			return

		duration_str=simpledialog.askstring('修改任务','请输入新任务时长',initialvalue=str(task.duration))
		if not duration_str or not duration_str.isdigit():
			messagebox.showerror('错误','请输入有效时长')
			return

		duration=int(duration_str)
		task.massion=massion
		task.last=duration
		self.update_task_list()








