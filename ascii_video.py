#!/usr/bin/env python3
"""
Renkli ASCII Video Dönüştürücü - GUI Versiyonu
Tkinter ile GUI penceresi içinde webcam ve ASCII çıktısını yan yana gösterir.
MP4 dosyası varsa onu kullanır, yoksa webcam kullanır.
"""

import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
import glob
import sys
import subprocess

def check_and_install_requirements():
    """Gerekli modülleri kontrol et ve kur"""
    required_packages = {
        'cv2': 'opencv-python',
        'PIL': 'pillow',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("📦 Eksik modüller kuruluyor...")
        for package in missing_packages:
            print(f"   → {package} kuruluyor...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        print("✅ Modüller başarıyla kuruldu!\n")

class ASCIIVideoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Renkli ASCII Video Dönüştürücü")
        self.root.geometry("1400x600")
        self.root.resizable(True, True)
        
        # Video kaynağını bul
        self.video_source = self.find_video_source()
        
        # Video kaynağını aç
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            print("Hata: Video kaynağı açılamadı!")
            return
        
        # Ayarlar
        self.ascii_width = 120
        self.ascii_height = 35
        self.running = True
        self.fps_limit = 60
        
        # ASCII karakter seti (en koyudan en açığa)
        self.ascii_chars = "@%#*+=-:. "
        self.ascii_len = len(self.ascii_chars)
        
        # GUI Bileşenleri
        self.setup_ui()
        
        # Video işleme thread'i
        self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()
        
        # Pencere kapatma
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def find_video_source(self):
        """MP4 dosyası ara, yoksa webcam kullan"""
        # Mevcut dizinde MP4 dosyası ara
        mp4_files = glob.glob("*.mp4")
        
        if mp4_files:
            video_file = mp4_files[0]
            print(f"✅ Video dosyası bulundu: {video_file}")
            return video_file
        else:
            print("📷 MP4 dosyası bulunamadı, webcam kullanılıyor...")
            return 0  # 0 = webcam
    
    def setup_ui(self):
        """GUI arayüzünü oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sol taraf - Orijinal Video/Webcam
        left_frame = ttk.LabelFrame(main_frame, text="Orijinal Video", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.video_label = tk.Label(left_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Sağ taraf - ASCII Çıktısı
        right_frame = ttk.LabelFrame(main_frame, text="Renkli ASCII Çıktısı", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # ASCII text widget
        self.ascii_text = tk.Text(
            right_frame,
            bg="black",
            fg="white",
            font=("Courier", 5),
            wrap=tk.NONE,
            state=tk.DISABLED
        )
        self.ascii_text.pack(fill=tk.BOTH, expand=True)
        
        # Kontrol paneli
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # FPS göstergesi
        self.fps_label = ttk.Label(control_frame, text="FPS: 0")
        self.fps_label.pack(side=tk.LEFT, padx=5)
        
        # Çıkış butonu
        exit_btn = ttk.Button(control_frame, text="Çıkış", command=self.on_closing)
        exit_btn.pack(side=tk.RIGHT, padx=5)
    
    def get_ascii_char(self, gray_value):
        """Gri değere karşılık gelen ASCII karakterini döndürür"""
        idx = int(gray_value / 256 * self.ascii_len)
        if idx >= self.ascii_len:
            idx = self.ascii_len - 1
        return self.ascii_chars[idx]
    
    def frame_to_colored_ascii(self, frame):
        """Kareyi ASCII sanatına dönüştürür (renksiz)"""
        try:
            # Yeniden boyutlandır
            resized = cv2.resize(frame, (self.ascii_width, self.ascii_height))
            
            # Gri tonlamaya çevir
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            
            lines = []
            h, w = gray.shape
            
            for y in range(h):
                line = ""
                for x in range(w):
                    gray_val = int(gray[y, x])
                    ascii_char = self.get_ascii_char(gray_val)
                    line += ascii_char
                
                lines.append(line)
            
            return "\n".join(lines)
        except Exception as e:
            print(f"ASCII dönüştürme hatası: {e}")
            return ""
    
    def video_loop(self):
        """Video işleme loop'u"""
        frame_count = 0
        fps_timer = time.time()
        frame_time = 1.0 / self.fps_limit
        last_frame_time = time.time()
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                # Video dosyası bitti, başa sar
                if isinstance(self.video_source, str):
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    continue
            
            # FPS kontrolü
            current_time = time.time()
            elapsed = current_time - last_frame_time
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)
            last_frame_time = time.time()
            
            # Video görüntüsünü göster
            self.update_video_display(frame)
            
            # ASCII çıktısını göster
            ascii_art = self.frame_to_colored_ascii(frame)
            self.update_ascii_display(ascii_art)
            
            frame_count += 1
            
            # FPS hesapla
            if frame_count % 30 == 0:
                elapsed = time.time() - fps_timer
                fps = frame_count / elapsed
                self.fps_label.config(text=f"FPS: {fps:.1f}")
    
    def update_video_display(self, frame):
        """Video görüntüsünü GUI'de göster"""
        try:
            # BGR'den RGB'ye çevir
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Boyutu ayarla (label'a sığması için)
            h, w = rgb.shape[:2]
            max_width = 600
            max_height = 500
            
            if w > max_width or h > max_height:
                scale = min(max_width / w, max_height / h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                rgb = cv2.resize(rgb, (new_w, new_h))
            
            # PIL Image'e çevir
            image = Image.fromarray(rgb)
            photo = ImageTk.PhotoImage(image)
            
            # Label'ı güncelle
            self.video_label.config(image=photo)
            self.video_label.image = photo
        except Exception as e:
            print(f"Video güncelleme hatası: {e}")
    
    def update_ascii_display(self, ascii_art):
        """ASCII çıktısını GUI'de göster"""
        try:
            self.ascii_text.config(state=tk.NORMAL)
            self.ascii_text.delete(1.0, tk.END)
            self.ascii_text.insert(1.0, ascii_art)
            self.ascii_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"ASCII güncelleme hatası: {e}")
    
    def on_closing(self):
        """Pencere kapatılırken temizlik yap"""
        self.running = False
        time.sleep(0.5)
        self.cap.release()
        self.root.destroy()

def main():
    # Modülleri kontrol et ve kur
    check_and_install_requirements()
    
    root = tk.Tk()
    app = ASCIIVideoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
