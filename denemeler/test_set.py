import json

with open("data/golden_queries_deduped.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 100 hand-written paraphrases, keyed by the EXACT original question text.
# Matching by text (not index) so this works no matter how deduping shifted row order.
paraphrases_by_question = {
    "Cirom ne kadar? / Satışlarım nasıl?": "Toplam satış gelirim nedir?",
    "Geride kalan 6 ayın cirosunu göster.": "Son altı ayın ciro tutarını gösterir misin?",
    "KDV hariç toplam cirosuna göre en çok ciro yapan 5 müşteriyi (Bill‑To) listeleyiniz.": "KDV hariç ciroya göre en çok satış yaptığımız ilk 5 müşteriyi listeler misin?",
    "Mayıs 2024 ve Mayıs 2025 ayları arasındaki net ciro farkı nedir?": "Mayıs 2024 ile Mayıs 2025 arasında net ciro ne kadar değişmiş?",
    "Geçen hafta teslim edilen siparişlerin toplam tutarı nedir?": "Geçtiğimiz hafta teslim edilen siparişlerin toplam tutarı ne kadar?",
    "Aktif kampanya fiyat listelerinde yer alan ve varsayılan perakende satış fiyatı 100 TL'den yüksek olan ürünler hangileri?": "Aktif kampanya fiyat listesinde olup perakende satış fiyatı 100 TL'yi aşan ürünler hangileri?",
    "Hangi aktif ürünlerin satış fiyatı, alış fiyatının %10 altında kalmış?": "Satış fiyatı, alış fiyatının %10 altında kalan aktif ürünler hangileri?",
    "Verdiğimiz çeklerden vadesi geçmiş olanların toplam tutarı nedir ve hangi tedarikçilere ait?": "Vadesi geçmiş, bizim verdiğimiz çeklerin toplam tutarı ve kime ait olduğu nedir?",
    "Geçen ay en yüksek KDV tutarına sahip satış faturalarımız hangileri?": "Geçtiğimiz ay KDV tutarı en yüksek olan satış faturalarımız hangileri?",
    "Hangi banka hesap numaralarından ne kadar tutarda çek düzenlemişiz (vermişiz)?": "Hangi banka hesabından ne kadarlık çek düzenlemişiz?",
    "Siparişlerimizden ne kadarı hiç irsaliye aşamasına geçmeden doğrudan faturalandı?": "İrsaliye düzenlenmeden direkt faturaya dönüşen siparişlerimiz ne kadar?",
    "Hizmet kategorisindeki ürünler için (fiziksel stok takibi yapılmayan) bu ay ne kadarlık açık sipariş tutarımız var?": "Stok takibi yapılmayan hizmet ürünlerinde bu ayki açık sipariş tutarımız ne kadar?",
    "Aktif olan ve varsayılan satış fiyatı tanımlanmış ürünlerimizden, şu an geçerli ve aktif bir fiyat listesinde belirli bir müşteriye özel (cari kod tanımlı) fiyatlandırması olanlar hangileri?": "Aktif fiyat listesinde belirli bir müşteriye özel fiyatlandırması bulunan, satış fiyatı tanımlı aktif ürünler hangileri?",
    "Vadesi bu ay içinde dolacak olan alacak çeklerimiz var mı ve toplam tutarı ne kadar?": "Bu ay vadesi gelecek alacak çeklerimiz var mı, toplam tutarı nedir?",
    "Son 3 ayda müşteriye ulaştırılması en uzun süren (depodan çıkıştan teslimata kadar) sevkiyatlarımız hangileriydi? Belge numaraları ve taşıyıcı firmalarıyla birlikte görebilir miyim?": "Son 3 ayda depodan çıkışla teslimat arasında en uzun süren sevkiyatlar hangileri, belge no ve taşıyıcı firmasıyla gösterir misin?",
    "Son 3 ay içinde herhangi bir çeke eklenmiş notları, çekin numarası ve tutarıyla birlikte listeler misin?": "Son 3 ayda çeklere eklenen notları, çek numarası ve tutarıyla birlikte gösterir misin?",
    "Başarılı kredi kartı tahsilatlarında, toplamda ne kadar net tahsilat yaptık ve bu tahsilatlar için ne kadar komisyon ödedik?": "Başarılı kredi kartı tahsilatlarımızın toplam net tutarı ve ödediğimiz komisyon ne kadar?",
    "Azami stok seviyesinin üzerinde stoğu olan ürünler hangileri?": "Stok miktarı azami seviyeyi aşan ürünler hangileri?",
    "Varsayılan satış fiyatı 100 TL'nin üzerinde olan aktif ürünlerimizden, aynı zamanda alış fiyatı olmayan (yani sadece satılan ama alınmayan) ürünler hangileri?": "Satış fiyatı 100 TL üzerinde olup alış fiyatı hiç girilmemiş aktif ürünler hangileri?",
    "İstanbul'da merkezi olan (fatura adresi İstanbul olan) aktif müşterilerimizden kaç tanesinin sevkiyat adresi de tanımlı?": "Fatura adresi İstanbul olan aktif müşterilerden kaçının sevkiyat adresi de kayıtlı?",
    "Aktif ve geçerli olup da henüz hiçbir ürün detayı tanımlanmamış fiyat listelerimiz hangileri?": "Aktif ve geçerli olduğu halde içinde hiç ürün detayı olmayan fiyat listelerimiz hangileri?",
    "Son 1 ay içinde notlarına ekli dosya (ekli belge) olan aktif müşterilerimiz kimler ve bu notların konuları nelerdir?": "Geçtiğimiz ay notuna dosya eklenmiş aktif müşteriler kimler ve notların konusu ne?",
    "Bu ay içinde, e-İrsaliye olarak düzenlediğimiz satış irsaliyeleriyle sevk ettiğimiz ürünlerin toplam tutarı ne kadar? Hangi ürünler bu tutara en çok katkı sağladı?": "Bu ay e-İrsaliye ile sevk edilen ürünlerin toplam tutarı ne kadar ve en çok hangi ürünler katkı sağladı?",
    "Bu ay içinde vadesi dolacak çek veya senetlerimiz var mı? Varsa, hangi müşterilerden ne kadar alacağımız var?": "Bu ay vadesi gelecek çek/senetlerimiz var mı, hangi müşteriden ne kadar alacağımız var?",
    "Bu yıl içinde toplam navlun ve sigorta maliyeti 0 olan (ücretsiz sevk edilen) irsaliye gönderi sayımız ne kadar?": "Bu yıl navlun ve sigorta maliyeti sıfır olan, yani ücretsiz gönderilen irsaliye sayımız kaç?",
    "Vadesi gelmiş ama henüz tahsil edilememiş (alacak) hangi faturalarımız var ve toplam tutarı ne kadar? Vadesine göre sıralayabilir misin?": "Vadesi geldiği halde tahsil edilmemiş alacak faturalarımız hangileri, vadeye göre sıralar mısın?",
    "Son 3 ayda taşıyıcı firmalara ödediğimiz toplam navlun ve sigorta tutarı ne kadar? Bu tutarların hangi taşıyıcı firmalara yapıldığını ve hangi irsaliyelerden kaynaklandığını görmek istiyorum. Her bir irsaliye için navlun ve sigorta detaylarını listeleyebilir misiniz?": "Son 3 ayda taşıyıcı firmalara ödenen toplam navlun/sigorta tutarını, hangi firmaya ve hangi irsaliyeye ait olduğunu detaylı gösterir misin?",
    "Son 6 ayda en yüksek toplam işlem hacmine sahip (alış ve satış dahil) ilk 10 müşterimiz kimler?": "Son yarım yılda alış-satış toplamında en yüksek işlem hacmine sahip ilk 10 müşteri kim?",
    "Şoför olarak görevlendirilmiş ancak TCKN bilgisi girilmemiş irsaliye gönderileri var mı? Varsa, bu gönderilerin irsaliye numaralarını ve ilgili şoförlerin ad/soyadlarını listeleyebilir misiniz?": "Şoförü atanmış ama TCKN'si girilmemiş irsaliye gönderileri var mı, varsa irsaliye no ve şoför adıyla listeler misin?",
    "Bu yıl içinde en çok alış yapılan ürünler hangileri ve bu ürünlerin toplam alış tutarı ne kadar?": "Bu yıl en çok satın aldığımız ürünler hangileri ve toplam alış tutarları nedir?",
    "Önümüzdeki dönemde geçerli olacak, yani başlangıç tarihi henüz gelmemiş olan aktif satış fiyat listelerimiz hangileri? Bu listelerin ne zaman başlayacağını da görebilir miyim?": "Başlangıç tarihi henüz gelmemiş, ileride geçerli olacak aktif satış fiyat listelerimiz hangileri ve ne zaman başlıyorlar?",
    "Son 3 ayda en çok stok çıkışı (satış, fire vb.) yapılan ilk 5 depo hangisi?": "Son 3 ayda en fazla stok çıkışı yaşanan ilk 5 depo hangisi?",
    "Geçen yıl e-İrsaliye olarak gönderip de alıcı tarafından henüz yanıtlanmamış irsaliyelerimiz var mı? Varsa, bu irsaliyelerin belge numaralarını ve teslim tarihlerini listeleyebilir misiniz?": "Geçen yıl gönderdiğimiz ama alıcının hâlâ yanıt vermediği e-İrsaliyeler var mı, belge no ve teslim tarihiyle gösterir misin?",
    "Toplam kaç farklı aktif müşterimizin iletişim bilgisi (telefon/mobil) var ve bunlardan kaçının şirket e-posta adresi kayıtlı?": "Telefon bilgisi olan aktif müşteri sayımız kaç ve bunlardan kaçının şirket e-postası var?",
    "Bu ay itibarıyla, banka entegrasyonu üzerinden yaptığımız (giden) Havale/EFT işlemlerinde toplam ne kadar ödeme gerçekleştirdik?": "Bu ay banka entegrasyonuyla yaptığımız giden Havale/EFT ödemelerinin toplamı ne kadar?",
    "İstanbul ve Ankara dışındaki şehirlerdeki müşterilerimizden bu yıl en çok tahsilat yaptığımız (alacak hareketleri) şehirler hangisi?": "İstanbul ve Ankara hariç, bu yıl en çok tahsilat yaptığımız şehirler hangileri?",
    "En çok hatalı gelen havale/EFT işlemi alan kendi banka hesaplarımız hangileri ve her biri için ne kadar toplam tutar hatalı geldi?": "En fazla hatalı havale/EFT alan banka hesaplarımız hangileri ve hatalı gelen toplam tutar ne kadar?",
    "Müşterilerimizden siparişini aldığımız ama henüz hiç teslimatını yapmadığımız ürünler hangileri? Bu ürünlerin kodunu, adını ve bekleyen toplam miktarını listeler misin?": "Siparişi alınmış ama hiç teslim edilmemiş ürünler hangileri, kod/ad/bekleyen miktarıyla gösterir misin?",
    "Geçerlilik süresi dolmuş veya pasif duruma getirilmiş satış fiyat listelerimiz hangileri? Bu listelerin adlarını ve son geçerlilik tarihlerini görebilir miyim?": "Süresi dolmuş ya da pasife alınmış satış fiyat listelerimiz hangileri, adları ve son geçerlilik tarihleriyle görebilir miyim?",
    "Satış fiyatı belirlenmiş olmasına rağmen, tedarikçisi (temin bilgisi) tanımlanmamış olan ürünlerimiz hangileri?": "Satış fiyatı olduğu halde tedarikçisi tanımlanmamış ürünler hangileri?",
    "İstanbul'daki banka şubelerimizin listesini, hangi bankaya ait olduklarını ve şube kodlarını görebilir miyim?": "İstanbul'daki banka şubelerimizi, bankası ve şube koduyla listeler misin?",
    "Müşterilerimizden aldığımız çekler arasında, en çok çek düzenleyen (keşideci) kişi veya kurumlar kimler ve bu çeklerin toplam tutarı ne kadar?": "Bize en çok çek veren keşideciler kimler ve toplam tutarları ne kadar?",
    "Bu ay kestiğimiz satış faturalarındaki toplam belge bazlı indirim tutarı ne kadardı?": "Bu ay kestiğimiz faturalardaki toplam indirim tutarı ne kadar?",
    "Bu yıl içinde iptal edilen veya bize geri dönen (iade edilen) kendi verdiğimiz çekler hangileri ve toplam tutarı ne kadar?": "Bu yıl iptal olan ya da iade edilen verdiğimiz çekler hangileri ve toplamı nedir?",
    "Şu ana kadar düzenlediğimiz irsaliyelerden, henüz hiçbir satırı faturalanmamış olanların toplam tutarı ne kadar?": "Hiç faturalanmamış irsaliyelerimizin toplam tutarı ne kadar?",
    "Son 6 ay içinde hiç teslimat yapılmamış açık siparişlerimizdeki ürünlerin toplam bekleyen miktarını ve tutarını ürün bazında listeler misin?": "Son yarım yılda hiç teslim edilmemiş açık siparişlerdeki ürünlerin bekleyen miktar ve tutarını ürün bazında gösterir misin?",
    "Son 6 ay içinde hiç not eklenmemiş veya hiç yetkili bilgisi tanımlanmamış aktif müşterilerimiz kimler?": "Son yarım yılda hiç not girilmemiş veya yetkilisi tanımlanmamış aktif müşteriler kimler?",
    "Başarılı kredi kartı tahsilatlarında en çok hangi ödeme yöntemleri kullanılmış ve her bir yöntemle toplam ne kadar tutar tahsil edilmiş?": "Başarılı kredi kartı tahsilatlarında en çok kullanılan ödeme yöntemleri hangileri ve her biriyle ne kadar tahsil edilmiş?",
    "Geçen yıl boyunca bize en az çek veren (adet olarak) ama hala aktif olan müşterilerimiz kimler? Bu müşterilerin listesini ve verdikleri çeklerin toplam tutarını görebilir miyim? (En az çek veren ilk 100 müşteri)": "Geçen yıl en az sayıda çek veren ama hâlâ aktif olan ilk 100 müşteriyi, çek tutarlarıyla birlikte listeler misin?",
    "Hangi ürünlerimizin satışlar hesabı (muhasebe) tanımlanmamış olmasına rağmen son 1 yıl içinde satışı yapılmış?": "Muhasebe satış hesabı tanımlanmadığı halde geçen yıl satışı yapılmış ürünler hangileri?",
    "Son 3 ayda kestiğimiz satış faturalarının ortalama KDV hariç tutarı ne kadar?": "Son 3 aydaki satış faturalarımızın ortalama KDV hariç tutarı nedir?",
    "Son çeyrekte, taşıyıcı firmalarımızın toplam kaç adet ürün sevk ettiğini ve en çok ürün sevk eden taşıyıcıyı görebilir miyim?": "Son çeyrekte taşıyıcı firmalarımızın toplam sevk ettiği ürün adedini ve en çok sevkiyat yapanı gösterir misin?",
    "Bu yıl kestiğimiz satış faturalarındaki KDV tutarları, oranlara göre nasıl dağılıyor?": "Bu yılki satış faturalarındaki KDV tutarları oranlara göre nasıl dağılım gösteriyor?",
    "Geçen ay en çok hangi ürün koduna sahip ürünleri sevk ettik ve bu ürünlerden toplam kaç adet gönderildi? Bu ürünlerin adlarını da görebilir miyim?": "Geçen ay en çok sevk ettiğimiz ürün kodları hangileri, kaç adet gönderilmiş ve ürün adları nedir?",
    "Son 1 yılda en çok ciroya sahip olup, sistemde tanımlı bir varsayılan perakende satış fiyatı (Satış Fiyatı 1) olmayan aktif ürünlerimiz hangileri?": "Geçen yıl en çok ciro yapan ama perakende satış fiyatı tanımlanmamış aktif ürünler hangileri?",
    "Geçerli ve aktif olan satış fiyat listelerimizde, 'BazMiktar'ı sıfırdan büyük olan (yani minimum alım adedi gerektiren) ürünlerden, aynı zamanda cari hesap kodu (müşteri) belirtilmiş olanlar hangileri? Bu ürünlerin kodlarını, listelerin adlarını ve ilgili cari kodlarını görmek istiyorum.": "Minimum alım şartı olup aynı zamanda belirli bir müşteriye özel tanımlanmış fiyat listesi kalemleri hangileri?",
    "Son altı ayda depomuza en çok giriş yapan ürünler hangileri ve her birinden toplam ne kadar geldi?": "Son 6 ayda depoya en çok giren ürünler hangileri ve ne kadar miktar gelmiş?",
    "Varsayılan perakende satış fiyatı (SatışFiyat1) tanımlanmış, ancak toptan satış fiyatı (SatışFiyat2) boş veya sıfır olan aktif ürünlerimiz var mı? Varsa bu ürünleri listeler misiniz?": "Perakende satış fiyatı girilmiş ama toptan satış fiyatı boş kalan aktif ürünler var mı?",
    "Hangi ürünler için açık siparişlerdeki bloke edilmiş miktar, toplam bekleyen miktarın %50'sinden fazlasını oluşturuyor? Bu ürünlerin kodunu, adını ve bloke oranını görmek istiyorum.": "Açık siparişlerde bloke miktarı, bekleyen miktarın yarısından fazlasını oluşturan ürünler hangileri?",
    "Bu ay yaptığımız (giden) havale/EFT işlemlerinden (entegrasyon üzerinden başarılı olanlar) karşı tarafın IBAN'ına göre toplam ne kadar ödeme yapıldı ve en çok hangi IBAN'a ödeme yaptık?": "Bu ay yaptığımız başarılı giden Havale/EFT ödemelerinde en çok hangi IBAN'a ne kadar ödeme yapılmış?",
    "Bu yıl içinde, toplam hacmi (brüt hacim) en yüksek olan irsaliye gönderilerimiz hangileri ve bu gönderileri hangi taşıyıcı firma yaptı? Ayrıca, bu gönderilerdeki toplam ürün miktarlarını da görmek istiyorum.": "Bu yıl brüt hacmi en yüksek irsaliye gönderilerimiz hangileri, hangi taşıyıcıyla yapılmış ve toplam ürün miktarı nedir?",
    "Son 3 ayda hakkında not girilmiş ve bu notlara ek dosya eklenmiş müşterilerimiz kimler? Hangi notlar eklenmiş?": "Son 3 ayda notuna dosya eklenen müşteriler kimler ve notlar ne hakkında?",
    "Geçen ay en çok gönderi yapan 3 taşıyıcı firmamız hangileri? Bu firmaların toplam gönderi miktarlarını ve toplam brüt ağırlıklarını görmek istiyorum.": "Geçtiğimiz ay en çok gönderi yapan ilk 3 taşıyıcı firma hangileri, gönderi miktarı ve ağırlığı nedir?",
    "Kritik stok seviyesinin üzerinde olmasına rağmen son 1 yılda hiç satılmamış ürünlerimiz hangileri?": "Kritik stok seviyesinin üzerinde olduğu halde bir yıldır hiç satılmayan ürünler hangileri?",
    "Banka entegrasyonu üzerinden başarısız olan havale/EFT işlemlerinde, en çok hangi karşı IBAN'lar (gönderici IBAN'ları) ile ilgili sorun yaşıyoruz ve bu IBAN'lara ait toplam başarısız işlem tutarı nedir?": "Başarısız havale/EFT işlemlerinde en çok sorun yaşadığımız gönderici IBAN'lar hangileri ve toplam başarısız tutar ne kadar?",
    "Portföyümüzde bulunan, vadesi gelmemiş ve vadesi geçmiş müşteri çeklerinin toplam tutarlarını ayrı ayrı görebilir miyim?": "Elimizdeki müşteri çeklerinden vadesi gelenlerle gelmeyenlerin toplam tutarını ayrı ayrı gösterir misin?",
    "Toplamda müşterilerimize ne kadarlık bir kredi limiti tanımlamışız?": "Müşterilerimize toplamda tanımladığımız kredi limiti ne kadar?",
    "Başlangıç tarihi henüz gelmemiş olan (gelecekte başlayacak) aktif satış fiyat listelerimiz var mı? Varsa bu listeleri ve başlangıç tarihlerini görebilir miyim?": "İleride başlayacak, henüz aktifleşmemiş satış fiyat listelerimiz var mı, başlangıç tarihleriyle görebilir miyim?",
    "Gelecek ayın ilk 15 günü içinde vadesi dolacak olan, firmamız tarafından verilmiş çeklerin toplam tutarı nedir ve en yüksek tutarlı ilk 5'ini listeler misin?": "Önümüzdeki ayın ilk yarısında vadesi gelecek verdiğimiz çeklerin toplamı ne kadar ve en yüksek 5 tanesi hangileri?",
    "Envanterimizde seri veya parti numarası ile takip edilen aktif ürünlerimizin toplam mevcut stok miktarı nedir?": "Seri/parti numarasıyla takip edilen aktif ürünlerin toplam mevcut stoğu ne kadar?",
    "Belirli bir özel kodla işaretlenmiş ürünlerimizden, geçen ay en çok ciro yapan ürün hangisiydi?": "Özel kodla işaretli ürünler arasında geçen ay en çok ciro yapan hangisiydi?",
    "Bu yıl içinde e-İrsaliye olarak düzenlediğimiz gönderilerde, en çok sevkiyatı hangi taşıyıcı firmalarla yaptık ve bu firmaların her biriyle kaç adet e-İrsaliye gönderisi gerçekleştirdik? İlk 5'i listeler misiniz?": "Bu yıl e-İrsaliye gönderilerinde en çok çalıştığımız ilk 5 taşıyıcı firma hangileri, kaçar gönderi yapmışlar?",
    "Depoda en çok hangi ürünlerin stok kartında resim tanımlanmış ve bu ürünlerin adları nelerdir?": "Stok kartında resmi tanımlı ürünlerimiz hangileri, adları nedir?",
    "Şu an beklemede olan kredi kartı tahsilat işlemlerimizin toplam net tutarı ve komisyon dahil toplam brüt tutarı ne kadar?": "Şu anda beklemede olan kredi kartı tahsilatlarının net ve komisyon dahil brüt toplamı ne kadar?",
    "Hangi ürünlerden ne kadar miktar sipariş edilmiş ama henüz hiç teslimat yapılmamış, yani tamamen açık durumda olan siparişlerimiz var?": "Sipariş edilip hiç teslim edilmemiş, tamamen açık durumdaki ürünler ve miktarları neler?",
    "En yüksek birim fiyatla sattığımız ilk 10 ürün ve bu ürünleri hangi müşterilere sattık?": "Birim fiyatı en yüksek olan ilk 10 satışımız hangileri ve hangi müşterilere yapılmış?",
    "Aktif olan ürünlerimizden, varsayılan alış fiyatı tanımlanmış ancak bu alış fiyatının birimi (adet, kg vb.) belirtilmemiş olanlar hangileri?": "Alış fiyatı girilmiş ama birimi belirtilmemiş aktif ürünler hangileri?",
    "Aktif ve geçerli olan satış fiyat listelerimizde, aynı ürüne (StokKodu) ait birden fazla farklı cari hesap kodu için özel fiyatlandırma detayı girilmiş ürünler hangileri? Bu durum, ürün bazında cariye özel fiyatlandırmanın karmaşıklığını gösterebilir.": "Aynı ürün için birden fazla müşteriye özel fiyatlandırması olan ürünler hangileri?",
    "Stokta bulunan aktif ürünlerimizin toplam değeri ne kadardır, varsayılan satış fiyatı 1 üzerinden hesaplarsak?": "Mevcut stoktaki aktif ürünlerin, satış fiyatı 1 üzerinden hesaplanan toplam değeri nedir?",
    "Aktif durumdaki ürünlerimizden, ana kartında varsayılan perakende satış fiyatı (Satış Fiyatı 1) tanımlanmış olmasına rağmen, bu fiyat için KDV kodu (SF1KDV1) belirtilmemiş olanlar hangileri? Bu durum, hatalı faturalandırmaya yol açabilir.": "Perakende satış fiyatı girilmiş ama bu fiyata ait KDV kodu boş bırakılmış aktif ürünler hangileri?",
    "Özel bir cari koduna (müşteriye) atanmış, şu an aktif ve geçerli olan kaç farklı fiyat listesi var? Bu listelerin adlarını ve kaç farklı müşteriye özel fiyatlandırma yapıldığını görmek istiyorum.": "Belirli müşterilere özel tanımlanmış, şu anda geçerli fiyat listesi sayımız kaç ve kaç müşteriyi kapsıyor?",
    "Bugüne kadar hiç teslim edilmemiş ama hala açık durumda olan siparişlerimizin toplam tutarı ne kadar? Bu tutarı en çok olan ilk 10 müşteriyi listeleyebilir misin?": "Hiç teslim edilmemiş açık siparişlerin toplam tutarı ne kadar ve en yüksek tutarlı ilk 10 müşteri kim?",
    "Son 7 gün içinde süresi dolmuş veya dolacak olan aktif fiyat listelerimiz hangileri? Bu listelerde yer alan ürün sayısını da görmek istiyorum ki etkilenen ürünleri anlayabilelim.": "Son bir hafta içinde süresi dolan veya dolacak aktif fiyat listelerimiz hangileri, kaç ürünü etkiliyor?",
    "Hangi ürünlerimizin mevcut stok seviyesi azami stok seviyesini aşmış durumda ve bu ürünlerden ne kadar fazlamız var?": "Stok seviyesi azami sınırı geçen ürünlerimiz hangileri ve ne kadar fazlamız var?",
    "Son 3 ayda fiili sevk tarihi olan ancak henüz fiili teslim tarihi girilmemiş (yani hala yolda görünen veya teslimat bilgisi eksik olan) irsaliyelerimiz var mı? Varsa bu irsaliyelerin belge numaralarını, fiili sevk tarihlerini ve taşıyıcı firmalarını listeleyebilir misiniz?": "Son 3 ayda sevk edilmiş ama teslim tarihi girilmemiş, yani hâlâ yolda görünen irsaliyelerimiz var mı?",
    "Açık siparişleri olan ancak kritik veya azami stok seviyesi tanımlanmamış ürünlerimiz hangileri? Bu ürünlerin kodlarını, adlarını ve toplam açık sipariş miktarlarını görmek istiyorum.": "Açık siparişi olduğu halde kritik/azami stok seviyesi tanımlanmamış ürünler hangileri?",
    "Son 3 ayda, kredi kartı işlemlerinde ortalama yanıt süresi (işlem başlatma ile yanıt alma arasındaki süre) kaç saniyedir ve başarılı/beklemedeki işlemler için bu süreler nasıl değişiyor?": "Son 3 ayda kredi kartı işlemlerinin ortalama yanıt süresi kaç saniye, başarılı ve bekleyen işlemler arasında fark var mı?",
    "Son 1 yıl içerisinde, standart (kağıt) irsaliye olarak düzenlediğimiz sevkiyatların toplam brüt ağırlığı e-İrsaliye olarak düzenlediklerimizden ne kadar farklı? İki senaryo tipine göre toplam brüt ağırlıkları karşılaştıran bir rapor alabilir miyim?": "Geçen yıl kağıt irsaliyeyle e-İrsaliye sevkiyatlarının toplam brüt ağırlıklarını karşılaştırır mısın?",
    "Son 3 ayda en çok sevk edilen (depodan çıkan) ürünlerimiz hangileri? Bu ürünlerin kodlarını, adlarını ve toplam sevk edilen miktarlarını listeler misin?": "Son 3 ayda depodan en çok çıkan ürünler hangileri, kod/ad/miktarıyla listeler misin?",
    "Belirli bir tarihten sonra (örneğin 2024 başından itibaren) stok giriş fişiyle depomuza giren ürünlerin toplam miktarı ve değeri ne kadar?": "2024 başından bu yana stok giriş fişiyle depoya giren ürünlerin toplam miktar ve değeri nedir?",
    "Aktif ve miktar takibi yapılan ürünlerimizde, ana kartındaki varsayılan satış KDV oranı ile, geçerli ve aktif bir satış fiyat listesinde belirtilen KDV oranı farklılık gösterenler var mı? Bu durum faturalandırmada tutarsızlığa yol açabilir.": "Ana karttaki KDV oranı ile fiyat listesindeki KDV oranı birbirinden farklı olan aktif ürünler var mı?",
    "Firmamız tarafından verilen çeklerden, şu anda banka tarafından tahsilatta olan (yani ödenmeyi bekleyen) çeklerin toplam tutarı nedir?": "Verdiğimiz çeklerden şu an bankada tahsil aşamasında olanların toplam tutarı ne kadar?",
    "Kredi kartı tahsilatlarında, ortalama en yüksek komisyon oranına sahip ödeme yöntemleri hangileri ve bu yöntemlerden toplam ne kadarlık işlem yapıldı?": "Kredi kartı tahsilatlarında ortalama komisyon oranı en yüksek olan ödeme yöntemleri hangileri?",
    "Toplamda ne kadar tutarda, vadesi henüz gelmemiş kendi çeklerimiz var? Bu tutarın ne kadarını önümüzdeki 3 ay içinde ödememiz gerekiyor?": "Vadesi henüz gelmemiş verdiğimiz çeklerin toplamı ne kadar ve önümüzdeki 3 ayda ne kadarını ödeyeceğiz?",
    "Kredi kartı tahsilatlarımızda, tek çekim ve taksitli ödemelerin toplam net tutar bazında dağılımı nasıldır?": "Kredi kartı tahsilatlarında tek çekim ile taksitli ödemelerin net tutar dağılımı nasıl?",
    "Vadesi henüz gelmemiş ve final bir işleme tabi tutulmamış olan döviz cinsinden çeklerimizin (hem aldığımız hem verdiğimiz) toplam tutarı, döviz cinslerine göre ayrı ayrı ne kadar?": "Vadesi gelmemiş, döviz cinsinden aldığımız ve verdiğimiz çeklerin toplamı döviz türüne göre ne kadar?",
    "Bu ay bize en çok ödeme yapan (alacaklandıran) ilk 5 müşterimiz kimler ve ne kadar ödeme yaptılar?": "Bu ay bize en çok ödeme yapan ilk 5 müşteri kimler, ne kadar ödemişler?",
    "Son 3 ayda birden fazla farklı sevkiyatta görev almış şoförlerimizin adlarını, soyadlarını, görevlerini ve toplam kaç farklı sevkiyatta yer aldıklarını görmek istiyorum.": "Son 3 ayda birden fazla sevkiyatta görev alan şoförlerimiz kimler, kaç sevkiyata katılmışlar?",
    "Son 6 ayda satışı yapılan (çıkış işlemi olan) ancak hiç ana alış fiyatı (StokFiyat.AlisFiyati1) tanımlanmamış ürünler hangileri? Bu ürünlerin karlılık analizi yapılamaz.": "Son yarım yılda satılmış ama alış fiyatı hiç tanımlanmamış ürünler hangileri?",
    "Bu ay içinde kredi kartı ile tahsil etmeye çalıştığımız ama başarısız veya beklemede olan işlemlerin sayısı ve toplam tutarı nedir?": "Bu ay kredi kartıyla tahsil etmeye çalışıp başarısız olan veya beklemede kalan işlemlerin sayısı ve tutarı ne?",
}

test_set = []
for idx, item in enumerate(data):
    q = item["question"]
    if q in paraphrases_by_question:
        test_set.append({
            "original_index": idx,
            "original_question": q,
            "expected_sql": item["sql"],
            "paraphrase": paraphrases_by_question[q]
        })

found_questions = {row["original_question"] for row in test_set}
missing = [q for q in paraphrases_by_question if q not in found_questions]

with open("data/paraphrase_test_set.json", "w", encoding="utf-8") as f:
    json.dump(test_set, f, ensure_ascii=False, indent=2)

print(f"Matched {len(test_set)} / {len(paraphrases_by_question)} paraphrases by exact text match")
if missing:
    print("Could not find these in the deduped dataset (removed as duplicates?):")
    for m in missing:
        print(" -", m)