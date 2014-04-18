#Vespse

###Vector Space Search Engine using a Term Document Matrix

Vector space search engines help us search unstructured documents for "topical" data. The documents directory contains 7 sample documents.  These 7 documents were obtained by crawling Yelp's search results for "Restaurants in Manhattan".  The crawler was built using the Impetus Framework found here:

https://github.com/richardjmarini/Impetus 

The simple sample crawler can found here: 

https://github.com/singleplatform/Impetus

The "business provided" blurb was then extracted from the documents.  
These blurbs are what you'll find in the documents directory of this project:

https://github.com/richardjmarini/Vespse/tree/master/documents

You'll notice the document contain only the content of the blurb and all the structure has been stripped away.  The documents are as follows:
```
0.txt: a french restaurant
1.txt: a french restaurant
2.txt: a french restaurant
3.txt: a spanish restaurant
4.txt: a spanish restaurant
5.txt: a spanish restaurant
6.txt: a Japanese resturant
```

We can then search the content of the documents for a given topic:

###Simple Example Usage:
```
$ ./search.py --query="french"

Results:
0.333333333333 ../documents/1.txt  <-- french
0.25153308489 ../documents/0.txt   <--- french
0.108465228909 ../documents/2.txt  <-- french
0.0 ../documents/5.txt             <-- spanish
0.0 ../documents/3.txt             <-- spanish
0.0 ../documents/6.txt             <-- Japanese
0.0 ../documents/4.txt             <-- spanish
```

####We can verify our results:
```
$ grep -i french ../documents/*.txt --files-with-matches
../documents/0.txt
../documents/1.txt
../documents/2.txt

```

If we manually examine those documents we'll find documents 0, 1 and 2, the two highest rank documents, are indeed French restaurants.  If we look at document 2 we'll see this an American restaurant with a "french twist" -- therefore it's the lowest ranked result of all documents containing the word French.

###More Complex Example:

We can also search for documents "like" other documents. Lets use document 2 as our search criteria. If you recall document 2 is an American restaurant but the document also contains the term French.  By using the entire document as the query (and not just keywords as the simple example showed above) we can discern what "type" of restaurant document 2 is and implicitly create a query to search for other documents "like" itself. Lets see what happens: 
```
$ cat ../documents/2.txt  | ./search.py 
Results:
1.0 ../documents/2.txt              <-- perfect match, itself, ignore this one
0.320147025048 ../documents/3.txt   <-- french resturant
0.286467233124 ../documents/0.txt   <-- french resturant
0.153392997769 ../documents/6.txt   <-- Japanese
0.15029382986 ../documents/4.txt    <-- spanish
0.11756333702 ../documents/5.txt    <-- spanish
0.108465228909 ../documents/1.txt   <-- spanish
```

As you can see, the closet matched documents to document 2 (an American Restaurant with a French Twist) were other French restaurants. We were able to discern that document 2 was an French Restaurant and due to the relevance of the word "French" within the document and then find other documents like itself. All with the same algorithm we used in the simple keyword search above.  Our program was able to recognize keywords within the document with out explicitly stating what the keywords are. 

That's about it!

Now, let's go have some Sake.  ...hmmm, where should we go?
```
$ ./search.py --query="sake"
Results:
0.353553390593 ../documents/6.txt
0.0 ../documents/0.txt
0.0 ../documents/1.txt
0.0 ../documents/2.txt
0.0 ../documents/5.txt
0.0 ../documents/3.txt
0.0 ../documents/4.txt
```


###Resources:
http://en.wikipedia.org/wiki/Vector_space_model

http://en.wikipedia.org/wiki/Tf-idf

http://en.wikipedia.org/wiki/Cosine_similarity

http://en.wikipedia.org/wiki/Norm_%28mathematics%29

###Other:
http://scikit-learn.org/stable/


