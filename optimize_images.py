"""
Script d'optimisation des images PNG pour réduire la taille des fichiers
sans perte significative de qualité.
"""
import os
from PIL import Image
import glob

def optimize_png(file_path, quality=85, max_width=800):
    """
    Optimise une image PNG en la redimensionnant et en la compressant.
    
    Args:
        file_path: Chemin vers l'image
        quality: Qualité de compression (1-100)
        max_width: Largeur maximale en pixels
    """
    try:
        with Image.open(file_path) as img:
            # Obtenir la taille originale
            original_size = os.path.getsize(file_path)
            width, height = img.size
            
            # Redimensionner si nécessaire
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"  ↓ Redimensionné: {width}x{height} → {max_width}x{new_height}")
            
            # Convertir en RGB si nécessaire (pour JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Garder la transparence pour PNG
                img.save(file_path, 'PNG', optimize=True)
            else:
                # Convertir en JPEG pour meilleure compression
                rgb_img = img.convert('RGB')
                jpeg_path = file_path.replace('.png', '.jpg')
                rgb_img.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
                
                # Supprimer l'ancien PNG si le JPEG est plus petit
                new_size = os.path.getsize(jpeg_path)
                if new_size < original_size:
                    os.remove(file_path)
                    print(f"  ✓ Converti en JPEG: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB")
                else:
                    os.remove(jpeg_path)
                    img.save(file_path, 'PNG', optimize=True)
                    new_size = os.path.getsize(file_path)
                    print(f"  ✓ Optimisé PNG: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB")
            
    except Exception as e:
        print(f"  ✗ Erreur: {e}")

def optimize_directory(directory, quality=85, max_width=800):
    """
    Optimise toutes les images PNG dans un répertoire.
    """
    png_files = glob.glob(os.path.join(directory, '*.png'))
    
    if not png_files:
        print(f"Aucune image PNG trouvée dans {directory}")
        return
    
    print(f"\n📁 Optimisation de {len(png_files)} images dans {directory}...")
    
    total_before = 0
    total_after = 0
    
    for png_file in png_files:
        print(f"\n🖼️  {os.path.basename(png_file)}")
        size_before = os.path.getsize(png_file)
        total_before += size_before
        
        optimize_png(png_file, quality, max_width)
        
        # Vérifier le nouveau fichier (peut être .jpg maintenant)
        base_name = png_file.replace('.png', '')
        if os.path.exists(f"{base_name}.jpg"):
            size_after = os.path.getsize(f"{base_name}.jpg")
        elif os.path.exists(png_file):
            size_after = os.path.getsize(png_file)
        else:
            size_after = 0
        
        total_after += size_after
    
    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ:")
    print(f"   Taille avant: {total_before/1024/1024:.2f} MB")
    print(f"   Taille après: {total_after/1024/1024:.2f} MB")
    print(f"   Économie: {(total_before-total_after)/1024/1024:.2f} MB ({(1-total_after/total_before)*100:.1f}%)")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Optimiser les images des partenaires
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    print("🚀 OPTIMISATION DES IMAGES - CONSEILUX")
    print("="*60)
    
    # Optimiser les logos de partenaires (plus petits)
    images_dir = os.path.join(static_dir, 'images')
    if os.path.exists(images_dir):
        optimize_directory(images_dir, quality=85, max_width=400)
    
    # Optimiser les logos de certifications (plus petits)
    logos_dir = os.path.join(static_dir, 'logos')
    if os.path.exists(logos_dir):
        optimize_directory(logos_dir, quality=85, max_width=300)
    
    print("✅ Optimisation terminée !")
    print("\n⚠️  IMPORTANT: Vérifiez les images avant de commit.")
    print("   Certaines images PNG ont été converties en JPEG.")
