# Girdi ve çıktı sözleşmesi

UTF-8 JSON nesnesi; örnek dosya alanların tam iç içe yapısını gösterir. Zamanlar bu laboratuvarda sayısal sanal zaman/gün değeridir; saat dilimi dönüşümü yapılmaz.

| Üst alan | Tür | Örnek |
|---|---|---|
| `requests` | `int` | 250 |
| `seed` | `int` | 42 |

## Semantik

Sanal zaman kullanılır; dört politika aynı varış verisiyle kıyaslanır.

Alan motorunun doğrulamaları `app.py` içinde açıkça bulunur. Eksik zorunlu anahtarlar hata verir. Satır bazında karantina/bulgu üreten motorlar rapora yazar; yapısal konfigürasyon hataları işlemi keser. Tam JSON Schema dosyası bu sürümün kapsamında değildir.

## Çıktı

Gerçek çıktı şeması ve örnek değerler `sample-report.json` içinde yer alır. Örnek işleme özgü sonuçlar `results.md` içinde açıklanır. Dış tüketici alan adlarını ve birimleri değiştirmeden sözleşmeyi sürümlemelidir.
