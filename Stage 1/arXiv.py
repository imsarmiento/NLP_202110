import requests
import json
from xml.dom import minidom


urls = ['http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=3000'
        'http://export.arxiv.org/api/query?search_query=all:covid&start=3000&max_results=3000',
        'http://export.arxiv.org/api/query?search_query=all:covid&start=6000&max_results=3000',
        'http://export.arxiv.org/api/query?search_query=all:covid&start=9000&max_results=3000']
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=4000&max_results=1000',
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=5000&max_results=1000',
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=6000&max_results=1000',
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=7000&max_results=1000',
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=8000&max_results=1000',
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=9000&max_results=1000',
        # 'http://export.arxiv.org/api/query?search_query=all:covid&start=10000&max_results=1000']



def load_urls(url):
    
    data = []
    response = requests.get(url)
    root = minidom.parseString(response._content)
    index = 0
    for entry in root.getElementsByTagName('entry'):
        my_dict = {}
        my_dict['id'] = index
        my_dict['internal_id'] = entry.getElementsByTagName('id')[0].firstChild.nodeValue.strip()
        my_dict['title'] = entry.getElementsByTagName('title')[0].firstChild.nodeValue.strip()
        my_dict['text'] = entry.getElementsByTagName('summary')[0].firstChild.nodeValue.strip()
        my_dict['publication_date'] = entry.getElementsByTagName('published')[0].firstChild.nodeValue.strip()
        my_dict['author'] = entry.getElementsByTagName('author')[0].getElementsByTagName('name')[0].firstChild.nodeValue.strip()
        my_dict['authors'] = []
        for author in entry.getElementsByTagName('author'):
            my_dict['authors'].append(author.getElementsByTagName('name')[0].firstChild.nodeValue.strip())
        data.append(my_dict)
        index+=1
    with open('arXiv.json', 'a') as json_file:
        json.dump(data, json_file)

load_urls(urls[0])

    

