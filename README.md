#Vector Space Search Engine 

###Simple Vector Space Search Engine using a Term Document Matrix

###Example Usage:
```
$ ./search.py --query="french resturants"

Results:
0.0613160175473 ../documents/0.txt    <-- highest ranked document
0.0253357267547 ../documents/15.txt   <-- second higest ranked document
0.0236242433804 ../documents/5.txt    <-- third higest ranked document
0.0 ../documents/1.txt                <-- unrelated "American Steakhouse"
0.0 ../documents/11.txt               <-- unrelated "Japanese" resturant -- and the document is mostly blank 
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

If we manually examine those documents we'll find documents 0 and 15, the two highest rank documents, are indeed full French resturants.  If we look at document 5 we'll see this an American cusine resturant and the document merley contains the word French in discussing how the Chef's broke with French conventions -- therefore it's the lowest ranked result of all documents containing the word French


We can also search for documents "like" other documents. Lets use document 5 as our search criteria. If you recall document 5 is an American resturant but the document also contains the term French.  Lets see what happens: 
```
$ cat ../documents/5.txt  | ./search.py 
Results:
0.803445878371 ../documents/5.txt      <-- The first "closet" match is the document itself (typically we'd ignore this)
0.142620585035 ../documents/3.txt      <-- The second "closet" match another "American Resturant"
0.133529489897 ../documents/1.txt      <-- The third "closet" match is an "American Steak House"
0.115629453888 ../documents/0.txt      <-- a french resturant, because of the word French in the orginal doc 
0.0742452152519 ../documents/15.txt    <-- another french resturant, same as above
0.0143866001622 ../documents/8.txt     <-- unrelated resturant but has some related terms such as "culinary"
-0.00141012332948 ../documents/11.txt  <-- lowest rank, document is pretty much blank
```

###Resources:
http://en.wikipedia.org/wiki/Vector_space_model

http://en.wikipedia.org/wiki/Tf-idf

http://en.wikipedia.org/wiki/Cosine_similarity

http://en.wikipedia.org/wiki/Norm_%28mathematics%29



