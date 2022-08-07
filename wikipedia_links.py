import wikipedia
import wikipediaapi

#this function takes refined list which comes from the get_names function and gives out a list with the corresponding wikipedia pages urls.
def get_links(l):
    wiki = wikipediaapi.Wikipedia('en')  
    #list which stores the corresponding wikipedia page wrt the listinput
    page = []
    page_links=[]
    for i in range(len(l)):
        #appends the page to the list
        page.append(wiki.page(l[i]))
        
        if(page[i].exists()):
            #prints the URL to the page
            page_links.append(page[i].fullurl)
        #takes care of the edge case i.e if the page does not exist,just points to wikipedia home page
        else:
            print("Page on",l[i],"does not exist")
            page_links.append("https://www.wikipedia.org/")
    return(page_links)

#this function takes raw list inputs and searches them using wikipedia api and then stores the first results' of each entry in a list.
def get_names(l):
    nicenames=[]
    for i in range(len(l)):
        temp = []
        
        temp=wikipedia.search(l[i])
        if len(temp)!=0:
            print(temp[0])
            nicenames.append(wikipedia.search(l[i])[0])
        print(nicenames)
    return(get_links(nicenames))
#print(get_names(["transistor","inductor","moore"]))

