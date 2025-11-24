import pandas as pd
from sqlalchemy import create_engine

# 1. KİRLİ VERİYİ OKU
# ---------------------------------------------------------
df = pd.read_csv("kirli_saglik_verisi.csv")
print("🧹 Sağlık verisi temizleniyor...")

# 2. TEMİZLİK ve DÖNÜŞTÜRME (Transformation)
# ---------------------------------------------------------

# Sayısal olması gereken sütunları temizle
# (Worldometer verisi nispeten temiz gelse de, garanti olsun diye numeric dönüşüm yapıyoruz)
cols_to_fix = ['raw_life_expectancy', 'raw_female_life', 'raw_male_life']

for col in cols_to_fix:
    # Sadece sayı ve nokta kalsın, gerisini sil (Regex gerekirse)
    # Burada basitçe pandas'ın to_numeric fonksiyonunu kullanıyoruz
    clean_col_name = col.replace("raw_", "") # 'raw_female_life' -> 'female_life'
    df[clean_col_name] = pd.to_numeric(df[col], errors='coerce')

# 3. YENİ VERİ ÜRETME (Feature Engineering)
# ---------------------------------------------------------
# Kadınlar erkeklerden ne kadar uzun yaşıyor?
df['gender_gap'] = df['female_life'] - df['male_life']

# Sadece temiz sütunları seçelim
df_clean = df[['country', 'life_expectancy', 'female_life', 'male_life', 'gender_gap']]

# Eksik verileri atalım
df_clean = df_clean.dropna()

print(f"✅ Temizlik tamamlandı! {len(df_clean)} ülke veritabanına hazır.")
print("\nEn Büyük Cinsiyet Farkı (Kadın - Erkek):")
print(df_clean.sort_values('gender_gap', ascending=False).head(3)[['country', 'gender_gap']])

# 4. POSTGRESQL'E YÜKLEME
# ---------------------------------------------------------
DB_USER = 'postgres'
DB_PASS = '1234' # <--- ŞİFRENİ YAZMAYI UNUTMA
# Veritabanı adını 'eticaret_db' kullanmaya devam edebiliriz, 
# ama gerçek hayatta 'saglik_db' diye yeni bir DB açardık.
conn_string = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/eticaret_db"

try:
    engine = create_engine(conn_string)
    df_clean.to_sql('health_stats', engine, index=False, if_exists='replace')
    print("\n🚀 Veriler PostgreSQL'deki 'health_stats' tablosuna yüklendi!")
except Exception as e:
    print("\n❌ Veritabanı Hatası:", e)