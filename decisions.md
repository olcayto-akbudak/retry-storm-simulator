# Tasarım kararları

## Alan motorunu CLI'dan ayırmak

`run(config)` orkestrasyonu kaynak kodun doğrudan test edilebilmesini sağlar. JSON arayüz taşınabilirliği artırır; bu sürüm kullanıcı arayüzü barındırmaz.

## Seçilen yöntem

Olay kuyruğu, token bucket, jitter, circuit breaker. Sanal zaman kullanılır; dört politika aynı varış verisiyle kıyaslanır.

## Bilinçli sınır

Ağ bağlantısı kurmaz; dağıtık devre kesicinin ve HTTP sunucusunun gerçek davranışını ayrıca ölçmek gerekir.

## Önerilen sonraki doğrulama

Gerçek kullanım hacmiyle testten önce mevcut kabul ve ret örneklerinin alan uzmanı tarafından onaylanması gerekir. Sonraki sürüm performans ölçümleri, dış adaptör sözleşmesi ve üretim gözlemlenebilirliğini ayrı karar kayıtlarında ele almalıdır.
