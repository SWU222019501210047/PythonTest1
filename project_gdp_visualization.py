#coding:gbk
"""
综合项目:世行历史数据基本分类及其可视化
作者：杨磊
日期：2020年6月5日

"""

import csv
import math
import pygal
import pygal_maps_world 

def read_csv_as_nested_dict(filename, keyfield, separator, quote): 
	result={}
	with open(filename,'rt',newline="")as csvfile:
		csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
		for row in csvreader:
			rowid=row[keyfield]
			result[rowid]=row
	return result
def reconcile_countries_by_name(plot_countries, gdp_countries):
	dict1={}
	set1=set()
	tuple1=(dict1,set1)
	for keys1 in plot_countries.keys():
		for values in gdp_countries.values():
			if plot_countries[keys1]==values['Country Name']:
				for year in range(1960,2016):
					if values[str(year)]!="":
						dict1[keys1]=values
	for keys2 in plot_countries.keys():
		if keys2 not in dict1:
			set1.add(keys2)				
	return tuple1
def build_map_dict_by_name(gdpinfo, plot_countries, year):
	set1=set()
	set2=set()
	set3=set()
	dict1={}
	tuple1=reconcile_countries_by_name(plot_countries,read_csv_as_nested_dict("isp_gdp.csv","Country Code",",",'"'))
	f=open(gdpinfo['gdpfile'],'rt')
	readers=csv.DictReader(f,delimiter=gdpinfo["separator"],quotechar=gdpinfo["quote"])
	for item in readers:
		for keys in plot_countries:
			countryname=plot_countries[keys]
			if countryname==item[gdpinfo['country_name']] and item[year]!='':
				dict1[keys]=math.log10(eval(item[year]))
			elif countryname==item[gdpinfo['country_name']] and item[year]!="":
				set2.add(keys)
	set1=tuple1[1]
	set3=set2-set1
	tuple2=(dict1,set1,set3)
	return tuple2			
def render_world_map(gdpinfo, plot_countries, year, map_file):
	worldmap_chart=pygal.maps.world.World()
	worldmap_chart.title="{}年全球GDP分布图".format(year)			
	worldmap_chart.add(year,build_map_dict_by_name(gdpinfo, plot_countries, year)[0])
	worldmap_chart.add('Not find in the world bank',build_map_dict_by_name(gdpinfo, plot_countries, year)[1])
	worldmap_chart.add('no data this year',build_map_dict_by_name(gdpinfo, plot_countries, year)[2])
	worldmap_chart.render_to_file(map_file)
	
def test_render_world_map(year):  #测试函数
    """
    对各功能函数进行测试
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } #定义数据字典
  
   
    pygal_countries = pygal.maps.world.COUNTRIES   # 获得绘图库pygal国家代码字典

    # 测试时可以1970年为例，对函数继续测试，将运行结果与提供的svg进行对比，其它年份可将文件重新命名
    render_world_map(gdpinfo, pygal_countries, year, "isp_gdp_world_name_{}.svg".format(year))
    print('文件已生成')
    
print("欢迎使用世行GDP数据可视化查询")
print("----------------------")
year=input("请输入需查询的具体年份:")
test_render_world_map(year)

	

		
		
		
		
		
			
				

 		
		
