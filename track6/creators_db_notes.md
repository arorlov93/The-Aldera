# Creators DB — заметки по транше №1 (2026-09-08)

**Итог транши:** 124 верифицированные строки в `creators_db.csv` (A=25, B=70, C=29; у 40 строк есть численность аудитории с датой источника). Все хендлы найдены в реальных источниках (URL видео/статьи в колонке `source_url`) — ничего не выдумано. Где подписчиков подтвердить не удалось, стоит `unknown` — это честнее, чем цифра с потолка.

## Методика (что реально работало в этой среде)

Прямой доступ к tiktok.com/instagram.com и почти ко всем сайтам-агрегаторам закрыт egress-прокси. **Работает только поисковый индекс** (WebSearch): он сам читает страницы и отдаёт выжимку. Отсюда два рабочих приёма:

1. **Доменно-ограниченный поиск по tiktok.com** (`allowed_domains: www.tiktok.com`) по «нашим» запросам: sleepy girl mocktail, adrenal cocktail, magnesium glycinate review, RYZE/Everyday Dose/Bloom/Goli/Nello/Beam/Moon Juice review, «5-9 before 9-5», night shift nurse routine, supplements for women in their 30s и т.п. В выдаче — URL реальных видео вида `tiktok.com/@handle/video/...` с полным кэпшеном (хэштеги, коды скидок, партнёрские метки). Это главный источник нано/микро-криейтеров: ~3-6 хендлов за запрос.
2. **Точечная верификация подписчиков**: запрос `"handle" tiktok followers` — счётчик подтягивается из Famous Birthdays / urlebird / collabstr / кэша профиля. Срабатывает ~70% случаев, 1 запрос = 1 криейтер.

Дополнительно: листиклы (Feedspot, Social Cat, netinfluencer, Heepsy, mmm-online) отдают в сниппетах по 2-5 имён с цифрами — но в основном макро-аккаунты (они ушли в tier C как «якоря»).

## Где искал (и выход по источникам)

| Источник | Выход | Комментарий |
|---|---|---|
| Поиск по tiktok.com по бренд-запросам (RYZE, Bloom, Goli, Nello, Arrae, Beam, Moon Juice, Everyday Dose, LMNT, Mixhers, OLLY) | ★★★★★ | Лучший канал: это уже готовые аффилиаты чужих supplement-брендов, с кодами и TTS-хэштегами |
| Поиск по tiktok.com по трендам (sleepy girl mocktail, adrenal cocktail, cortisol, 5-9 routine, that girl, sunday reset, night shift nurse) | ★★★★☆ | Точный нишевый фит; часть аккаунтов мелкие и без цифр |
| Верификация `"handle" tiktok followers` | ★★★★☆ | Famous Birthdays/urlebird дают свежие цифры |
| Feedspot топ-листы (female health, weight loss, mental health) | ★★★☆☆ | Цифры есть, но в сниппет попадают 2-4 имени; много макро |
| Social Cat / netinfluencer / Influence Agency / Silk+Sonder (ADHD) | ★★★☆☆ | Имена+цифры, но списки полузакрыты |
| Heepsy / Modash / Favikon / Collabstr страницы рейтингов | ★★☆☆☆ | Сами страницы за пейволлом; в сниппеты попадает мало |
| Instagram-поиск (`allowed_domains: instagram.com`) | ★★☆☆☆ | Хендлы видно, но ни цифр, ни кэпшенов; IG-крыло базы почти пустое |
| Статьи «top wellness influencers» (GOAT, Dear Media, stackinfluence, viralnation) | ★☆☆☆☆ | Только мега-имена, для аутрича бесполезно |

## Важные пометки к данным

- `followers_approx` всегда с датой/источником; пометка **stale** = цифра из листикла 2025 — начала 2026 г. `unknown` = аккаунт существует (видео по source_url), но счётчик не нашёлся — добить при аутриче (профиль открывается вручную за 5 секунд).
- Двое отмечены как **вероятно UK** (@itsnasg, @moveswithmaci — по признакам в кэпшенах): для TikTok Shop US не подойдут, держу в C, чтобы не потерять работу.
- @adridiaries ушла с TikTok в IG (@adridiaries_) — контакт только через IG.
- Контакт почти везде «TikTok DM»: email в био через поисковый индекс не вытащить (linktree заблокирован). Email-колонку добивать на этапе аутрича: linktr.ee/{handle}, beacons.ai/{handle}, IG-био, «партнёрства» в профиле.

