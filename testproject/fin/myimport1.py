from eventregistry import *
er = EventRegistry(apiKey = 'f97425bc-cc68-4da2-a302-9be8eb8ad153')
q = QueryArticlesIter(
    keywords = QueryItems.OR(["USA", "Canada"]),
    dataType = ["news", "blog"])
# obtain at most 500 newest articles or blog posts
for art in q.execQuery(er, sortBy = "date", maxItems = 1):
    print (art)
    
