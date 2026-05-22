# 🎨 Renkli ASCII Video Dönüştürücü

Bir video dosyasını veya webcam görüntüsünü gerçek zamanlı olarak **renkli ASCII sanatına** dönüştüren Python uygulaması. GUI penceresi içinde orijinal video ve ASCII çıktısını yan yana gösterir.

## ✨ Özellikler

- 🎥 **Webcam & Video Dosyası Desteği** - MP4 dosyası varsa otomatik olarak kullanır
- 🎨 **Tam Renkli ASCII Çıktısı** - 24-bit ANSI renkleri ile gerçek renkler
- 🖼️ **GUI Arayüzü** - Orijinal video ve ASCII çıktısını yan yana gösterir
- ⚡ **Gerçek Zamanlı İşleme** - 30 FPS optimize edilmiş performans
- 🔧 **Otomatik Kurulum** - Tüm bağımlılıkları otomatik olarak kurar
- 🔄 **Video Döngüsü** - Video dosyası bitince başa sarılır

## 📋 Gereksinimler

- Python 3.7+
- OpenCV (`opencv-python`)
- Pillow (`pillow`)
- NumPy (`numpy`)

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Kur

```bash
python install.py
```

veya manuel olarak:

```bash
pip install -r requirements.txt
```

### 2. Uygulamayı Başlat

```bash
python ascii_video.py
```

## 📖 Kullanım

### Webcam ile Başlat (Varsayılan)
```bash
python ascii_video.py
```

### Video Dosyası ile
Dizine bir `video.mp4` dosyası koyun ve çalıştırın:
```bash
python ascii_video.py
```
Uygulama otomatik olarak MP4 dosyasını bulur ve kullanır.

## 🎮 Kontroller

- **Çıkış**: "Çıkış" butonuna tıklayın veya pencereyi kapatın
- **Pause/Resume**: Şu anda desteklenmiyor (gelecek sürüm)

## 🏗️ Proje Yapısı

```
asciicamera/
├── ascii_video.py          # Ana uygulama (GUI)
├── install.py              # Otomatik kurulum scripti
├── requirements.txt        # Bağımlılıklar
├── README.md              # Bu dosya
└── video.mp4              # (İsteğe bağlı) Video dosyası
```

## 🔧 Teknik Detaylar

### Renkli ASCII Dönüştürme

1. **Video Karesini Oku** - OpenCV ile video/webcam karesini al
2. **Boyutlandır** - ASCII çıktı boyutuna yeniden boyutlandır
3. **Renk Analizi** - Her piksel için RGB değerini al
4. **Parlaklık Hesapla** - Gri tonlamaya çevir
5. **ASCII Karakteri Seç** - Parlaklığa uygun karakter seç
6. **Renk Kodu Ekle** - ANSI 24-bit renk kodunu ekle
7. **Göster** - GUI'de renkli ASCII çıktısını göster

### ANSI Renk Kodları

```
\033[38;2;R;G;Bm<karakter>
```

Örnek: `\033[38;2;255;0;0mA` → Kırmızı "A" karakteri

## 📊 Performans

| Ayar | Değer |
|------|-------|
| FPS Sınırı | 30 |
| ASCII Genişliği | 80 karakter |
| ASCII Yüksekliği | 25 satır |
| Threading | Evet (arka planda işleme) |

## 🐛 Sorun Giderme

### Webcam Açılamıyor
- Başka bir uygulama webcamı kullanıyor olabilir
- Kamera izinlerini kontrol edin
- Farklı bir kamera numarası deneyin

### Renkler Gösterilmiyor
- Terminal ANSI renk desteğini etkinleştirmelidir
- Windows 10+ gereklidir
- VS Code veya modern terminal kullanın

### Yavaş Çalışıyor
- Daha güçlü bir bilgisayar kullanın
- Video dosyasının çözünürlüğünü azaltın
- Arka planda çalışan uygulamaları kapatın

### Video Dosyası Bulunamıyor
- MP4 dosyasını aynı dizine koyun
- Dosya adının `.mp4` ile bittiğinden emin olun
- Dosya yolunda Türkçe karakterler varsa sorun olabilir

## 📝 Dosya Açıklamaları

### `ascii_video.py`
Ana uygulama dosyası. Tkinter GUI, OpenCV video işleme ve ASCII dönüştürme kodunu içerir.

### `install.py`
Otomatik kurulum scripti. `requirements.txt` dosyasındaki tüm bağımlılıkları kurar.

### `requirements.txt`
Proje bağımlılıkları ve sürümleri.

## 🎯 Gelecek Özellikler

- [ ] Pause/Resume kontrolü
- [ ] Özel ASCII karakter seti seçimi
- [ ] Çıktı boyutu ayarlama (GUI'de)
- [ ] Video kaydetme
- [ ] Ekran görüntüsü alma
- [ ] Farklı renk modları

## 📄 Lisans

MIT

## 👨‍💻 Geliştirici

Renkli ASCII Video Dönüştürücü

## 🤝 Katkıda Bulunun

Hata bulduysanız veya öneriniz varsa lütfen bildirin!

---

**Sürüm**: 1.0.0  
**Son Güncelleme**: 2026-05-22