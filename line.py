from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from mpl_toolkits import mplot3d
import numpy as np

def item_extract(filename,item_dict):
    with open(f"Lenta/{filename}", encoding='utf-8', mode="r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        div_all = soup.find_all("div","item")

        for item in div_all:
            item_name = item.find("table", "receipt-row-1").text.strip()
            item_name = list(map(str.strip,item_name.split(";")))
            item_count = item.find("table", "receipt-row-2").text.strip()
            item_count = list(map(str.strip,item_count.split("\n")))

            if item_name[0] in item_dict.keys():
                item_dict[item_name[0]][filename]=item_count[2]
            else:
                item_dict[item_name[0]] = {}
                item_dict[item_name[0]][filename]=item_count[2]
    return item_dict


def plot(item_dict):
    item_name = list(item_dict.keys())
    item_count = list(item_dict.values())
    item_count = [float(x) for x in item_count]
    #item_price = [x for x in r]
    plt.figure(figsize=(12, 4))
    plt.scatter(item_count, item_name, color='#ff0000', label="27.03.22")
    plt.grid()
    plt.subplots_adjust(left=0.33)
    plt.title("Динамика цен")
    plt.xlabel('Цена')
    plt.ylabel('Наименование')
    plt.savefig('plot.png',bbox_inches='tight')

    plt.legend()
    plt.show()


item_dict = {}
file_name = []
for filename in os.listdir("Lenta"):
    file_name.append(filename)
    item_dict = item_extract(filename, item_dict)
file_name_cut = [x[:5] for x in file_name]
print(file_name_cut)

# print(item_dict)

del_it = []
for _ in item_dict:
    if len(item_dict[_]) <= 2:
        del_it.append(_)
for _ in del_it:
    item_dict.pop(_)
print(item_dict)
item_name = list(item_dict.keys())
# item_count = list(item_dict.values())
# item_count = [float(x) for x in item_count]

# print(item_count)
#item_price = [x for x in r]
# plt.figure(figsize=(12, 4))
plt.figure(figsize=(12,8))
for y in item_name:
    item_count = []
    for _ in file_name:

        z = item_dict[y].get(_, False)
        if z:
            item_count.append(z)
        else:
            #item_count.append(np.nan)
            item_count.append(0)
    # plt.scatter(item_count, item_name, color='#ff0000', label=_)
    item_count = [float(x) for x in item_count]
    flag_start = False
    print(item_count)
    for _ in range(len(item_count)-1):
        if item_count[_] == 0 and not flag_start:
            item_count[_]=np.nan
        else:
            if item_count[_+1] == 0:
                item_count[_+1]=item_count[_]
            else:
                flag_start = False

    # print(len(file_name),"=", file_name)
    print(item_count)
    plt.plot(file_name_cut, item_count,  label=y)
    #plt.plot(file_name, item_name,  label=_)

plt.grid()

plt.subplots_adjust(left=0.055)
plt.title("Динамика цен")
plt.xlabel('Цена')
plt.ylabel('Наименование')
plt.savefig('plot.png',bbox_inches='tight')
plt.legend()
plt.show()

