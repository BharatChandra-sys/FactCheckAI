# Extension ZIP Setup

To make the download work, you need to:

1. **Create the extension ZIP file:**
   ```bash
   cd C:\Users\bc833\Downloads\fake-news-extension
   # Create a ZIP of the extension folder
   Compress-Archive -Path extension -DestinationPath factcheckai-website\public\factcheckai-extension.zip
   ```

2. **The ZIP file should be placed at:**
   `factcheckai-website/public/factcheckai-extension.zip`

3. **Users will download it from:**
   `https://yourdomain.com/factcheckai-extension.zip`

## What to include in the ZIP:
- The entire `/extension` folder
- All manifest files
- All popup HTML/CSS/JS files
- All background scripts
- All content scripts
- Icons and assets

## Note:
The installation guide at `/install` page will guide users through:
1. Downloading the ZIP
2. Extracting it
3. Loading it as an unpacked extension in Chrome/Edge
