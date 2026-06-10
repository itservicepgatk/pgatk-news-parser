import re

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find intro
    intro_match = re.search(r'<div itemprop="articleBody">(.*?)<dl class="tabs"', content, re.DOTALL)
    intro_html = intro_match.group(1).strip() if intro_match else ""

    # Find tabs
    tabs_match = re.search(r'<dl class="tabs".*?>(.*?)</dl>', content, re.DOTALL)
    tabs_html = tabs_match.group(1).strip() if tabs_match else ""
    
    # Extract tab titles
    tab_titles = []
    for m in re.finditer(r'<dt.*?<h3><a.*?>(.*?)</a></h3>', tabs_html, re.DOTALL):
        tab_titles.append(m.group(1).strip())
        
    # Extract tab contents
    # Find all <dd ...>...</dd>
    # The first dd might be empty or skipped based on the html
    dd_matches = re.findall(r'<dd[^>]*>(.*?)</dd>', content, re.DOTALL)
    
    # Usually the first <dd> is a duplicate of intro or empty
    # In our case:
    # <dt style="display:none;"></dt><dd style="display:none;"> ... intro duplicate ... </dd>
    # Then <dt ... tab1 >, <dt ... tab2 > ...
    # Then <div class="current"><dd ...> tab1 content </dd>
    # Then <dd ...> tab2 content </dd>
    
    # Clean up dd_matches by checking their content
    # Let's just find the tabs exactly
    
    tab_contents = []
    
    # Find the section after </dl> which contains the <dd> tags
    # Wait, the <dd> tags are actually inside the dl, or mixed?
    # Let's extract <dd ...>(.*?)</dd>
    
    valid_dds = []
    for dd in dd_matches:
        text = dd.strip()
        if "О Государственной программе" in text and "О дополнительных мерах" in text:
            continue # This is the duplicate intro
        valid_dds.append(text)
        
    # Zip titles and contents
    tabs = []
    for i in range(min(len(tab_titles), len(valid_dds))):
        tabs.append({
            "title": tab_titles[i],
            "content": valid_dds[i]
        })
        
    return intro_html, tabs

def generate_tsx(intro, tabs, out_path):
    # Convert HTML links in intro from /zdorovyj-obraz-zhizni... to React Router Link or normal a
    intro = intro.replace('class="', 'className="')
    intro = intro.replace('style="text-align: justify;"', 'className="text-justify mb-4"')
    intro = intro.replace('style="text-align: center;"', 'className="text-center mb-4"')
    intro = intro.replace('style="text-align: left;"', 'className="text-left mb-4"')
    
    # Remove empty <p>&nbsp;</p>
    intro = intro.replace('<p>&nbsp;</p>', '')
    intro = intro.replace('<hr>', '<hr className="my-6 border-slate-200" />')
    intro = intro.replace('<ul', '<ul className="list-disc pl-6 space-y-2 mb-4"')
    intro = intro.replace('<ol', '<ol className="list-decimal pl-6 space-y-2 mb-4"')

    tab_data_str = "[\n"
    for t in tabs:
        content = t['content']
        content = content.replace('class="', 'className="')
        content = content.replace('style="text-align: justify;"', 'className="text-justify mb-4"')
        content = content.replace('style="text-align: center;"', 'className="text-center mb-4"')
        content = content.replace('style="text-align: left;"', 'className="text-left mb-4"')
        content = content.replace('<ul', '<ul className="list-disc pl-6 space-y-2 mb-4"')
        content = content.replace('<ol', '<ol className="list-decimal pl-6 space-y-2 mb-4"')
        
        # Escape quotes for JSON string
        import json
        tab_data_str += f"  {{\n    title: {json.dumps(t['title'])},\n    content: {json.dumps(content)}\n  }},\n"
    tab_data_str += "]"

    tsx_content = f"""import React, {{ useState }} from 'react';
import {{ HeartPulse, Activity, Leaf, ShieldAlert, FileText, ChevronRight, Apple }} from 'lucide-react';
import {{ Link }} from 'react-router-dom';

export default function HealthyLifestyle() {{
  const [activeTab, setActiveTab] = useState(0);

  const tabs = {tab_data_str};

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {{/* Hero Section */}}
      <div className="bg-gradient-to-br from-emerald-600 via-green-600 to-teal-700 py-16 px-4 md:px-8 shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
        <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-emerald-400 rounded-full blur-[100px] opacity-20"></div>
        
        <div className="max-w-4xl mx-auto relative z-10 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/20 backdrop-blur-sm border border-white/30 mb-6 text-green-100">
            <HeartPulse className="w-8 h-8" />
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold text-white mb-6 leading-tight">
            Здоровый образ жизни
          </h1>
          <p className="text-green-50 text-lg md:text-xl max-w-2xl mx-auto opacity-90">
            Здоровье нации, физическое развитие и пропаганда здорового образа жизни
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 md:px-8 -mt-8 relative z-20">
        
        {{/* Intro Content */}}
        <div className="bg-white rounded-3xl shadow-xl border border-slate-100 overflow-hidden mb-12 p-8 md:p-12">
          <div className="prose prose-slate max-w-none text-slate-700 md:text-lg leading-relaxed space-y-4">
            <div dangerouslySetInnerHTML={{{{ __html: {repr(intro)} }}}} />
          </div>
        </div>

        {{/* Tabs Section */}}
        <div className="flex flex-col lg:flex-row gap-8">
          
          {{/* Tabs Navigation */}}
          <div className="lg:w-1/3 shrink-0">
            <div className="bg-white rounded-2xl shadow-md border border-slate-100 overflow-hidden sticky top-24">
              <div className="p-4 bg-emerald-50 border-b border-emerald-100 text-emerald-800 font-bold flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Материалы по ЗОЖ
              </div>
              <div className="flex flex-col">
                {{tabs.map((tab, idx) => (
                  <button
                    key={{idx}}
                    onClick={{() => setActiveTab(idx)}}
                    className={{`text-left px-5 py-4 border-b border-slate-50 last:border-0 transition-colors flex items-center justify-between group ${{
                      activeTab === idx 
                        ? 'bg-emerald-500 text-white font-medium' 
                        : 'hover:bg-slate-50 text-slate-700'
                    }}`}}
                  >
                    <span className="pr-4">{{tab.title}}</span>
                    <ChevronRight className={{`w-4 h-4 shrink-0 transition-transform ${{
                      activeTab === idx ? 'text-emerald-100 translate-x-1' : 'text-slate-300 group-hover:text-emerald-500 group-hover:translate-x-1'
                    }}`}} />
                  </button>
                ))}}
              </div>
            </div>
          </div>

          {{/* Tab Content */}}
          <div className="lg:w-2/3">
            <div className="bg-white rounded-2xl shadow-md border border-slate-100 p-8 min-h-[500px]">
              <h2 className="text-2xl font-bold text-slate-800 mb-6 flex items-center gap-3">
                {{tabs[activeTab]?.title}}
              </h2>
              <div className="prose prose-slate max-w-none text-slate-700 leading-relaxed space-y-4">
                <div dangerouslySetInnerHTML={{{{ __html: tabs[activeTab]?.content || '' }}}} />
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}}
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(tsx_content)

if __name__ == "__main__":
    intro, tabs = parse_html("d:/Workspace/Web/PGATK Website/pravovaya.txt")
    generate_tsx(intro, tabs, "d:/Workspace/Web/PGATK Website/pages/HealthyLifestyle.tsx")
    print("Generated HealthyLifestyle.tsx")
