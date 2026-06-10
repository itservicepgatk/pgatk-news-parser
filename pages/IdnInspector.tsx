import React from 'react';
import { ShieldAlert, Phone, Smartphone, MapPin, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function IdnInspector() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <Link 
          to="/okazanie-socialno-pedagogicheskoy-pomochi" 
          className="inline-flex items-center gap-2 text-slate-500 hover:text-blue-600 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Назад к разделу СППС
        </Link>
        
        <div className="bg-white rounded-3xl shadow-xl border border-slate-100 overflow-hidden relative">
          <div className="absolute top-0 left-0 w-full h-32 bg-red-600">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
          </div>
          
          <div className="relative z-10 pt-16 px-8 pb-10 text-center">
            <div className="w-32 h-32 mx-auto bg-white rounded-full flex items-center justify-center shadow-lg border-4 border-red-50 mb-6">
              <ShieldAlert className="w-16 h-16 text-red-600" />
            </div>
            
            <h1 className="text-sm font-bold text-slate-400 tracking-widest uppercase mb-2">
              Инспекция по делам несовершеннолетних
            </h1>
            <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-4">
              Участковый инспектор ИДН Пинского ГОВД
            </h2>
            
            <p className="text-slate-600 mb-8 max-w-lg mx-auto">
              По всем вопросам, относящимся к компетенции инспекции по делам несовершеннолетних, Вы можете обратиться к лейтенанту милиции:
            </p>
            
            <div className="bg-red-50 rounded-2xl p-6 mb-8 inline-block border border-red-100">
              <p className="text-xl md:text-2xl font-extrabold text-red-700">
                КИСЛЮК ИРИНА ЛЕОНИДОВНА
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left max-w-xl mx-auto">
              <div className="flex items-start gap-4 p-4 rounded-xl bg-slate-50">
                <div className="bg-white p-2 rounded-lg shadow-sm text-red-600 shrink-0">
                  <Phone className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Рабочие телефоны</p>
                  <p className="font-bold text-slate-800 text-lg">8 (0165) 64-11-47</p>
                  <p className="font-bold text-slate-800 text-lg">8 (0165) 64-20-46</p>
                </div>
              </div>
              
              <div className="flex items-start gap-4 p-4 rounded-xl bg-slate-50">
                <div className="bg-white p-2 rounded-lg shadow-sm text-red-600 shrink-0">
                  <Smartphone className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Мобильный телефон (GSM)</p>
                  <p className="font-bold text-slate-800 text-lg">8 (044) 755-92-64</p>
                </div>
              </div>
              
              <div className="flex items-start gap-4 p-4 rounded-xl bg-slate-50 md:col-span-2">
                <div className="bg-white p-2 rounded-lg shadow-sm text-red-600 shrink-0">
                  <MapPin className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Адрес инспекции</p>
                  <p className="font-bold text-slate-800 text-lg">
                    225710, г. Пинск, ул. Сухая, 52а
                  </p>
                  <p className="text-slate-600">инспекция по делам несовершеннолетних Пинского ГОВД</p>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  );
}
