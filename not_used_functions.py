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

# Check
print(len(sf.shapes())) # >> 368 (Taiwan's TWON counts)
print(sf.records()[1]) # >> Record #1: ['T21', '10013210', '屏東縣', '佳冬鄉', 'Jiadong Township', 'T', '10013']

# Convert to Panda.DataFrame
def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords' 
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

df = read_shapefile(sf)
df.shape

# Check
print(df.sample(5))
'''
    TOWNID  TOWNCODE COUNTYNAME TOWNNAME            TOWNENG COUNTYID COUNTYCODE                                             coords
68     N18  10007160        彰化縣      永靖鄉  Yongjing Township        N      10007  [(120.57537662200002, 23.93329744600004), (120...
267    I02  10020020        嘉義市       西區      West District        I      10020  [(120.45173459900002, 23.46256943800006), (120...
30     G11  10002110        宜蘭縣      大同鄉    Datong Township        G      10002  [(121.58703876900006, 24.72011115300006), (121...
207    F33  65000040        新北市      永和區    Yonghe District        F      65000  [(121.5123947940001, 25.021745959000043), (121...
28     G08  10002080        宜蘭縣      冬山鄉  Dongshan Township        G      10002  [(121.75112031700007, 24.693860188000087), (12...
'''

def plot_shape(id, s=None):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    return x0, y0

print('1.\n',df.TOWNENG)
town = u'Jiadong Township'
print('\n\n2.\n',df[df.TOWNENG == town].index[0])
com_id = df[df.TOWNENG == town].index[0]
plot_shape(com_id, town)