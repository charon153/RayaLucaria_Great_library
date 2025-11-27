import tkinter as tk
import math


class TimePicker(tk.Toplevel):
	def __init__(self, parent, title="修改计时时长"):
		super().__init__(parent)
		self.title(title)
		self.geometry("400x400")
		self.transient(parent)  # 依附于主窗口
		self.grab_set()  # 模态窗口，阻止操作主窗口

		# 初始化时间变量
		self.hour = 0
		self.minute = 0
		self.final_seconds = 0

		# 创建画布（表盘绘制区域）
		self.canvas = tk.Canvas(self, width=250, height=250, bg="white")
		self.canvas.pack(pady=20)

		# 确认按钮
		tk.Button(self, text="确认", command=self.on_confirm).pack(pady=10)

		# 绑定鼠标事件
		self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
		self.canvas.bind("<B1-Motion>", self.on_mouse_move)
		self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

		self.dragging = None  # 标记当前拖动的指针（None/hour/minute）
		self.draw_clock()  # 初始绘制表盘

	def draw_clock(self):

		self.canvas.delete("all")  # 清空画布
		center_x, center_y = 125, 125  # 表盘中心坐标
		radius = 100  # 表盘半径

		# 1. 绘制表盘外圈（圆形）
		self.canvas.create_oval(
			center_x - radius, center_y - radius,
			center_x + radius, center_y + radius,
			outline="#333", width=3
		)

		# 2. 绘制12小时刻度（加粗长刻度）
		for hour in range(12):
			# 计算刻度角度（0度在顶部，顺时针增加）
			angle = (hour * 30 - 90) * (math.pi / 180)  # 30度/小时（360/12）
			# 刻度起点（靠近中心）和终点（靠近外圈）
			x1 = center_x + (radius - 20) * math.cos(angle)
			y1 = center_y + (radius - 20) * math.sin(angle)
			x2 = center_x + (radius - 5) * math.cos(angle)
			y2 = center_y + (radius - 5) * math.sin(angle)
			self.canvas.create_line(x1, y1, x2, y2, fill="#333", width=3)

		# 3. 绘制60分钟短刻度（每5分钟一个）
		for minute in range(60):
			if minute % 5 != 0:  # 跳过与小时刻度重合的位置
				angle = (minute * 6 - 90) * (math.pi / 180)  # 6度/分钟（360/60）
				x1 = center_x + (radius - 15) * math.cos(angle)
				y1 = center_y + (radius - 15) * math.sin(angle)
				x2 = center_x + (radius - 5) * math.cos(angle)
				y2 = center_y + (radius - 5) * math.sin(angle)
				self.canvas.create_line(x1, y1, x2, y2, fill="#666", width=1)

		# 4. 绘制时针
		hour_angle = (self.hour % 12 * 30 + self.minute * 0.5 - 90) * (math.pi / 180)
		hour_length = 50  # 时针长度（短于分针）
		hour_x = center_x + hour_length * math.cos(hour_angle)
		hour_y = center_y + hour_length * math.sin(hour_angle)
		self.canvas.create_line(
			center_x, center_y, hour_x, hour_y,
			fill="#000", width=4, arrow="last"
		)

		# 5. 绘制分针
		minute_angle = (self.minute * 6 - 90) * (math.pi / 180)
		minute_length = 80  # 分针长度（长于时针）
		minute_x = center_x + minute_length * math.cos(minute_angle)
		minute_y = center_y + minute_length * math.sin(minute_angle)
		self.canvas.create_line(
			center_x, center_y, minute_x, minute_y,
			fill="#555", width=2, arrow="last"
		)

		# 6. 绘制表中心圆点
		self.canvas.create_oval(
			center_x - 5, center_y - 5,
			center_x + 5, center_y + 5,
			fill="#333"
		)

	def get_angle_from_mouse(self, x, y):

		center_x, center_y = 125, 125
		dx = x - center_x  # 鼠标与中心的水平偏移
		dy = y - center_y  # 鼠标与中心的垂直偏移
		angle = math.degrees(math.atan2(dy, dx))  # 计算弧度对应的角度
		angle = (angle + 90) % 360  # 转换为0度在顶部的坐标系
		return angle

	def on_mouse_down(self, event):

		center_x, center_y = 125, 125
		distance = math.hypot(event.x - center_x, event.y - center_y)  # 鼠标到中心的距离
		# 时针区域（距离中心30-60像素）
		if 30 < distance < 60:
			self.dragging = "hour"
		# 分针区域（距离中心60-90像素）
		elif 60 < distance < 90:
			self.dragging = "minute"

	def on_mouse_move(self, event):

		if not self.dragging:
			return
		angle = self.get_angle_from_mouse(event.x, event.y)
		# 更新小时（每30度对应1小时）
		if self.dragging == "hour":
			self.hour = round(angle / 30) % 12
		# 更新分钟（每6度对应1分钟）
		elif self.dragging == "minute":
			self.minute = round(angle / 6) % 60
		self.draw_clock()  # 实时重绘表盘

	def on_mouse_up(self, event):

		self.final_seconds = self.hour * 3600 + self.minute * 60

	def on_confirm(self):

		self.on_mouse_up(None)
		self.destroy()

	def show_and_get(self):

		self.wait_window()
		return self.final_seconds


# 测试代码（直接运行可查看效果）
if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()  # 隐藏主窗口
	picker = TimePicker(root)
	print(f"选择的时长：{picker.show_and_get()}秒")
	root.destroy()