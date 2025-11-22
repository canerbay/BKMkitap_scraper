import requests
import json
import pandas as pd

def fetch_books_from_api(query="macera"):
    """
    BKM Kitap arama API'sini kullanarak verileri JSON formatında çeker
    ve Pandas DataFrame olarak döndürür. HTML parsing gerektirmez.
    """
    
    base_url = "https://bkm-best.wawlabs.com/search_v2"
    
    # API'ye gönderilecek filtre ve arama parametreleri
    payload_data = {
        "query": query,
        "facet": [
            {"field": "category", "type": "value"}, 
            {"field": "writer", "type": "value"}, 
            {"field": "brand", "type": "value"}
        ],
        "filter": [
            {"field": "category", "type": "value", "values": []}, 
            {"field": "brand", "type": "value", "values": []}, 
            {"field": "writer", "type": "value", "values": []}
        ]
  
    }

    # Tarayıcı taklidi yapan header bilgileri
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Origin': 'https://www.bkmkitap.com',
        'Referer': 'https://www.bkmkitap.com/'
    }
    
    try:
        # JSON verisini string parametre olarak gönderiyoruz
        response = requests.get(
            base_url, 
            params={"search_params": json.dumps(payload_data)}, 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # API yanıtında 'res' (result) anahtarı kontrolü
            if "res" in data:
                books = data["res"]
                cleaned_list = []
                
                for book in books:
                    # Fiyat verilerini sayısal formata çevirme (Virgül -> Nokta)
                    try:
                        sale_price = float(book.get("sale_price", "0").replace(",", "."))
                        old_price = float(book.get("price_not_discounted", "0").replace(",", "."))
                    except (ValueError, AttributeError):
                        sale_price = 0.0
                        old_price = 0.0

                    cleaned_list.append({
                        "id": book.get("id"),
                        "title": book.get("title"),
                        "author": book.get("writer"),
                        "publisher": book.get("publisher"),
                        "price": sale_price,
                        "old_price": old_price,
                        "discount_percent": book.get("discount_ratio"),
                        "stock_status": "In Stock" if book.get("stock_level") == "1" else "Out of Stock",
                        "category": book.get("category"),
                        "link": book.get("link")
                    })
                
                return pd.DataFrame(cleaned_list)
            else:
                print(f"Uyarı: Beklenen veri anahtarı bulunamadı. Mevcut anahtarlar: {data.keys()}")
                return pd.DataFrame()
                
        else:
            print(f"Hata: API yanıt vermedi. Durum kodu: {response.status_code}")
            return pd.DataFrame()

    except Exception as e:
        print(f"İstek sırasında hata oluştu: {e}")
        return pd.DataFrame()
