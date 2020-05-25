import requests
import json
from selenium import webdriver
def abrirNavegador():
    driver = webdriver.Chrome()
    pages = 1
    hasPage = 0
    while(hasPage == 0):
        animes = capturarAnimes(pages)
        print("========================")
        print("Animes Capturados da Api")
        print("========================")
        if(animes != []):
           animes = json.loads(animes)
           for anime in animes:
               driver.get(anime['link'])
               imgClass = driver.find_element_by_id("capaAnime")
               capaAnime = imgClass.find_element_by_tag_name('img').get_attribute('src')
               print("Capturando dados do Anime: "+anime['title']['rendered'])
               sobre = driver.find_element_by_class_name("boxAnimeSobre")
               infos = sobre.find_elements_by_class_name('boxAnimeSobreLinha')
               for info in infos:
                   info = info.text.split(':')
                   if(info[0] == "Formato"):
                        formato = info[1]
                   if(info[0] == "Gênero"):
                        genero = info[1]
                   if (info[0] == "Tipo de Episódio"):
                       tipo_ep = info[1]
                   if (info[0] == "Status do Anime"):
                       status_anime = info[1]
                   if (info[0] == "Ano de Lançamento"):
                       ano_lancamento = info[1]
               slug = anime['slug']
               titulo = anime['title']['rendered']
               link_original = anime['link']
               sinopse = driver.find_element_by_class_name('sinopse').text

               dataAnime = {"id": anime['id'], "nome" :titulo, "slug": slug,"link":link_original,"image_dafault":capaAnime,'formato':formato, 'genero': genero, 'tipo_ep':tipo_ep , 'status_anime':status_anime, 'ano_lancamento': ano_lancamento, "sinopse": sinopse }
               print(dataAnime)
               responseAnime = sendAnime(dataAnime)
               if (responseAnime == 200):
                   print("Anime enviado com sucesso")
                   print("========================")

               divEpisodios = driver.find_element_by_id('listadeepisodios')
               episodios = divEpisodios.find_elements_by_tag_name('a')
               for episodio in episodios:
                   urlEp = episodio.get_attribute('href')
                   driver.execute_script("window.open('"+urlEp+"', '_blank')")
                   driver.switch_to.window(driver.window_handles[1])
                   episodioTitle = driver.find_element_by_class_name('PostsSectionTitulo').text
                   videoUrl = driver.find_element_by_tag_name('source').get_attribute('src')
                   idEpisode = driver.current_url.split('/')
                   print(idEpisode)
                   dataEpisode = {'id':idEpisode[3],'anime_id': anime['id'],'title' : episodioTitle, 'url' : videoUrl}
                   responseEpisode = sendEpisode(dataEpisode)
                   if(responseEpisode == 200):
                       print("Episodio enviado com sucesso")
                       print("========================")
                   driver.close()
                   driver.switch_to.window(driver.window_handles[0])
        else:
            hasPage = 1
        pages += 1


def capturarAnimes(page):
    response  = requests.get("https://www.animesorion.tube/wp-json/wp/v2/posts?categories=780&page=1")
    return response.text
def sendAnime(data):
    response = requests.post('http://localhost:8000/api/v1/cadastrar/anime', data=data)
    return response.status_code

def sendEpisode(data):
    response = requests.post('http://localhost:8000/api/v1/cadastrar/episode/anime', data=data)
    print(response.text)
    return response.status_code
abrirNavegador()

