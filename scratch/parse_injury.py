import re
import json

def generate():
    with open('d:/Workspace/Web/PGATK Website/pravovaya.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # The text we care about is inside <div itemprop="articleBody"> ... </div>
    # Actually, we can just extract from lines 15 to 18 in pravovaya.txt which is the paragraphs.
    lines = text.split('\n')
    p_lines = lines[14:18] # index 14 is line 15
    
    # We will join them and format it
    content = '\n'.join(p_lines)
    
    content = content.replace('class="', 'className="')
    content = content.replace('style="text-align: justify;"', 'className="text-justify mb-6"')
    content = content.replace('style="text-align: center;"', 'className="text-center mb-6"')
    content = content.replace('style="text-align: left;"', 'className="text-left mb-6"')
    
    # The links are currently <a href="...">...</a>. Let's make them style nicely
    content = content.replace('<a href=', '<a className="text-amber-600 hover:text-amber-700 underline font-medium" href=')
    content = content.replace('<br>', '<br />')

    # Images
    # There are 12 images: /images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/1.jpg to 12.jpg
    images_str = "[\n"
    for i in range(1, 13):
        images_str += f"    '/images/1Novosti/2023/Noybr/ProfilaktikaTravmatizma/{i}.jpg',\n"
    images_str += "  ]"

    tsx_content = f"""import React, {{ useState }} from 'react';
import {{ ShieldAlert, Activity, ChevronLeft, ChevronRight, X, AlertTriangle, Crosshair }} from 'lucide-react';
import {{ Lightbox }} from '../components/Lightbox';

export default function InjuryPrevention() {{
  const [selectedImage, setSelectedImage] = useState<number | null>(null);

  const images = {images_str};

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {{/* Hero Section */}}
      <div className="bg-gradient-to-br from-amber-600 via-orange-600 to-red-700 py-16 px-4 md:px-8 shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/black-scales.png')] opacity-10"></div>
        <div className="absolute -left-20 -bottom-20 w-64 h-64 bg-amber-400 rounded-full blur-[100px] opacity-20"></div>
        
        <div className="max-w-4xl mx-auto relative z-10 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/20 backdrop-blur-sm border border-white/30 mb-6 text-amber-100">
            <ShieldAlert className="w-8 h-8" />
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold text-white mb-6 leading-tight">
            Профилактика травматизма
          </h1>
          <p className="text-amber-50 text-lg md:text-xl max-w-2xl mx-auto opacity-90">
            Важная информация о причинах и способах предупреждения производственного, бытового, транспортного и других видов травматизма.
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 md:px-8 -mt-8 relative z-20">
        
        {{/* Content */}}
        <div className="bg-white rounded-3xl shadow-xl border border-slate-100 overflow-hidden mb-12 p-8 md:p-12">
          <div className="prose prose-slate max-w-none text-slate-700 md:text-lg leading-relaxed">
            <div dangerouslySetInnerHTML={{{{ __html: {repr(content)} }}}} />
          </div>
        </div>

        {{/* Image Gallery */}}
        <h2 className="text-3xl font-bold text-slate-800 mb-8 text-center flex items-center justify-center gap-4">
          <AlertTriangle className="w-8 h-8 text-amber-500" />
          Информационные материалы
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-12">
          {{images.map((src, index) => (
            <div 
              key={{index}} 
              className="aspect-[3/4] rounded-xl overflow-hidden shadow-sm hover:shadow-xl transition-all cursor-pointer group relative border border-slate-200 bg-slate-100"
              onClick={{() => setSelectedImage(index)}}
            >
              <img 
                src={{src}} 
                alt={{`Памятка ${{index + 1}}`}} 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                onError={{(e) => {{
                  (e.target as HTMLImageElement).src = 'https://placehold.co/600x800/e2e8f0/94a3b8?text=%D0%9D%D0%B5%D1%82+%D1%84%D0%BE%D1%82%D0%BE';
                }}}}
              />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300" />
            </div>
          ))}}
        </div>

      </div>

      {{/* Lightbox */}}
      <Lightbox 
        images={{images}}
        selectedIndex={{selectedImage}}
        onClose={{() => setSelectedImage(null)}}
      />
    </div>
  );
}}
"""
    with open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'w', encoding='utf-8') as f:
        f.write(tsx_content)

if __name__ == '__main__':
    generate()
