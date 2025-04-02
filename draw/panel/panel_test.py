import panel as pn  
from bokeh.plotting import figure  
# 必须初始化Panel扩展  
pn.extension()  
# 创建图表时添加radius参数  
p = figure(width=400, height=300)  
# 替换p.circle为动态半径版本
p.circle([1, 2, 3], [4, 5, 6], radius={'field': 'y', 'transform': p.dodge}, size=slider)
# 创建滑块  
slider = pn.widgets.IntSlider(start=0, end=10, value=5)  
# 组合布局并展示  
pn.Column(slider, p).servable()
