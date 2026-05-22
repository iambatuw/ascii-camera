#!/usr/bin/env python3
"""
Otomatik Kurulum Scripti
Gerekli tüm modülleri otomatik olarak kurar.
"""

import subprocess
import sys
import os

def install_requirements():
    """requirements.txt dosyasındaki modülleri kur"""
    print("=" * 60)
    print("Renkli ASCII Video Dönüştürücü - Otomatik Kurulum")
    print("=" * 60)
    print()
    
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"Hata: {requirements_file} dosyası bulunamadı!")
        return False
    
    print(f"📦 Modüller kuruluyor ({requirements_file})...")
    print()
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", requirements_file
        ])
        print()
        print("✅ Tüm modüller başarıyla kuruldu!")
        print()
        return True
    except subprocess.CalledProcessError as e:
        print()
        print(f"❌ Kurulum sırasında hata oluştu: {e}")
        return False

def main():
    success = install_requirements()
    
    if success:
        print("=" * 60)
        print("🎉 Kurulum tamamlandı!")
        print("=" * 60)
        print()
        print("Uygulamayı başlatmak için:")
        print("  python ascii_video.py")
        print()
        return 0
    else:
        print("=" * 60)
        print("❌ Kurulum başarısız oldu!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())