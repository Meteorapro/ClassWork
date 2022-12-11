import pandas
from tqdm import tqdm


# 标签初始化
abnormal_error=[]

# 取出需要标注的异常数据的id值
data_error=pandas.read_csv("..\\data\\A03-error_data0.csv",encoding='ANSI',usecols=['item_id','item_price','item_sales_volume','item_sales_amount','user_id'])
print('ID read successfully!')
# 更改异常数据的标签，使之与总数据匹配
data_error.rename(columns={'item_id':'ITEM_ID','item_price':'ITEM_PRICE','item_sales_volume':'ITEM_SALES_VOLUME','item_sales_amount':'ITEM_SALES_AMOUNT','user_id':'USER_ID'},inplace=True)
# print(data_error)

# 记录异常数据的标签
for i in range(data_error.shape[0]):
    abnormal_error.append(1)

# 将标签数据和原数据进行合并
data_error=pandas.concat([data_error,pandas.DataFrame({'abnormal':abnormal_error})],axis=1)

# 读取总数据信息
data_list=pandas.read_csv("..\\data\\data_202109.tsv",sep='\t',encoding='ANSI',usecols=['ITEM_ID','ITEM_PRICE','ITEM_SALES_VOLUME','ITEM_SALES_AMOUNT','USER_ID'])
print('data_list read successfully!')

abnormal=[]
# 获取正常数据的标签
k=1
for i in tqdm(range(200000)):
    # 如果ID不是异常数据的ID则认为是正常数据
    if data_list.loc[i]['ITEM_ID'] not in data_error['ITEM_ID'].values:
        abnormal.append(0)
        k+=1
    if k>100000:
        break

# 将标签数据和原数据进行合并
data_list=pandas.concat([data_list,pandas.DataFrame({'abnormal':abnormal})],axis=1)

# 将标签数据和原数据进行合并
data_total=pandas.concat([data_error,data_list[:100000]],ignore_index=True)
print(data_total)

data_total.to_csv("..\\data\\data_total.csv",encoding='ANSI')
