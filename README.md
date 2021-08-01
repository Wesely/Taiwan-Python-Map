Python 台灣行政區地圖 (2021)

![image](https://user-images.githubusercontent.com/5109822/127766998-798e882a-9182-4152-a9b1-2f0711ea38bf.png)

以 python 讀取政府開放平台的 ShapeFile 地圖資訊。歡迎引用或是協作
  
另有縣市資訊、村里資訊與各種行政地圖資訊 例如：
- 直轄市、縣市界線(TWD97經緯度)
- 鄉鎮市區界線(TWD97經緯度) | 政府資料開放平臺: https://data.gov.tw/dataset/7441
- 村里界歷史圖資(TWD97經緯度)
- 比例尺十萬分之一參考索引圖框_TWD97經緯度

都是一樣選擇下載 SHP格式 的檔案，然後參照 `render_script.py` 的內容即可

對於 SHP格式 shapefile其他欄位的讀取，請參考 `unused_functions.py` 或是 References 內的網站
![image](https://user-images.githubusercontent.com/5109822/127767144-42a9af5c-8386-4abc-ab97-92b5b9d53f9a.png)


## Output
![image](https://user-images.githubusercontent.com/5109822/127766998-798e882a-9182-4152-a9b1-2f0711ea38bf.png)
![image](https://user-images.githubusercontent.com/5109822/127767050-660213fd-dae6-468b-ad06-3e6998d67197.png)


# Requirements 
```
pip install pyshp
pip install pandas
pip install seaborn
```
以及 numpy + matplotlib

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
更加詳細的定義可以參考第一個reference （實作參考 `not_used_functions.py`)
可以看到上述欄位含義如下
```
    TOWNID  TOWNCODE COUNTYNAME TOWNNAME            TOWNENG COUNTYID COUNTYCODE                                             coords
68     N18  10007160        彰化縣      永靖鄉  Yongjing Township        N      10007  [(120.57537662200002, 23.93329744600004), (120...
267    I02  10020020        嘉義市       西區      West District        I      10020  [(120.45173459900002, 23.46256943800006), (120...
30     G11  10002110        宜蘭縣      大同鄉    Datong Township        G      10002  [(121.58703876900006, 24.72011115300006), (121...
207    F33  65000040        新北市      永和區    Yonghe District        F      65000  [(121.5123947940001, 25.021745959000043), (121...
28     G08  10002080        宜蘭縣      冬山鄉  Dongshan Township        G      10002  [(121.75112031700007, 24.693860188000087), (12...

```

# Plot

畫圖的時候把 x,y 座標的 list 讀取出來，但會發現有很多奇妙的線。
![奇怪的線](https://user-images.githubusercontent.com/5109822/127766772-6c3bf7f6-86ab-42e2-839e-a19294389ef7.png)

放大
![放大 奇怪的線](https://user-images.githubusercontent.com/5109822/127766775-cbea6219-c6d2-46db-b2e8-8b61354e1629.png)

再放大
![放到最大 奇怪的線](https://user-images.githubusercontent.com/5109822/127766779-656931e2-707e-4e06-afb6-5a2cdf87fccf.png)
![澎湖連線](https://user-images.githubusercontent.com/5109822/127766783-f517c190-43d4-445e-91c0-e93654046e01.png)

會發現，其實原始資料並沒有把每一個countour獨立成一個list，於是每個行政區都一筆畫完成，導致島嶼之間有一條線。
所以程式碼中插入了這段：

```py
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
再調整一下字體位置，但由於字體目前放在「重心」的位置附近，有時候可能會導致文字出界。
例如行政區左側曲線使用了100個座標點而右側只用了10個的話，會導致座標嚴重偏左。
只好日後再來處理了。

![修正中文字體位置](https://user-images.githubusercontent.com/5109822/127766799-039d4fba-ad3a-4fbd-b0b7-4abbb3b3b04b.png)

