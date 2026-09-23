# Короткий список китайских производителей, проверка по базам FDA США

Проверка сделана **23 сентября 2026** по открытым данным FDA. Метод и результат ниже.
Предыдущая версия этого файла содержала Talvenda, компанию без собственного производства.
Она удалена.

---

## Что в FDA можно проверить, а что нельзя

Это надо понимать до того, как читать таблицу, иначе легко поверить в пустую бумажку.

**Нельзя проверить регистрацию предприятия.** Реестр Food Facility Registration закрыт законом,
21 U.S.C. 350d(a)(4): сведения о регистрации не подлежат раскрытию. Ни мы, ни кто-либо другой
не может подтвердить чужой номер FDA. Значит строка «FDA registered» на сайте китайского завода
**не проверяется в принципе и не стоит ничего**. Это ровно та дыра, в которую мы шли с прошлым
поставщиком: у них был номер и была дата окончания, и проверить их было нельзя никак.

**Можно проверить негатив.** Открыты: импортные алерты (Import Alerts, режим DWPE, то есть
задержание партии на границе без физического осмотра), отказы во ввозе, предупредительные письма.

Отсюда следует главное ограничение метода: **FDA даёт только отрицательный отбор.**
По базам FDA можно вычеркнуть плохого. Подтвердить, что компания является заводом,
а не торговым домом, по базам FDA нельзя. Это закрывается только выездом на площадку.

---

## Что именно проверено

**44 импортных алерта FDA**, все, что относятся к пище и биодобавкам: серии 54 (биодобавки),
99 (пища, маркировка, тяжёлые металлы, пестициды), 23 (микотоксины и готовые биодобавки),
45 (красители), 36 (мёд), 25, 41, 66. Около 40 МБ текста списков.

Предупредительные письма (Warning Letters) автоматически снять не удалось, их выдача закрыта
скриптом на стороне FDA. **Этот источник остаётся непроверенным, и я его за проверенный не выдаю.**

---

## Вычёркиваю по результатам проверки

### Sirio Healthcare (Anhui) Co., Ltd

**Import Alert 45-02**, «Detention Without Physical Examination and Guidance of Foods Containing
Illegal and/or Undeclared Colors», запись опубликована 08.03.2023.

Адрес в списке FDA: No. 1980 Hongqi South Rd, Economic and Technological Development Zone,
Maanshan, Anhui, CHINA. Это ровно тот адрес анхойской площадки, что указан на сайте самой Sirio.

Запись по продукту датирована **02.01.2025**:

> MULTIVITAMIN PECTIN GUMMY (Super Greens Gummy)
> Notes: 75810 - CHLOROPHYLLIN-COPPER COMPLEX (POTASSIUM SODIUM COPPER CHLOROPHYLLIN) - non-permitted

Это **пектиновые гуммис, то есть буквально наша форма выпуска**, и попались на красителе,
который в США не разрешён.

Оговорка, которую надо знать: под алертом **одна площадка группы**, анхойская. Головная
Sirio Pharma в Шаньтоу и Sirio Nutrition в Гуандуне в списках FDA не числятся. Формально
писать им можно. Но группа, у которой линия гуммис ловит непозволенный краситель в 2025 году,
показывает, как в ней устроен входной контроль сырья, и это уже не про одну площадку.

### Weihai Baihe Biology Technological Co., Ltd (BIOHIGH)

Тот самый завод, которого я в прошлой версии поставил третьим за сильный набор сертификатов.
**Он в двух алертах сразу.**

**Import Alert 45-02**, запись от 01.12.2014, адрес No. 552 Chengda Road, Chengshanzhen Rongcheng,
Weihai, Shandong:

> Desc: Aloe Vera Softgel
> Notes: FDA inspection revealed the firm used unsafe color additives in their dietary supplement
> products; Aloe Vera Softgel - Iron oxide (red, yellow...)

**Import Alert 99-39**, «Detention Without Physical Examination of Imported Food Products That
Appear to Be Misbranded», запись от 24.04.2023, тот же адрес:

> Desc: Honey Complex Beverage
> Notes: ... the component product labels fail to declare all the common or usual names of each
> ingredient. For example, the product label lists "Hedera Helix extract", but this is not the
> common or usual name of the dietary ingredient.

