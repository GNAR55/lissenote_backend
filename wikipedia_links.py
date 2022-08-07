import wikipedia
import wikipediaapi

def get_links(nword_list):
    """this function takes refined list which comes from the get_names function and gives out a list with the corresponding wikipedia pages urls."""

    wiki = wikipediaapi.Wikipedia('en')

    page_links=[]

    for word in nword_list:
        #appends the page to the list
        page = wiki.page(word)

        if(page.exists()):
            #appends the URL to the page
            page_links.append(page.fullurl)

        #takes care of the edge case i.e if the page does not exist,just points to wikipedia home page
        else:
            print("Page about",word,"does not exist")
            page_links.append("https://www.wikipedia.org/")

    return(page_links)

def get_names(word_list):
    """This function takes raw list inputs and searches them using wikipedia api and then stores the first results' of each entry in a list."""

    nicenames = []
    for word in word_list:
        search_res = wikipedia.search(word)
        if search_res:
            nicenames.append(search_res[0])
        # print(nicenames)

    return nicenames

if __name__ == "__main__":
    print(get_links(get_names(["transistor","inductor","moore"])))