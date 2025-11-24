🏥 Küresel Sağlık ve Demografi Analizi (ETL & Visualization)

📌 Proje Özeti

Bu proje, Worldometer verilerini kullanarak ülkelerin yaşam beklentisi (Life Expectancy) istatistiklerini analiz eden uçtan uca bir veri mühendisliği ve analitik çalışmasıdır.

Amaç, sadece hazır CSV dosyalarını kullanmak yerine; kendi verisini toplayan (Scraping), temizleyen (Cleaning) ve veritabanında saklayan (Warehousing) otomatize bir veri hattı (Pipeline) kurmaktır.

Proje sonucunda, ülkelerin sosyo-ekonomik durumlarının yaşam süresine ve özellikle cinsiyetler arası yaşam farkına (Gender Gap) etkisi incelenmiştir.

🛠 Kullanılan Teknolojiler ve Mimari

Bu proje, verinin ham halden bilgiye dönüşüm sürecini simüle eden 3 katmanlı bir ETL mimarisine sahiptir:

Katman

Dosya

Görev ve Teknoloji

1. Extraction (Veri Toplama)

saglik_scraper.py

BeautifulSoup & Requests kütüphaneleri ile Worldometer web sitesinden anlık verinin HTML tablosu olarak kazınması.

2. Transformation (Dönüştürme)

saglik_etl.py

Pandas kullanılarak metin tabanlı verilerin sayısal formata çevrilmesi, hatalı kayıtların temizlenmesi ve "Gender Gap" gibi yeni özniteliklerin (Feature Engineering) hesaplanması.

3. Loading & Analysis (Yükleme)

saglik_analizi.py

Temiz verinin PostgreSQL veritabanına yüklenmesi, SQL ile sorgulanması ve Seaborn ile görselleştirilmesi.

📊 Temel Çıkarımlar

Veritabanından SQL sorgularıyla çekilen veriler görselleştirildiğinde aşağıdaki çarpıcı sonuçlara ulaşılmıştır:

💡 Teknik Notlar:

Proje, web sitesindeki HTML yapısı değişse bile table etiketlerini dinamik olarak bulacak şekilde hataya dayanıklı (Robust) tasarlanmıştır.

Veritabanı bağlantısı için SQLAlchemy ORM yapısı kullanılmış, şifre güvenliği için parametrik yapı tercih edilmiştir.

🚀 Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için:

Gerekli kütüphaneleri yükleyin:

pip install pandas sqlalchemy psycopg2-binary matplotlib seaborn beautifulsoup4 requests


PostgreSQL veritabanı ayarlarını (DB_PASS) kod dosyalarında güncelleyin.

Veri hattını (Pipeline) sırasıyla çalıştırın:

python saglik_scraper.py  # Veriyi internetten çeker
python saglik_etl.py      # Temizler ve DB'ye yükler
python saglik_analizi.py  # Analiz eder ve grafiği çizer



Bu proje, açık kaynak veriler kullanılarak eğitim ve portföy amacıyla @batuhankytn tarafından geliştirilmiştir.
