# 
#  make_journal_index.py
#     
#  

import requests
import sys
import datetime
import time
import os
import re

# Disable warning output
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)




def get_content(url):
  response = requests.get(url, verify=False)
  return response.text  

#------ main

url_head_1 = 'https://srad.jp/~'
url_tail_1 = '/journal'

url_getidx_0   = 'https://srad.jp/search.pl?op=journals&uid={}'
url_getidx_head ='https://srad.jp/search.pl?threshold=-1&op=journals&sort=1&uid={}&start='
url_jnl_head = 'https://srad.jp/~{}/journal/'

fname_index_local = 'index_local_{}.html'



#------------ main

if (len(sys.argv) != 3):
  print('usage: ', sys.argv[0], '  <handle> <id>', sep="")
  exit(1)

handle_name = sys.argv[1] 
url = url_head_1 + handle_name + url_tail_1

id = sys.argv[2]
id_int = int(id)
    

print(handle_name, ' さんの ID は、', id, 'です。', sep="")

save_folder = id + '_' + handle_name

if os.path.exists(save_folder):
    print('フォルダ: ', save_folder, ' を確認しました', sep="")
else:
    print('フォルダ: ', save_folder, ' が見つかりません。終了します。', sep="")
    exit(1)

fname_idx_list = save_folder + '/jnl_no_list.txt' 

if os.path.exists(fname_idx_list):
    print('ファイル: ', fname_idx_list, ' を確認しました', sep="")
else:
    print('ファイル: ', fname_idx_list, ' が見つかりません。終了します。', sep="")
    exit(1)




with open(fname_idx_list, "r" ) as f:
   content = f.read()

idx_num_all = content.splitlines()
#print(idx_num_all, '\n len=', len(idx_num_all)) #DEBUG

pattern1 = r"<title>(.*?)</title>"
pattern2 = r"<time(.*?)</time>"
pattern3 = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})"

num_date_title_list = []

# check date, title in each journal
n = 0
for jnl_num in idx_num_all:
  fname_jnl = save_folder + '/jnl_' + id + '-' + jnl_num + '.html'
  #print(fname_jnl)
  with open(fname_jnl, "r" , encoding='utf-8') as f:
    content = f.read()

  print('journal #', jnl_num, '------------------------------------------------------', sep="") 
  matches = re.findall(pattern1, content, re.DOTALL)  # re.DOTALLで改行も含めてマッチ  
  for match in matches:
    extracted_content = match.strip()
    #print(f"抽出された内容_1: {extracted_content}")
    if 'の日記' in extracted_content:
        ar = extracted_content.split(' | ')
        print('title=', ar[0], sep="")
        jnl_title = ar[0]
  matches = re.findall(pattern2, content, re.DOTALL)  # re.DOTALLで改行も含めてマッチ  
  for match in matches:
    extracted_content = match.strip()
    print(f"抽出された内容_2: {extracted_content}")
    if 'datetime' in extracted_content:
        match = re.search(pattern3, extracted_content)
        datetime_str = match.group(1)
        print('datetime_str=', datetime_str, sep="")   #DEBUG
        date_str, time_str = datetime_str.split("T")
        year, month, day = date_str.split("-")
        hour, minute = time_str.split(":")  
        print(f"年月日: {year}-{month}-{day}, 時分: {hour}:{minute}")
        date_rec = year + '-' + month + '-' + day + ' ' + hour + ':' + minute

  num_date_title_list.append([jnl_num, date_rec, jnl_title]) 
  #n += 1
  #if n > 15:
  #   break


print(num_date_title_list)

content_index_html = '<html>\n'
content_index_html += '<meta charset="utf-8">\n'
content_index_html += '<body>\n'
content_index_html += '<b>' + handle_name + 'の日記' + '</b><br>\n'

for item in num_date_title_list:
  jnl_num = item[0]
  date_rec = item[1]
  jnl_title = item[2]
  content_index_html += "#" + jnl_num + ' (' + date_rec + ') : '
  content_index_html += '<a href="jnl_' + id + '-' + jnl_num + '.html">' + jnl_title + '</a><br>\n' 

content_index_html += '</body>\n</html>'

fname_idx_local = save_folder + '/index_local.html'
with open(fname_idx_local, "w+", encoding='utf-8') as f:
    f.write(content_index_html)
