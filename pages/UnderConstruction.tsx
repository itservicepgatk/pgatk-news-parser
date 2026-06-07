import React from 'react';
import { HardHat, Wrench, Construction, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function UnderConstruction({ title = "Раздел находится в разработке", backLink = "/" }) {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center">
        
        <div className="relative inline-block mb-10">
          <div className="absolute inset-0 bg-amber-400 blur-3xl opacity-20 rounded-full"></div>
          <div className="w-40 h-40 mx-auto bg-amber-50 rounded-full flex items-center justify-center border-4 border-amber-200 relative z-10 shadow-xl">
            <Construction className="w-20 h-20 text-amber-500 animate-pulse" />
          </div>
          
          {/* Floating elements */}
          <div className="absolute -top-4 -right-4 w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg border border-slate-100 z-20 animate-bounce" style={{ animationDelay: '0.2s' }}>
            <HardHat className="w-6 h-6 text-amber-600" />
          </div>
          <div className="absolute -bottom-2 -left-4 w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg border border-slate-100 z-20 animate-bounce" style={{ animationDelay: '0.5s' }}>
            <Wrench className="w-5 h-5 text-slate-400" />
          </div>
        </div>
        
        <h1 className="text-3xl md:text-5xl font-extrabold text-slate-800 mb-6">
          {title}
        </h1>
        
        <p className="text-lg text-slate-500 mb-10 max-w-lg mx-auto">
          Мы активно работаем над наполнением этой страницы. Совсем скоро здесь появится много полезной и интересной информации. Загляните сюда чуть позже!
        </p>
        
        <div className="inline-flex overflow-hidden rounded-full p-1 bg-slate-100 border border-slate-200 shadow-inner">
          <div className="w-full h-2 bg-gradient-to-r from-amber-300 via-amber-500 to-amber-300 rounded-full animate-[shimmer_2s_infinite] bg-[length:200%_100%]"></div>
        </div>
        
      </div>
    </div>
  );
}
