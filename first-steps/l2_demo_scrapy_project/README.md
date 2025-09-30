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
