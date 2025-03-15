#!/usr/bin/env python3
import os
import requests
from urllib.parse import urlparse
from pathlib import Path

def download_image(url, save_path):
    """
    Download an image from a URL and save it to the specified path.
    
    Args:
        url (str): URL of the image to download
        save_path (str): Path where the image will be saved
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Save the image
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                
        print(f"Successfully downloaded: {save_path}")
        
    except Exception as e:
        print(f"Error downloading {url} to {save_path}: {e}")

def main():
    # Base directory for static files
    base_dir = 'static/images'
    
    # Dictionary mapping file paths to image URLs
    images = {
        # Banner Images
        f'{base_dir}/electronics-banner.jpg': 'https://thumbs.dreamstime.com/z/electronics-online-shopping-banner-devices-delivery-box-270532354.jpg',
        f'{base_dir}/clothing-banner.jpg': 'https://img.freepik.com/free-photo/online-fashion-shopping-concept_23-2150401320.jpg',
        f'{base_dir}/summer-collection.jpg': 'https://img.freepik.com/free-photo/flat-lay-summer-vacation-concept_23-2149395979.jpg',
        
        # Placeholder Images
        f'{base_dir}/product-placeholder.jpg': 'https://placehold.co/400x400/f0f0f0/a0a0a0?text=Product+Image',
        f'{base_dir}/category-placeholder.jpg': 'https://placehold.co/600x400/f0f0f0/a0a0a0?text=Category+Image',
        f'{base_dir}/amazon-logo.png': 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
        f'{base_dir}/amazon-logo-white.png': 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
        
        # Category Images
        f'{base_dir}/category-men.jpg': 'https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg',
        f'{base_dir}/category-women.jpg': 'https://images.pexels.com/photos/709790/pexels-photo-709790.jpeg',
        f'{base_dir}/category-kids.jpg': 'https://images.pexels.com/photos/346796/pexels-photo-346796.jpeg',
        f'{base_dir}/category-accessories.jpg': 'https://images.pexels.com/photos/691046/pexels-photo-691046.jpeg',
        
        # Fashion Blog Images
        f'{base_dir}/fashion-blog-1.jpg': 'https://images.pexels.com/photos/6626903/pexels-photo-6626903.jpeg',
        f'{base_dir}/fashion-blog-2.jpg': 'https://images.pexels.com/photos/1884581/pexels-photo-1884581.jpeg',
        f'{base_dir}/fashion-blog-3.jpg': 'https://images.pexels.com/photos/1884583/pexels-photo-1884583.jpeg',
        
        # Default Banner
        f'{base_dir}/banners/default-banner.jpg': 'https://m.media-amazon.com/images/G/31/Gateway/Toys/XCM_Manual_1462830_4676843_1500x300_1X._CB569915225_.jpg',
        
        # Electronics Brand Logos
        f'{base_dir}/brands/apple.png': 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg',
        f'{base_dir}/brands/samsung.png': 'https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg',
        f'{base_dir}/brands/sony.png': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg',
        f'{base_dir}/brands/dell.png': 'https://upload.wikimedia.org/wikipedia/commons/1/18/Dell_logo_2016.svg',
        f'{base_dir}/brands/lg.png': 'https://upload.wikimedia.org/wikipedia/commons/b/bf/LG_logo_%282015%29.svg',
        
        # Clothing Brand Logos
        f'{base_dir}/brands/levis.png': 'https://upload.wikimedia.org/wikipedia/commons/7/75/Levi%27s_logo.svg',
        f'{base_dir}/brands/zara.png': 'https://upload.wikimedia.org/wikipedia/commons/f/fd/Zara_Logo.svg',
        f'{base_dir}/brands/adidas.png': 'https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg',
        f'{base_dir}/brands/nike.png': 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg',
        f'{base_dir}/brands/gap.png': 'https://upload.wikimedia.org/wikipedia/commons/6/69/Gap_logo.svg',
        f'{base_dir}/brands/puma.png': 'https://upload.wikimedia.org/wikipedia/commons/8/88/Puma_logo.svg',
        
        # Product Images
        f'{base_dir}/products/echo.png': 'https://m.media-amazon.com/images/I/61MbLLagiVL._AC_UY218_.jpg',
        f'{base_dir}/products/firetv.png': 'https://m.media-amazon.com/images/I/41Y7P2QEBOL._AC_UY218_.jpg',
        f'{base_dir}/products/iphone.png': 'https://m.media-amazon.com/images/I/618Bb+QzDmL._AC_UY218_.jpg',
        f'{base_dir}/products/anker.png': 'https://cdn.shopify.com/s/files/1/0765/2137/3999/files/A1695_Amazon_Listing_Copy-TD_PD_UK_V1.png',
        f'{base_dir}/products/guitar.png': 'https://m.media-amazon.com/images/I/51PDJU+-mNL.jpg',
        f'{base_dir}/products/skateboard.png': 'https://images.onewheel.com/home/4-pint-x-homepage-mobile@2x.jpg',
        f'{base_dir}/products/espresso.png': 'https://www.wacaco.com/cdn/shop/products/Barista_Kit-PNG--001-LD.png',
        f'{base_dir}/products/smartphone.png': 'https://gallery.yopriceville.com/var/albums/Free-Clipart-Pictures/Hi-Tech-PNG/Mobile_Phone_Transparent_PNG_Clip_Art_Image.png',
    }
    
    # Download each image
    for filepath, url in images.items():
        download_image(url, filepath)
    
    print("\nImage download complete!")
    print(f"Downloaded {len(images)} images to the project directories.")
    print("\nIf some images failed to download, you may need to manually download them from the URLs provided.")

if __name__ == "__main__":
    main()