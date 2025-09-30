import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"  # tên định danh của spider
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",  # url đầu tiên spider gửi request đến
    ]

    def parse(self, response):  # hàm được tự động gọi khi có response trả về
        for quote in response.css("div.quote"):  # chọn tất cả các div có class= "quote"
            yield {  # trả về dữ liệu sẽ được gom lại
                "author": quote.xpath("span/small/text()").get(),  # lấy tên tác giả
                "text": quote.css("span.text::text").get(),  # lấy phần text
            }
            next_page = response.css(
                "li.next a::attr('href')"
            ).get()  # lấy url trang kế tiếp
            if next_page is not None:  # nếu có
                yield response.follow(
                    next_page, self.parse
                )  # gửi request đến trang kế và gọi lại hàm parse
