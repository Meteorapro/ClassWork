import pandas
from tqdm import tqdm

data_list=pandas.read_csv("..\\data\\data_total.csv",encoding='ANSI',usecols=['ITEM_ID', 'ITEM_PRICE', 'ITEM_SALES_VOLUME', 'ITEM_SALES_AMOUNT', 'USER_ID'])

data_trains = pandas.DataFrame(columns=['ITEM_ID', 'ITEM_PRICE', 'ITEM_SALES_VOLUME', 'ITEM_SALES_AMOUNT', 'USER_ID'])
data_tests = pandas.DataFrame(columns=['ITEM_ID', 'ITEM_PRICE', 'ITEM_SALES_VOLUME', 'ITEM_SALES_AMOUNT', 'USER_ID'])


for i in tqdm(range(data_list.shape[0])):
    data = data_list.loc[i].to_frame().T
    if i % 9 == 0 or i % 10 == 0:
        data_tests = pandas.concat([data_tests, data])
    else:
        data_trains = pandas.concat([data_trains, data])

# print(data_trains)
# print(data_tests)

data_trains.to_csv("..\\MatlabCode\\trains.csv",header=False,index=False,encoding='ANSI')
data_tests.to_csv("..\\MatlabCode\\tests.csv",header=False,index=False,encoding='ANSI')