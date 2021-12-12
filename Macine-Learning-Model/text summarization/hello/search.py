from google import google
print('Search here: ')
search=input()
search_results=google.search('inurl:'+search)
print(search_results)