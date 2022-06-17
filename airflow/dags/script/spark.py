# import findspark
# findspark.init()

import pyspark
import pandas as pd
import argparse
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql import types
from pyspark.sql import SparkSession
from collections import defaultdict

# TODO local
# spark = SparkSession.builder \
#     .master("spark://172.30.240.1:7077") \
#     .appName('test') \
#     .getOrCreate()

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

parser = argparse.ArgumentParser(description='Spark preprocessing')

parser.add_argument('--input_path', required=True)
parser.add_argument('--output_path', required=True)

args = parser.parse_args()

input_path = args.input_path
output_path = args.output_path


schema = types.StructType([
types.StructField('index', types.StringType(), True),
types.StructField('_id', types.StringType(), True),
types.StructField('art_url', types.StringType(), True),
types.StructField('item_type', types.StringType(), True),
types.StructField('utc_date', types.StringType(), True),
types.StructField('country_code', types.StringType(), True),
types.StructField('track_album_slug_text', types.StringType(), True),
types.StructField('country', types.StringType(), True),
types.StructField('slug_type', types.StringType(), True),
types.StructField('amount_paid_fmt', types.StringType(), True),
types.StructField('item_price', types.FloatType(), True),
types.StructField('item_description', types.StringType(), True),
types.StructField('art_id', types.FloatType(), True),
types.StructField('url', types.StringType(), True),
types.StructField('amount_paid', types.FloatType(), True),
types.StructField('releases', types.StringType(), True),
types.StructField('artist_name', types.StringType(), True),
types.StructField('currency', types.StringType(), True),
types.StructField('album_title', types.StringType(), True),
types.StructField('amount_paid_usd', types.FloatType(), True),
types.StructField('package_image_id', types.FloatType(), True),
types.StructField('amount_over_fmt', types.StringType(), True),
types.StructField('item_slug', types.StringType(), True),
types.StructField('addl_count', types.StringType(), True),
])

df = spark.read \
        .option("header","true") \
        .schema(schema) \
        .csv(input_path)

# TODO some transformation
df = df \
    .drop(df.index) \
    .withColumn("unix_timestamp", F.concat_ws(".",F.from_unixtime(F.substring(col("utc_date"),0,10),"yyyy-MM-dd HH:mm:ss"),F.substring(col("utc_date"),-3,3)).cast(types.TimestampType()))

def filter_date(df):
    '''
    this function will cut dataframe by date. for each day!
    the code seem to be more python than spark since I'm still new to spark tho
    '''
    def get_datetime_str(df, opt=True):
        '''
        to get max/min of date-month-year from dataframe.
        probably not the best method but its work
        '''
        try:
            tmp_df = df.select(
                            F.year("unix_timestamp").alias('year'), 
                            F.month("unix_timestamp").alias('month'), 
                            F.dayofmonth("unix_timestamp").alias('day')
            )
            if opt:
                day, month, year = tmp_df.select([F.max("day")]).collect()[0].__getitem__('max(day)'), \
                                    tmp_df.select([F.max("month")]).collect()[0].__getitem__('max(month)'), \
                                    tmp_df.select([F.max("year")]).collect()[0].__getitem__('max(year)')
                print(f'Done collecting MAX, date:{day} month:{month} year:{year}')

            else:
                day, month, year = tmp_df.select([F.min("day")]).collect()[0].__getitem__('min(day)'), \
                                    tmp_df.select([F.min("month")]).collect()[0].__getitem__('min(month)'), \
                                    tmp_df.select([F.min("year")]).collect()[0].__getitem__('min(year)')
                print(f'Done collecting MIN, date:{day} month:{month} year:{year}')

        except Exception as e:
            print(f"Exception while trying to get max/min date-year-month - {e}")

        return {'day':f'{day}',
                'month':f'{month}',
                'year':f'{year}'}


    max, min = get_datetime_str(df, True), get_datetime_str(df, False)
    print(f'MAX/MIN variable collected... \nMAX: {max} \nMIN: {min}')
    days, months, year = [i+1 for i in range(30)], [9, 10], 2020 # set day-month-year, since this project only have 2 month of data we will make its easy
    result_df = defaultdict()
    
    try:
        for idx, month in enumerate(months):
            # print(f'Looping at month: {month}')
            for jdx, day in enumerate(days):
                # print(f'Looping at day: {day}')
                # print(f'DEBUG {min}, {max}')
                if day < int(min['day']) & month == int(min['month']):
                    print(f'{day}-{month} is lower than min date \nCONTINUE..')
                    continue
                elif day > int(max['day']) & month == int(max['month']):
                    print(f'{day}-{month} is greater than min date Finishing the process.. \nBREAK..')
                    break
                df_day_month = df.filter(F.col("unix_timestamp").between(f'{year}-{month}-{day} 00:00:00',f'{year}-{month}-{day} 23:59:59'))
                result_df[f'bandcamp_sale_{day:02d}_{month:02d}_{year}'] = df_day_month
    except Exception as e:
            print(f"Exception while trying to organize data from dataframe - {e}")
    
    return result_df

date_organize_dict = filter_date(df)

print(f'Start writing file..')
for df_name, df_value in date_organize_dict.items():
    df_value \
        .repartition(4) \
        .write.parquet(f'{output_path}/{df_name[17:19]}/{df_name[14:16]}', mode='overwrite') # saved to `data/month/day/*.parquet`