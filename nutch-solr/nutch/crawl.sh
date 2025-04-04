#!/bin/bash

CRAWL_DEPTH=3
NUTCH_LOCAL="/root/nutch_source/runtime/local"

bin/nutch inject $NUTCH_LOCAL/conf/urls/

for i in $(seq 1 $CRAWL_DEPTH); do
  echo "Round $i of crawling"
  bin/nutch generate crawl/crawldb crawl/segments
  #bin/nutch generate -topN 1000
  bin/nutch fetch -all
  bin/nutch parse -all
  bin/nutch updatedb crawl/crawldb -all
done

bin/nutch invertlinks crawl/crawldb/linkdb -dir crawl/crawldb/segments
bin/nutch index crawl/crawldb/ -linkdb crawl/crawldb/linkdb/ -dir crawl/crawldb/segments/ -filter -normalize -deleteGone