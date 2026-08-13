# Embedding Model Karşılaştırması

Soru–SQL eşleştirme sistemi için 6 farklı embedding modelinin karşılaştırılması.

## Amaç

Kullanıcının doğal dilde sorduğu bir soruyu (örn. "Bu ay ne kadar ciro yaptım?"), önceden hazırlanmış `golden_queries` veri setindeki doğru SQL sorgusuyla eşleştirebilecek en uygun embedding modelini bulmak.

## Kullanılan Veri

`golden_queries_.json` — 1.525 soru-SQL çifti. 5 adet duplicate soru tespit edilip çıkarıldı, 1.520 kayıtla devam edildi.

## Test Edilen Modeller

- **multilingual-e5-large** (zorunlu referans model)
- **BAAI/bge-m3**
- **emrecan/bert-base-turkish-cased-mean-nli-stsb-tr**
- **selmanbaysan/bert-base-turkish-uncased-cachedmnrl-contrastive-loss**
- **atasoglu/1mb-turkish-embeddings**
- **Cohere embed-multilingual-v3.0** (bulut tabanlı)

## Yöntem

1. Her modelle veri setindeki sorular vektörleştirilip FAISS ile indekslendi.
2. Arama, cosine similarity ile yapıldı.
3. Veri setinden 100 soru seçilip anlamı korunarak farklı şekilde yeniden yazıldı (paraphrase), test seti olarak kullanıldı.
4. Her model için Recall@1, Recall@3, MRR, ortalama sorgu süresi, RAM kullanımı ve maliyet ölçüldü.

## Sonuçlar

| Model | Recall@1 | Recall@3 | MRR | Hız (ms) |
|---|---|---|---|---|
| multilingual-e5-large | %88 | %94 | 0.9083 | 78.10 |
| BAAI/bge-m3 | %83 | %90 | 0.8650 | 82.38 |
| emrecan | %83 | %94 | 0.8800 | 22.69 |
| selmanbaysan/trmteb | %80 | %91 | 0.8500 | 21.50 |
| atasoglu/1mb | %9 | %21 | 0.1383 | 0.17 |
| Cohere embed-multilingual-v3.0 | %89 | %97 | 0.9300 | 7.91 |

Detaylı analiz ve öneri için `rapor.pdf` dosyasına bakın.

## Klasör Yapısı

```
├── data/              # Veri setleri, metadata, sonuç dosyaları
├── index/             # Her model için indeks oluşturma script'leri
├── evaluate/           # Her model için değerlendirme script'leri
├── outputs/           # Üretilen grafikler
├── pareto.ipynb        # Doğruluk-hız karşılaştırma analizi
├── rapor.pdf          # Detaylı proje raporu
└── notes.md           # Çalışma notları
```

## Nasıl Çalıştırılır

Her model için iki script var: önce `index/build_index_<model>.py` ile indeks oluşturulur, sonra `evaluate/evaluate_<model>.py` ile test edilir.

```bash
python index/build_index_e5_large.py
python evaluate/evaluate_e5_large.py
```

## Sonuç

Doğruluk, hız, RAM ve maliyet bir arada değerlendirildiğinde **Cohere embed-multilingual-v3.0** öne çıkıyor. Veri gizliliği önemliyse ya da yerel/offline çalışmak gerekiyorsa, **emrecan** veya **selmanbaysan/trmteb** düşük doğruluk kaybıyla iyi bir alternatif sunuyor.
