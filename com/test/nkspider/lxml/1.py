for i in range(0,10):
    url_str = "https://movie.douban.com/review/best/?start={}"
    print(url_str.format(str(i*10)))