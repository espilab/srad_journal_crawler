# 
#  srad_journal_crawler.py
#    getting srad.jp journal content
#    2024-2-8 by espy (3615)
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

def get_content_omitjs(url):
  content = get_content(url)
  content = content.replace('<script', '<!-- <script')
  content = content.replace('</script>', '</script> -->')
  return content

def get_and_save(url, fname, omitjs):
  if omitjs:
    content = get_content_omitjs(url)
  else:
    content = get_content(url)
  # print(response.text)
  with open(fname, "w+", encoding='utf-8') as f:
    f.write(content)
  return content


#------ main

url_head_1 = 'https://srad.jp/~'
url_tail_1 = '/journal'

url_getidx_0   = 'https://srad.jp/search.pl?op=journals&uid={}'
url_getidx_head ='https://srad.jp/search.pl?threshold=-1&op=journals&sort=1&uid={}&start='
url_jnl_head = 'https://srad.jp/~{}/journal/'

if (len(sys.argv) != 2):
  print('usage: ', sys.argv[0], '  <handle>', sep="")
  print('  Notice: handle name is case-sencitive.')
  exit(1)

handle_name = sys.argv[1] 
url = url_head_1 + handle_name + url_tail_1

print('user: ', handle_name, ' の情報取得中...', sep="")
content = get_content(url)

#print(content)  ##DEBUG

pattern = r"{} \((\d+)\)".format(handle_name)
#print('pattern = ', pattern)   #DEBUG

id_int = -1

# ハンドルネームから IDを得る
for a_line in content.split("\n"):
  #print('LINE=', a_line)   #DEBUG
  #if a_line.find(handle_name) > 0:
  #  print('@@@@=',a_line)
  match = re.search(pattern, a_line)
  if match:
    #print('##### match => ', a_line)  #DEBUG
    id = match.group(1)
    #print('id=', id)  #DEBUG
    id_int = int(id)
    

if id_int < 0:
  print('Error:  user ', handle_name, ' not found.', sep="")

print(handle_name, ' さんの ID は、', id, 'です。', sep="")
url_getidx_0   = url_getidx_0.format(id)
url_getidx_head = url_getidx_head.format(id)
url_jnl_head = url_jnl_head.format(handle_name)

save_folder = id + '_' + handle_name

print('フォルダ: ', save_folder, 'を作成します', sep="")
if not os.path.exists(save_folder):
    os.mkdir(save_folder)
else:
    print('フォルダ: ', save_folder, 'は既に存在します', sep="")


#print(url_getidx_0)     #DEBUG
#print(url_getidx_head)     #DEBUG

save_file_path = save_folder + '/' + 'idx_' + id + '-0.html'
print('joural の index (start=0)を取得中')
get_and_save(url_getidx_0, save_file_path, True)

# ----- get index of journals
jnl_no_list = []
num = 10
fetch_flag = True
while fetch_flag:   #DEBUG  and (num <= 50):
  print('journal index (start={})を取得中'.format(num))
  url = url_getidx_head + str(num)
  save_file_path = save_folder + '/' + 'idx_' + id + '-' + str(num) + '.html'
  content = get_and_save(url, save_file_path, True)
  # pick up the id_number of each journal
  pattern = r"{}/journal/(\d+)".format(handle_name)
  for a_line in (content.split("\n")):
    match = re.search(pattern, a_line)
    if match:
      jnl_id = match.group(1)
      #print(jnl_id)   #DEBUG
      jnl_no_list.append(jnl_id)

  if '次の 10 件の' in content:
    num += 10
    # time.sleep(1)
  else:
    print('最後の index を取得しました。')
    fetch_flag = False

# print(jnl_no_list)    #DEBUG
print(handle_name, ' さんの日記エントリは ', len(jnl_no_list), ' 件でした。', sep="")

# number list output to file
fname = save_folder + '/jnl_no_list.txt'  
jnl_no_list.reverse()
with open(fname, "w+", encoding='utf-8') as f:
  for item in jnl_no_list:
    f.write(item + '\n')

# ----- get each journal
n = 0
for j_no in jnl_no_list:
  url_jnl = url_jnl_head + j_no
  n += 1
  print('(', n, ') ', url_jnl, ' を取得中', sep="")
  save_file_path = save_folder + '/' + 'jnl_' + id + '-' + j_no + '.html'
  content = get_and_save(url_jnl, save_file_path, True)
  time.sleep(1)

print('完了しました。')