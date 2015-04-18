from django.shortcuts import render_to_response
from django.http import HttpResponse

import newsSummarizer
def home(request):
    
    return render_to_response("myApp/base.html")
										
def search(request):
    errors = []
    
    if 'url' in request.GET:
        url = request.GET['url']
        if not url:
            errors.append('Please enter a url')
        else:
            result = usingTitleAlgorithm(url)
            title = result[3]
            return render_to_response("myApp/home.html", {'var1': title,
                                                          'var2': result[0],
                                                          'var3': result[1],
                                                          'var4': result[2]})
    return render_to_response("myApp/home.html", {'errors': errors})
