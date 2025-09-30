# Demo hoạt động của Spider trong Scrapy
* Chạy Spider bằng lệnh sau:
```
scrapy runspider spider_demo.py -o quotes.json1
```
* Sau khi chạy sẽ thu được một file JSON nội dung gồm `text` và `author` của quotes từ trang `https://quotes.toscrape.com/tag/humor/`
* Quá trình crawl của spider là async, bất đồng bộ, tức Scrapy không cần đợi một request hoàn thành mà có thể tiếp tục gửi request và làm những công việc khác
