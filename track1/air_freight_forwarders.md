# Авиафрахт Китай → США: форвардеры для запроса котировок

**Задача:** проверить рыночную ставку для авиадоставки пробной партии стик-паков (порошковые БАДы) Сиань → Майами. Поставщик просит **~$12.5/кг DDP all-in** — проверяем, насколько это завышено.

**Спецификация груза (вставлять в запрос котировки):**
- Груз: порошковые пищевые добавки (магний, электролиты, кофейные смеси) в розничных коробках; не ДГ, не жидкость
- ~60 коробов 40×40×45 см, объёмный вес ~12 кг/короб → **~720 кг chargeable**
- Origin: Сиань (XIY) или забор с хаба PVG/CAN; в будущем возможны Чжэнчжоу, Гуанчжоу, Ухань, Нанкин
- Destination: Майами, FL (MIA), до двери или аэропорт + брокер
- Условия: DDP или DAP c US-таможней **включая FDA Prior Notice** (диетические добавки)
- Забор: середина–конец сентября 2026

---

## 1. Сводная таблица форвардеров (10 + 2 платформы)

| # | Компания | Город | Специализация | FDA / DDP опыт | Email | Сайт |
|---|----------|-------|---------------|----------------|-------|------|
| 1 | **VoltFreight** | Шэньчжэнь | DDP-специалист Китай→США, еда/добавки | **Да, профильный**: собственный гайд по FDA Prior Notice для еды/БАДов, DDP до двери | info@voltfreight.com | [voltfreight.com](https://voltfreight.com/shipping-food-from-china-to-usa/) |
| 2 | **Winsky Freight** | Шэньчжэнь | DDP air/sea Китай→США, Amazon FBA | DDP до двери США — да; FDA — уточнить в запросе | sales@winskyfreight.com | [winskyfreight.com](https://www.winskyfreight.com/) |
| 3 | **Super International Shipping (SIS)** | Гонконг / Гуанчжоу | DDP air Китай→США, e-commerce | DDP — да (отдельная DDP-страница); FDA — уточнить | info@super-internationalshipping.com | [super-internationalshipping.com](https://super-internationalshipping.com/shipping-service-from-china/ddp-shipping-from-china/) |
| 4 | **Forest Shipping** | Гуанчжоу (HQ Дунгуань, офисы в 18 городах Китая + США) | Крупный FBA/DDP-оператор, air+sea | DDP/FBA — ядро бизнеса; FDA — уточнить | support@forestshipping.com, forest@forestshipping.com | [forestshipping.com](https://www.forestshipping.com/) |
| 5 | **DFH Logistics** | Гуанчжоу/Шэньчжэнь | Air/sea DDP Китай→США, публикует тарифы | DDP — да, публикуют ставки $5–10/кг air DDP | info@dfhlogistics.com | [dfhlogistics.com](https://dfhlogistics.com/air-freight-from-china-to-usa/) |
| 6 | **Tonlexing Logistics** | Шэньчжэнь | DDP air/sea Китай→США | DDP — да (профильные гайды по DDP USA) | info@tonlexing.com | [tonlexing.com](https://www.tonlexing.com/comprehensive-guide-to-ddp-shipping-from-china-to-the-usa/) |
| 7 | **BETTERluck (BL) Shipping** | Гуанчжоу | Авиа/море, **профильная страница по health supplements в США** | Да: позиционируются на добавках; DDP — да | sales8@blshipping.com | [blshipping.com](https://blshipping.com/agent/a_freight_forwarder_can_post_Health_supplements_from_China) |
| 8 | **Dimerco Express Group** | Тайбэй; ~50 офисов в Китае, вкл. **Сиань** | Классический азиатский авиафорвардер (IATA), сильный на внутренних хабах Китая | Регулируемые грузы — да; DDP по запросу | info@dimerco.com, sales@dimerco.com | [dimerco.com](https://dimerco.com/global-logistics-network/china-freight-forwarder/) |
| 9 | **Sinotrans Limited** | Пекин (госхолдинг), филиал в Шэньси/Сиане | Крупнейший форвардер Китая, авиа-подразделение Sinoair | Работают со всеми категориями; DDP через агентов в США | marketing@sinotrans.com | [sinotrans.com](http://www.sinotrans.com/col/col3886/index.html) |
| 10 | **KLN / Kerry Logistics (Kerry EAS в Китае)** | Гонконг; офисы по всему Китаю | IATA-форвардер полного цикла, air export из Китая | Регулируемые грузы — да; DDP по запросу | contact@kerrylogistics.com; air export Пекин: oliverwang@kerryeas.com | [kln.com](https://www.kln.com/en/contacts/) |
| П1 | **Freightos.com** (маркетплейс) | онлайн | Мгновенные котировки от десятков форвардеров, бенчмарк | Фильтр по door-to-door; FDA указывается в деталях груза | — (онлайн-квота) | [freightos.com](https://www.freightos.com/) |
| П2 | **Flexport** | онлайн / США | Цифровой форвардер, свой брокеридж (в т.ч. FDA) | **Да**: собственная US-таможня, FDA-clearance; есть страница ставок Shenzhen→Miami | — (квота на сайте) | [flexport.com/rates/cnszp/usmia](https://www.flexport.com/rates/cnszp/usmia) |

Резерв: DDPCHAIN, Шэньчжэнь — sale@ddpchain.com, публикуют тарифы air Китай→США ([ddpchain.com/usa](https://ddpchain.com/usa/)); SF International (SF Express) — квота через сайт [sf-international.com](https://www.sf-international.com/us/en/), но это скорее B2C/экспресс-канал.

**Примечания:**
- Минимальный объём: у DDP-линий (№1–7) типичный минимум 21–100 кг — наши 720 кг для них «сладкий» размер, дают скидку от базовой ставки.
- Из перечисленных прямой офис в Сиане подтверждён у Dimerco и Sinotrans; DDP-линии №1–7 заберут груз в Сиане курьером/фурой до своего склада в CAN/SZX/PVG (обычно +¥1–2/кг).
- FDA Prior Notice: явно заявлен у VoltFreight, BETTERluck, Flexport. Остальным в запросе обязательно писать: *«Cargo is FDA-regulated dietary supplements — please confirm you handle FDA Prior Notice + customs clearance, or quote DAP airport + we use our broker»*.

---

## 2. Рыночные бенчмарки ставок (2025–2026)

| Источник | Что показывает | Ставка |
|----------|----------------|--------|
| [Freightos Air Index (FAX), Greater China → North America](https://www.freightos.com/enterprise/terminal/fax-greater-china-asia-to-north-america/) | Спот аэропорт–аэропорт, general cargo, weight break 300–1000 кг | **~$6.5–7.0/кг** (август 2026; пик >$7.0, к концу месяца ~$6.5) |
| [STAT Times / Freightos outlook 2026](https://www.stattimes.com/air-cargo/global-air-cargo-rates-ease-after-peak-season-freightos-data-shows-1357688) | Динамика транстихоокеанских ставок | Китай→США ~+20% к 2025 г., >$7/кг на пиках |
| [BSI Freight, China→World 2026](https://www.bsifreight.com/knowledge/guides-resources/air-freight-rates-from-china-to-world) | Диапазон Китай→США 2026 | **$4.50–8.20/кг** (аэропорт–аэропорт); пик-сезон сен–ноя **+25–40%** |
| [DFH Logistics — Air freight China→USA](https://dfhlogistics.com/air-freight-from-china-to-usa/) | Публичный прайс DDP air door-to-door | **$5–10/кг** general cargo |
| [AiDeliv — DDP shipping cost China→USA](https://aideliv.com/ddp-shipping-cost) | Примеры DDP air all-in | **$7.57–8.29/кг** |
| [DDPCHAIN — China→USA](https://ddpchain.com/usa/) | DDP air линии (FBA/e-commerce) | **$4–10/кг**, 6–12 дней |
| [DFH — Shipping rates China→USA](https://dfhlogistics.com/shipping-rates-from-china-to-usa/) | Надбавка Восточное побережье (Майами) vs Запад | **+$0.5–1.5/кг** для air |

### Вывод: честная all-in ставка для нашего груза

Сборка для 720 кг chargeable, XIY→MIA, DDP c FDA, сентябрь 2026 (начало пик-сезона):

- База аэропорт–аэропорт (FAX): ~$6.5–7.0/кг, у DDP-линий через консолидацию на LAX/ORD/JFK — дешевле, $5.5–6.5/кг
- Майами (Восточное побережье, не главный air-хаб) — +$0.5–1.5/кг
- Забор в Сиане + фура до хаба CAN/PVG — +$0.3–0.5/кг
- FDA Prior Notice + брокер + bond — фикс ~$200–400/партия ≈ +$0.3–0.6/кг на 720 кг
- Пошлина на добавки (HS 2106.90) — зависит от тарифов на кит. товары; в DDP её обязаны включить и расшифровать отдельно

**Честный all-in DDP: ~$7.5–9.5/кг** (из CAN/PVG — ближе к $7–8.5; из Сианя в пик — до $9.5).
**Ставка поставщика $12.5/кг завышена на ~30–45%** (маржа посредника $2.5–4.5/кг ≈ $1,800–3,200 на партию). При этом $6–8/кг «all-in DDP до Майами с FDA» в сентябрьский пик — скорее нижняя граница, реалистичен таргет **≤$9/кг**, а при отгрузке из Гуанчжоу/Шанхая — **≤$8/кг**.

---

## 3. Рекомендация (с кого начать)

Начать параллельно с трёх: **VoltFreight** (info@voltfreight.com — профиль «еда/БАДы + FDA Prior Notice», дадут самую релевантную DDP-цену) и **Dimerco** (sales@dimerco.com — офис в Сиане, честная классическая котировка XIY→MIA как ориентир «сверху»), плюс мгновенный бенчмарк на **Flexport** ([flexport.com/rates/cnszp/usmia](https://www.flexport.com/rates/cnszp/usmia)) / Freightos без переписки.
Второй волной — Winsky, Forest, SIS, DFH, BETTERluck: 3–4 ответа дадут коридор рынка, с которым идти к поставщику пересматривать $12.5/кг.
