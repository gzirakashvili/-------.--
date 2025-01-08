import cloudscraper, json, time
from bs4 import BeautifulSoup
import functs.mainfunctions as mainfunctions
from io import BytesIO
from PIL import Image


scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
data_genres = {"1":"ფილმი","2":"ანიმაციური","3":"ბიოგრაფიული","4":"დეტექტივი","5":"დოკუმენტური","6":"დრამა","7":"ეროტიული","8":"ვესტერნი","9":"თრილერი","10":"ისტორიული","11":"კომედია","12":"კრიმინალური","13":"მელოდრამა","14":"მოკლემეტრაჟიანი","15":"მუსიკალური","16":"მძაფრ-სიუჟეტიანი","17":"საახალწლო","18":"საბავშვო","19":"სათავგადასავლო","20":"საომარი","21":"საოჯახო","22":"საშინელებათა","23":"სპორტული","24":"ფანტასტიკა","25":"ფენტეზი","26":"რომანტიკული","27":"მისტიკური","37":"დორამები","38":"ანიმე","39":"მალე ქართულად"}
for i in range(1, 301):
    print("გვერდი", str(i))
    content = scraper.get("https://mykadri.tv/filmebi_qartulad/page/"+str(i)+"/").text
    soup = BeautifulSoup(content, 'html.parser')
    container = soup.find('div', class_='row row-cols-3 row-cols-sm-4 row-cols-lg-6 gx-3 gy-5')
    for movie in container.find_all('div', class_='col'):
        try:
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
                movie_href_ENG = str(soup_inner.find_all('div', class_='player-container')[-1].find('iframe')['data-lazy']).strip()
            except Exception as e:
                movie_href_ENG = ''
                pass
            meta_search_querys = soup_inner.find('div', class_='movie__meta d-none d-lg-block').find_all('p')[-1].text
            movie_container = soup_inner.find('div', class_='player-container')
            thumb = str(soup_inner.find('img', id='player-poster')['src']).strip()
            movie_cover = soup_inner.find('meta', property='og:image')['content']
            js_QUERY = movie_container.find("script").text
            descr = soup_inner.find('p', class_='movie__meta-body m-0').text
            metas_texts = soup_inner.find_all('p', class_='movie__meta mb-1')
            ganre_id = "1"
            genre_arr = ['1']
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
            if ('movie: "' in js_QUERY):
                movie_href = str(js_QUERY.split('"')[1]).strip().replace('embed/', 'v/')
                try:
                    for g in genre_list.split(','):
                        for b in data_genres:
                            if (str(g).strip() == data_genres[b]):
                                ganre_id = ganre_id+'::'+b
                                genre_arr.append(b)
                    if mainfunctions.check_movie(name_GEO) != True:
                        movie_cover = mainfunctions.upload_cover(str(movie_cover).split('/')[-1],scraper.get(movie_cover).content)
                        thumb = mainfunctions.upload_cover(str(thumb).split('/')[-1],scraper.get(thumb).content)
                        if movie_href != '' and movie_href != None:
                            mainfunctions.post(genre_arr,ganre_id,descr,trailer_iframe,meta_search_querys,name_GEO,name_ENG,thumb,movie_cover,imdb,year,director,actors,movie_href_ENG,movie_href)
                except Exception as e:
                    print(e, name_GEO, str(i))
            else:
                print(href, "პლაგინი ვერ მოიძებნა")
        except Exception as e:
            print(e, "შეცდომა", str(i))
    time.sleep(30)