Два эпизода с разницей в девять лет, и оба про одно: в продукт кладут то, что нельзя,
и пишут на этикетке не то, что внутри. Для бренда, построенного на совпадении напечатанного
с содержимым, это дисквалификация.

---

## Прошли проверку

Ни одного упоминания ни в одном из 44 алертов.

| # | Компания | Город | Почта | Сертификаты, заявленные ими | Что проверять дальше |
|---|---|---|---|---|---|
| 1 | **Handian Nutrition** | Нанкин, Цзянсу | **lara.han@handian.cc**, **sales01@hdnutra.com** | GMP, BRCGS, NSF, FSSC 22000, HACCP, FDA, HALAL, SGS, TÜV | Уже давали письменные цены: морской мох $1.80, ежовик $1.98. Тупик был по минимуму 6 667 банок. Ломать минимум |
| 2 | **Zhengzhou Linnuo Pharmaceutical** | Чжэнчжоу, Хэнань | **sales01@linnuobio.com** | ISO 22000, ISO 9001, HACCP, FDA | **Минимум 500-1000 банок**, единственный, кто изначально проходит по нашему объёму. Завод с 2009, 50 000 м² |
| 3 | **Biocaro Pharmaceutical** | Чжэнчжоу, Хэнань | **miya@biocarohealth.cn** | GMP, HALAL, ISO 22000, FDA | Завод с 2000, 30 000 м². Минимум называли 5 000 банок, для нас много |
| 4 | **Guangzhou Jiabeikang** | Гуанчжоу, Гуандун | **phisen@jiabeikang.net** | заявляют BRCGS, GMP, ISO 22000, HACCP, FDA, HALAL, TÜV | По FDA чист. **Но: три сайта, три разных юрлица, четыре адреса.** «Jiabeikang (Guangzhou) Pharmaceutical Holdings» и «Guangzhou Jiabeikang Industrial Co., Ltd.», адреса в Хуаду и в Байюне. Закрывается визитом за полчаса |
| 5 | **Hebei Huanwei Biotech** | Шицзячжуан, Хэбэй | **info@huanweibio.com**, +86 311 68021001 | заявляют OEM по гуммис, капсулам, софтгелям | По FDA чист. Профиль смешанный: главная страница сайта про пищевые и кормовые добавки и аминокислоты, а готовые формы заявлены отдельно. Спросить, делают ли они готовую банку под этикетку |
| 6 | **Sirio Pharma**, головная в Шаньтоу | Шаньтоу, Гуандун | **sales@siriopharma.com** | BRCGS, NSF, FSSC 22000, ISO 9001 / 14001 / 45001, HACCP, TGA, USDA Organic | **Головная чиста, но площадка группы в Анхое под алертом, см. выше.** Если писать, то с прямым условием: производство не на анхойской площадке, подтвердить письменно |

**Сертификаты в таблице это их собственные заявления, а не проверенный факт.** Проверяются
в реестре выдавшего: BRCGS на brcgs.com Directory, NSF на nsf.org, FSSC на fssc22000.com.
Проверю по каждому, кто ответит, до любых денег.

---

## Исключены отдельно, не по FDA

- **Talvenda**, Шанхай. Адрес офиса квартира в Цинпу, производства описаны как партнёрские
  в трёх городах. Не завод.
- **Nutreebio**, Нанкин. Структура через **NUTREEBIO (HONG KONG) LIMITED**, адрес производства
  это офис в бизнес-центре. Гонконгская прокладка, по вашему правилу не рассматриваем.
- **Nanjing Nutrabuilding (NNB)** и **Hunan Nutramax**. Сырьё и ингредиенты, не готовая банка.
- **Dalian Dante**. Жевательная резинка с ксилитом и пастилки, не биодобавки.
- **Guangdong Suntree (zhancui.cn)**. Кондитерская фабрика, не биодобавки.

---

## Чего эта проверка не доказывает

Отсутствие компании в алертах FDA означает ровно одно: **у неё нет чёрной метки**.
Это не значит, что у неё есть цех. Торговый дом из одной комнаты тоже никогда не попадёт
в импортный алерт, потому что от его имени в США ничего не ввозится.

