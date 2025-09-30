# 📂 Cấu trúc thư mục project của Scrapy
```
tutorial/
    scrapy.cfg            # file cấu hình cho Scrapy khi chạy project

    tutorial/             # module Python của project
        __init__.py

        items.py          # mô tả cấu trúc dữ liệu trích xuất ra

        middlewares.py    # kiểm soát request/response

        pipelines.py      # xử lý dữ liệu được yield ra từ spiders

        settings.py       # cấu hình project

        spiders/          # chứa các spider
            __init__.py
```

# ▶️ Chạy spider trong Scrapy project
Để chạy spider trong project, đảm bảo bạn đang ở thư mục project, chạy lệnh:
```bash
scrapy crawl <spider_id>
```

# 📑 Trích xuất dữ liệu trong Scrapy

## 1. Sử dụng CSS Selector
**Cú pháp cơ bản:**
```python
response.css("CSS_SELECTOR")
```

- Kết quả trả về là object `SelectorList` (danh sách các node HTML tìm được).
- Tiếp tục bằng cách lấy một kết quả bằng `.get()` hoặc lấy tất cả kết quả bằng `.getall()`.

---

### 1.1. Ví dụ minh hoạ
Giả sử HTML có dạng:
```html
<div class="quote">
  <span class="text">“The world as we have created it...”</span>
  <span>by <small class="author">Albert Einstein</small></span>
</div>
```

#### Lấy trích dẫn
```python
response.css("div.quote span.text::text").get()
```

#### Lấy tên tác giả
```python
response.css("div.quote small.author::text").get()
```

**Output:**
```python
>>> response.css("div.quote small.author::text").get()
'Albert Einstein'
```

---

### 1.2 Các hậu tố thường dùng
- **`::text`**: chỉ lấy phần text trong tag.
```python
>>> response.css("div.quote small.author").get()
'<small class="author" itemprop="author">Albert Einstein</small>'
```

- **`::attr(href)`**: lấy giá trị thuộc tính.
### 1.3. Ngoại lệ
Truy cập vào `SelectorList` rỗng sẽ cho ra ngoại lệ `IndexError`:
```
>>>response.css("noelement")[0].get()
Traceback (most recent call last):
...
IndexError: list index out of range
```
Thay vào đó, nên dùng `get()` vì kết quả trả về sẽ là `None` nếu rỗng
```
response.css("noelement").get()
```
## 2. Sử dụng XPath
### 2.1. Cú pháp cơ bản
```python
response.xpath("XPATH_EXPRESSION")
```
* Trả về `SelectorList` giống `.css()`
* Dùng `get()` để lấy một kết quả hoặc `getall()` để lấy hết
### 2.2 Ví dụ minh hoạ
* Giả sử HTML có dạng
```html
<div class="quote">
  <span class="text">“The world as we have created it...”</span>
  <span>by <small class="author">Albert Einstein</small></span>
</div>
```
* Lấy trích dẫn
  * `//div[@class='quote]`: tìm tất cả thẻ `div` có `class` là `quote` trong HTML
  * `/span[@class= 'text']`: đi xuống mức con, tìm các thẻ `span` có `class` là `text`
  * `/text()`: lấy text bên trong
```python
response.xpath("//div[@class='quote']/span[@class='text']/text()").get()
```
* Lấy tác giả
  * `//small[@class='author']` để đi xuống bất kỳ mức nào, tìm thẻ `small`
```python
response.xpath("//div[@class= 'quote]//small[@class='author']/text()").get()
```
## 3. Trích xuất trong spider
### Từ khoá `yield`
* `yield` biến một hàm bình thường thành *generation function*
* Khi hàm chạy đến `yield`, nó trả về giá trị đó nhưng *không kết thúc hàm*
* Lần gọi hàm tiếp theo sẽ tiếp tục chạy từ chỗ `yield` trở đi
```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
```
# Lưu trữ dữ liệu crawl được
## Feed Exports
* Option `-O` để ghi đè nếu file đã tồn tại
* Option `-o` thay vào đó gán dữ liệu mới vào file đã tồn tại
```bash
scrapy crawl quotes -O quotes.json
```
# Tìm đến url kế tiếp
* Tìm đến một url
```python
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```
* Tìm đến tất cả các url
  * `author_page_links = response.css(".author + a")`
    * Tìm đến tất cả các link nằm ngay sau tên các tác giả, chính là link bio của tác giả
      * `response.css(".author + a")`: Thẻ `<a>` đứng ngay sau phần tử có class là `author`
  * `yield from response.follow_all(author_page_links, self.parse_author)`
    * Với mỗi link tìm được, Scrapy sẽ follow theo để đến bio của tác giả và gọi hàm `parse_author` để xử lý.
  * `pagination_links = response.css("li.next a")`
    * Lấy link đến trang kế tiếp
  * `yield from response.follow_all(pagination_links, self.parse)`
    * Đi đến trang kế tiếp và gọi hàm `parse` để xử lý
```python
def parse(self, response):
    author_page_links = response.css(".author + a")
    yield from response.follow_all(author_page_links, self.parse_author)

    pagination_links = response.css("li.next a")
    yield from response.follow_all(pagination_links, self.parse)

def parse_author(self, response):
    def extract_with_css(query):
        return response.css(query).get(default="").strip()

    yield {
        "name": extract_with_css("h3.author-title::text"),
        "birthdate": extract_with_css(".author-born-date::text"),
        "bio": extract_with_css(".author-description::text"),
    }
```
# Truyền tham số khi gọi spider
```
scrapy crawl quotes -O quotes-humor.json -a tag=humor
```
* Truyền tham số sử dụng option `-a`
```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```
