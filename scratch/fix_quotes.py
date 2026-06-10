import codecs
import re

with codecs.open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace single quotes surrounding the __html with backticks, because the inner HTML contains single and double quotes.
# Wait, actually, let's just properly escape the inner single quotes. Or use backticks.
# Let's find dangerouslySetInnerHTML={{ __html: '...' }}
start_str = "dangerouslySetInnerHTML={{ __html: '"
end_str = "' }} />"

start_idx = text.find(start_str)
if start_idx != -1:
    end_idx = text.find(end_str, start_idx + len(start_str))
    
    # We found the block. Let's extract inner text.
    inner = text[start_idx + len(start_str) : end_idx]
    
    # Let's just use backticks for the outer template literal
    inner = inner.replace('`', '\\`').replace('${', '\\${')
    
    new_text = text[:start_idx] + 'dangerouslySetInnerHTML={{ __html: `' + inner + '` }} />' + text[end_idx + len(end_str):]
    
    with codecs.open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Fixed using single quote search.")
else:
    print("Single quote format not found.")
    
    # What if it's double quote format?
    start_str2 = 'dangerouslySetInnerHTML={{ __html: "'
    end_str2 = '" }} />'
    start_idx = text.find(start_str2)
    if start_idx != -1:
        end_idx = text.rfind(end_str2) # there might be inner double quotes, so rfind is safer
        inner = text[start_idx + len(start_str2) : end_idx]
        inner = inner.replace('`', '\\`').replace('${', '\\${')
        new_text = text[:start_idx] + 'dangerouslySetInnerHTML={{ __html: `' + inner + '` }} />' + text[end_idx + len(end_str2):]
        with codecs.open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("Fixed using double quote search.")
