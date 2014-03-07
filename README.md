#Vector Space Search Engine 

###Simple Vector Space Search Engine using a Term Document Matrix

Vector space search engines help us search unstructured documents for "topical" data. The documents directory contains 7 sample documents.  These 7 documents were obtained by crawling Yelp's search results for "Restaurants in Manhattan".  The crawler was build using the Impetus Framework found here:

https://github.com/richardjmarini/Impetus 

The simple sample crawler can found here: 

https://github.com/singleplatform/Impetus1

The "business provided" blurb was then extracted from the documents.  
These blurbs are what you'll find in the documents directory of this project:

https://github.com/richardjmarini/VectorSpaceSearchEngine/tree/master/documents

You'll notice the document contain only the content of the blurb and all the structure has been stripped away.  The documents are as follows:
```
0.txt: a french restaurant
1.txt: an american steakhouse
3.txt: an american tavern
5.txt: an american bar and grill containing the word French
8.txt: a healthfood restaurant
11.txt: a japanese restaurant
15.txt: another french restaurant
```

We can then search the content of the documents for a given topic:

###Simple Example Usage:
```
$ ./search.py --query="french"

Results:
0.0613160175473 ../documents/0.txt    <-- highest ranked document
0.0253357267547 ../documents/15.txt   <-- second higest ranked document
0.0236242433804 ../documents/5.txt    <-- third higest ranked document
0.0 ../documents/1.txt                <-- unrelated "American Steakhouse"
0.0 ../documents/11.txt               <-- unrelated "Japanese" restaurant -- and the document is mostly blank 
0.0 ../documents/8.txt                <-- unrelated "health food"
0.0 ../documents/3.txt                <-- unrelated "American Tavern"
```

####We can verify our results:
```
$ grep -i french ../documents/*.txt --files-with-matches
../documents/0.txt
../documents/15.txt
../documents/5.txt

```

If we manually examine those documents we'll find documents 0 and 15, the two highest rank documents, are indeed full French restaurants.  If we look at document 5 we'll see this an American cuisine restaurant and the document mereley contains the word French in discussing how the Chef's broke with French conventions -- therefore it's the lowest ranked result of all documents containing the word French.

###More Complex Example:

We can also search for documents "like" other documents. Lets use document 5 as our search criteria. If you recall document 5 is an American restaurant but the document also contains the term French.  By using the entire document as the query (and not just keywords as the simple example showed above) we can discern what "type" of restaurant document 5 is and implicitly create a query to search for other documents "like" itself. Lets see what happens: 
```
$ cat ../documents/5.txt  | ./search.py 
Results:
0.803445878371 ../documents/5.txt      <-- The first "closet" match is the document itself (typically we'd ignore this)
0.142620585035 ../documents/3.txt      <-- The second "closet" match another "American Restaurant"
0.133529489897 ../documents/1.txt      <-- The third "closet" match is an "American Steak House"
0.115629453888 ../documents/0.txt      <-- a french restaurant, because of the word French in the orginal doc 
0.0742452152519 ../documents/15.txt    <-- another french restaurant, same as above
0.0143866001622 ../documents/8.txt     <-- unrelated restaurant but has some related terms such as "culinary"
-0.00141012332948 ../documents/11.txt  <-- lowest rank, document is pretty much blank
```

As you can see, the closet matched documents to document 5 (an American Restaurant) were other American restaurants. We were able to discern that document 5 was an American Restaurant and due to the relevance of the world "American" within the document and then find other documents like itself. All with the same algorithm we used in the simple keyword search above.  Our program was able to recognize keywords within the document with out explicitly stating what the keywords are. 

That's about it!

Now, let's go have some Sake.  ...hmmm, where should we go?
```
$ ./search.py --query="sake"
Results:
0.396005214833 ../documents/11.txt
0.0 ../documents/0.txt
0.0 ../documents/1.txt
0.0 ../documents/8.txt
0.0 ../documents/5.txt
0.0 ../documents/3.txt
0.0 ../documents/15.txt
```


###Resources:
http://en.wikipedia.org/wiki/Vector_space_model

http://en.wikipedia.org/wiki/Tf-idf

http://en.wikipedia.org/wiki/Cosine_similarity

http://en.wikipedia.org/wiki/Norm_%28mathematics%29

###Other:
http://scikit-learn.org/stable/


