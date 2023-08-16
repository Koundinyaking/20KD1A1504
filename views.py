from django.http import JsonResponse
import requests
from concurrent.futures import ThreadPoolExecutor
import time

def get_numbers(request):

    start_time = time.time()
    
    urls = request.GET.getlist('url')
    
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                if data:
                    results.extend(data['numbers'])
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
     
    sorted_nums = sorted(set(results))
    
    response_time = time.time() - start_time
    
    return JsonResponse({'numbers': sorted_nums, 'response_time': response_time})
        
        
def fetch(url):
    try:
        response = requests.get(url, timeout=0.5)
        return response.json()
    except requests.exceptions.Timeout:
        print('Timeout for URL: ', url)
        return {}