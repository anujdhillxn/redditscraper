def get_audio(url):
    f = 0
    for i in range(len(url)):
        if(url[i] == '_'):
            f = i
    return url[:f]+"_audio.mp4"