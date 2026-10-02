# İşletim ve hata inceleme

1. `python --version` ile 3.12 veya daha yeni sürümü doğrulayın.
2. Depo kökünde testleri çalıştırın; başarısız test varken senaryoyu referans kabul etmeyin.
3. `scenario.json` dosyasının bir kopyasını değiştirin; referans örneği koruyun.
4. `python app.py demo --input <dosya> --output deney.json` çalıştırın.
5. Beklenen ret/inceleme ile beklenmeyen exception durumunu ayırın.
6. Çıktıyı `sample-report.json` ile karşılaştırın; sentetik negatif örnekleri otomatik başarıya çevirmeyin.

## Projeye özgü kontrol

Ortak varışlar → olay heap → hız sınırı → sağlayıcı kesintisi → retry/deadline

Sanal zaman kullanılır; dört politika aynı varış verisiyle kıyaslanır.

## Arıza çözümü

JSON parse hatasında girdi biçimini; eksik alan hatasında sözleşmeyi; kural ihlalinde alan bulgusunu; SQLite kilidinde eşzamanlı yazıcı sayısını inceleyin. Gerçek veriyi paylaşmadan önce anonimleştirin. Başarı iddiasını raporun gate/valid/fit/correct/state alanının ilgili semantiğiyle ilişkilendirin; sadece exit code yeterli değildir.

## Üretim açığı

Ağ bağlantısı kurmaz; dağıtık devre kesicinin ve HTTP sunucusunun gerçek davranışını ayrıca ölçmek gerekir.
