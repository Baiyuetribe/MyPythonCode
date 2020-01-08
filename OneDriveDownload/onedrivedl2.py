"""
-------------------------------------------------
   File Name：     OneDrive云盘目录批量下载 
   Description :  
   Author :       baiyuetribe
   date：          2019/01/07
-------------------------------------------------
   使用方法:    python onedrivedl.py 加上OneDrive云盘目录链接
   实际案例：   python onedrivedl.py https://cloud.baiyue.one/?/Books/
-------------------------------------------------
"""
import os
import requests
import re
import threading
import sys
import tqdm 
from urllib.request import urlopen


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

def get_urls(url):

    r = requests.get(url,headers=headers)
    #folder_name = re.findall(r'"...*?">(\w+.*?)</a>\n',r.text)[0]
    urls = re.findall(r'<a\shref=".*?"\starget.*?\n.*?\n.*?\n.*?\n',r.text)
  
    return urls
    
def save_file(url):

    title = re.findall(r'<span>(\w+.*?)</span>',url)[0]
    download_url = 'https://' + re.findall(r'(.*?)/',base_url)[2] + re.findall(r'<a\shref="(.*?)"\starget',url)[0]
    #print(title + '--->' + download_url)
    #保存数据
    # with open('OneDrive\\' + title,'wb') as f:
    #     f.write(requests.get(download_url,headers=headers).content)
    #存txt文档
    # with open('onedive.txt','a',encoding='utf8') as f:
    #     f.write(f'{title}   --->   {download_url}\n')
    
    # print(f'{title} 已保存成功')
    download_from_url(download_url,title)

def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm.tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    #return file_size    

def main(base_url):
    if not os.path.exists('OneDrive'):
        os.mkdir('OneDrive')     
    urls = get_urls(base_url)
    threads = []    #444创建进程列表

        
    for url in urls:
        t = threading.Thread(target=save_file,args=(url,))  #增加进程
        threads.append(t)        
    for t in threads:
        t.start()   #依次启动所有进程
        
    for t in threads:
        t.join()
        
    print('所有文件都已下载完毕')    

        
if __name__ == "__main__":
    base_url = sys.argv[1]    #填写要爬取的地址
    main(base_url)

    


    
