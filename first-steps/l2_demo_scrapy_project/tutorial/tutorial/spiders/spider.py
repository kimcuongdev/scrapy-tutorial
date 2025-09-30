from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:  # với mỗi url, yield một scrapy.Request object
            yield scrapy.Request(
                url=url, callback=self.parse
            )  # mỗi khi nhận được phản hồi, gọi đến hàm parse

    """
    Thay vì định nghĩa tường minh hàm start(), có thể định nghĩa 
    start_urls = ["https://quotes.toscrape.com/page/1/", "https://quotes.toscrape.com/page/2/"]
    """

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
