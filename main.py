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
		self.root.title("BestTimer")
		self.root.geometry("600x600")
		self.tasks=[]
		self.present_task=None
		self.is_running=False
		self.timer_id=None
		self.setup_ui()
		self.current_task_index=None
		self.timer_running=False



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
		ttk.Button(control_frame,text='暂停',command=self.pause_timer).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)
		ttk.Button(control_frame,text='停止',command=self.stop_timer).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)

		#创建导入导出框架
		io_frame=ttk.Frame(main_frame,padding=10)
		io_frame.pack(fill=tk.X)

		#创建导入导出按钮
		ttk.Button(io_frame,text='导入任务',command=self.import_tasks).pack(side=tk.LEFT,expand=True,fill=tk.X,padx=5)
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

	#删除任务的方法
	def delete_task(self):
		selected=self.task_listbox.curselection()
		if not selected:
			messagebox.showwarning('提示','输入一个任务')
			return

		index=selected[0]
		del self.tasks[index]
		self.update_task_list()

	#开始计时
	#获取选中任务的索引
	#若选中任务已完成则提示
	#更改计时器状态

	def start_timer(self):
		selected=self.task_listbox.curselection()
		if not selected:
			messagebox.showwarning('提示','请选择一个任务')
			return

		self.current_task_index=selected[0]
		task=self.tasks[self.current_task_index]
		if task.status == 'completed':
			messagebox.showwarning('提示','任务完成')
			return

		task.status = 'running'
		self.timer_running=True
		self.update_task_list()
		self.update_timer()


	#暂停计时器
	#当任务进行时，任务状态改为暂停、
	#使用after方法避免继续倒计时
	def pause_timer(self):
		if self.current_task_index is not None:
			self.tasks[self.current_task_index].status = 'paused'
			self.timer_running=False
			if self.timer_id:
				self.root.after_cancel(self.timer_id)
				self.timer_id = None

	#停止倒计时
	#当有任务运行时，将其改为未开始
	#重置剩余任务时长
	#停止计时器并且取消after任务
	#重置及时器

	def stop_timer(self):
		if self.current_task_index is not None:
			task=self.tasks[self.current_task_index]
			task.status = 'default'
			task.last=task.duration
			self.timer_running=False

			if self.timer_id:
				self.root.after_cancel(self.timer_id)
				self.timer_id = None
			self.timer_label.config(text='00:00:00')
			self.update_task_list()

	#更新倒计时,显示剩余时间

	def update_timer(self):
		if not self.timer_running or self.current_task_index is None:
			return

		task=self.tasks[self.current_task_index]
		task.last-=1
		if task.last<=0:
			task.last=0
			task.status='completed'
			self.timer_running=False
			messagebox.showinfo('提示',f'任务{task.massion}已完成')
			self.timer_label.config(text='00:00:00')

		else:
			self.timer_label.config(text=self.format_time(task.last))
			self.timer_id = self.root.after(1000,self.update_timer)

		self.update_task_list()



	#以csv格式导出文件
	def export_tasks(self):
		filepath=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
		if not filepath:
			return
		with open(filepath,'w',newline='',encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(['任务名称','总时长','状态','剩余时间'])
			for task in self.tasks:
				writer.writerow([task.massion,task.duration,task.status,task.last])

		messagebox.showinfo('成功',f'任务导出到{filepath}')

	#以csv格式导入文件
	# 在弹出的对话框中选择csv文件，若未选择，则返回。
	# 清空self.tasks列表，读取每一行数据，创建task
	def import_tasks(self):
		filepath=filedialog.askopenfilename(filetypes=[('CSV','*.csv')])

		if not filepath:
			return

		try:
			with open(filepath,'r',encoding='utf-8') as f:
				reader = csv.DictReader(f)
				self.tasks = []
				for row in reader:
					self.tasks.append(Task(
						massion=row['任务名称'],
						duration=row['总时长'],
						status=row['状态'],
						last=row['剩余时间']


					))
			self.update_task_list()
			messagebox.showinfo('成功',f'导入{len(self.tasks)}个任务')
		except Exception as e:
			messagebox.showerror('错误',f'导入失败{str(e)}')


if __name__ == "__main__":
    root = tk.Tk()
    app = Maincontrol(root)
    root.mainloop()










