#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re
import json
from fake_useragent import UserAgent
session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'}
# headers = {'User-Agent': UserAgent().random}
for i in range(501, 527):
    print(f'page: {i} !!!')
    url = 'http://ximiyouyue.com/article/{}.html'.format(i)
    html = session.get(url, )
    print(html.text)
    target_ids = re.findall('ximiyouyue\.com/file/(.*?)\"', html.text)
    print(target_ids)

    for target_id in target_ids:
        print(target_id)
        url = 'https://webapi.ctfile.com/getfile.php?path=file&passcode=&token=false&r=0.91554242380956&ref='
        # url = 'https://webapi.ctfile.com/getfile.php?path=file&f=24620621-430513963&passcode=&token=false&r=0.599447157449291&ref='
        params = {
            'f':target_id
        }
        headers1 = {'Host': 'webapi.ctfile.com', 'Connection': 'keep-alive',
                   'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                   'Accept': 'application/json, text/javascript, */*; q=0.01', 'sec-ch-ua-mobile': '?0',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
                   'Origin': 'http://xz.ximiyouyue.com', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Dest': 'empty', 'Referer': 'http://xz.ximiyouyue.com/file/24620621-430475005',
                   'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}

        html = session.get(url, params=params, headers=headers1)
        print(html)

        print('1111', html.text)
        url = 'https://webapi.ctfile.com/get_file_url.php?' \
              '&mb=0&app=0&acheck=1&verifycode=&rd=0.13362368683152948'
        uid = target_id.split('-')[0]
        fid = target_id.split('-')[1]
        file_chk = re.findall('file_chk\":\"(.*?)\"', html.text)[0]
        print("uid:%s fid:%s file_chk:%s"%(uid,fid, file_chk))
        params = {
            'uid':uid,
            'fid':fid,
            'folder_id':'0',
            'file_chk':file_chk
        }
        html = session.get(url, headers=headers, params=params, verify=False, )
        print(html.text)
        print(html)

        url = json.loads(html.text)['downurl']
        print('download_url:', url)
        html = session.get(url, )
        name = target_id
        print(html)
        if html.status_code == 200:
            with open(f'{name}.mp3', 'wb') as f:
                    f.write(html.content)
                    print(f'{name} save success')
                    f.close()
        else:
            raise ValueError(html)
