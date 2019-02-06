from newspaper import Article 

b = open("links2.txt","r+")  
#A new article from TOI 
i = 0
fileno = 1001
while i<50:
    z = b.readline()
    i+=1
    if z.find("https://www.hindustantimes.com/cricket/") == -1:
        continue
        # print(z)
    print(str(fileno)+"-----\n")
    z = z[:len(z)-1]
    print(z)
    url = z

    #For different language newspaper refer above table 
    toi_article = Article(url, language="en") # en for English
    name = "News"+str(fileno)+".txt"
    file = open(name,"w")
    #To download the article 
    toi_article.download() 
      
    #To parse the article 
    toi_article.parse() 
      
    #To perform natural language processing ie..nlp 
    toi_article.nlp() 
      
    #To extract title 
    print("Article's Title:") 
    print(toi_article.title) 
    file.write(toi_article.title)
    file.write('\n')
    
    print("n") 
      
    #To extract text 
    print("Article's Text:") 
    print(toi_article.text) 
    print("n") 

    file.write(toi_article.text)
      
    #To extract summary 
    print("Article's Summary:") 
    print(toi_article.summary) 
    print("n") 
      
    #To extract keywords 
    print("Article's Keywords:") 
    print(toi_article.keywords) 
    fileno += 1