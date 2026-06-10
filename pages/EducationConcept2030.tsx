import React from 'react';
import { BookOpen, FileText, ChevronRight, CheckCircle2 } from 'lucide-react';
import conceptData from '../src/data/Concept2030Data.json';

const EducationConcept2030: React.FC = () => {
  return (
    <div className="animate-in fade-in duration-500 w-full space-y-8">
      
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-3xl p-8 md:p-12 shadow-lg text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none transform translate-x-10 -translate-y-10">
          <BookOpen className="w-64 h-64" />
        </div>
        
        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/30 border border-blue-400/30 text-blue-100 font-medium text-sm mb-6 backdrop-blur-sm">
            <FileText className="w-4 h-4" />
            <span>Официальный документ</span>
          </div>
          
          <h2 className="text-3xl md:text-5xl font-display font-bold mb-6 leading-tight max-w-4xl">
            Концепция развития системы образования Республики Беларусь до 2030 года
          </h2>
          
          <p className="text-lg text-blue-100 max-w-3xl leading-relaxed">
            Фундаментальный документ, определяющий стратегические цели, задачи и приоритетные направления развития национальной системы образования на долгосрочную перспективу.
          </p>
        </div>
      </div>

      {/* Content Rendering */}
      <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
        {conceptData.map((section: any, index: number) => {
          // Skip the first title if it matches the main title exactly, or just render normally.
          const isMainTitle = index === 0 && section.title.includes("Концепция");
          
          if (isMainTitle && section.content.length === 0) return null;

          return (
            <div key={index} className={`p-8 md:p-12 ${index > 0 ? 'border-t border-slate-100' : ''}`}>
              {/* Section Title */}
              {(!isMainTitle && section.title) && (
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center shrink-0 mt-1">
                    <ChevronRight className="w-5 h-5 text-blue-600" />
                  </div>
                  <h3 className="text-2xl font-bold text-primary-900 leading-tight">
                    {section.title}
                  </h3>
                </div>
              )}
              
              {/* Section Content */}
              <div className="space-y-4 text-slate-700 leading-relaxed text-lg text-justify">
                {section.content.map((paragraph: string, pIdx: number) => {
                  // If paragraph looks like a list item
                  if (paragraph.startsWith('-') || paragraph.match(/^\d+\./)) {
                    return (
                      <div key={pIdx} className="flex items-start gap-3 pl-4 sm:pl-8 my-2">
                        <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-1" />
                        <span className="text-slate-700">{paragraph.replace(/^- /, '')}</span>
                      </div>
                    );
                  }
                  
                  return (
                    <p key={pIdx} className="mb-4">
                      {paragraph}
                    </p>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
};

export default EducationConcept2030;
