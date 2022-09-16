from math import radians, cos, sin, asin, sqrt
import pandas as pd
from database import engine


def haversine(lon1, lat1, lon2, lat2):
    '''
    function to calculate distance between two lat long coordinates
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles

    return c * r


def get_dataframe(address,long,lat,distance): 
    '''
    To filter out records which are come withing distance range of coordinates
    '''
    df = pd.read_sql_query(
    sql = address.statement,
    con = engine
    )
    
    current_lat_long=(long,lat)
    def row_hsign(row):
        return haversine(*current_lat_long,row['long'],row['lat'])

    df["distance"]=df.apply(row_hsign,axis=1)
    df=df.loc[df['distance'] <distance]
    address_ids = df["id"].tolist()
    return address_ids