## Как добивать базу до 500 (следующие транши)

1. **Бренд-аффилиаты — масштабировать №1-источник.** Ещё не отработаны: MaryRuth's, Ancient Nutrition, Micro Ingredients, Toplux, Sunday Scaries (lion's mane!), True Sea Moss (их аффилиаты = наши SKU 1-в-1), Wellgard, Physician's Choice, Waterboy, Cadence, Liquid IV, Alani Nu, Olipop-крыло. По 1-2 запроса на бренд × ~4 хендла = +80-120 строк.
2. **Тренд-запросы, которые ещё не выжаты:** #sleepygirlmocktail (перебирать вариациями: «no olipop», «magnesium version», «tried for 30 days»), #morningshed, #wellnessgirlie, #hotgirlwalk + electrolytes, #adhdtok + supplements, #teachertok tired, #nursesoftiktok night shift, #postpartum energy, «cozy cardio». +60-100 строк.
3. **Внутри TikTok Shop (когда откроется селлер-кабинет):** Affiliate Center → «Find creators» с фильтрами Health, 10k-300k, US — это заменит весь ручной поиск; текущая CSV станет затравкой для «target invite».
4. **Верификацию цифр** делать только для кандидатов в топ-100 — по 1 запросу на хендл; для остальных цифра не критична (TTS сам покажет GMV-потенциал).
5. **IG-крыло**: искать тех же людей — у 80% TikTok-микро есть IG с email-кнопкой; это и есть путь к email-контактам.

## Критерии отбора топ-50 из базы (рекомендация)

