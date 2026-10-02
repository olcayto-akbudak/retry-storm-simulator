# Çalıştırılmış kabul sonuçları

Python 3.12.14, sentetik `scenario.json`; yerel test sayısı **8**, tümü başarılı. Ham test günlüğü `test-log.txt`.

none: başarı 190/250, çağrı 250, amplifikasyon 1.0, başarılı p95 0.23939 sn; fixed: başarı 245/250, çağrı 390, amplifikasyon 1.56, başarılı p95 13.916545 sn; jitter: başarı 248/250, çağrı 397, amplifikasyon 1.588, başarılı p95 14.632209 sn; circuit: başarı 250/250, çağrı 259, amplifikasyon 1.036, başarılı p95 15.082051 sn

Sonuçlar yalnız bu örneğe aittir; üretim doğruluğu veya performans garantisi olarak yorumlanmamalıdır. Ölçülen iş sonucunu kontrol edin; örnek negatif vaka içeriyorsa ret beklenir. Tam çıktı `sample-report.json`.

## Sınanan davranışlar

| Test | Kontrol |
|---|---|
| `test_no_retry` | no retry |
| `test_reproducible` | reproducible |
| `test_deadline` | deadline |
| `test_duplicate` | duplicate |
| `test_capacity` | capacity |
| `test_policy` | policy |
| `test_attempt_bound` | attempt bound |
| `test_empty` | empty |

## Gelişmiş deney planı

1. Kesintiyi tek aralık yerine birden fazla pencereden üretin.
2. Retry-After ile jitter politikasını aynı varışlarda kıyaslayın.
3. Saatlik throughput için deadline ve token rate duyarlılık matrisi çıkarın.
4. Dağıtık breaker durumu ile yerel breaker arasındaki çağrı amplifikasyonunu simüle edin.
