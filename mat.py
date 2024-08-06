import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# 示例数据
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([10, 20, 25, 30, 40, 35, 45, 50, 55, 60])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # 调整底部空间以放置按钮
sc = ax.scatter(x, y)
line, = ax.plot(x, y, linestyle='-', marker='o')  # 绘制折线图

highlight = ax.scatter([], [], color='red', s=100)  # 用于高亮显示最近点位的散点图
highlight_index = None  # 用于存储高亮点的索引

# 定义鼠标点击事件处理函数
def on_click(event):
    global highlight_index
    if event.inaxes is not None and event.inaxes != ax_button:
        x_click = event.xdata
        y_click = event.ydata
        distances = np.sqrt((x - x_click)**2 + (y - y_click)**2)
        highlight_index = distances.argmin()
        nearest_x = x[highlight_index]
        nearest_y = y[highlight_index]
        highlight.set_offsets([nearest_x, nearest_y])
        print(f"Highlight Index: {highlight_index}")
        print(f"Coordinate: ({nearest_x}, {nearest_y})")
        print(f"Highlight Index: {highlight_index}")
        print(f"Coordinate: ({nearest_x}, {nearest_y})")
        fig.canvas.draw()

# 定义按钮点击事件处理函数
def delete_point(event):
    global x, y, highlight_index
    if highlight_index is not None:
        if highlight_index == 0 or highlight_index == len(x) - 1:
            print("Cannot interpolate at the boundary points.")
            return
        # 用相邻两点插值
        y[highlight_index] = (y[highlight_index - 1] + y[highlight_index + 1]) / 2
        highlight_index = None
        sc.set_offsets(np.column_stack((x, y)))
        line.set_data(x, y)
        fig.canvas.draw()

# 创建按钮
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
btn = Button(ax_button, 'Delete Point')
btn.on_clicked(delete_point)

# 连接鼠标点击事件到事件处理函数
cid = fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()