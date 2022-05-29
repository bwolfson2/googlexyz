from django.shortcuts import render

from bs4 import BeautifulSoup 
import requests 
import os
if os.environ.get("ENVIRONMENT","") != "light":
    from engine.scrapers import sample_scraper
    from engine.processors.combined_processors import get_clustered_results, get_result_dicts
import sys
import json
print(sys.path)



def query(request):
    print("requesting home")
    return render(request, 'engine/home.html')
    

def results(request):
    if request.method == "POST":
        query = request.POST.get('search')
        if query == "":
            return render(request, 'engine/home.html')
        else:
            result_cache = os.environ.get("CACHE_RESULTS_DIR","")
            result_filename = f"CACHE_RESULTS_DIR/{query}.json"
            if os.path.exists(result_filename):
                with open(result_filename, "r") as f:
                    results = json.loads(f.read())
                    return render(request, 'engine/results.html', {"query":query,"results": results})
            results = sample_scraper.lycos_search(query)
            ordered_results = get_clustered_results(results)
            result_dicts = get_result_dicts(ordered_results)
            with open(result_filename, "w") as f:
                json.dump(result_dicts, f)
            context = {
                'query':query,
                'results':result_dicts
            }
            return render(request, 'engine/results.html', context)
    else:
        return render(request, 'engine/results.html')


def about(request):
    return render(request, 'engine/about.html')