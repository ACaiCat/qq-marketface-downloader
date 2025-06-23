import os
import sys
import requests
from tqdm import tqdm
from urllib.parse import urlparse, parse_qs


def download(id):
    widthURI = f"https://gxh.vip.qq.com/club/item/parcel/{str(id)[-1:]}/{id}_android.json"
    data = requests.get(widthURI).json()
    height = data["supportSize"][0]["Height"]
    width = data["supportSize"][0]["Width"]
    print("表情尺寸：{}x{}".format(width, height))
    type = data["type"]
    cnt = data["imgs"].__len__()
    print("表情数量：{}".format(cnt))
    if not os.path.exists(os.getcwd() + "/downloads"):
        os.mkdir(os.getcwd() + "/downloads")
    os.chdir(os.getcwd() + "/downloads")
    if not os.path.exists("[{}] {}".format(id, data["name"])):
        os.mkdir("[{}] {}".format(id, data["name"]))
    os.chdir("[{}] {}".format(id, data["name"]))
    plist = tqdm(data["imgs"])
    for i in plist:
        imgURI = (f"https://gxh.vip.qq.com/club/item/parcel/item/{i["id"][0:2]}/{i["id"]}/raw{height}.gif")
        img = requests.get(imgURI)
        
        if (len(img.content) != 0):
            with open(f"{i["name"]}.gif", "wb") as f:
                f.write(img.content)
        else:
            imgURI = (f'https://gxh.vip.qq.com/club/item/parcel/item/{i["id"][0:2]}/{i["id"]}/{height}x{width}.png')
            img = requests.get(imgURI)
            with open(f"{i["name"]}.png", "wb") as f:
                f.write(img.content)
            
                
    print(f"下载完成！保存路径：{os.getcwd()}")


def check(id):
    infodataURI = f"https://gxh.vip.qq.com/qqshow/admindata/comdata/vipEmoji_item_{id}/xydata.json"
    try:
        infodataRAW = requests.get(infodataURI)
        infodata = infodataRAW.json()["data"]
    except Exception as e:
        print("请求错误！" + str(e))
        print(infodataRAW.status_code)
        sys.exit()
    print(f"[{id}] { infodata["baseInfo"][0]["name"]} - {infodata["baseInfo"][0]["desc"]}")
    print(f"{infodata["baseInfo"][0]["tag"][0]}")
    download(id)


if __name__ == "__main__":
    arg = input("请输入表情ID或表情链接：")

    if arg.isdigit():
        id = arg
    else:
        parsed_url = urlparse(arg)
        query_params = parse_qs(parsed_url.query)
        id = query_params.get('id', [None])[0]

    if id is None:
        print(f"无效链接，请使用表情详细页链接")
        sys.exit()
    
    
    check(id)
