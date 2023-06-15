import scrapy
from scrapy.loader import ItemLoader
from photos.items import PhotosItem

class IstockSpider(scrapy.Spider):
    page = 1
    name = "istock"
    allowed_domains = ["www.istockphoto.com"]
    start_urls = ["https://www.istockphoto.com/search/2/image?page=1&phrase=love%20/"]

    def parse(self, response):
        for photos in response.xpath("//picture/img"):
            loader = ItemLoader(item=PhotosItem(), selector=photos)
            url = photos.xpath(".//@src").extract_first()
            loader.add_value('image_urls', url)
            yield loader.load_item()
        while self.page != 2 :
            self.page += 1
            yield scrapy.Request(url=f"https://www.istockphoto.com/search/2/image?page={self.page}&phrase=love%20/", callback=self.parse)
