import os
import re

# Read pravovaya.txt
with open('d:/Workspace/Web/PGATK Website/pravovaya.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract text block for Injury Prevention
start_marker = '<p style="text-align: justify;"><strong>Травматизм</strong>'
end_marker = '<p style="text-align: justify;">&nbsp;</p>\t</div>'

start_idx = text.find(start_marker)
end_idx = text.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    raw_html = text[start_idx:end_idx].strip()
else:
    # Fallback to general start
    start_idx = text.find('<strong>Травматизм</strong>')
    raw_html = text[start_idx-35:end_idx]

# Clean up raw HTML
# Remove AllVideos plugins comments and divs
raw_html = re.sub(r'<!-- JoomlaWorks.*?ends here -->', '', raw_html, flags=re.DOTALL)
raw_html = re.sub(r'<!-- JoomlaWorks.*?starts here -->', '', raw_html, flags=re.DOTALL)
raw_html = re.sub(r'<div class="avPlayerWrapper.*?</div>\s*</div>\s*</div>', '', raw_html, flags=re.DOTALL)

# REMOVE Widgetkit / UIkit gallery code that is causing crosses
raw_html = re.sub(r'<div class="uk-scope".*?</script>\s*</div>', '', raw_html, flags=re.DOTALL)

# Remove all inline images inside the raw HTML
raw_html = re.sub(r'<p[^>]*>\s*<img[^>]+>\s*</p>', '', raw_html)
raw_html = re.sub(r'<img[^>]+>', '', raw_html)

# Convert <p style="text-align: justify;"> to <p className="text-justify mb-6">
raw_html = raw_html.replace('<p style="text-align: justify;">', '<p className="text-justify mb-6">')
raw_html = raw_html.replace('<p>', '<p className="text-justify mb-6">')

# Add styling to links
raw_html = raw_html.replace('<a ', '<a className="text-amber-600 hover:text-amber-700 underline font-medium" ')

# Fix any unescaped backticks or ${
raw_html = raw_html.replace('`', '\\`').replace('${', '\\${')

# The glitchy word
raw_html = re.sub(r'[^\w\s\.\<\>\/\=\"\'-_]+гольного опьянения', 'алкогольного опьянения', raw_html)

tsx_content = f"""import React, {{ useState }} from 'react';
import {{ ShieldAlert, ChevronLeft, ChevronRight, X }} from 'lucide-react';

const Lightbox = ({{ images, selectedIndex, onClose, onSelectIndex }}: any) => {{
  if (selectedIndex === null) return null;

  const handleNext = (e: any) => {{
    e.stopPropagation();
    onSelectIndex((selectedIndex + 1) % images.length);
  }};

  const handlePrev = (e: any) => {{
    e.stopPropagation();
    onSelectIndex((selectedIndex - 1 + images.length) % images.length);
  }};

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90" onClick={{onClose}}>
      <button onClick={{onClose}} className="absolute top-4 right-4 text-white hover:text-gray-300">
        <X className="w-8 h-8" />
      </button>
      <button onClick={{handlePrev}} className="absolute left-4 text-white hover:text-gray-300">
        <ChevronLeft className="w-12 h-12" />
      </button>
      <button onClick={{handleNext}} className="absolute right-4 text-white hover:text-gray-300">
        <ChevronRight className="w-12 h-12" />
      </button>
      <div className="relative max-w-7xl max-h-[90vh] mx-4" onClick={{e => e.stopPropagation()}}>
        <img src={{images[selectedIndex]}} alt="Памятка" className="max-w-full max-h-[90vh] object-contain rounded-lg" />
      </div>
    </div>
  );
}};

export default function InjuryPrevention() {{
  const [selectedImage, setSelectedImage] = useState<number | null>(null);

  const images = [
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/1.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/2.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/3.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/4.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/5.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/6.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/VnimanieGololed_1.jpg',
    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/VnimanieGololed_2.jpg'
  ];

  return (
    <div className="bg-slate-50 min-h-screen pb-20 font-sans pt-12">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-amber-600 p-8 text-white text-center">
            <ShieldAlert className="w-16 h-16 mx-auto mb-4 opacity-90" />
            <h1 className="text-3xl md:text-4xl font-bold mb-2">Профилактика травматизма</h1>
            <p className="text-amber-100 text-lg">Сохранение жизни и здоровья — наш главный приоритет</p>
          </div>

          <div className="p-8 md:p-12">
            <div className="prose prose-lg max-w-none prose-amber" dangerouslySetInnerHTML={{{{ __html: `{raw_html}` }}}} />
          </div>
        </div>

        {{/* Image Gallery */}}
        <div className="max-w-6xl mx-auto mt-12">
          <h2 className="text-3xl font-bold text-slate-800 mb-8 text-center flex items-center justify-center gap-4">
            <span className="w-12 h-1 bg-amber-500 rounded-full"></span>
            Памятки
            <span className="w-12 h-1 bg-amber-500 rounded-full"></span>
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {{images.map((src, index) => (
              <div 
                key={{index}} 
                className="group relative aspect-[3/4] bg-slate-100 rounded-xl overflow-hidden cursor-pointer shadow-md hover:shadow-xl transition-all duration-300"
                onClick={{() => setSelectedImage(index)}}
              >
                <img 
                  src={{src}} 
                  alt={{`Памятка ${{index + 1}}`}}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300 flex items-center justify-center">
                  <span className="bg-white/90 text-slate-900 px-4 py-2 rounded-full font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300 transform translate-y-4 group-hover:translate-y-0">
                    Увеличить
                  </span>
                </div>
              </div>
            ))}}
          </div>
        </div>

        {{/* Video Gallery */}}
        <div className="max-w-5xl mx-auto mt-16 mb-8">
          <h2 className="text-3xl font-bold text-slate-800 mb-8 text-center flex items-center justify-center gap-4">
            <span className="w-12 h-1 bg-amber-500 rounded-full"></span>
            Видеоматериалы
            <span className="w-12 h-1 bg-amber-500 rounded-full"></span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="aspect-video rounded-xl overflow-hidden shadow-lg border border-slate-200">
              <iframe src="https://www.youtube.com/embed/PXYN_uQ6h04" className="w-full h-full" allowFullScreen></iframe>
            </div>
            <div className="aspect-video rounded-xl overflow-hidden shadow-lg border border-slate-200">
              <iframe src="https://www.youtube.com/embed/rV58Qz1zFik" className="w-full h-full" allowFullScreen></iframe>
            </div>
            <div className="aspect-video rounded-xl overflow-hidden shadow-lg border border-slate-200">
              <iframe src="https://www.youtube.com/embed/LEx7AlOvX3w" className="w-full h-full" allowFullScreen></iframe>
            </div>
            <div className="aspect-video rounded-xl overflow-hidden shadow-lg border border-slate-200">
              <iframe src="https://www.youtube.com/embed/yNXvmKG1RK0" className="w-full h-full" allowFullScreen></iframe>
            </div>
          </div>
        </div>

      </div>

      {{/* Lightbox */}}
      <Lightbox 
        images={{images}}
        selectedIndex={{selectedImage}}
        onClose={{() => setSelectedImage(null)}}
        onSelectIndex={{setSelectedImage}}
      />
    </div>
  );
}}
"""

with open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'w', encoding='utf-8') as f:
    f.write(tsx_content)

print('Rewrite complete without inline images or widgetkit crosses')
