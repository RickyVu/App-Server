from django.urls import get_resolver, URLResolver
import copy


def get_all_urls(l = get_resolver(), intermediate="", result = []):
    for url in l.url_patterns:
        if isinstance(url, URLResolver):
            intermediate+=str(url.pattern)
            get_all_urls(url, intermediate=intermediate, result=result)
            intermediate=intermediate[:intermediate.index(str(url.pattern))]
        else:
            result.append(intermediate+str(url.pattern))
    return list(dict.fromkeys(result))