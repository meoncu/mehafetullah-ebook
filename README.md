# Mehâfetullâh (Allah Korkusu) — Abdülkâdir Geylânî (k.s.)
### 121 Sayfa Tam Metin Dijital E-Kitap, Yerel Veritabanı ve Mobil Uygulama

Bu depo, **Gavs-ı A'zam eş-Şeyh Abdülkâdir Geylânî (k.s.)** Hazretlerinin **"Mehâfetullâh (Allah Korkusu)"** adlı tasavvufî ve ahlâkî eserinin 121 sayfalık tam metin dijitalleştirilmiş halini, yerel JSON/JS veritabanını, modern web okuyucusunu, bağımsız tek dosya sürümünü ve Android projesini içermektedir.

---

## 📖 Kitap Künyesi

* **Eser:** Mehâfetullâh (Allah Korkusu)
* **Müellif:** Gavs-ı A'zam eş-Şeyh Abdülkâdir Geylânî (küddise sirruhu)
* **Külliyat Sırası:** Abdülkâdir Geylânî Külliyatı: 10
* **Tercüme:** Kâzım Ağcakaya
* **Hazırlayan:** Mustafa Kasadar
* **Yayınevi:** Medine Yayıncılık (Ravza Yayınları kuruluşu)
* **Baskı & Tarih:** 1. Baskı — İstanbul, 2012
* **ISBN:** 978-605-4411-74-0
* **Toplam Sayfa:** 121 Sayfa (Eksiksiz tam metin)
* **İçindekiler:** 69 Müstakil Konu ve Vaaz Başlığı

---

## ✅ 121 Sayfa Eksiksiz Denetim Raporu

Orijinal PDF belgesi ile veritabanı birebir karşılaştırılmış ve tüm sayfalar doğrulanmıştır:

* **Toplam Sayfa Sayısı:** 121 / 121 Sayfa
* **Metin İçeren Sayfalar:** 115 Sayfa (18.428 Kelime, 133.737 Karakter)
* **Geleneksel Mizanpaj Yaprakları:** 6 Sayfa (Sayfa 1: Orijinal Kapak Görseli, Sayfa 2: Geleneksel Boş Yaprak, Sayfa 5, 55, 95, 109: Kitabın basılı orijinalinde yer alan bölüm ayırıcı yapraklar)
* **Türkçe Karakter Bütünlüğü:** `ç, ğ, ı, ö, ş, ü, İ, Â, Î, Û` tüm harfler ve uzatmalar korunmuştur.
* **Eksik veya Hatalı Sayfa Sayısı:** 0

---

## 📱 Uygulama Özellikleri

1. **Sayfa Numaralandırması (1 / 121):**
   * Üst başlıkta ve alt gezinme çubuğunda anlık sayfa numarası (`Sayfa X / 121`).
   * "Sayfaya Git" modal penceresi (1-121 kaydırma çubuğu ve Kapak, İçindekiler, Hayatı, Vaaz hızlı butonları).
2. **69 Konulu İçindekiler Menüsü:**
   * Sol çekmeceden açılan, sayfa numaralarıyla eşleştirilmiş fihrist ve fihrist içi anlık filtreleme.
3. **4 Özel Okuma Teması:**
   * 📜 **Sepya**: Sıcak kağıt dokusu, göz yormayan klasik kitap hissi.
   * ☀️ **Gündüz (Açık)**: Temiz beyaz arka plan, koyu gri yazılar.
   * 🌙 **Gece (Koyu)**: Mat antrasit arka plan, yumuşak açık yazılar.
   * 🖤 **OLED (Siyah)**: AMOLED ekranlar için tam siyah ve maksimum batarya tasarrufu.
4. **Tipografi ve Okuma Ayarları (`Aa`):**
   * Font boyutu büyütme/küçültme (`A-` / `A+`, 14px - 28px).
   * Klasik Serif / Modern Sans-Serif yazı tipi seçimi.
   * İki yana yaslı, düşme başlıklı (drop-cap) ve süslemeli geleneksel sayfa düzeni.
5. **Canlı Arama (🔍):**
   * 121 sayfanın tamamında bellek içi anında arama ve sarı renkle işaretlenmiş pasaj sonuçları.
6. **Kaldığın Yeri Hatırlama:**
   * Tarayıcı kapatılıp tekrar açıldığında en son okunan sayfadan devam eder (`localStorage`).
7. **PWA (Progressive Web App):**
   * Çevrim dışı çalışma desteği (`manifest.json` ve `sw.js`).
8. **Tek Dosya Sürüm (`standalone_mehafetullah.html`):**
   * 457 KB büyüklüğünde, tüm CSS, JS, görsel ve 121 sayfayı tek dosyada toplayan, sunucusuz çalışan sürüm.

---

## 📂 Dizin Yapısı

```
mehafetullah-ebook/
├── www/                                # Mobil Web / PWA Uygulaması
│   ├── index.html                      # Ana okuyucu arayüzü
│   ├── styles.css                      # Tema ve tipografi stilleri
│   ├── app.js                          # Gezinme, arama ve durum yönetimi
│   ├── book_database.json              # 121 sayfalık JSON veritabanı
│   ├── book_database.js                # Yerel JS veritabanı
│   ├── cover.jpg                       # Orijinal kitap kapağı
│   ├── manifest.json                   # PWA manifesti
│   └── sw.js                           # Çevrim dışı Service Worker
├── extracted_pages/                    # 121 Sayfanın Ayrı Ayrı Düz Metin Dosyaları
│   ├── page_0001.txt                   # Kapak Görseli
│   ├── page_0002.txt                   # Boş Yaprak
│   ├── ...
│   └── page_0121.txt                   # Külliyat Kataloğu
├── android/                            # Android Studio Projesi
│   ├── app/src/main/AndroidManifest.xml
│   ├── app/src/main/java/com/mehafetullah/ebook/
│   │   ├── MainActivity.java           # WebView tabanlı ana aktivite
│   │   └── DatabaseHelper.java         # Yerel SQLite veritabanı yardımcısı
│   └── app/src/main/assets/www/        # Web varlıkları
├── standalone_mehafetullah.html        # Tek dosya bağımsız sürüm (457 KB)
├── pdf/                                # Orijinal PDF Kaynağı
│   └── Mehafetullah_Allah_korkusu.pdf
├── verify_all_pages.py                 # Sayfa doğrulama ve denetim scripti
└── README.md                           # Proje dokümantasyonu
```

---

## 🚀 Çalıştırma

### 1. Web Tarayıcısında Açmak:
`www/index.html` dosyasını doğrudan bir tarayıcıda açabilir veya yerel sunucu başlatabilirsiniz:
```bash
python -m http.server 8080 --directory www
```

### 2. Tek Dosya Sürümü:
`standalone_mehafetullah.html` dosyasını herhangi bir cihaza (telefon, tablet, bilgisayar) kopyalayıp çift tıklayarak internetsiz açabilirsiniz.

### 3. Android Studio ile Derlemek:
`android/` klasörünü Android Studio ile açıp doğrudan APK olarak derleyebilirsiniz.

---

## 📜 Lisans & Telif
Bu dijitalleştirme çalışması ilim, tefekkür ve eğitim amaçlı hazırlanmıştır. Eserin metin hakları ilgili yayınevine aittir.
