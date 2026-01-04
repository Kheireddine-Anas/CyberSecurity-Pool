
# arachnida - Web Scraping & Metadata Project

## Project Overview
This project is part of the 1337 School Cybersecurity Pool. It consists of two main tools:
- **spider**: Recursively downloads images from a website.
- **scorpion**: Extracts and displays metadata (EXIF, etc.) from image files.

## How It Works
- **spider**: Given a URL, downloads all images (jpg, jpeg, png, gif, bmp) from the site, optionally recursively and to a specified depth/path.
- **scorpion**: Given one or more image files, displays their metadata, including EXIF data and creation date.

## Usage

### 1. spider - Download Images
```bash
./spider [-r] [-l N] [-p PATH] URL
```
- `-r` : Recursively download images from the URL.
- `-l N` : Set maximum recursion depth (default: 5).
- `-p PATH` : Set download directory (default: ./data/).
- Supported extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

### 2. scorpion - Show Image Metadata
```bash
./scorpion FILE1 [FILE2 ...]
```
- Displays EXIF and other metadata for each image file.
- Supports the same extensions as spider.

## How the Technologies Work

### Web Scraping
- The spider tool makes HTTP requests to download web pages and parses them to find image links.
- It follows links recursively (if `-r` is set), up to the specified depth.
- Downloads images to the specified directory.

### Metadata Extraction
- The scorpion tool reads image files and extracts metadata such as EXIF tags, creation date, and more.
- EXIF data can include camera info, timestamps, GPS, and more.

## File Structure
```
arachnida/
├── Spider         # Image downloader
├── Scorpion       # Metadata extractor
└── README.md      # This file
```

## Notes
- Do not use wget, scrapy, or similar tools; all logic must be implemented by you.
- Bonus: Add metadata editing/deletion or a GUI for scorpion (only if mandatory part is perfect).

## References
- [EXIF standard](https://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf)
- [Web scraping basics](https://realpython.com/python-web-scraping-practical-introduction/)
