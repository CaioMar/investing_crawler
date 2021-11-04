from datetime import datetime
import time

import scrapy

from selenium import webdriver

from investing import settings
from investing.items import InvestingItem

class InvestingfiisarticlesSpider(scrapy.Spider):
    name = 'InvestingFIIsArticles'
    allowed_domains = ['https://br.investing.com/search/?q=FIIs&tab=articles']
    start_urls = ['https://br.investing.com/search/?q=FIIs&tab=articles']
    partial_loading = 1
    article_selector = 'div.articleItem'

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path=settings.CHROME_DRIVER, 
            chrome_options=options
        )
        self.last_step = 0
        
    def converged(self) -> bool:

        current_step = len(self.driver.find_elements_by_css_selector(InvestingfiisarticlesSpider.article_selector))

        #convergence condition
        if self.last_step == current_step:
            return True

        self.last_step = current_step
        return False

    def complete_loading(self) -> webdriver.Chrome:
        
        #Scrolls to end of page to load more articles
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #Waits for request to finish
        time.sleep(InvestingfiisarticlesSpider.partial_loading)

        if not self.converged():

            self.driver = self.complete_loading()
        
        return self.driver

    def parse(self, response):

        self.driver.get(response.url)

        self.complete_loading()

        article_elements = self.driver.find_elements_by_css_selector(InvestingfiisarticlesSpider.article_selector)

        self.articles = []

        for article in article_elements:
            article_link = article.find_element_by_css_selector('a.title').get_attribute('href')
            print(article_link, self.articles, dir(self.articles))
            self.articles.append(dict(
                    article_link = article.find_element_by_css_selector('a.title').get_attribute('href'),
                    article_title = article.find_element_by_css_selector('a.title').get_attribute('innerHTML'),
                    article_author = article.find_element_by_css_selector('div.articleDetails span').get_attribute('innerHTML').replace('Por ',''),
                    article_date = datetime.strptime(article.find_element_by_css_selector('div.articleDetails time').get_attribute('innerHTML'),'%d.%m.%Y').strftime('%Y-%m-%d'),
                    article_type = article_link.split('/')[3],
                )
            )
            #article_text =  self.parse_article(article_link=article_link)

        for article in self.articles:

            article['article_text'] =  self.parse_article(article_link=article['article_link'])

            yield InvestingItem(
                **article
            )

    def parse_article(self, article_link):

        self.driver.get(article_link)

        text   =  "".join(list(map(lambda x: x.get_attribute('innerHTML'), self.driver.find_elements_by_css_selector("div.WYSIWYG p"))))

        return text
