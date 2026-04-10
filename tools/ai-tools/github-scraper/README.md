# GitHub Scraper
GitHub 数据分析与爬虫工具，支持 API 自动分页、速率限制处理、数据分析。

## 安装
```bash
pip install -e .
```

## 使用

### 爬取用户资料
```bash
python main.py user <username>
python main.py user <username> --format json --save result.json
```

### 搜索仓库
```bash
python main.py search "machine learning python"
python main.py search "react hooks" --limit 20
```

### Python 调用
```python
from src.api import GitHubAPI
from src.scraper import GitHubScraper

api = GitHubAPI()
scraper = GitHubScraper(api)
profile = scraper.scrape_user("wdg631")
print(f"followers: {profile.followers}")
```
