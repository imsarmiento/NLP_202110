import multiprocessing as mp
import numpy as np
from time import sleep
import requests
import datetime
import re
import os
import time
import json

url = 'https://core.ac.uk:443/api-v2/search'
apiKey = 'Oavohb17gNZT02xLJD6iU8GrfyMCeKAk'
path = f'{url}?apiKey={apiKey}'
print('Path', path)


filename = 'rawdata2.json'
working_dir = os.getcwd()
fn = os.path.join(working_dir, "datasets", filename)
print(fn)

def processQueryResult(results):
    dateReg = r'\d\d\d\d-\d?\d-\d?\d'
    all_results = []

    for queryResult in results:
        authors = queryResult['_source']['authors']
        iduk = queryResult['_source']['id']
        title = queryResult['_source']['title']
        description = queryResult['_source']['description']
        text =  queryResult['_source']['fullText']
        paperType = queryResult["_type"]
        print('description:', description)
        if description is not None:
            text = description
        all_results.append({
            "id": iduk,
            "source": f'ukcore/{paperType}',
            "author": authors,
            "title": title,
            "text": text
        })
    return json.dumps(all_results, indent=2)


def getQuery(query, startPage: int, endPage: int, pageSize: int, nroProcesses: int):
    while startPage < endPage:
        body = [
            {
                "query": query,
                "page": startPage,
                "pageSize": pageSize,
            }
        ] 
        r = requests.post(path, json=body)
        final_json = processQueryResult(r[0]["data"])
        startPage += nroProcesses


def worker(page, q):
    basic_queries = [
    {
        "query": "coronavirus",
        "page": page+1,
        "pageSize": 100,
    }]
    r = requests.post(path, json=basic_queries)
    print('data', r.json())
    if (r.json() is not None and
     r.json()[0] is not None and 
     r.json()[0]['data'] is not None):
        result = processQueryResult(r.json()[0]['data'])
        q.put(result)
        return result


def listener(q):
    '''listens for messages on the q, writes to file. '''

    with open(fn, 'w') as f:
        f.write('[' + '\n')
        while 1:
            m = q.get()
            if m == 'kill':
                break
            f.write(str(m).lstrip("[").rstrip("]") + ',\n')
            f.flush()
        f.write(']' + '\n')


def main():
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(mp.cpu_count() + 2)

    #put listener to work first
    watcher = pool.apply_async(listener, (q,))

    #fire off workers
    jobs = []
    for i in range(100, 102):
        job = pool.apply_async(worker, (i, q))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs: 
        job.get()

    #now we are done, kill the listener
    q.put('kill')
    pool.close()
    pool.join()


if __name__ == "__main__":
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    main()
