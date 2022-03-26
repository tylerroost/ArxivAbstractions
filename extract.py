"""
selenium code to pull the title and abstract from a set of arxiv links from an arxiv-sanity search into a csv with labeled columns using pandas
"""
import pandas as pd
from selenium import webdriver
import time

def create_search_term(search):
    """replaces spaces with + """
    return search.replace(" ", "+")

def create_csv(search_term):
    """searches arxiv-sanity-lite for search_term, resulting in a list elements of class rel_paper, where the links are the href of the child class rel_title"""
    driver = webdriver.Chrome()
    driver.get('https://arxiv-sanity-lite.com/?q=' + search_term + "&rank=time&tags=&pid=&time_filter=&svm_c=0.01&skip_have=no")
    time.sleep(15) 
    paper_list = driver.find_elements_by_class_name('rel_paper')
    links = [paper.find_element_by_class_name('rel_title').find_element_by_tag_name('a').get_attribute('href') for paper in paper_list]
    titles = [paper.find_element_by_class_name('rel_title').find_element_by_tag_name('a').text for paper in paper_list]
    abstracts = [paper.find_element_by_class_name('rel_abs').text for paper in paper_list]
    return titles, abstracts, links

def save_links_to_csv(search):
    """takes in search and searches arxiv-sanity-lite using create_links and create_search_term then saves the links to a csv file"""
    titles, abstracts, links = create_csv(create_search_term(search))
    links_df = pd.DataFrame({"title": titles, "abstract": abstracts, "link": links})
    links_df.to_csv(search + ".csv", index=False)
    return titles, abstracts, links

if __name__ == '__main__':
    print("Enter search term: ")
    search = input()
    titles, _, _ = save_links_to_csv(search)
    for title in titles:
        print(title)