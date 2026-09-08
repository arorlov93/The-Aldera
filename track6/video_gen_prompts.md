# AI-видеогенерация — промпты для якорных видео The Aldera

Статус: API Replicate / fal.ai / Kling / MiniMax / Veo доступны из среды (проверено 08.09).
Ждём API-ключ владельца. План: генерирую клипы по 5-10 сек → монтирую в ffmpeg
(склейка, титры-хуки, цветокор, 9:16) → вставляю в лендинг/отдаю файлом.

Рекомендация модели: **Kling 2.5 Turbo** (лучший физический реализм жидкости/сыпучки,
~$0.3-0.5 за 5-сек клип) или **Veo 3 Fast** (лучшее качество, ~$1.5-3 за 8 сек).
Бюджет hero-видео целиком: $5-15 с итерациями.

## Якорь №1 — магниевый стик → стакан (hero лендинга)

Клип A (хук, 5с):
> Macro cinematic shot, a hand tears open a matte cream-colored supplement stick packet
> with dark green accents, fine pale powder begins to pour out, moody dark green studio
> background, soft window light from the left, shallow depth of field, photorealistic,
> 4k, vertical 9:16

Клип B (шипение, 5-10с):
> Extreme macro shot, fine powder pouring into a tall glass of cold sparkling water,
> golden lemonade tint, fizzing bubbles rising rapidly, droplets of condensation on the
> glass, dark forest-green background, dramatic side lighting, slow motion, photorealistic
> product commercial, vertical 9:16

Клип C (глоток/ритуал, 5с):
> Cozy evening scene, a woman in a soft sweater takes a slow sip from a glass of pale
> golden fizzy drink, warm dim bedroom lighting, book and candle on nightstand, calm
> relaxed mood, cinematic shallow depth of field, photorealistic, vertical 9:16

Клип D (финал-упаковка, 3-5с):
> Product shot, minimalist supplement box standing on a stone surface, deep emerald green
> and cream packaging, soft studio lighting, slow camera push-in, premium commercial
> style, photorealistic, vertical 9:16

## Якорь №2 — разлом капсулы

> Extreme macro, two fingers snap open a clear supplement capsule, fine herbal powder
> spills out in slow motion forming a small mound on a black slate surface, dust
> particles catching the light, dramatic rim lighting, photorealistic, vertical 9:16

## Якорь №3 — гамми макро

> Macro shot, a knife slices a glossy amber gummy in half revealing dense translucent
> texture, then fingers gently squeeze the half showing elasticity, studio lighting on
> dark green backdrop, photorealistic food commercial, vertical 9:16

## Якорь №4 — весы-манифест

> Macro overhead shot, fine powder being poured slowly onto a small jewelry scale, digital
> display counting up to 150, minimalist lab aesthetic, cream and green tones, precise
> clinical lighting, photorealistic, vertical 9:16

## Правила
- Упаковка в генерациях — БЕЗ читаемого текста (AI искажает буквы): нейтральная
  крем/зелёная банка. Логотип и титры накладываю в ffmpeg поверх.
- В листинги маркетплейсов AI-видео не ставим как «реальный продукт» — только на
  лендинг/соцсети как стилизованный ролик, до съёмки реальных образцов.
- Каждый клип: 2-3 генерации, отбираем лучшую. Титры-хуки из content-factory §2, † где надо.
