import cloudscraper
import random,string,json,hashlib
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup
scraper = cloudscraper.create_scraper(disableCloudflareV1=True)

cookies = {
    'selected_language': 'Georgian',
    'dle_user_id': '285',
    'dle_password': '88d6db501926809b65666c8fc392290c',
    'dle_compl': '46',
    'dle_newpm': '0',
    'PHPSESSID': '91ntk8brmc2bit59g183p8o0qt',
}
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ka;q=0.8,ka-GE;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'selected_language=Georgian; dle_user_id=285; dle_password=3b8abf9447a7033dbd4ff8cbd2c4122e; dle_compl=46; dle_newpm=0; PHPSESSID=em732g4avsplnl2uaalcoasc7m',
    'origin': 'https://kinoebi.in',
    'priority': 'u=1, i',
    'referer': 'https://kinoebi.in/admin.php?mod=addnews&action=addnews',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def upload_cover(name,img):

    files = {
        'name': (None, name),
        'chunk': (None, '0'),
        'chunks': (None, '1'),
        'subaction': (None, 'upload'),
        'news_id': (None, '0'),
        'area': (None, 'xfieldsimage'),
        'author': (None, 'Nika'),
        'xfname': (None, 'cover'),
        'user_hash': (None, 'c94b13cddf53151453c5ea933889da8d254537e6'),
        'qqfile': (name, img, 'image/jpg'),
    }
    boundary = '----WebKitFormBoundary' \
            + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=files, boundary=boundary)

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ka;q=0.8,ka-GE;q=0.7',
        'content-type': m.content_type,
        # 'cookie': 'selected_language=Georgian; dle_user_id=285; dle_password=3b8abf9447a7033dbd4ff8cbd2c4122e; dle_compl=46; dle_newpm=0; PHPSESSID=em732g4avsplnl2uaalcoasc7m',
        'origin': 'https://kinoebi.in',
        'priority': 'u=1, i',
        'referer': 'https://kinoebi.in/admin.php?mod=addnews&action=addnews',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = scraper.post('https://kinoebi.in/engine/ajax/controller.php?mod=upload',cookies=cookies,headers=headers,data=m)
    try:
        return json.loads(response.text)['xfvalue']
    except Exception as e:
        print(e, response.text)
        

def upload_poster(name, img):

    files = {
        'name': (None, name),
        'chunk': (None, '0'),
        'chunks': (None, '1'),
        'subaction': (None, 'upload'),
        'news_id': (None, '0'),
        'area': (None, 'xfieldsimage'),
        'author': (None, 'Nika'),
        'xfname': (None, 'poster'),
        'user_hash': (None, 'c94b13cddf53151453c5ea933889da8d254537e6'),
        'qqfile': (name, img, 'image/jpg'),
    }
    boundary = '----WebKitFormBoundary' \
            + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=files, boundary=boundary)

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ka;q=0.8,ka-GE;q=0.7',
        'content-type': m.content_type,
        # 'cookie': 'selected_language=Georgian; dle_user_id=285; dle_password=3b8abf9447a7033dbd4ff8cbd2c4122e; dle_compl=46; dle_newpm=0; PHPSESSID=em732g4avsplnl2uaalcoasc7m',
        'origin': 'https://kinoebi.in',
        'priority': 'u=1, i',
        'referer': 'https://kinoebi.in/admin.php?mod=addnews&action=addnews',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = scraper.post('https://kinoebi.in/engine/ajax/controller.php?mod=upload',cookies=cookies,headers=headers,data=m)
    try:
        return json.loads(response.text)['xfvalue']
    except Exception as e:
        print(e, response.text)

def check_movie(name):
    params = {
        'mod': 'find_relates',
    }

    data = {
        'title': name,
        'user_hash': 'c94b13cddf53151453c5ea933889da8d254537e6',
    }

    response = scraper.post('https://kinoebi.in/engine/ajax/controller.php', params=params, cookies=cookies, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    for ahrefs in soup.find_all('a'):
        if ahrefs.text == name:
            print("ფილმი არსებობს")
            return True

def post(genre_arr,genre_id,desc,trailer_iframe,meta_search_querys,name_GEO,name_ENG,thumb,cover,imdb,year,director,actors,movie_href_ENG,movie,isseries = ''):
    if isseries != '':
        series = movie
        movie = ''
    else:
        isseries = ''
        series = '{ "url": "სერიის ლინკი", "title": "სერია 1" },\r\n{ "url": "სერიის ლინკი", "title": "სერია 2" },\r\n{ "url": "სერიის ლინკი", "title": "სერია 3" },\r\n{ "url": "სერიის ლინკი", "title": "სერია 4" },\r\n{ "url": "სერიის ლინკი", "title": "სერია 5" },\r\n{ "url": "სერიის ლინკი", "title": "სერია 6" }\r\n'
    params = {
        'mod': 'addnews',
        'action': 'addnews',
    }

    data = {
        'title': name_GEO,
        'newdate': '',
        'category[]': genre_arr,
        'category_custom_sort': genre_id,
        'short_story': '<p>'+desc+'</p>',
        'full_story': '<p>'+desc+'</p>',
        'xfield[title_ka]': name_GEO,
        'xfield[title_en]': name_ENG,
        'xfield[title_ru]': '',
        'xfield[georgian]': '1',
        'xfield[poster]': thumb,
        'xfield[cover]': cover,
        'xfield[imdb]': imdb,
        'xfield[year]': year,
        'xfield[country]': '',
        'xfield[duration]': '',
        'xfield[director]': director,
        'xfield[actors]': actors,
        'xfield[episodes]': '',
        'xfield[last_season]': '',
        'xfield[last_episode]': '',
        'xfield[player_mp4_movie]': '',
        'xfield[player_1_movie]': movie,
        'xfield[player_2_movie]': '',
        'xfield[player_3_movie]': '',
        'xfield[player_4_movie]': '',
        'xfield[player_5_movie]': '',
        'xfield[player_en_movie]': movie_href_ENG,
        'xfield[player_ru_movie]': '',
        'xfield[player_1_serial]': '',
        'xfield[player_2_serial]': '',
        'xfield[player_3_serial]': '',
        'xfield[player_serial]': '',
        'xfield[axali-fleieri-1]': isseries,
        'xfield[axali-fleieri]': series,
        'xfield[trailer]': trailer_iframe,
        'approve': '1',
        'allow_main': '1',
        'allow_rating': '1',
        'allow_comm': '1',
        'vote_title': '',
        'frage': '',
        'vote_body': '',
        'catalog_url': '',
        'alt_name': '',
        'related_ids': '',
        'tags': meta_search_querys,
        'expires': '',
        'expires_action': '0',
        'password': '',
        'meta_title': '',
        'descr': '',
        'keywords': '',
        'mod': 'addnews',
        'action': 'doaddnews',
        'duplicateprotection': hashlib.md5(str(name_GEO).encode('utf-8')),
        'user_hash': 'c94b13cddf53151453c5ea933889da8d254537e6',
    }

    response = scraper.post('https://kinoebi.in/admin.php', params=params, cookies=cookies, headers=headers, data=data)
