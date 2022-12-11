import pandas
from tqdm import tqdm


# 取出需要标注的异常数据的id值
data_id=pandas.read_csv("..\\data\\A03-error_data0.csv",encoding='ANSI',usecols=['item_id'])
print('ID read successfully!')
# print(data_id.values)

# 读取总数据信息
data_list=pandas.read_csv("..\\data\\data_202109.tsv",sep='\t',encoding='ANSI')
print('data_list read successfully!')
# print(data_list)

data_error=pandas.DataFrame(columns=data_list.columns)
data_error.set_index('ITEM_ID')

data_len=data_list.shape[0]

for i in tqdm(range(data_len)):
    if data_list.loc[i]['ITEM_ID'] in data_id.values:
        data=data_list.loc[i].to_frame().T
        data_error=pandas.concat([data_error,data])
        print(data_list.loc[i]['ITEM_ID'],'succeed!')

print(data_error)
data_error.to_csv("..\\data\\error_data.csv",index=True,header=False)
