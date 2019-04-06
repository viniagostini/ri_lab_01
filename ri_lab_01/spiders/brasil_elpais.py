# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for next_page_url in response.css('a::attr(href)').getall():
            if (self.__is_aticle_url(next_page_url)):        
                yield scrapy.Request("https:" + next_page_url, callback=self.__get_article)
                
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def __get_article(self, response): 
        ps = response.css('div.articulo__contenedor p::text').getall()
        article_text = ''
        for p in ps:
            article_text += p.replace("\n", "")
        return {
            'titulo': response.css('h1.articulo-titulo::text').get(default='Sem titulo'),
            'subtitulo': response.css('h2.articulo-subtitulo::text').get(default='Sem subtitulo'),
            'autor': response.css('span.autor-nombre a::text').get(default='Sem autor'),
            'data': response.css('time::attr(datetime)').get(default='Sem data'),
            'secao': response.url.split('/')[-2],
            'texto': article_text,
            'url': response.url
        }

    def __is_aticle_url (self, url):
        #[...document.querySelectorAll('a[href]')].map(a => a.href).filter(href => href.includes('brasil.elpais.com/brasil/2019'))
        return "brasil.elpais.com/brasil/2019" in url

