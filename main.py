from crawl.crawler import *
from analyzer.indexer import *

#reverage: 122639
#inverse:252670
if __name__ == "__main__":
    codeList = [252670]
    for code in codeList:
        try:
            #get price data
            data = Crawler.get_price(code, 50)

            #make index data
            data = Index.make_index(data, IndexRequest())
            print(data)
        except Exception as e:
            print(str(e))
            raise