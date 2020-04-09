from utils import broadcast, getNews, getNewsDetail

MESSAGE_TEMPLATE = \
'''宇高のホームページが更新されました。

{title}

{content}

記事のURLはこちらです。
{url}
'''


for n in getNews():
    # broadcast(MESSAGE_TEMPLATE.format(
    #     **n,
    #     content=getNewsDetail(n["url"])
    # ))
    pass
