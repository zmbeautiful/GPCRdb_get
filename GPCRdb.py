import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
from Bio.PDB import *

# 传入URL，相当于用鼠标点进了这个网页
r = requests.get('https://gpcrdb.org/interaction/')

# 解析URL
soup = BeautifulSoup(r.text, 'html.parser')
content_list = soup.find_all('ul', 'dropdown-menu structure_select')

# print(content_list)
pdb_list = []


for content in content_list:
    li_tags = content.find_all('li')
    data = [li_tag.text.split()[0] for li_tag in li_tags]
    pdb_list += data
    # print(content.h3.a.text)

pdbl = PDBList()
for pdbid in pdb_list:
    pdbl.retrieve_pdb_file(pdbid, pdir='./pdbdata/', file_format='pdb')
