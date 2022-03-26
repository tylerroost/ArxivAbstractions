"""
selenium code to pull the title and abstract from a set of arxiv links from an arxiv-sanity search into a csv with labeled columns using pandas
"""
import pandas as pd
from selenium import webdriver
import time


def get_title(link):
    """returns the title of a given arxiv link"""

    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5) 

    try:
        title_element = driver.find_element_by_id('title')  
        return title_element.text  
    except:  
        return None

def get_abstract(link):
    """returns the abstract of a given arxiv link"""

    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5) 

    try:
        abs_element = driver.find_element_by_id('abstract')  
        return abs_element.text  
    except:  
        return None

def get_links(links_csv_path):
    """returns a list of arxiv links from a csv file"""
    links_df = pd.read_csv(links_csv_path)
    return [link for link in links_df['Link']]


def create_search_term(search):
    """replaces spaces with + """
    return search.replace(" ", "+")

def create_links(search_term):
    """searches arxiv-sanity-lite for search_term, resulting in a list elements of class rel_paper, where the links are the href of the child class rel_title"""
    driver = webdriver.Chrome()
    driver.get('https://arxiv-sanity-lite.com/?q=' + search_term + "&rank=time&tags=&pid=&time_filter=&svm_c=0.01&skip_have=no")
    time.sleep(5) 
    paper_list = driver.find_elements_by_class_name('rel-paper')
    links = [paper.find_element_by_class_name('rel-title').find_element_by_tag_name('a').get_attribute('href') for paper in paper_list]
    return links

def save_links_to_csv(search):
    """takes in search and searches arxiv-sanity-lite using create_links and create_search_term then saves the links to a csv file"""
    links = create_links(create_search_term(search))
    links_df = pd.DataFrame({"Link": links})
    links_df.to_csv(search + ".csv", index=False)

if __name__ == '__main__':
    print("Enter search term: ")
    search = input()
    save_links_to_csv(search) 
    links = get_links(search + ".csv")
    titles = [get_title(link) for link in links]
    for title in titles:
        print(title)