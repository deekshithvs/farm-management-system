import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template,request
import mysql.connector
#import imgdetect as id
app = Flask(__name__)


#@app.route("/analysis/<string:consuid>/<int:flag>",methods=['GET','POST'])
def chart(consuid,flag,type):
    data = {"days": [], "bugs": [], "costs": []}
    for i in range(1, 11):
        data['days'].append(i)
        data['bugs'].append(random.randint(1,100))
        data['costs'].append(random.uniform(1.00, 1000.00))
    values = {"days": [], "costs": []}
    cropName="cereals"
    if (request.method=='POST'):
                cropName=request.form["cropName"]
                print(cropName)
    if( flag==0):
        sql_select_Query = "select count(*) ,date from requests  where status=true and farmerID=%s  group by date order by date "
    # else:
    #     sql_select_Query = "select avg(Rate), time from productdetails where CropType=\""+cropName+"\" group by time order by time; "
    cursor = db.cursor()
    cursor.execute(sql_select_Query,(consuid,))
    records = cursor.fetchall()
    for row in records:
        values['days'].append(str(row[1]))
        values['costs'].append(int(row[0]))
    hover = create_hover_tool()
    plot = create_bar_chart(values, "amount", "days",
                            "costs", hover)
    script, div = components(plot)
    return script, div
   # return render_template("chart.html", bars_count=111,
                         #  the_div=div, the_script=script,consuid=consuid)
@app.route('/plantDiseaseRecognition/<string:type>/<string:email>',methods=['POST','GET'])
def plantDiseaseRecognition(type,email):
        if(request.method=='POST'):
                cropImageURL=request.form["imageURL"]
                print(cropImageURL)
                # cur=db.cursor()
                # cropImageURL="C:\\Users\deekshith\Documents\\"+cropImageURL
                # query='INSERT INTO  DiseaseRecognition(email,usertype,imageURL,time)  values(%s,%s,%s,%s)'
                # values=(email,type,cropImageURL,datetime.datetime.now())
                # cur.execute(query,values)
                # db.commit()
                print(img)
                cropImageURL="C:\\Users\deekshith\Desktop\m.vpd.png"
                res=img.predict(cropImageURL)
                print(res)
                res1=img.predict(cropImageURL)
                            
        return render_template('login.html')



def create_hover_tool():
    # we'll code this function in a moment
    return None


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#234544"
    plot.yaxis.axis_label = "quantity"
    plot.xaxis.axis_label = "date"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "--"
    plot.xaxis.major_label_orientation = 1
    return plot

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="werock@1",
  database="farmsample"
)
#img=id.image()
if __name__ == '__main__':
   app.run(debug=False)