# Cấu trúc thư mục project của Scrapy
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

# Chạy spider trong Scrapy project
Để chạy spider trong project, đảm bảo bạn đang ở thư mục project, chạy lệnh
```
scrapy crawl <spider_id>
```
# Trích xuất dữ liệu trong Scrapy
## Sử dụng CSS
* Cú pháp cơ bản:
```
response.css("CSS_SELECTOR")
```
** Kết quả trả về là object `SelectorList` (danh sách các node HTML tìm được).
** Tiếp tục bằng cách lấy một kết quả bằng `.get()` hoặc lấy tất cả kết quả bằng `.getall()`

* Ví dụ minh hoạ:
** Giả sử HTML có dạng:
```
<div class="quote">
  <span class="text">“The world as we have created it...”</span>
  <span>by <small class="author">Albert Einstein</small></span>
</div>
```
** Lấy trích dẫn:
```
response.css("div.quote span.text::text").get()
```
** Lấy tên tác giả
```
response.css("div.quote small.author::text").get()
```

Output:
```
>>> response.css("div.quote small.author::text").get()
'Albert Einstein'
```
* Các hậu tố thường dùng:
** `::text`: chỉ lấy phần text trong tag
```
>>> response.css("div.quote small.author").get()      
'<small class="author" itemprop="author">Albert Einstein</small>'
```
** `::attr(href)`: lấy giá trị thuộc tính