import React from 'react';
import { ShieldAlert, Info, FileText, AlertTriangle, Droplets, Snowflake, MapPin, Scale, Calendar, ExternalLink } from 'lucide-react';

const Osvod: React.FC = () => {
  return (
    <div className="animate-in fade-in duration-500 w-full space-y-8">
      
      {/* Header Profile Section */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm flex flex-col md:flex-row gap-8 items-center md:items-start relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-50 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
        
        <div className="flex-1 text-center md:text-left relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 font-medium text-sm mb-4">
            <ShieldAlert className="w-4 h-4" />
            <span>ОСВОД</span>
          </div>
          
          <h2 className="text-3xl font-display font-bold text-primary-900 mb-2">
            Наварич Валерий Адамович
          </h2>
          <p className="text-lg text-slate-600 font-medium max-w-2xl">
            Председатель первичной организации ОСВОД учреждения образования «Пинский государственный аграрно-технический колледж имени А.Е. Клещева»
          </p>
        </div>
      </div>

      {/* Main Info */}
      <div className="bg-slate-50 rounded-2xl p-8 border border-slate-200 text-slate-700 leading-relaxed text-justify space-y-4">
        <p>
          Предметом и целью деятельности ОСВОД, в соответствии с Уставом утвержденным Постановлением Совета Министров Республики Беларусь от 19 ноября 2004 года № 1473 пункт 9, является максимально возможное снижение вероятности гибели людей на водах в Республике Беларусь.
        </p>
        <p>
          В своей деятельности служба ОСВОД руководствуется Указами Президента Республики Беларусь № 298 от 29 июня 2009 года «Вопросы Белорусского республиканского общества спасания на водах», № 332 от 25 июля 2013 года, Уставом ОСВОД, Правилами охраны жизни людей на водах Республики Беларусь, утвержденными Постановлением Совета Министров Республики Беларусь № 1623 от 11.12.2009.
        </p>
        
        <h3 className="text-xl font-bold text-primary-900 mt-6 mb-4 flex items-center gap-2">
          <Info className="w-5 h-5 text-blue-600" />
          Государственно-значимые задачи ОСВОД:
        </h3>
        <ul className="list-disc pl-6 space-y-2 text-slate-700">
          <li>спасание и охрану жизни людей на водах республики в районах действия спасательных станций и постов;</li>
          <li>организовывает и проводит разъяснительную работу среди населения по предупреждению несчастных случаев на водах;</li>
          <li>обучает население приемам спасания и оказания первой помощи лицам, терпящим бедствие на водах;</li>
          <li>участвует в проведении аварийно-спасательных, спасательных и поисковых работ на водах.</li>
        </ul>

        <div className="mt-6">
          <a href="https://pravo.by/pdf/2009-303/2009-303(020-039).pdf" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-colors shadow-sm">
            <FileText className="w-5 h-5" />
            Правила охраны жизни людей на водах Республики Беларусь
          </a>
        </div>
      </div>

      {/* Rules Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Water Rules */}
        <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
            <Droplets className="w-48 h-48" />
          </div>
          <h3 className="text-2xl font-bold text-primary-900 mb-6 flex items-center gap-3 relative z-10">
            <Droplets className="w-6 h-6 text-blue-500" />
            Правила поведения на воде
          </h3>
          
          <div className="space-y-6 relative z-10 text-slate-700 text-justify">
            <div>
              <h4 className="font-bold text-lg mb-3">Общие правила:</h4>
              <ul className="space-y-2">
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>воздержитесь от купания в неизвестных и не предназначенных для этой цели водоемах;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>избегайте купания в одиночку;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не купайтесь в нетрезвом состоянии;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не ныряйте в незнакомых местах;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не заплывайте за буйки;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не выплывайте на судовой ход и не приближайтесь к судам;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не устраивайте игр в воде, связанных с захватами;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не доводите себя до переохлаждения и переутомления;</span></li>
                <li className="flex gap-3"><AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /><span>не оставляйте детей у воды без присмотра.</span></li>
              </ul>
            </div>
            <div className="bg-blue-50 p-6 rounded-xl border border-blue-100">
              <h4 className="font-bold text-lg mb-2 text-blue-900">Действия в экстремальных ситуациях:</h4>
              <p className="mb-2">Если вы устали в воде не нужно теряться - следует сохранять спокойствие. Повернитесь на спину, отдохните, спокойно расправив руки и ноги, закрыв глаза, положите голову на воду и расслабьтесь.</p>
              <p className="mb-2"><strong>При судорогах:</strong> бедра - согните ногу в колене, прижмите пятку к спине; кистей рук - резко сжимайте и разжимайте пальцы; живота - подтяните колени; икроножной мышцы - поднимите ногу и подтяните стопу к себе.</p>
              <p>Если попали в течение — плывите по течению, приближаясь к берегу. Если упали в воду — наберите воздух, примите вертикальное положение и старайтесь спастись без паники.</p>
            </div>
          </div>
        </div>

        {/* Ice Rules */}
        <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
            <Snowflake className="w-48 h-48" />
          </div>
          <h3 className="text-2xl font-bold text-primary-900 mb-6 flex items-center gap-3 relative z-10">
            <Snowflake className="w-6 h-6 text-sky-500" />
            Правила поведения на льду
          </h3>
          
          <div className="space-y-6 relative z-10 text-slate-700 text-justify">
            <div>
              <p className="mb-3 font-medium">Безопасным считается лед толщиной не менее 10 см в пресной воде. Лед голубого цвета — прочный, белый — в два раза слабее, серый или матово белый — ненадежен.</p>
              <ul className="space-y-2">
                <li className="flex gap-3"><Info className="w-5 h-5 text-sky-500 shrink-0 mt-0.5" /><span>Не переходите водоем в запрещенных местах, не выезжайте на лед на автотранспорте.</span></li>
                <li className="flex gap-3"><Info className="w-5 h-5 text-sky-500 shrink-0 mt-0.5" /><span>Не выходите на тонкий лед в начале зимы и весной.</span></li>
                <li className="flex gap-3"><Info className="w-5 h-5 text-sky-500 shrink-0 mt-0.5" /><span>Ни в коем случае нельзя выходить на лед в темное время суток и при плохой видимости.</span></li>
                <li className="flex gap-3"><Info className="w-5 h-5 text-sky-500 shrink-0 mt-0.5" /><span>Нельзя проверять прочность льда ударом ноги. Прощупывайте путь палкой.</span></li>
                <li className="flex gap-3"><Info className="w-5 h-5 text-sky-500 shrink-0 mt-0.5" /><span>При переходе группой соблюдайте расстояние 5-6 м.</span></li>
                <li className="flex gap-3"><Info className="w-5 h-5 text-sky-500 shrink-0 mt-0.5" /><span>Замерзшую реку лучше перейти на лыжах, расстегнув крепления.</span></li>
              </ul>
            </div>
            <div className="bg-sky-50 p-6 rounded-xl border border-sky-100">
              <h4 className="font-bold text-lg mb-2 text-sky-900">Что делать, если вы провалились:</h4>
              <p className="mb-2">Не паникуйте. Раскиньте руки и зацепитесь за кромку льда. Осторожно налягте грудью на край и забросьте ноги на лед. Ползите в ту сторону, откуда пришли.</p>
              <h4 className="font-bold text-lg mb-2 text-sky-900 mt-4">Если нужна Ваша помощь:</h4>
              <p>Вооружитесь палкой или веревкой. Ползком двигайтесь к полынье. Бросьте пострадавшему спасательное средство за несколько метров. Доставьте в теплое место и энергично разотрите тело (не давайте алкоголь!).</p>
            </div>
          </div>
        </div>
      </div>

      {/* Locations */}
      <div className="bg-emerald-50/50 rounded-2xl p-8 border border-emerald-100">
        <h3 className="text-2xl font-bold text-primary-900 mb-6 flex items-center gap-3">
          <MapPin className="w-6 h-6 text-emerald-600" />
          Места массового отдыха для купания
        </h3>
        <p className="mb-4 text-slate-700">Перечень мест массового отдыха, расположенных у водных объектов и используемых для оздоровления населения г.Пинска и Пинского района:</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {[
            'Пляж № 1 города Пинска', 'Пляж № 2 города Пинска', 'Пляж водохранилища аг. Парохонск',
            'Пляж водохранилища Жидче', 'Пляжи водохранилища Погост: аг. Новый Двор, д. Вяз',
            'КУП ДРОЦ «Свитанак»', 'ЧП «Езерский и К»', 'Пляж водохранилища Горново',
            'Пляж водохранилища Мокрая Дуброва', 'Пляж озера «Кривичи-1»', '2 пляжа озера Кончицкое',
            'Пляж озера Городищенское', 'Пляж реки Ясельда д. Поречье'
          ].map((place, idx) => (
            <div key={idx} className="flex items-center gap-2 bg-white p-3 rounded-lg shadow-sm border border-slate-100 text-sm font-medium text-slate-700">
              <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
              {place}
            </div>
          ))}
        </div>
      </div>

      {/* Administrative Responsibility */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
        <h3 className="text-2xl font-bold text-primary-900 mb-6 flex items-center gap-3">
          <Scale className="w-6 h-6 text-rose-600" />
          Ответственность за административные правонарушения
        </h3>
        <p className="mb-6 text-slate-600">Меры ответственности за нарушение ст.ст. 16.34, 19.1, 19.3, 24.42 Кодекса Республики Беларусь об административных правонарушениях</p>
        
        <div className="space-y-6">
          <div className="p-6 bg-slate-50 rounded-xl border border-slate-100">
            <h4 className="font-bold text-lg text-primary-900 mb-2">Статья 16.34. Загрязнение либо засорение вод</h4>
            <p className="text-slate-700 text-sm leading-relaxed text-justify">
              Загрязнение либо засорение поверхностных или подземных вод влекут наложение штрафа до 20 базовых величин (на юр. лицо - до 500 БВ). Нарушение режима осуществления хоз. деятельности в водоохранных зонах влечет штраф до 10 БВ (до 50 БВ на юр. лицо).
            </p>
          </div>
          
          <div className="p-6 bg-slate-50 rounded-xl border border-slate-100">
            <h4 className="font-bold text-lg text-primary-900 mb-2">Статья 19.1. Мелкое хулиганство</h4>
            <p className="text-slate-700 text-sm leading-relaxed text-justify">
              Оскорбительное приставание к гражданам и другие умышленные действия, нарушающие общественный порядок - влекут наложение штрафа в размере от 2 до 30 базовых величин, или общественные работы, или административный арест.
            </p>
          </div>

          <div className="p-6 bg-slate-50 rounded-xl border border-slate-100">
            <h4 className="font-bold text-lg text-primary-900 mb-2">Статья 19.3. Распитие алкогольных напитков и потребление наркотических средств</h4>
            <p className="text-slate-700 text-sm leading-relaxed text-justify">
              Распитие алкогольных напитков в общественных местах, либо появление в состоянии опьянения влечет штраф до 8 БВ. Повторно в течение года - штраф от 2 до 15 БВ, или общественные работы, или арест. Появление в состоянии наркотического опьянения влечет штраф от 5 до 10 БВ (на рабочем месте от 8 до 12 БВ, а потребление в общественном месте от 10 до 15 БВ).
            </p>
          </div>

          <div className="p-6 bg-rose-50 rounded-xl border border-rose-100">
            <h4 className="font-bold text-lg text-rose-900 mb-2">Статья 24.42. Купание в запрещенных местах</h4>
            <p className="text-rose-800 text-sm leading-relaxed font-medium">
              Купание в запрещенных местах рек, озер или иных водоемов - влечет наложение штрафа в размере от 1 до 3 базовых величин.
            </p>
          </div>
        </div>
      </div>

      {/* Plan Table */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="bg-slate-50 p-6 border-b border-slate-200">
          <h3 className="text-xl font-bold text-primary-900 flex items-center gap-3 justify-center text-center">
            <Calendar className="w-6 h-6 text-blue-600" />
            План работы первичной организации ОСВОД на 2025/2026 учебный год
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-700 text-sm uppercase tracking-wider">
                <th className="p-4 border-b border-slate-200 font-bold w-12 text-center">№</th>
                <th className="p-4 border-b border-slate-200 font-bold">Содержание работы</th>
                <th className="p-4 border-b border-slate-200 font-bold whitespace-nowrap">Сроки</th>
                <th className="p-4 border-b border-slate-200 font-bold">Ответственные</th>
              </tr>
            </thead>
            <tbody className="text-sm text-slate-700 divide-y divide-slate-100">
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">1</td>
                <td className="p-4">Пропаганда деятельности ОСВОД и вовлечение новых членов в первичную организацию</td>
                <td className="p-4 whitespace-nowrap">в течение года</td>
                <td className="p-4">члены ОСВОД</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">2</td>
                <td className="p-4">Организация сбора индивидуальных членских взносов и перечисления их на счет ОСВОД</td>
                <td className="p-4 whitespace-nowrap">в установл. порядке</td>
                <td className="p-4">Наварич В.А.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">3</td>
                <td className="p-4">Размещение на информационных стендах памяток по предупреждению несчастных случаев</td>
                <td className="p-4 whitespace-nowrap">в течение года</td>
                <td className="p-4">Наварич В.А., воспитатели общежитий</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">4</td>
                <td className="p-4">Размещение на официальном сайте колледжа актуальной информации для сезонных периодов</td>
                <td className="p-4 whitespace-nowrap">в течение года</td>
                <td className="p-4">инженер-программист</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">5</td>
                <td className="p-4">Оформление информационного бюллетеня «Справка о несчастных случаях с людьми на водах»</td>
                <td className="p-4 whitespace-nowrap">в течение года</td>
                <td className="p-4">Наварич В.А.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">6</td>
                <td className="p-4">Занятия по обучению правилам самоспасания на воде и навыкам оказания первой помощи</td>
                <td className="p-4 whitespace-nowrap">в течение года</td>
                <td className="p-4">Преподаватели ДП и МП</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">7</td>
                <td className="p-4">Организация работы кинолектория «Безопасность на водах»</td>
                <td className="p-4 whitespace-nowrap">в течение года</td>
                <td className="p-4">Зам. директора по ВР, Наварич В.А.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">8</td>
                <td className="p-4">Участие в Неделе безопасного и ответственного поведения</td>
                <td className="p-4 whitespace-nowrap">сентябрь</td>
                <td className="p-4">члены ОСВОД, кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">9</td>
                <td className="p-4">Проведение мероприятий в рамках Дня безопасности на льду</td>
                <td className="p-4 whitespace-nowrap">ноябрь-декабрь</td>
                <td className="p-4">члены ОСВОД, кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">10</td>
                <td className="p-4">Тематическая выставка-обзор литературы по теме «Безопасность на водах»</td>
                <td className="p-4 whitespace-nowrap">ноябрь, апрель</td>
                <td className="p-4">Крайниченко С.В.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">11</td>
                <td className="p-4">Инструктаж по мерам безопасности (под роспись)</td>
                <td className="p-4 whitespace-nowrap">ноябрь, апрель</td>
                <td className="p-4">Наварич В.А., кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">12</td>
                <td className="p-4">Участие в мероприятиях «Безопасный Новый год»</td>
                <td className="p-4 whitespace-nowrap">декабрь</td>
                <td className="p-4">члены ОСВОД, кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">13</td>
                <td className="p-4">Организация занятий с учащимися на уроках физкультуры (раздел «Плавание»)</td>
                <td className="p-4 whitespace-nowrap">по отд. плану</td>
                <td className="p-4">Наварич В.А., преподаватели ФК</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">14</td>
                <td className="p-4">Ознакомление с мерами ответственности (ст.ст. 16.34, 19.1, 19.3, 24.42 КоАП)</td>
                <td className="p-4 whitespace-nowrap">апрель</td>
                <td className="p-4">Наварич В.А., кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">15</td>
                <td className="p-4">Мероприятия в рамках Дня основания Белорусского ОСВОД</td>
                <td className="p-4 whitespace-nowrap">25 апреля</td>
                <td className="p-4">члены ОСВОД, кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">16</td>
                <td className="p-4">Мероприятия в рамках Недели безопасности на водах</td>
                <td className="p-4 whitespace-nowrap">май</td>
                <td className="p-4">члены ОСВОД, кураторы</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">17</td>
                <td className="p-4">Участие в общем родительском собрании с приглашением председателя Пинского ОСВОД</td>
                <td className="p-4 whitespace-nowrap">июнь</td>
                <td className="p-4">Наварич В.А.</td>
              </tr>
              <tr className="hover:bg-slate-50 transition-colors">
                <td className="p-4 text-center text-slate-400 font-medium">18</td>
                <td className="p-4">Организация дежурства активистов ОСВОД в местах несанкционированного купания</td>
                <td className="p-4 whitespace-nowrap">июнь - август</td>
                <td className="p-4">Наварич В.А., Мелюх А.В.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Useful Links */}
      <div className="bg-slate-800 rounded-2xl p-8 text-white">
        <h3 className="text-xl font-bold mb-6 border-b border-slate-700 pb-4">
          Полезные ссылки
        </h3>
        <ul className="space-y-4">
          <li>
            <a href="https://mchs.gov.by/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 text-slate-300 hover:text-white transition-colors group">
              <ExternalLink className="w-5 h-5 text-slate-500 group-hover:text-blue-400 shrink-0" />
              <span>Министерство по Чрезвычайным ситуациям Республики Беларусь</span>
            </a>
          </li>
          <li>
            <a href="http://osvod.www.by/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 text-slate-300 hover:text-white transition-colors group">
              <ExternalLink className="w-5 h-5 text-slate-500 group-hover:text-blue-400 shrink-0" />
              <span>РГОО «Белорусское республиканское общество спасания на водах» (ОСВОД)</span>
            </a>
          </li>
          <li>
            <a href="https://pinsk.eu/obshestva-i-fondy/obshestvennaya-organizaciya-osvod/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 text-slate-300 hover:text-white transition-colors group">
              <ExternalLink className="w-5 h-5 text-slate-500 group-hover:text-blue-400 shrink-0" />
              <span>Пинская городская организация ОСВОД</span>
            </a>
          </li>
          <li>
            <a href="https://pinsk.eu/page/397/osvod-vesna/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 text-slate-300 hover:text-white transition-colors group">
              <ExternalLink className="w-5 h-5 text-slate-500 group-hover:text-blue-400 shrink-0" />
              <span>Методические материалы ОСВОД (видеоролики)</span>
            </a>
          </li>
        </ul>
      </div>

    </div>
  );
};

export default Osvod;
