import React from 'react';
import { Megaphone, Users, Target, BookOpen, CheckCircle2, MessageSquare, ClipboardList, Lightbulb } from 'lucide-react';

export default function UnifiedInformationDay() {
  const tasks = [
    {
      icon: <Megaphone className="w-6 h-6 text-blue-500" />,
      text: "Разъяснение идеологии белорусского государства и основных направлений проводимой государственной политики."
    },
    {
      icon: <Users className="w-6 h-6 text-indigo-500" />,
      text: "Широкое информирование граждан страны о деятельности Президента Республики Беларусь, Национального собрания Республики Беларусь, Совета Министров Республики Беларусь и других государственных органов."
    },
    {
      icon: <MessageSquare className="w-6 h-6 text-emerald-500" />,
      text: "Изучение общественного мнения и анализ общественно-политической ситуации в стране."
    },
    {
      icon: <Target className="w-6 h-6 text-red-500" />,
      text: "Определение приоритетных направлений в информационно-пропагандистской работе среди трудовых коллективов и учащихся."
    },
    {
      icon: <ClipboardList className="w-6 h-6 text-amber-500" />,
      text: "Оказание методической и организационной помощи членам групп, обеспечение контроля за их деятельностью."
    },
    {
      icon: <BookOpen className="w-6 h-6 text-violet-500" />,
      text: "Изучение и обобщение опыта идеологической и информационной работы информационно-пропагандистских групп, подготовка рекомендаций по совершенствованию их деятельности."
    },
    {
      icon: <Lightbulb className="w-6 h-6 text-cyan-500" />,
      text: "Рассмотрение поступивших в ходе единых дней информирования обращений граждан; реагирование на анализ заявлений, жалоб во время выступлений членов информационно-пропагандистских групп."
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-indigo-900 via-blue-900 to-slate-900 py-16 px-4 md:px-8 shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/connected-points.png')] opacity-20"></div>
        <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-blue-500 rounded-full blur-[100px] opacity-20"></div>
        
        <div className="max-w-4xl mx-auto relative z-10 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/10 backdrop-blur-sm border border-white/20 mb-6 text-blue-300">
            <Megaphone className="w-8 h-8" />
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold text-white mb-6 leading-tight">
            Единый день информирования
          </h1>
          <p className="text-blue-100 text-lg md:text-xl max-w-2xl mx-auto opacity-90">
            Подготовка и проведение единых дней информирования в ученических и трудовых коллективах
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 md:px-8 -mt-8 relative z-20">
        
        {/* Info Card */}
        <div className="bg-white rounded-3xl shadow-xl border border-slate-100 overflow-hidden mb-12 p-8 md:p-12">
          <div className="prose prose-slate max-w-none text-slate-700 md:text-lg leading-relaxed text-justify space-y-6">
            <p>
              Одной из наиболее активных форм идеологической работы являются встречи информационно-пропагандистских групп и докладчиков с ученическими и трудовыми коллективами в рамках единого дня информирования.
            </p>
            <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-2xl my-8">
              <p className="font-medium text-blue-900 m-0 text-left">
                <strong>Единый день информирования</strong> – это комплекс мероприятий, проводимых ежемесячно (каждый третий четверг месяца), которые проводят члены информационно-пропагандистских групп и приглашённые докладчики.
              </p>
            </div>
            <p>
              Роль единых дней информирования, на которых выступают члены информационно-пропагандистских групп, очень велика. Они являются эффективным звеном «обратной связи» с людьми, разъясняют их права и обязанности, политику государства и решения местных властей; в ходе проведения единых дней информирования происходит обмен мнениями по наиболее актуальным общественным вопросам, не остаются без внимания проблемы города, республики, ученического и трудового коллективов.
            </p>
            <p>
              Поступившие предложения, замечания и просьбы обобщаются, по ним принимаются меры, контролируется их исполнение.
            </p>
            <p>
              Единые дни информирования, как никакая другая форма работы позволяют развивать плодотворное взаимодействие власти и граждан страны. Многие вопросы, озвученные на едином дне информирования, решаются более оперативно, а люди убеждаются во внимательном отношении руководителей к их проблемам. Очень важно, когда каждый учащийся, член трудового коллектива реально видит, что местная власть готова решать его проблемы. Практика при этом показывает, что любой вопрос всегда проще решить на месте, в рабочем порядке, чем бюрократическими методами.
            </p>
          </div>
        </div>

        {/* Tasks Section */}
        <h2 className="text-3xl font-bold text-slate-800 mb-8 text-center flex items-center justify-center gap-4">
          <CheckCircle2 className="w-8 h-8 text-blue-600" />
          Основные задачи групп
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {tasks.map((task, index) => (
            <div 
              key={index} 
              className={`bg-white rounded-2xl p-6 shadow-md border border-slate-100 hover:shadow-lg transition-shadow flex gap-4 ${
                index === tasks.length - 1 && tasks.length % 2 !== 0 ? 'md:col-span-2 md:w-1/2 md:mx-auto' : ''
              }`}
            >
              <div className="shrink-0 bg-slate-50 p-3 rounded-xl">
                {task.icon}
              </div>
              <p className="text-slate-700 font-medium">
                {task.text}
              </p>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
