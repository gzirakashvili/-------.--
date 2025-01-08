import cloudscraper, json, time
from bs4 import BeautifulSoup
import functs.mainfunctions as mainfunctions

scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
#data_genres = {"1":"ფილმი","2":"ანიმაციური","3":"ბიოგრაფიული","4":"დეტექტივი","5":"დოკუმენტური","6":"დრამა","7":"ეროტიული","8":"ვესტერნი","9":"თრილერი","10":"ისტორიული","11":"კომედია","12":"კრიმინალური","13":"მელოდრამა","14":"მოკლემეტრაჟიანი","15":"მუსიკალური","16":"მძაფრ-სიუჟეტიანი","17":"საახალწლო","18":"საბავშვო","19":"სათავგადასავლო","20":"საომარი","21":"საოჯახო","22":"საშინელებათა","23":"სპორტული","24":"ფანტასტიკა","25":"ფენტეზი","26":"რომანტიკული","27":"მისტიკური","28":"სერიალი","29":"თურქული სერიალები","30":"ინდური სერიალები","31":"უკრაინული სერიალები","32":"რუსული სერიალები","33":"ბრაზილიური სერიალები","34":"ესპანური სერიალები","35":"კოლუმბიური სერიალები","36":"იტალიური სერიალები","37":"დორამები","38":"ანიმე","39":"მალე ქართულად"}
data_genres = {"2":"ანიმაციური","3":"ბიოგრაფიული","4":"დეტექტივი","5":"დოკუმენტური","6":"დრამა","7":"ეროტიული","8":"ვესტერნი","9":"თრილერი","10":"ისტორიული","11":"კომედია","12":"კრიმინალური","13":"მელოდრამა","14":"მოკლემეტრაჟიანი","15":"მუსიკალური","16":"მძაფრ-სიუჟეტიანი","17":"საახალწლო","18":"საბავშვო","19":"სათავგადასავლო","20":"საომარი","21":"საოჯახო","22":"საშინელებათა","23":"სპორტული","24":"ფანტასტიკა","25":"ფენტეზი","26":"რომანტიკული","27":"მისტიკური","37":"დორამები","38":"ანიმე","39":"მალე ქართულად"}
for i in range(1, 14):
    print("გვერდი", str(i))
    content = scraper.get("https://mykadri.tv/serialebi_qartulad/page/"+str(i)+"/").text
    soup = BeautifulSoup(content, 'html.parser')
    container = soup.find('div', class_='row row-cols-3 row-cols-sm-4 row-cols-lg-6 gx-3 gy-5')
    for movie in container.find_all('div', class_='col'):
        name_GEO = str(movie.find('div', class_='post-title').find_all('div')[0].find('a')['title']).strip()
        name_ENG = str(movie.find('div', class_='post-title').find_all('div')[1].find('a')['title']).strip()
        href = str(movie.find('div', class_='post-title').find_all('div')[0].find('a')['href']).strip()
        movie_inner = scraper.get(href)
        soup_inner = BeautifulSoup(movie_inner.text, 'html.parser')
        try:
            trailer_iframe = soup_inner.find('div', class_='modal-body').find('iframe')['data-src']
        except Exception as e:
            trailer_iframe = ''
            pass
        try:
            movie_href_ENG = soup_inner.find_all('div', class_='player-container').find('iframe')['data-lazy']
        except Exception as e:
            movie_href_ENG = ''
            pass
        meta_search_querys = soup_inner.find('div', class_='movie__meta d-none d-lg-block').find_all('p')[-1].text
        movie_container = soup_inner.find('div', class_='player-container')
        thumb = str(soup_inner.find('img', id='player-poster')['src']).strip()
        movie_cover = soup_inner.find('meta', property='og:image')['content']
        try:
            js_QUERY = movie_container.find("script").text
            if "source: 'iframe'," not in js_QUERY or 'source: "iframe",' not in js_QUERY:
                js_QUERY = soup_inner.find_all('div', class_='player-container')[1].find("script").text
        except:
            pass
        descr = soup_inner.find('p', class_='movie__meta-body m-0').text
        metas_texts = soup_inner.find_all('p', class_='movie__meta mb-1')
        ganre_id = "28"
        genre_arr = ['28']
        for meta in metas_texts:
            if ('კატეგორია:' in meta.text):
                genre_list = str(meta.find('span', class_='movie__meta-body').text).strip()
            elif ('წელი:' in meta.text):
                year = str(meta.find('span', class_='movie__meta-body').text).strip()
            elif ('IMDB:' in meta.text):
                imdb = str(meta.find('span', class_='movie__meta-body').text).strip()
            elif ('მსახიობები:' in meta.text):
                actors = str(meta.find('span', class_='movie__meta-body').text).strip()
            elif ('რეჟისორი:' in meta.text):
                director = str(meta.find('span', class_='movie__meta-body').text).strip()
        try:
            for g in genre_list.split(','):
                for b in data_genres:
                    if (str(g).strip() == data_genres[b]):
                        ganre_id = ganre_id+'::'+b
                        genre_arr.append(b)
            series_data = ""
            if "1:[" in js_QUERY:
                movie_href = str(js_QUERY.split('{1')[1].split('}]}')[0]).strip()
            else:
                movie_href = str(js_QUERY.split('{"1"')[1].split('}]}')[0]).strip()
            if "label" not in movie_href:
                movie_href = json.loads('{"1"'+movie_href+"}]}")
                for series in movie_href:
                    series_data += "jifr.push(["+series+","+str(movie_href[series]).replace('[','').replace(']','').replace('embed/','v/').replace("'",'"')+"]);"
                first_series = str(movie_href['1'][0]['url']).replace('embed/','v/')
                try:
                    if mainfunctions.check_movie(name_GEO) != True:
                        movie_cover = mainfunctions.upload_cover(str(movie_cover).split('/')[-1],scraper.get(movie_cover).content)
                        thumb = mainfunctions.upload_cover(str(thumb).split('/')[-1],scraper.get(thumb).content)
                        for g in genre_list.split(','):
                            for b in data_genres:
                                if (str(g).strip() == str(data_genres[b]).strip()):
                                    ganre_id += '::'+b
                                    genre_arr.append(b)
                        mainfunctions.post(genre_arr,ganre_id,descr,trailer_iframe,meta_search_querys,name_GEO,name_ENG,thumb,movie_cover,imdb,year,director,actors,movie_href_ENG,series_data,first_series)
                except Exception as e:
                    print(e, name_GEO)
        except Exception as e:
            print(href, "პლაგინი ვერ მოიძებნა")
    time.sleep(30)