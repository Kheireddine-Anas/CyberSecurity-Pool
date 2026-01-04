

# Cybersecurity Pool - 1337 School

Collection of cybersecurity projects from the 1337 School Cybersecurity Pool.

## Projects

### ✅ Arachnida
Introductory project to web scraping and metadata extraction.
See arachnida/README.md for details.

### ✅ ft_otp
Time-based One-Time Password (TOTP) implementation.
See ft_otp/README.md for details.


### ✅ Arachnida
**Summary:** Introductory project to web scraping and metadata.
**Version:** 1.00

#### Contents
1. [Introduction](#introduction)
2. [Prologue](#prologue)
3. [Mandatory Part](#mandatory-part)
4. [Exercise 1 - Spider](#exercise-1---spider)
5. [Exercise 2 - Scorpion](#exercise-2---scorpion)
6. [Bonus Part](#bonus-part)
7. [Submission and Peer-evaluation](#submission-and-peer-evaluation)

#### 1. Introduction
This project will allow you to process data from the web:
- Create a program to automatically extract information from the web.
- Create a second program to analyze these files and manipulate the metadata.
Metadata is information describing other data, often found in images and documents, and can reveal sensitive information about their creators or editors.

#### 2. Prologue
Arachnids are a class of chelicerate arthropods with over 100,000 species, including spiders, ticks, scorpions, and mites. Their main features are four pairs of legs and chelicerae for grabbing food.

#### 3. Mandatory Part
You must create two programs (scripts or binaries):
- **spider**: Extracts all images from a website recursively, given a URL.
- **scorpion**: Parses image files for EXIF and other metadata, displaying them.
You may use libraries for HTTP requests and file handling, but the core logic must be your own. Using tools like wget or scrapy is forbidden.

#### 4. Exercise 1 - Spider
Extracts all images from a website recursively.
**Usage:** `./spider [-r -l N -p PATH] URL`
- `-r`: Recursively download images from the URL.
- `-r -l [N]`: Set maximum recursion depth (default: 5).
- `-p [PATH]`: Set download directory (default: ./data/).
Supported extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

#### 5. Exercise 2 - Scorpion
Receives image files as parameters and parses them for EXIF and other metadata.
**Usage:** `./scorpion FILE1 [FILE2 ...]`
Must support the same extensions as spider. Displays basic attributes and EXIF data.

#### 6. Bonus Part
- Option to modify/delete metadata in scorpion.
- Graphical interface for viewing/managing metadata.
Bonus is only evaluated if the mandatory part is perfect.

#### 7. Submission and Peer-evaluation
Submit your assignment in your Git repository. Only repository content will be evaluated. Double-check folder and file names.

### 🚧 ft_otp
Time-based One-Time Password (TOTP) implementation
- Based on RFC 6238 and RFC 4226
- Secure key storage and OTP generation


## Structure

```
cyber_security_pool/
├── arachnida/
│   └── README.md
├── ft_otp/
│   └── README.md
└── [future projects]
```


## About

This repository contains security-focused projects covering:
- Web scraping and reconnaissance
- Cryptography and authentication systems


## Author

1337 School - Cybersecurity Pool
