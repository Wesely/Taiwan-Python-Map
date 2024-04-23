import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns

# init visual style
sns.set(style='whitegrid', palette='pastel', color_codes=True)
sns.mpl.rc('figure', figsize=(10,6))

# import shapefile
shp_path = './mapdata202104280245/TOWN_MOI_1100415.shp'
sf = shp.Reader(shp_path)
sf.shapeRecords

'''
    TOWNID  TOWNCODE COUNTYNAME TOWNNAME            TOWNENG COUNTYID COUNTYCODE                                             coords
68     N18  10007160        彰化縣      永靖鄉  Yongjing Township        N      10007  [(120.57537662200002, 23.93329744600004), (120...
267    I02  10020020        嘉義市       西區      West District        I      10020  [(120.45173459900002, 23.46256943800006), (120...
30     G11  10002110        宜蘭縣      大同鄉    Datong Township        G      10002  [(121.58703876900006, 24.72011115300006), (121...
207    F33  65000040        新北市      永和區    Yonghe District        F      65000  [(121.5123947940001, 25.021745959000043), (121...
28     G08  10002080        宜蘭縣      冬山鄉  Dongshan Township        G      10002  [(121.75112031700007, 24.693860188000087), (12...
'''

# Plotting a complete map
def plot_map(sf, x_lim = None, y_lim = None, figsize = (9,7)):
    '''
    Plot map with lim coordinates
    '''
    plt.figure(figsize = figsize)
    id=0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        
        if min(x) < 118 :
            print(id, shape)
            continue

        # split every cycles
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
        
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0-0.01, y0-0.004, shape.record[3], fontsize=6)
        
        id = id+1
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()


"""
選擇中文字型，另外開啟terminal執行：
$fc-list :lang=zh-tw

比方說我看到： 
/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3a9dbc8ddc8b85f43055a28fb5d551e905d43de2.asset/AssetData/LiHeiPro.ttf: LiHei Pro:style=Medium,中黑,Halbfett,Normaali,Moyen,Medio,ミディアム,중간체,Médio,Средний,Normal,中等,Media

我就在下面把字體設為 LiHei Pro 
"""
plt.rcParams['font.sans-serif'] = ['LiHei Pro']
plot_map(sf)