Поэтому порядок остаётся прежним: письмо, документы, проверка сертификатов в реестрах,
визит на площадку, и только потом деньги.

---

## Письмо для рассылки, английский

> **Subject:** Quotation request, 6 gummy and capsule SKUs, US brand
>
> Hello,
>
> We are The Aldera, a US supplement brand. Our legal entity is 518 Group LLC, registered in Florida.
> We are placing our first production order this autumn and we are choosing a manufacturer now.
>
> We need six products: sea moss gummies, ashwagandha gummies, lion's mane gummies, tongkat ali
> capsules, L-theanine capsules and saffron extract capsules. The full specification is attached.
>
> Please send us four things.
>
> 1. Which of the six you already produce as a stock formula, and the exact dose in each one.
> 2. Price per bottle at 1,000 / 2,500 and 5,000 bottles, FOB and also delivered to Miami, with the
>    label applied.
> 3. Your minimum order quantity per product, and the lead time in working days from label approval
>    to finished bottles shipped.
> 4. Copies of your business licence, your food production licence with the categories, and one
>    recent certificate of analysis with measured numbers on it.
>
> Two questions we ask every manufacturer, because they decide whether we can work together.
> Which colour additives do you use in your gummies, and are all of them permitted in the United
> States? And do you confirm that every ingredient will be declared on the label by its common or
> usual name?
>
> Our representative will visit the factory before we place the order, so please also send the
> address of the production site.
>
> Best regards,
> Aleksandr Orlov
> 518 Group LLC, The Aldera
> aleksor@thealdera.com
> thealdera.com

## Дословный перевод

> **Тема:** Запрос котировки, 6 позиций гуммис и капсул, бренд из США
>
> Здравствуйте,
>
> Мы The Aldera, американский бренд БАДов. Наше юридическое лицо 518 Group LLC, зарегистрировано
> во Флориде. Мы размещаем первый производственный заказ этой осенью и сейчас выбираем производителя.
>
> Нам нужны шесть продуктов: гуммис с морским мхом, гуммис с ашвагандой, гуммис с ежовиком,
> капсулы тонгкат али, капсулы L-теанина и капсулы экстракта шафрана. Полная спецификация приложена.
>
> Пришлите нам четыре вещи.
>
> 1. Какие из шести вы уже производите как готовую формулу, и точную дозу в каждой.
> 2. Цену за банку при 1 000 / 2 500 и 5 000 банок, FOB и также с доставкой в Майами,
>    с наклеенной этикеткой.
> 3. Ваш минимальный заказ на позицию, и срок в рабочих днях от утверждения этикетки
>    до отгрузки готовых банок.
> 4. Копии вашей бизнес-лицензии, вашей лицензии на производство пищевой продукции с категориями,
>    и один недавний сертификат анализа с измеренными числами.
>
> Два вопроса, которые мы задаём каждому производителю, потому что от них зависит, сможем ли
> мы работать вместе. Какие красители вы используете в гуммис, и все ли они разрешены
> в Соединённых Штатах? И подтверждаете ли вы, что каждый ингредиент будет указан на этикетке
> своим общепринятым названием?
>
> Наш представитель посетит фабрику до размещения заказа, поэтому пришлите также адрес
> производственной площадки.
>
> С уважением,
> Александр Орлов
> 518 Group LLC, The Aldera
> aleksor@thealdera.com
> thealdera.com

**Абзац про красители и названия ингредиентов добавлен не случайно.** Это ровно те два нарушения,
за которые в алертах FDA сидят Sirio Anhui и Weihai Baihe. Вопрос, заданный в первом письме,
сразу показывает, понимает ли собеседник, о чём речь, или отвечает «конечно, всё разрешено».

## Что приложить

`docs/pdf/The Aldera - Production Spec EN.pdf`

Китайскую версию к письму не прикладывать, она для разговора с технологом на самой фабрике.

## Чего в письме намеренно нет

- Нашей целевой цены
- Годовых объёмов
- Слова custom, просим stock formula
- Упоминания, что мы ушли от предыдущего поставщика и почему