Брать в первую волну аутрича строки, где совпадает ≥3 из:
1. **Tier A** и размер 10k-300k подтверждён (или nano 10-50k — у них лучшая конверсия в ответ на DM и самая высокая ER);
2. **Уже аффилиат чужого supplement-бренда** (RYZE/Bloom/Goli/Arrae/Nello/LMNT — колонка why_fit): умеют снимать shoppable-видео, знают механику TTS, порог входа = просто лучший % комиссии;
3. **Ниша = наш SKU напрямую**: cortisol/adrenal (магний-стики, saffron), sleepy girl mocktail / сон (магний), ADHD/focus (lion's mane), moms energy (electrolytes, mushroom coffee), sea moss girls;
4. **US-подтверждён** (город/сеть магазинов/US-бренды в кэпшенах) — обязательное условие TTS;
5. **Формат — обзоры/рутины, а не чистая эстетика**: review-аккаунты (@meag.reviews-тип) конвертят в TTS лучше, чем aesthetic-аккаунты.

Анти-критерии: врачи/фармацевты-мега (юридически осторожны с клеймами, дороги), UK/AU/CA-криейтеры, аккаунты чисто food-review без wellness-угла (C-строки).

Приоритетные A-строки этой транши для первых DM: @theracheldodge, @ruthswingler, @marinawrightwellness, @ericananglefit, @simonesharice, @jenlaurenn, @tasteofnutrition, @wearegirlswhoeat, @glutenfreejackie, @laurenhefez, @chiomaadavido, @foodiesushiqueen (TTS-профи), @amateurfoodalchemist, @habitsofagoddess, @taylorflesherr, @_megan.little_.

---

# Транша №2 (2026-09-10)

**Итог:** +150 верифицированных строк (A=21, B=99, C=30) → **274 всего**. Методика транши №1 без изменений: только поисковый индекс, у каждой строки реальный source_url из выдачи, ничего не выдумано. Дубли против базы отсеяны скриптом.

## Что сработало лучше всего (новое в этой транше)

1. **Партнёрские хэштеги — главный апгрейд методики.** Запросы вида `"ollypartner"`, `"golipartner"`, `"bloompartner"`, `"maryruthspartner"`, `"lemmepartner"` (домен tiktok.com) отдают готовых аффилиатов с кодами прямо в кэпшене. Один запрос = 2-4 подтверждённых партнёра чужого supplement-бренда. Так найдены почти все новые A: @esnyhannah, @nazyfarnoosh (97.9k), @cararosedipietro (282.5k), @bri_ewing, @modhippiehabits (95.5k, New Chapter #Ad) и якоря C (@itskatesteinberg 2.9M, @lindamont 4.4M).
2. **Бренд-обзоры** (Sunday Scaries, True Sea Moss, MaryRuth's, Waterboy, Liquid IV, Olly, Hilma, Thorne, AG1, Lemme, ARMRA, Physician's Choice, Micro Ingredients, Goli-ashwa, Bloom greens): стабильно 2-5 хендлов на запрос. Жемчужины: @eatswithalee (75.3k, код EATSWITHALE20 у Hilma), @mindfulmarlaa (код MARLA20), @mylifeasamerica (обзор lion's mane gummies Sunday Scaries — наш SKU 1-в-1).
3. **Тренд-запросы**: cortisol face (@itsbrookeelle 214.2k — история восстановления), morning shed (5 новых), night shift nurse bag (@geezelouiseeeee 126.1k ICU SF), teacher 5am (@ms.johnson.teachess), kids magnesium (5 мам), PCOS smoothie, креатин для женщин, proffee, ASMR night routine, sleepy girl mocktail вариации.
4. **Верификация подписчиков**: 20 запросов, ~85% попаданий (Famous Birthdays/urlebird/Exolyt/Analisa). По-прежнему делать только для кандидатов в A.

## Что выжато / что осталось

| Источник | Статус |
|---|---|
| Партнёрские хэштеги (olly/goli/bloom/maryruths/lemme/hydroflask/cse) | ★★★★★ — НЕ выжат: остались arrae, nello, beam, mudwtr, armra, liquidiv, waterboy, alani × partner |
| Бренд-обзоры новых брендов | ★★★★☆ — рабочий; Cymbiotika/ARMRA дают коды в сниппетах, но без хендлов (искать «код + tiktok») |
| Тренд-запросы | ★★★☆☆ — начинают повторяться (sleepy girl / adrenal выдают уже наших) |
| Sunday Scaries бренд-майнинг | ★★☆☆☆ — выдача забита словом-мемом, не брендом |
| Liquid IV / AG1 | ★★★☆☆ — много discover-страниц, мало хендлов |
| 9-5 corporate girl | ★☆☆☆☆ — почти только discover-страницы |

## Пометки к данным транши №2

- **UK/AU-флаги (в C):** @chaos.to.sanity (84.5k, UK — жаль, идеальный lion's mane/ADHD профиль), @brittney_saunders (AU), @cl8ire888 (Novomins=UK), @hollyb_fitness («colourways»), @carmen_mair («stabilises»). Проверять при аутриче: @sairahayati, @poppymead, @trinicookingwithnatasha_, @kaanade (3.8M, возможно BR).
- **Собственные бренды — не трогать как аффилиатов:** @wellnesswithlinds (основатель drinksymbi), @maymoves (своя фабрика, не внесена).
- Приоритетные A этой транши для DM-волны: @eatswithalee, @itsbrookeelle, @cararosedipietro, @nazyfarnoosh, @katieyovin, @geezelouiseeeee, @modhippiehabits, @esnyhannah, @mindfulmarlaa, @mylifeasamerica, @candidlycarlie_, @mads_gainz.
- TTS-профи (deals/coupon-аккаунты, конвертят в shoppable сразу): @smartgadgetmama, @saleseekerscentral, @couponingwithtina, @tiktok.savvy (+ якорь C @austinfendler 369k).

## План на траншу №3 (до 500)

1. Партнёрские хэштеги оставшихся брендов (см. таблицу) — ожидание +40-60 A/B.
2. Коды из сниппетов без хендлов: `"NICOLECHANEY" armra`, `"LEXIESEGER" cymbiotika`, `"KATHERINEAIKEN10"` и т.п. — точечный поиск владельца кода.
3. IG-крыло для собранных 274 (email-контакты через IG-био) — на этапе аутрича.
4. Довериться Affiliate Center TTS, когда откроется кабинет: текущая база = target invite list.
