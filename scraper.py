import requests
from bs4 import BeautifulSoup

# URL alvo
url = 'https://www.rpgsite.net/feature/9602-persona-5-royal-exam-answers-class-test-solutions'

# Fazendo a requisição
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    titulo = soup.title.string
    print("Título da página:", titulo)
else:
    print("puErro ao acessar a página:", response.status_code)
