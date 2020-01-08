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
    with open('OneDrive\\' + title,'wb') as f:
        f.write(requests.get(download_url,headers=headers).content)
    
    print(f'{title} 已保存成功')
    

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
    base_url = sys.argv[1]    
    main(base_url)
