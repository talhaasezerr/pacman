# pacman
# 🎮 Pacman Game

Klasik Pac-Man oyununun Python ve Pygame kullanılarak yapılmış bir kopyası.

## 📋 Özellikler

- **Klasik Pac-Man oynanışı**: Labirentte dolaşın ve tüm yemekleri toplayın
- **4 Farklı hayalet**: Her biri farklı davranış özellikleri ve gecikmeli başlangıçları ile
- **Güçlendirici peletler**: Büyük pelletleri yiyerek hayaletleri yenebilirsiniz
- **Skor sistemi**: Normal peletler için 10 puan, güçlendirici peletler için 50 puan
- **Can sistemi**: 3 can ile başlayın
- **Yüksek skor**: Oyun boyunca en yüksek skorunuzu takip edin
- **Oyun duraklama**: P tuşu ile oyunu durdurun/devam ettirin
- **Yumuşak animasyonlar**: Pac-Man'ın ağız hareketi ve canlı renkler

## 🎯 Oyun Hedefi

Hayaletlerden kaçarken labirentteki tüm normal ve güçlendirici peletleri toplayın. Büyük peletleri yiyerek hayaletleri geçici olarak yenebilir duruma gelebilirsiniz.

## 🕹️ Kontroller

| Tuş | Aksiyon |
|-----|---------|
| ⬆️ W / Yukarı Ok | Yukarı hareket |
| ⬇️ S / Aşağı Ok | Aşağı hareket |
| ⬅️ A / Sol Ok | Sola hareket |
| ➡️ D / Sağ Ok | Sağa hareket |
| P | Oyunu duraklat/devam ettir |
| R | Oyunu yeniden başlat |
| ESC | Oyundan çık |

## 🚀 Kurulum

### Gereksinimler

- Python 3.6 veya üstü
- Pygame kütüphanesi

### Adım Adım Kurulum

1. **Kodu indirin veya klonlayın**
   ```bash
   git clone <repo-url>
   cd ders_projeleri
   ```

2. **Gerekli kütüphaneleri yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

3. **Oyunu çalıştırın**
   ```bash
   python pacman.py
   ```

## 🎮 Oynanış

1. Oyun başladığında "GET READY!" mesajını göreceksiniz
2. Ok tuşları veya WASD tuşlarını kullanarak Pac-Man'ı hareket ettirin
3. Labirentteki tüm küçük beyaz noktaları (peletleri) toplayın
4. Büyük yanıp sönen peletler güçlendiricidir - bunları yediğinizde hayaletleri yiyebilirsiniz
5. Tüm peletleri toplayarak seviyeyi tamamlayın
6. 3 can ile başlarsınız - bir hayalet sizi yakalayınca bir can kaybedersiniz

## 🏆 Puanlama

- **Küçük pelet**: 10 puan
- **Güçlendirici pelet**: 50 puan
- **Hayalet yemek**: 200 puan (güçlendirilmiş moddayken)

## 🎨 Renkler ve Karakterler

- **Pac-Man**: Sarı yanıp sönen ağız animasyonu
- **Kırmızı Hayalet**: Agresif takipçi
- **Pembe Hayalet**: Pusuda bekleyen
- **Camgöbeği Hayalet**: Tuzak kurucu
- **Turuncu Hayalet**: Rastgele hareket eden

## 🔧 Teknik Detaylar

- **Ekran boyutu**: 570x680 piksel
- **FPS**: 60
- **Labirent boyutu**: 19x21 karo
- **Karo boyutu**: 30 piksel
- **Pac-Man hızı**: 3 piksel/frame
- **Hayalet hızı**: 2.5 piksel/frame (normal), 1.25 piksel/frame (korkmuş halde)
- **Güçlendirme süresi**: 480 frame (yaklaşık 8 saniye)

## 🐛 Bilinen Sorunlar

- Labirent duvarlarına çok hızlı yaklaşırken hafif takılmalar olabilir
- Hayaletler bazen köşelerde bekleyebilir

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirme

Oyunu geliştirmek veya özelleştirmek için:
- `TILE_SIZE` değerini değiştirerek oyun boyutunu ayarlayın
- `speed` değerlerini değiştirerek zorluk seviyesini ayarlayın
- `ORIGINAL_LEVEL` dizisini değiştirerek yeni labirent tasarımları oluşturun

## 🙏 Teşekkürler

Klasik Pac-Man oyunundan esinlenilmiştir.

---

**İyi Eğlenceler! 🎮👻**
