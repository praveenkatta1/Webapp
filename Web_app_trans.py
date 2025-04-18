from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
 
app = Flask(__name__)
 
BLOG_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Web Translator</title>
<style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }
        h1 { color: #2c3e50; }
        p { line-height: 1.6; color: #34495e; }
        .lang-selector { margin-bottom: 20px; }
</style>
</head>
<body>
<h1>Welcome To Ascus Tech Private Limited Company</h1>
<p>Ascus Tech Private Limited is a modern software development company focused on delivering innovative, high-performance solutions for businesses across various sectors. We specialize in web development, cloud platforms, and data-driven applications.</p>
<p>Our team thrives on using powerful tools like Python and Flask to create secure, scalable web applications tailored to client needs. We believe in continuous learning and adaptability, keeping up with the latest in tech to build future-ready solutions.</p>
<p>Today, I'm excited to talk about my journey in learning Python and Flask! It's been a rewarding experience diving into backend development, understanding how web servers work, and creating my first dynamic applications. Stay tuned for tutorials, tips, and projects!</p>
</body>
</html>
"""
 
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ja': 'Japanese',
    'zh-cn': 'Chinese (Simplified)',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese'
}
 
def extract_text(html_content):
    """Extract visible text nodes from HTML content including the title."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    text_nodes = [element.strip() for element in soup.find_all(string=True) if element.strip()]
    return text_nodes, soup
 
def translate_text(text_nodes, target_language='es'):
    """Translate list of text nodes to the target language."""
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_nodes = []
        for text in text_nodes:
            translated = translator.translate(text)
            translated_nodes.append(translated)
        return translated_nodes
    except Exception as e:
        print(f"Translation error: {e}")
        return text_nodes
 
def replace_text_in_html(soup, original_texts, translated_texts):
    """Replace original text with translated text, including the <title>."""
    index = 0
    for element in soup.find_all(string=True):
        if element.strip():
            try:
                if index < len(original_texts) and element.strip() == original_texts[index]:
                    element.replace_with(translated_texts[index])
                index += 1
            except Exception as e:
                print(f"Error replacing text: {e}")
    return str(soup)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    languages = [(code, name) for code, name in LANGUAGES.items()]
    target_language = 'en'
    translated_html = BLOG_HTML
    page_title = "Web Translator"
 
    if request.method == 'POST':
        target_language = request.form.get('language', 'en')
        original_texts, soup = extract_text(BLOG_HTML)
        translated_texts = translate_text(original_texts, target_language)
        translated_soup = BeautifulSoup(replace_text_in_html(soup, original_texts, translated_texts), 'html.parser')
 
        page_title = translated_soup.title.string if translated_soup.title else page_title
        body_content = translated_soup.body.decode_contents()  # only body inner content
        translated_html = body_content
 
    return render_template(
        'translator.html',
        translated_html=translated_html,
        languages=languages,
        selected_language=target_language,
        page_title=page_title
    )
 
if __name__ == '__main__':
    app.run(debug=True)
