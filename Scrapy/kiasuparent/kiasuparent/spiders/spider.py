import scrapy


class KiasuSpider(scrapy.Spider):
    name = 'kiasuparent'

    start_urls = [
        'https://forums.hardwarezone.com.sg/forums/pc-gaming.382/',
    ]

    def parse(self, response):
        for topic_list in response.xpath('//div[has-class("structItem-title")]'):
            # for topic in topic_list.xpath('li/dl/dt'):
            yield {
                'topic': topic_list.xpath('a/text()').get(),
            }
            yield response.follow(topic_list.xpath('a/@href').get(), \
                self.parse) # go to the inside data 'content'

        for post in response.xpath('//article[has-class("message message--post js-post js-inlineModContainer")]'):
            yield {
                'author': post.css('a.username::text').get(),
                'content': post.css('div.bbWrapper::text').get(),
            }
            break

        next_page = response.xpath('//div[has-class("block-outer")]/div/nav/div/a[has-class("pageNav-jump pageNav-jump--next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)