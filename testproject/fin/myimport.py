from eventregistry import *
er = EventRegistry(apiKey = 'f97425bc-cc68-4da2-a302-9be8eb8ad153')
q = QueryArticlesIter(
    keywords = "Elon Musk",
    keywordsLoc = "title",
    ignoreKeywords = "SpaceX",
    sourceUri = "nytimes.com")
for article in q.execQuery(er, sortBy = "rel",
        returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(concepts = True, categories = True)),
        maxItems = 1):
        print (article)
        print('ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
