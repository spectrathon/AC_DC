from youtubesearchpython import VideosSearch


def yt_recommend():
    videosSearch = VideosSearch('Permutations', limit=5)

    results = videosSearch.result()

    video_url = [{'url':video['link'],'title':video['title']} for video in results['result']]
    return(video_url)