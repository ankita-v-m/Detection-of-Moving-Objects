from bokeh.models.annotations import Title
from motion_detector import df                      
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool,ColumnDataSource

df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")     # Convert dateTime into required format
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

p=figure(x_axis_type="datetime",height=100, width=500, sizing_mode = "scale_width",title="Motion Graph")    # Plot a graph
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])         # Add hover property and specify tooltips
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="green",source=cds)          # Chose Quadrant as a glyph(pictograph) 

output_file("Graph1.html")
show(p)

