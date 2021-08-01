
# Requirements 
```
pip install pyshp
pip install pandas
pip install seaborn
```
(also, numpy + matplotlib)

# References
1. Mapping Geograph Data in Python
https://towardsdatascience.com/mapping-geograph-data-in-python-610a963d2d7f

2. Matplotlib安裝中文字體
https://pyecontech.com/2020/03/27/python_matplotlib_chinese/


______

由於政府提供的地圖檔案是 `.sfh` shapefile. 我們需要安裝 `pandas` 來讀取

```py
shp_path = './mapdata202104280245/TOWN_MOI_1100415.shp'
sf = shp.Reader(shp_path)
```

透過此段程式碼讀取 shapefile
點進 `shapefily.py` 原始碼可以看到定義:

```py
    def shapeRecord(self, i=0):
        """Returns a combination geometry and attribute record for the
        supplied record index."""
        i = self.__restrictIndex(i)
        return ShapeRecord(shape=self.shape(i), record=self.record(i))

    def shapeRecords(self):
        """Returns a list of combination geometry/attribute records for
        all records in a shapefile."""
        return ShapeRecords(self.iterShapeRecords())
```

表示 `shapfile` 內包含了 `shapeRecords`，總共 368 個 `shapeRecord` 代表了台灣 368 個鄉鎮
而 `shapeRecord` 內又包含了 `.shape()` 與 `.record`

`shapeRecord.shape`是我們要的經緯度座標
`shapeRecord.record` 則是如下格式 ：
```
>>> sf.shapeRecords()[0].record
Record #-1: ['V02', '10014020', '臺東縣', '成功鎮', 'Chenggong Township', 'V', '10014']
```

這就是我們畫地圖需要的全部資訊了。

那V是什麼意思？
更加詳細的定義可以參考第一個reference （實作參考 `not_used_functions.py`)
可以看到 
```
    TOWNID  TOWNCODE COUNTYNAME TOWNNAME            TOWNENG COUNTYID COUNTYCODE                                             coords
68     N18  10007160        彰化縣      永靖鄉  Yongjing Township        N      10007  [(120.57537662200002, 23.93329744600004), (120...
267    I02  10020020        嘉義市       西區      West District        I      10020  [(120.45173459900002, 23.46256943800006), (120...
30     G11  10002110        宜蘭縣      大同鄉    Datong Township        G      10002  [(121.58703876900006, 24.72011115300006), (121...
207    F33  65000040        新北市      永和區    Yonghe District        F      65000  [(121.5123947940001, 25.021745959000043), (121...
28     G08  10002080        宜蘭縣      冬山鄉  Dongshan Township        G      10002  [(121.75112031700007, 24.693860188000087), (12...

```

那是一個 countyCode ，不太確定用途。

# Plot

畫圖的時候把 x,y 座標的 list 讀取出來，但會發現有很多奇妙的線。
放大
再放大
會發現，其實原始資料並沒有把每一個countour獨立成一個list，會導致每個行政區都一筆畫完成。
所以程式碼中插入了這段

```
    points = list(zip(x,y))
    visited = set()
    xx = []
    yy = []
    for p in points :
        if p in visited :
            plt.plot(xx, yy, 'k')
            xx = []
            yy = []
        else :
            xx.append(p[0])
            yy.append(p[1])
            visited.add(p)
```
把原始的 x,y list 先存起來。遇到重複的點的時候也就是畫了一整圈的時候，才一次 plot 出來。
再調整一下字體位置，這樣就完成了。
