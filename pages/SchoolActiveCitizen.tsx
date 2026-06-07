import React from 'react';
import { Target, Users, Scale, MessageCircle, FileText, ExternalLink, ShieldCheck } from 'lucide-react';

const SchoolActiveCitizen: React.FC = () => {
  return (
    <div className="animate-in fade-in duration-500 w-full space-y-8">
      
      {/* Intro Block */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none group-hover:scale-110 transition-transform duration-700">
          <Users className="w-48 h-48" />
        </div>
        
        <h2 className="text-2xl font-bold text-primary-900 mb-6 relative z-10 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center">
            <Users className="w-5 h-5 text-blue-600" />
          </div>
          Формирование гражданственности
        </h2>
        
        <p className="text-lg text-slate-700 leading-relaxed text-justify relative z-10">
          В <span className="font-bold text-primary-900">«Школе Активного Гражданина»</span> формируется готовность учащихся в будущем участвовать в общественно-политической жизни страны, выполняя гражданские роли (избирателя, законопослушного гражданина, члена общественных организаций и т.д.), готовность самостоятельно принимать решения в сфере государственно-общественных отношений, нести ответственность за принятые решения и их последствия.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8 relative z-10">
          <div className="flex items-center gap-3 p-4 bg-slate-50 rounded-xl border border-slate-100">
            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shrink-0">
              <Scale className="w-4 h-4 text-blue-500" />
            </div>
            <span className="text-sm font-medium text-slate-700">Роль законопослушного гражданина</span>
          </div>
          <div className="flex items-center gap-3 p-4 bg-slate-50 rounded-xl border border-slate-100">
            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shrink-0">
              <ShieldCheck className="w-4 h-4 text-blue-500" />
            </div>
            <span className="text-sm font-medium text-slate-700">Ответственность за решения</span>
          </div>
        </div>
      </div>

      {/* Main Goal Block */}
      <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-8 shadow-md text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 p-6 opacity-10 pointer-events-none">
          <Target className="w-40 h-40" />
        </div>
        
        <h3 className="text-xl font-bold mb-6 flex items-center gap-3 relative z-10 border-b border-blue-500/30 pb-4">
          <Target className="w-6 h-6 text-blue-200" />
          Основная задача
        </h3>
        
        <div className="space-y-4 relative z-10">
          <div className="flex items-start gap-4">
            <div className="w-6 h-6 rounded-full bg-blue-500/50 flex items-center justify-center shrink-0 mt-0.5">
              <div className="w-2 h-2 rounded-full bg-white"></div>
            </div>
            <p className="text-blue-50 leading-relaxed">
              <strong className="text-white">Расширение знаний</strong> учащихся о политических и социально-экономических событиях в Республике Беларусь.
            </p>
          </div>
          <div className="flex items-start gap-4">
            <div className="w-6 h-6 rounded-full bg-blue-500/50 flex items-center justify-center shrink-0 mt-0.5">
              <div className="w-2 h-2 rounded-full bg-white"></div>
            </div>
            <p className="text-blue-50 leading-relaxed">
              <strong className="text-white">Развитие умений анализировать</strong> информацию о социальных явлениях и процессах.
            </p>
          </div>
          <div className="flex items-start gap-4">
            <div className="w-6 h-6 rounded-full bg-blue-500/50 flex items-center justify-center shrink-0 mt-0.5">
              <MessageCircle className="w-3 h-3 text-white" />
            </div>
            <p className="text-blue-50 leading-relaxed">
              <strong className="text-white">Ведение дискуссии</strong> по проблемам развития современного общества.
            </p>
          </div>
        </div>
      </div>

      {/* Document Link */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 hover:border-blue-200 hover:shadow-md transition-all group">
        <div className="flex items-center gap-5">
          <div className="w-14 h-14 rounded-full bg-blue-50 flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
            <FileText className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h4 className="font-bold text-primary-900 text-lg mb-1">Примерная тематика мероприятий проекта</h4>
            <p className="text-slate-500 text-sm">для VIII–XI классов в 2025/2026 учебном году</p>
          </div>
        </div>
        
        <a 
          href="https://disk.yandex.com/i/rQI0AmY1p1aH5Q" 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium transition-colors shrink-0"
        >
          <span>Смотреть документ</span>
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>

    </div>
  );
};

export default SchoolActiveCitizen;
