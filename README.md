# BKM Kitap Scraper

BKM Kitap'ın arama API'sini kullanarak kitap verilerini çeken minimal Python fonksiyonu.


## Kurulum

```bash
pip install requests pandas
```

## Kullanım

```python
from bkm_scraper import fetch_books_from_api

# Arama yap
df = fetch_books_from_api(query="macera")

# İlk 10 sonuç
print(df.head(10))

# CSV'ye kaydet
df.to_csv("kitaplar.csv", index=False, encoding="utf-8-sig")
```

## Dönen Veri

DataFrame kolonları: `id`, `title`, `author`, `publisher`, `price`, `old_price`, `discount_percent`, `stock_status`, `category`, `link`

## Not

Veri bulunamazsa boş DataFrame döner.

**⚠️ Bu proje yalnızca eğitim amaçlıdır. Ticari kullanım için değildir.**
