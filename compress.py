import joblib
import os

print("🔄 Modeller sıkıştırılıyor, lütfen bekleyin...")

# Orta segment modelini yükle ve sıkıştırarak yeniden kaydet
if os.path.exists('apple_orta_rf_model.pkl'):
    orta = joblib.load('apple_orta_rf_model.pkl')
    # compress=9 en yüksek sıkıştırma seviyesidir
    joblib.dump(orta, 'apple_orta_rf_model_compressed.pkl', compress=9)
    print("✅ Orta segment modeli başarıyla sıkıştırıldı! -> apple_orta_rf_model_compressed.pkl")

# Premium segment modelini yükle ve sıkıştırarak yeniden kaydet
if os.path.exists('apple_premium_rf_model.pkl'):
    premium = joblib.load('apple_premium_rf_model.pkl')
    joblib.dump(premium, 'apple_premium_rf_model_compressed.pkl', compress=9)
    print("✅ Premium segment modeli başarıyla sıkıştırıldı! -> apple_premium_rf_model_compressed.pkl")

print("🎉 İşlem tamamlandı!")