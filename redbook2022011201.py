# 爬取千瓜的接口
import requests
from flask import Flask

__all__ = {
    "get_token_user",
}

##################### 千瓜相关Begin  #######################


def get_token_user():
    '''
     获取用户的token
     目前先使用测试的token 后续优化
    '''
    user_token = "Hm_lvt_c6d9cdbaf0b464645ff2ee32a71ea1ae=1641955208; ASP.NET_SessionId=qoww2k4rilp33bppoua3ux1m; User=UserId=87412c3500555d06&Password=2fedbb2fe284c648a670431557ae8dff&ChildId=0; Hm_lpvt_c6d9cdbaf0b464645ff2ee32a71ea1ae=1641975407"
    return user_token


g_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Cookie": get_token_user()
}

g_xhs_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Cookie": "xhsTrackerId=ad65feac-1b9f-420f-c282-4068c1f82434; xhsTracker=url=noteDetail&searchengine=baidu; customerClientId=072754555480177; smidV2=202201061625174782003dd7b6beec15ce749a80e87b54008ad4cba532361d0; extra_exp_ids=commentshow_clt1,gif_clt1,ques_exp2; timestamp2=20220112260213bf67ea32a131a4ad20; timestamp2.sig=ZX4lJUSVZY5_GcQ9NfzRryRkBrLdIptSWWA8BxXRIEk"
}


##################### 千瓜相关End  #######################

#####################   测试调用 Begin ##########################


urllink = "https://www.xiaohongshu.com/discovery/item/61d81a24000000000102ed54"


def get_note_url(urlink):
    url = "http://api.qian-gua.com/Track/SearchNoteByUrl?url=" + urlink
    res = requests.get(url, headers=g_headers)
    res.encoding = 'utf-8'
    code = res.content
    html_doc = str(code, 'utf-8')
    return html_doc

# 用户主页信息


# test_url(res_url)
#####################    End   #################################


####################   Flask Begin #######################
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'HelloWorld'


@app.route('/base_info/<uid>')
def get_base_info(uid):
    link = "https://www.xiaohongshu.com/user/profile/" + uid
    res = requests.get(link, headers=g_xhs_headers)
    html_doc = str(res.content, 'utf-8')
    n_pos = html_doc.find('''"redId":"''')
    str_ = html_doc[n_pos:]
    h_pos = str_.find(",")
    red_id = str_[9:h_pos-1]
    print("red_id:" + red_id)
    api_qiangua = 'http://api.qian-gua.com/blogger/GetList'
    post_data = {
        "KeyWord": red_id,
        "SortType": 0,
        "pageIndex": 1,
        "pageSize": 10
    }
    resp = requests.post(api_qiangua, headers=g_headers,data=post_data)
    print(resp.content)
    return resp.content


@app.route('/note_info/<uuid>')
def get_note_info(uuid):
    red_link = "https://www.xiaohongshu.com/discovery/item/" + uuid
    result = get_note_url(red_link)
    return result

####################   Flask End #######################


####################   启动服务  #########################
if __name__ == '__main__':
    app.run('0.0.0.0', port=8001)
