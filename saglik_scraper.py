import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. HEDEF SİTE (Worldometer - Life Expectancy)
# ---------------------------------------------------------
url = "https://www.worldometers.info/demographics/life-expectancy/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print(f"🏥 Sağlık verilerine bağlanılıyor: {url}")

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("✅ Bağlantı Başarılı! Veriler çekiliyor...")
    else:
        print(f"❌ Siteye erişilemedi. Hata Kodu: {response.status_code}")
        exit()
except Exception as e:
    print(f"Hata: {e}")
    exit()

# 2. HTML AYIKLAMA
# ---------------------------------------------------------
soup = BeautifulSoup(response.content, "html.parser")

# GÜNCELLEME: Belirli bir ID aramak yerine sayfadaki "table" etiketlerini arıyoruz.
tables = soup.find_all("table")

if not tables:
    print("❌ HATA: Sayfada hiç tablo bulunamadı!")
    exit()

# Genelde veriler sayfadaki ilk veya ikinci tablodadır. Biz ilkini alalım.
table = tables[0]

# Satırları bul (tbody varsa içine bak, yoksa direkt tabloya bak)
tbody = table.find("tbody")
if tbody:
    rows = tbody.find_all("tr")
else:
    rows = table.find_all("tr")

# Başlık satırını (ilk satır) atlamak için kontrol
if len(rows) > 0 and "Country" in rows[0].text:
    rows = rows[1:]

print(f"Toplam {len(rows)} ülke verisi bulundu.\n")

data = []

for row in rows:
    cols = row.find_all("td")
    
    # Bazı satırlar boş veya reklam olabilir, kontrol edelim
    if len(cols) < 5:
        continue
    
    # Sütunların yerini siteyi inceleyerek bulduk:
    # 0: Sıra, 1: Ülke, 2: Yaşam Beklentisi (Her ikisi), 3: Kadın, 4: Erkek
    
    try:
        ulke_adi = cols[1].text.strip()
        genel_omur = cols[2].text.strip()
        kadin_omur = cols[3].text.strip()
        erkek_omur = cols[4].text.strip()
        
        data.append({
            "country": ulke_adi,
            "raw_life_expectancy": genel_omur,
            "raw_female_life": kadin_omur,
            "raw_male_life": erkek_omur
        })
    except IndexError:
        continue

# 3. KİRLİ VERİYİ KAYDET
# ---------------------------------------------------------
df = pd.DataFrame(data)

if df.empty:
    print("❌ HATA: Veri çekilemedi, tablo yapısı beklenenden çok farklı.")
else:
    print("🔍 KİRLİ SAĞLIK VERİSİ (İlk 5 Satır):")
    print(df.head())

    df.to_csv("kirli_saglik_verisi.csv", index=False)
    print("\n💾 'kirli_saglik_verisi.csv' kaydedildi.")