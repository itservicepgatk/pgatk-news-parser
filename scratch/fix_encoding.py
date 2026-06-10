import codecs
import re

with codecs.open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# Replace the mangled part
# The original sentence was: "Одной из важных мер по профилактике уличного травматизма является борьба с бытовым пьянством, поскольку уличные травмы часто получают лица в состоянии алкогольного опьянения.</p>"
# We will use regex to find the broken fragment and replace it
text = re.sub(r'гольного опьянения\.</p>', 'алкогольного опьянения.</p>', text)

# The bad byte before "гольного" needs to be removed
text = re.sub(r'[^\w\s\.\<\>\/\=\"\'-_]+алкогольного', 'алкогольного', text)

with codecs.open('d:/Workspace/Web/PGATK Website/pages/InjuryPrevention.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success')
