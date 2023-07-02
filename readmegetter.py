import numpy as np
from urllib.parse import urljoin
import requests, bs4, time, os
import openai

try:
    openai.api_key = os.getenv('OPENAI_API_KEY')
except:
    openai.api_key = streamlit.secrets['OPENAI_API_KEY']

class ReadmeGetter:
    def __init__(self):
        self.READMES = {}
        self.repo_links = []
    
    
    def get_repos(self, profile_link):
        # Takes a GitHub profile link and gathers links to all pinned repos
        class_="js-pinned-items-reorder-container"
        
        response = requests.get(profile_link)
        soup = bs4.BeautifulSoup(response.content, features="lxml")
        pins  = soup.find_all(class_=class_)
        pinned_repos = pins[0]
        links = pinned_repos.find_all('a', href=True)
        self.base_url = "https://www.github.com"
        repo_links = []

        # saving list of absolute links

        for link in links:
            # relative link
            rel_link = link['href']
            abs_link = urljoin(self.base_url,rel_link)

            # remove stars and forks
            if abs_link.endswith('stargazers') | abs_link.endswith('forks'):
                pass
            else:
                self.repo_links.append(abs_link)
                
    def get_readmes(self):
        # Gather readmes.  Must be used AFTER get_repos()
        for repo in self.repo_links:

            # get response
            response = requests.get(repo)
            # make a beautiful soup
            soup = bs4.BeautifulSoup(response.content, features="lxml")

            articles = soup.find_all('article')
            try:
                readme = articles[0]

                key = repo.replace(self.base_url+'/','')#.replace('/','')
                self.READMES[key] = readme.text
        
            except Exception as e:
                display(e)
                print(repo)
            sec_sleep = np.random.choice([1.9,1.2, 1.34,1.1,0.9])
            time.sleep(sec_sleep)
                
    def get_summaries(self, profile_link):
        summaries = {}
        prefix = """Please summarize the project readme following the colon into 3 bullet points
        suitable for a resume that would impress a data science hiring manager.
        The bullet points should highlight the skills necessary to complete the project:"""

        self.get_repos(profile_link)
        self.get_readmes()

        for key, readme in self.READMES.items():
            trunc_readme = readme[:4097] if len(readme) > 4097 else readme
            response = openai.ChatCompletion.create(
                model = 'gpt-3.5-turbo',
                messages=[{'role':'user', 'content':prefix + trunc_readme}]
                )
            summaries[key] = response.choices[0].message.content

        return summaries