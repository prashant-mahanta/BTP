# Smart Text Analysis for Information Visualisation

This project is my B.Tech project a 2-semester project. I have started working on the project in January. 
The project is divided into two components:
  1. Creating tools for text understanding and Analysis.
  2. Developing a framework for Information Visualization.
  
## Work done until now: 
For the first module, I have scraped news articles related to cricket. 
From this unstructured text, I have applied Stanford NER tagger to extract attribute-value(s) pairs modified them accordingly(pruning) to get proper phrases and exported the data to NoSQL framework.
To find the dependency in the text I am trying different methods. The one which I am working now is creating an undirected graph for each of the attributes (POLD - Person Organisation Location Date). Then find out the strongly connected components. Then based on the other attributes try to find the information about the component obtained from the graph. I will be exploring more way for text analytics. I have developed a search engine which is build using Node.JS using Express.JS module and database stored in MongoDB. The query is also parsed through the Stanford NER tagger which increases the precision on the system.  Presentation Link - [Here](https://github.com/prashant-mahanta/BTP/blob/master/Evaluation-1.pdf) (Regarding data and work more in description).

## Work to be done: 
I need to develop a platform where a user can see the real-time interactive visualizations on cricket news.  Scope: Can be worked on multiple areas such as Politics, events or different category of news.
