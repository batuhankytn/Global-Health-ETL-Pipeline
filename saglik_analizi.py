import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# 1. BAĞLANTI AYARLARI
# ---------------------------------------------------------
DB_USER = 'postgres'
DB_PASS = '1234' # <--- ŞİFRENİ YAZMAYI UNUTMA
# Daha önce eticaret_db içine atmıştık, oradan okuyalım
conn_string = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/eticaret_db"

try:
    engine = create_engine(conn_string)
    print("✅ Veritabanına bağlanıldı.")
except Exception as e:
    print("Bağlantı Hatası:", e)
    exit()

# 2. SQL ANALİZİ: Cinsiyet Farkı (Gender Gap) Analizi
# ---------------------------------------------------------
# Kadınların erkeklerden ne kadar uzun yaşadığını (Gender Gap) inceliyoruz.
# Farkın en yüksek olduğu ilk 15 ülkeyi getirelim.

sql_query = """
SELECT 
    country,
    life_expectancy,
    female_life,
    male_life,
    gender_gap
FROM 
    health_stats
ORDER BY 
    gender_gap DESC
LIMIT 15;
"""

try:
    df = pd.read_sql(sql_query, engine)
    print("\n--- Cinsiyet Farkının En Yüksek Olduğu Ülkeler ---")
    print(df[['country', 'gender_gap', 'life_expectancy']])
except Exception as e:
    print("❌ HATA: Tablo bulunamadı. Önce 'saglik_etl.py' dosyasını çalıştırdığından emin ol.")
    exit()

# 3. GÖRSELLEŞTİRME (Bar Chart)
# ---------------------------------------------------------
plt.figure(figsize=(14, 8))
sns.set_style("whitegrid")

# Bar grafiği çizelim (Yatay Bar Chart daha okunaklı olur)
sns.barplot(data=df, x='gender_gap', y='country', palette='magma')

# Grafik detayları
plt.title('Kadın ve Erkek Yaşam Süresi Farkının En Yüksek Olduğu 15 Ülke', fontsize=16)
plt.xlabel('Yaş Farkı (Kadın - Erkek)', fontsize=12)
plt.ylabel('Ülke', fontsize=12)

# Değerleri çubukların ucuna yazalım
for index, value in enumerate(df['gender_gap']):
    plt.text(value + 0.1, index, f"+{str(round(value, 1))} Yıl", va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig("Saglik_Gender_Gap.png")
print("\n✅ Grafik 'Saglik_Gender_Gap.png' olarak kaydedildi.")
plt.show()