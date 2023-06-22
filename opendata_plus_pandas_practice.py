# -*- coding: utf-8 -*-
"""
使用 youbike 2.0 資料，完成以下5項

1. 大安區與信義區，共有多少個測站
2. 全台北市總車格數最多的五個站點名稱
3. 台北市哪個行政區的 站點/平方公里 數值最低 (難)

選擇行政區之後，先更新資料，分別以 matplotlib / google chart 顯示以下資訊
4. 直方圖 - 該行政區之可用車輛數 (sbi) 之遞減排序，前10名 (數量不變，但順序會變)
5. 圓餅圖 - 站點/平方公里 分布 (同上)
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

# pandas for json
import pandas as pd
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json" # youbike 2.0
json_df = pd.read_json(url) # test.json
#print(json_df)
#json_df.head()
json_df.tail()

"""#作業1

"""

temp = json_df[(json_df["sarea"]=="大安區") | (json_df["sarea"]=="信義區")]
temp.count()

"""#作業2"""

temp2 = json_df.sort_values(by = "tot", ascending = False) #遞減
temp2[["sna","tot"]].head()

"""#作業3"""

import pandas as pd

url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
json_df = pd.read_json(url)

area = {
    '松山區': 9.2878,
    '信義區': 11.2077,
    '大安區': 11.3614,
    '中山區': 13.6821,
    '中正區': 7.6071,
    '大同區': 5.6815,
    '萬華區': 8.8522,
    '文山區': 31.5090,
    '南港區': 21.8424,
    '內湖區': 31.5787,
    '士林區': 62.3682,
    '北投區': 56.8216,
    '臺大專區':0.4755,
    '臺大公館校區':0.1432
}

low = []
for a in pd.unique(json_df["sarea"]):
    count = json_df["sarea"].value_counts()[a]
    density = count / area[a]
    low.append({'行政區': a, '站點/平方公里': density})

temp3 = pd.DataFrame(low).sort_values(by="站點/平方公里", ascending=True)
temp3.head(1)

"""#作業4"""

from IPython.core.display import clear_output
import ipywidgets as widgets

# 建立下拉式選單選項
AREALIST=list(pd.unique(json_df["sarea"]))
options = AREALIST
# 建立下拉式選單
dropdown = widgets.Dropdown(
    options=options,
    value=options[0],  # 預設選擇第一個選項
    description='下拉式選單：'
)
# 定義下拉式選單選取後的動作
def on_dropdown_change(change):
    Sna=change['new']
    #print(Sna)
    df = json_df[json_df['sarea'] == Sna][['sbi','sna']].sort_values('sbi').tail(10)
    clear_output()

    # 繪製直方圖
    sna = df['sna']
    sbi = df['sbi']
    plt.bar(sna, sbi)
    # 設定圖表標題與軸標籤
    plt.title('YouBike2.0 站點與車輛數量')
    plt.xlabel('站點名稱')
    plt.ylabel('車輛數量')
    # 設定x軸文字旋轉角度
    plt.xticks(rotation=90)
    # 顯示圖表

    display(dropdown)
    display(df)
    plt.show()

# 將下拉式選單的動作綁定到 on_dropdown_change 函式上
dropdown.observe(on_dropdown_change, names='value')
# 顯示下拉式選單
display(dropdown)
#display(df )

"""#作業5

"""

temp3.head(20)
LOWLIST=temp3.values.tolist()
LOWLIST

from IPython.display import HTML

pi='''<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['地區', '站點/平方公里'],
         ['北投區', 1.4255142410632577],
 ['士林區', 1.827854579737751],
 ['文山區', 2.538957123361579],
 ['南港區', 3.9830787825513676],
 ['內湖區', 4.845037952797297],
 ['臺大公館校區', 6.983240223463687],
 ['萬華區', 7.681706242515985],
 ['信義區', 8.387091017782417],
 ['松山區', 8.398113654471457],
 ['中山區', 10.013082786999071],
 ['大同區', 10.208571680014082],
 ['大安區', 14.346823454855915],
 ['中正區', 14.854543781467314],
 ['臺大專區', 109.35856992639327]
       ]);

        var options = {
          title: '地區, 站點/平方公里'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart" style="width: 1200px; height: 600px;"></div>
  </body>
</html>'''
HTML(pi)
