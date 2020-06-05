import os
from itertools import product
from string import ascii_lowercase
import concurrent.futures
import math

# Set the number of concurrent spiders you want to crawl
THREADS = 4

# # Just random combos I thought will not give many results for testing purpose
# keywords = ['xqc', 'ycv', 'hcz', 'hzc', 'pfg', 'wqv']

keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]

# index pointer for keywords
at_keyword = 0
total_crawlers = len(keywords)
# Function to run the spider on


def char_spider(i):
    global at_keyword
    os.system(f"python user.py {keywords[at_keyword + i]}")
    return f"Spider Done for {keywords[at_keyword + i]}"


# Multiple spiders
for _ in range(math.ceil(total_crawlers/THREADS)):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = []
        for i in range(THREADS):
            if at_keyword+i < total_crawlers:
                f = executor.submit(char_spider, i)
                results.append(f)
            else:
                break

        for f in results:
            print(f.result())
        at_keyword += THREADS
