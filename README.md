# 📚 HSK1 Chinese Character Workbook Generator

A Python script that combines individual Chinese character practice worksheets into a single A4 PDF workbook with a styled cover page.

## ✨ Features

- 🎨 **Custom Cover Page**: Black sidebar with title and centered artwork
- 📄 **A4 Format**: All pages resized and centered to A4
- 🔢 **Page Numbers**: Automatic page numbering at the top of each page
- 🧹 **Clean Pages**: Removes unwanted images and hyperlinks from worksheets
- 🖋️ **Custom Fonts**: Uses HanyiSentyPagoda for Chinese characters

## 📋 Prerequisites

- Python 3.7+
- Required Python packages:
  ```bash
  pip install PyPDF2 reportlab
  ```

## 📁 Project Structure

```
chinese-sheet/
├── script.py              # Main script
├── cover.png              # Cover artwork image
├── fonts/                 # Font folder
│   └── HanyiSentyPagoda.ttf
├── worksheets/            # Input PDF folder
│   ├── 1.pdf
│   ├── 2.pdf
│   └── ...
└── Chinese_Workbook_A4.pdf  # Output (generated)
```

## 🚀 Usage

1. **Prepare your worksheets**:

   - Place individual character worksheet PDFs in the `worksheets/` folder
   - Name them numerically: `1.pdf`, `2.pdf`, `3.pdf`, etc.

2. **Add cover artwork**:

   - Place your cover image as `cover.png` in the project root
   - The image will be automatically centered on the cover page

3. **Run the script**:

   ```bash
   python script.py
   ```

4. **Output**:
   - The combined workbook will be saved as `Chinese_Workbook_A4.pdf`

## ⚙️ Configuration

Edit the configuration section in `script.py`:

```python
INPUT_DIR = "./worksheets"           # Input folder
OUTPUT_FILE = "Chinese_Workbook_A4.pdf"  # Output filename
COVER_IMAGE = "cover.png"            # Cover artwork
```

## 🎨 Cover Page Customization

The cover page includes:

- **Title**: "MY HSK1 壹 NOTEBOOK" (customizable in `make_final_cover()`)
- **Sidebar**: 55pt black sidebar on the left
- **Background**: Soft cream color (#F9F8F0)
- **Artwork**: Centered `cover.png` image

To customize the title, edit the text in `make_final_cover()`:

```python
c.drawString(title_x, A4_HEIGHT - 130, "MY")
c.drawString(title_x, hsk_y, "HSK1")
c.drawString(title_x + hsk_width + chinese_padding, hsk_y, "壹")
c.drawString(title_x, A4_HEIGHT - 245, "NOTEBOOK")
```

## 🔤 Font Requirements

The script uses:

- **Latin text**: Helvetica-Bold (built-in)
- **Chinese character on cover**: HanyiSentyPagoda (included in `fonts/` folder)

### Font Lookup Order

The script looks for the HanyiSentyPagoda font in this order:

1. `./fonts/HanyiSentyPagoda.ttf` (local folder - recommended)
2. `C:\Windows\Fonts\HanyiSentyPagoda.ttf` (system fonts)
3. `C:\Windows\Fonts\HanyiSentyPagoda_Regular.ttf` (system fonts)
4. Falls back to STSong-Light if not found

**Note**: The `fonts/` folder with `HanyiSentyPagoda.ttf` is included in the repository.

## 📝 Example Output

```
Found 14 files. Creating workbook with centered cover...

  1. 1.pdf
  2. 2.pdf
  ...
  14. 14.pdf

✅ Saved: Chinese_Workbook_A4.pdf (15 pages)
```

## 🛠️ Troubleshooting

**Issue**: Chinese characters not displaying correctly

- **Solution**: Ensure `fonts/HanyiSentyPagoda.ttf` exists in the project folder

**Issue**: Cover image not appearing

- **Solution**: Verify `cover.png` exists in the project root

**Issue**: Worksheets not in correct order

- **Solution**: Ensure worksheet PDFs are named with numbers only: `1.pdf`, `2.pdf`, etc.

## 📄 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Happy Learning! 加油！** 🎉
