#!/usr/bin/env python3
"""Build README.md and README_<lang>.md from prompts.json.

Usage:
    python3 scripts/build_readme.py
"""
import json
from urllib.parse import quote
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "zenlee123/awesome-ai-image-prompts"

LANG_NAMES = {
    "en": "English", "zh": "简体中文", "ja": "日本語", "ko": "한국어",
    "es": "Español", "fr": "Français", "de": "Deutsch", "pt": "Português",
}

MODEL_NAMES = {
    "google/gemini-nano-banana-2.1-t2i": "Nano Banana 2.1",
    "google/gemini-3-pro-image-t2i": "Gemini 3 Pro Image",
    "openai/gpt-image-2.5-flare-t2i": "GPT Image 2.5",
}

UI = {
    "en": {
        "promo_title": 'Try these prompts on AIImage.com',
        "promo_desc": 'No API key or setup needed: open [AIImage.com]({home}), pick Nano Banana Pro, Nano Banana 2 or GPT Image 2.5, paste a prompt and get your image in seconds. **Start free.**',
        "try": 'Try on AIImage',
        "tools": 'Free Image Tools',
        "tools_desc": 'Polish your generated images with free online tools on AIImage.com:',
        "tool_names": ['Background Remover', 'Remove Object', 'Change Background Color', 'Image to Image', 'GIF Maker', 'Compress Image'],
        "tagline": "A curated collection of AI image generator prompts in 8 languages, each with a real generated preview.",
        "intro": "Every prompt below was run on a real model and the result is shown right next to it. Copy a prompt in your own language and paste it into Nano Banana, GPT Image, Gemini, Midjourney, Seedream, Flux or any other image generator.",
        "gallery": "Gallery", "contents": "Contents",
        "model": "Model", "ratio": "Aspect ratio",
        "note": "Preview images were generated from the English prompt. Modern multilingual models give very similar results from the translated prompts.",
        "api": "Generate via API",
        "api_desc": "All previews were generated with [RouterBase](https://routerbase.com), one OpenAI-compatible API for Nano Banana, GPT Image, Gemini, Seedream and more:",
        "tips": "Prompt Writing Tips",
        "tips_list": [
            "**Subject first**: say clearly what the image is about, then add details.",
            "**Name the medium**: photo, watercolor, 3D render, ukiyo-e, poster…",
            "**Describe the light**: golden hour, Rembrandt lighting, neon, overcast.",
            "**Add camera terms** for photos: lens (35mm, 85mm), aperture (f/1.4), angle.",
            "**Put text in quotes**: models render `\"JAZZ NIGHTS\"` far more accurately than unquoted text.",
        ],
        "contrib": "Contributing",
        "contrib_desc": "PRs are welcome! Add an entry to `prompts.json` (all 8 languages, or just the ones you know), then run `python3 scripts/generate.py` and `python3 scripts/build_readme.py`.",
        "license": "License",
        "license_desc": "Prompts and images are released under [CC0 1.0](LICENSE): use them for anything, no attribution needed.",
        "star": "If this collection helps you, please give it a ⭐ star!",
    },
    "zh": {
        "promo_title": '在 AIImage.com 上试试这些提示词',
        "promo_desc": '无需 API key，无需任何配置：打开 [AIImage.com]({home})，选择 Nano Banana Pro、Nano Banana 2 或 GPT Image 2.5，粘贴提示词，几秒就能出图。**免费开始。**',
        "try": '在 AIImage 试用',
        "tools": '免费图片工具',
        "tools_desc": 'AIImage.com 还提供免费在线工具，帮你进一步处理生成的图片：',
        "tool_names": ['一键抠图', 'AI 消除', '更换背景色', '图生图', 'GIF 制作', '图片压缩'],
        "tagline": "精选 AI 生图提示词合集，支持 8 种语言，每条都附真实生成的效果图。",
        "intro": "下面每条提示词都在真实模型上跑过，效果图就放在旁边。复制你熟悉语言的版本，粘贴到 Nano Banana、GPT Image、Gemini、Midjourney、即梦 Seedream、Flux 等任意生图工具即可使用。",
        "gallery": "效果预览", "contents": "目录",
        "model": "模型", "ratio": "画面比例",
        "note": "效果图使用英文提示词生成。主流多语言模型使用翻译后的提示词也能得到非常接近的效果。",
        "api": "通过 API 生成",
        "api_desc": "所有效果图均由 [RouterBase](https://routerbase.com) 生成。它用一套兼容 OpenAI 的 API 接入 Nano Banana、GPT Image、Gemini、Seedream 等模型：",
        "tips": "提示词写作技巧",
        "tips_list": [
            "**主体先行**：先说清楚画面主体是什么，再补充细节。",
            "**指明媒介**：照片、水彩、3D 渲染、浮世绘、海报……",
            "**描述光线**：黄金时刻、伦勃朗光、霓虹、阴天柔光。",
            "**照片加入相机参数**：焦段（35mm、85mm）、光圈（f/1.4）、拍摄角度。",
            "**文字放进引号**：写成 `\"JAZZ NIGHTS\"`，模型渲染文字会准确得多。",
        ],
        "contrib": "参与贡献",
        "contrib_desc": "欢迎提交 PR！在 `prompts.json` 中新增条目（8 种语言都写，或只写你会的），然后运行 `python3 scripts/generate.py` 和 `python3 scripts/build_readme.py`。",
        "license": "许可证",
        "license_desc": "提示词与图片以 [CC0 1.0](LICENSE) 发布：可用于任何用途，无需署名。",
        "star": "如果这个合集对你有帮助，欢迎点个 ⭐ Star！",
    },
    "ja": {
        "promo_title": 'AIImage.com でこのプロンプトを試す',
        "promo_desc": 'API キーも設定も不要：[AIImage.com]({home}) を開いて Nano Banana Pro、Nano Banana 2、GPT Image 2.5 から選び、プロンプトを貼り付けるだけで数秒で画像が完成。**無料で始められます。**',
        "try": 'AIImage で試す',
        "tools": '無料画像ツール',
        "tools_desc": '生成した画像は AIImage.com の無料オンラインツールでさらに仕上げられます：',
        "tool_names": ['背景削除', 'オブジェクト削除', '背景色の変更', '画像から画像', 'GIF メーカー', '画像圧縮'],
        "tagline": "8 か国語に対応した AI 画像生成プロンプト集。すべてのプロンプトに実際の生成例付き。",
        "intro": "以下のプロンプトはすべて実際のモデルで生成し、その結果を横に掲載しています。お好きな言語のプロンプトをコピーして、Nano Banana、GPT Image、Gemini、Midjourney、Seedream、Flux などの画像生成 AI に貼り付けてください。",
        "gallery": "ギャラリー", "contents": "目次",
        "model": "モデル", "ratio": "アスペクト比",
        "note": "プレビュー画像は英語のプロンプトから生成しています。最新の多言語モデルなら、翻訳版のプロンプトでもほぼ同じ結果が得られます。",
        "api": "API で生成する",
        "api_desc": "プレビュー画像はすべて [RouterBase](https://routerbase.com) で生成しました。OpenAI 互換の API ひとつで Nano Banana、GPT Image、Gemini、Seedream などを利用できます：",
        "tips": "プロンプト作成のコツ",
        "tips_list": [
            "**主題を最初に**：何を描くかをはっきり書いてから詳細を足す。",
            "**表現手法を指定**：写真、水彩、3D レンダリング、浮世絵、ポスターなど。",
            "**光を描写する**：ゴールデンアワー、レンブラントライティング、ネオン、曇天。",
            "**写真ならカメラ用語を**：レンズ（35mm、85mm）、絞り（f/1.4）、アングル。",
            "**文字は引用符で囲む**：`\"JAZZ NIGHTS\"` のように書くと文字の描画精度が大きく上がります。",
        ],
        "contrib": "コントリビュート",
        "contrib_desc": "PR 歓迎です！`prompts.json` にエントリーを追加し（8 言語すべて、または分かる言語だけで OK）、`python3 scripts/generate.py` と `python3 scripts/build_readme.py` を実行してください。",
        "license": "ライセンス",
        "license_desc": "プロンプトと画像は [CC0 1.0](LICENSE) で公開しています。クレジット表記不要で自由に使えます。",
        "star": "役に立ったら ⭐ スターをお願いします！",
    },
    "ko": {
        "promo_title": 'AIImage.com에서 이 프롬프트를 사용해 보세요',
        "promo_desc": 'API 키도 설정도 필요 없습니다. [AIImage.com]({home})에서 Nano Banana Pro, Nano Banana 2, GPT Image 2.5 중 하나를 고르고 프롬프트를 붙여 넣으면 몇 초 만에 이미지가 완성됩니다. **무료로 시작하세요.**',
        "try": 'AIImage에서 사용해 보기',
        "tools": '무료 이미지 도구',
        "tools_desc": '생성한 이미지는 AIImage.com의 무료 온라인 도구로 더 다듬을 수 있습니다:',
        "tool_names": ['배경 제거', '객체 지우기', '배경색 변경', '이미지로 이미지 생성', 'GIF 만들기', '이미지 압축'],
        "tagline": "8개 언어로 제공하는 AI 이미지 생성 프롬프트 모음. 모든 프롬프트에 실제 생성 결과 포함.",
        "intro": "아래의 모든 프롬프트는 실제 모델로 생성했으며 결과 이미지를 바로 옆에 보여 줍니다. 원하는 언어의 프롬프트를 복사해 Nano Banana, GPT Image, Gemini, Midjourney, Seedream, Flux 등 어떤 이미지 생성기에든 붙여 넣으세요.",
        "gallery": "갤러리", "contents": "목차",
        "model": "모델", "ratio": "화면 비율",
        "note": "미리보기 이미지는 영어 프롬프트로 생성했습니다. 최신 다국어 모델은 번역된 프롬프트로도 거의 같은 결과를 냅니다.",
        "api": "API로 생성하기",
        "api_desc": "모든 미리보기 이미지는 [RouterBase](https://routerbase.com)로 생성했습니다. OpenAI 호환 API 하나로 Nano Banana, GPT Image, Gemini, Seedream 등을 사용할 수 있습니다:",
        "tips": "프롬프트 작성 팁",
        "tips_list": [
            "**주제를 먼저**: 무엇을 그릴지 분명히 쓴 뒤 세부 사항을 더하세요.",
            "**표현 방식을 지정**: 사진, 수채화, 3D 렌더링, 우키요에, 포스터 등.",
            "**빛을 묘사**: 골든아워, 렘브란트 조명, 네온, 흐린 날.",
            "**사진에는 카메라 용어를**: 렌즈(35mm, 85mm), 조리개(f/1.4), 앵글.",
            "**텍스트는 따옴표로**: `\"JAZZ NIGHTS\"`처럼 쓰면 글자를 훨씬 정확하게 그립니다.",
        ],
        "contrib": "기여하기",
        "contrib_desc": "PR 환영합니다! `prompts.json`에 항목을 추가하고(8개 언어 전부 또는 아는 언어만), `python3 scripts/generate.py`와 `python3 scripts/build_readme.py`를 실행하세요.",
        "license": "라이선스",
        "license_desc": "프롬프트와 이미지는 [CC0 1.0](LICENSE)으로 공개되어 출처 표기 없이 자유롭게 사용할 수 있습니다.",
        "star": "도움이 되었다면 ⭐ 스타를 눌러 주세요!",
    },
    "es": {
        "promo_title": 'Prueba estos prompts en AIImage.com',
        "promo_desc": 'Sin API key ni configuración: abre [AIImage.com]({home}), elige Nano Banana Pro, Nano Banana 2 o GPT Image 2.5, pega un prompt y obtén tu imagen en segundos. **Empieza gratis.**',
        "try": 'Probar en AIImage',
        "tools": 'Herramientas de imagen gratis',
        "tools_desc": 'Retoca tus imágenes generadas con las herramientas online gratuitas de AIImage.com:',
        "tool_names": ['Quitar fondo', 'Eliminar objetos', 'Cambiar color de fondo', 'Imagen a imagen', 'Creador de GIF', 'Comprimir imagen'],
        "tagline": "Una colección seleccionada de prompts para generadores de imágenes con IA en 8 idiomas, cada uno con una vista previa real.",
        "intro": "Cada prompt se ha probado en un modelo real y el resultado aparece junto a él. Copia el prompt en tu idioma y pégalo en Nano Banana, GPT Image, Gemini, Midjourney, Seedream, Flux o cualquier otro generador de imágenes.",
        "gallery": "Galería", "contents": "Contenido",
        "model": "Modelo", "ratio": "Relación de aspecto",
        "note": "Las imágenes de muestra se generaron con el prompt en inglés. Los modelos multilingües actuales dan resultados muy parecidos con los prompts traducidos.",
        "api": "Generar por API",
        "api_desc": "Todas las vistas previas se generaron con [RouterBase](https://routerbase.com), una API compatible con OpenAI para Nano Banana, GPT Image, Gemini, Seedream y más:",
        "tips": "Consejos para escribir prompts",
        "tips_list": [
            "**El sujeto primero**: di claramente qué muestra la imagen y luego añade detalles.",
            "**Nombra la técnica**: foto, acuarela, render 3D, ukiyo-e, póster…",
            "**Describe la luz**: hora dorada, iluminación Rembrandt, neón, día nublado.",
            "**Usa términos de cámara** en fotos: objetivo (35 mm, 85 mm), apertura (f/1.4), ángulo.",
            "**Pon el texto entre comillas**: los modelos dibujan `\"JAZZ NIGHTS\"` con mucha más precisión.",
        ],
        "contrib": "Contribuir",
        "contrib_desc": "¡Los PR son bienvenidos! Añade una entrada a `prompts.json` (en los 8 idiomas o solo en los que conozcas) y ejecuta `python3 scripts/generate.py` y `python3 scripts/build_readme.py`.",
        "license": "Licencia",
        "license_desc": "Los prompts y las imágenes se publican bajo [CC0 1.0](LICENSE): úsalos para lo que quieras, sin necesidad de atribución.",
        "star": "Si esta colección te resulta útil, ¡dale una ⭐ estrella!",
    },
    "fr": {
        "promo_title": 'Essayez ces prompts sur AIImage.com',
        "promo_desc": 'Sans clé API ni configuration : ouvrez [AIImage.com]({home}), choisissez Nano Banana Pro, Nano Banana 2 ou GPT Image 2.5, collez un prompt et obtenez votre image en quelques secondes. **Commencez gratuitement.**',
        "try": 'Essayer sur AIImage',
        "tools": "Outils d'image gratuits",
        "tools_desc": "Peaufinez vos images générées avec les outils en ligne gratuits d'AIImage.com :",
        "tool_names": ["Supprimer l'arrière-plan", 'Effacer un objet', 'Changer la couleur de fond', 'Image vers image', 'Créateur de GIF', 'Compresser une image'],
        "tagline": "Une sélection de prompts pour générateurs d'images IA en 8 langues, chacun accompagné d'un véritable aperçu généré.",
        "intro": "Chaque prompt ci-dessous a été exécuté sur un vrai modèle, et le résultat est affiché juste à côté. Copiez le prompt dans votre langue et collez-le dans Nano Banana, GPT Image, Gemini, Midjourney, Seedream, Flux ou tout autre générateur d'images.",
        "gallery": "Galerie", "contents": "Sommaire",
        "model": "Modèle", "ratio": "Format",
        "note": "Les aperçus ont été générés à partir du prompt anglais. Les modèles multilingues récents donnent des résultats très proches avec les prompts traduits.",
        "api": "Générer via l'API",
        "api_desc": "Tous les aperçus ont été générés avec [RouterBase](https://routerbase.com), une API compatible OpenAI pour Nano Banana, GPT Image, Gemini, Seedream et plus encore :",
        "tips": "Conseils de rédaction",
        "tips_list": [
            "**Le sujet d'abord** : dites clairement ce que montre l'image, puis ajoutez les détails.",
            "**Nommez la technique** : photo, aquarelle, rendu 3D, ukiyo-e, affiche…",
            "**Décrivez la lumière** : heure dorée, éclairage Rembrandt, néon, ciel couvert.",
            "**Ajoutez des termes photo** : objectif (35 mm, 85 mm), ouverture (f/1,4), angle.",
            "**Mettez le texte entre guillemets** : les modèles rendent `\"JAZZ NIGHTS\"` bien plus fidèlement.",
        ],
        "contrib": "Contribuer",
        "contrib_desc": "Les PR sont les bienvenues ! Ajoutez une entrée dans `prompts.json` (dans les 8 langues ou seulement celles que vous maîtrisez), puis lancez `python3 scripts/generate.py` et `python3 scripts/build_readme.py`.",
        "license": "Licence",
        "license_desc": "Les prompts et les images sont publiés sous [CC0 1.0](LICENSE) : utilisez-les librement, sans attribution.",
        "star": "Si cette collection vous est utile, laissez-lui une ⭐ étoile !",
    },
    "de": {
        "promo_title": 'Probiere diese Prompts auf AIImage.com aus',
        "promo_desc": 'Kein API-Key, keine Einrichtung: Öffne [AIImage.com]({home}), wähle Nano Banana Pro, Nano Banana 2 oder GPT Image 2.5, füge einen Prompt ein und erhalte dein Bild in Sekunden. **Kostenlos starten.**',
        "try": 'Auf AIImage testen',
        "tools": 'Kostenlose Bild-Tools',
        "tools_desc": 'Bearbeite deine generierten Bilder mit den kostenlosen Online-Tools von AIImage.com:',
        "tool_names": ['Hintergrund entfernen', 'Objekt entfernen', 'Hintergrundfarbe ändern', 'Bild zu Bild', 'GIF-Ersteller', 'Bild komprimieren'],
        "tagline": "Eine kuratierte Sammlung von Prompts für KI-Bildgeneratoren in 8 Sprachen, jeweils mit einer echten generierten Vorschau.",
        "intro": "Jeder Prompt wurde auf einem echten Modell ausgeführt, das Ergebnis steht direkt daneben. Kopiere den Prompt in deiner Sprache und füge ihn in Nano Banana, GPT Image, Gemini, Midjourney, Seedream, Flux oder einen anderen Bildgenerator ein.",
        "gallery": "Galerie", "contents": "Inhalt",
        "model": "Modell", "ratio": "Seitenverhältnis",
        "note": "Die Vorschaubilder wurden mit dem englischen Prompt erzeugt. Moderne mehrsprachige Modelle liefern mit den übersetzten Prompts sehr ähnliche Ergebnisse.",
        "api": "Per API generieren",
        "api_desc": "Alle Vorschauen wurden mit [RouterBase](https://routerbase.com) erzeugt, einer OpenAI-kompatiblen API für Nano Banana, GPT Image, Gemini, Seedream und mehr:",
        "tips": "Tipps zum Prompt-Schreiben",
        "tips_list": [
            "**Motiv zuerst**: sag klar, worum es im Bild geht, dann folgen die Details.",
            "**Nenne das Medium**: Foto, Aquarell, 3D-Rendering, Ukiyo-e, Poster…",
            "**Beschreibe das Licht**: goldene Stunde, Rembrandt-Licht, Neon, bedeckter Himmel.",
            "**Kamerabegriffe für Fotos**: Objektiv (35 mm, 85 mm), Blende (f/1,4), Perspektive.",
            "**Text in Anführungszeichen**: `\"JAZZ NIGHTS\"` wird von Modellen deutlich genauer dargestellt.",
        ],
        "contrib": "Mitmachen",
        "contrib_desc": "PRs sind willkommen! Füge einen Eintrag in `prompts.json` hinzu (in allen 8 Sprachen oder nur in denen, die du kannst) und führe `python3 scripts/generate.py` sowie `python3 scripts/build_readme.py` aus.",
        "license": "Lizenz",
        "license_desc": "Prompts und Bilder stehen unter [CC0 1.0](LICENSE): frei für jeden Zweck, ohne Namensnennung.",
        "star": "Wenn dir diese Sammlung hilft, gib ihr gern einen ⭐ Stern!",
    },
    "pt": {
        "promo_title": 'Teste estes prompts no AIImage.com',
        "promo_desc": 'Sem chave de API nem configuração: abra o [AIImage.com]({home}), escolha Nano Banana Pro, Nano Banana 2 ou GPT Image 2.5, cole um prompt e receba sua imagem em segundos. **Comece grátis.**',
        "try": 'Testar no AIImage',
        "tools": 'Ferramentas de imagem grátis',
        "tools_desc": 'Dê o toque final nas imagens geradas com as ferramentas online gratuitas do AIImage.com:',
        "tool_names": ['Remover fundo', 'Remover objeto', 'Mudar cor de fundo', 'Imagem para imagem', 'Criador de GIF', 'Comprimir imagem'],
        "tagline": "Uma coleção selecionada de prompts para geradores de imagens com IA em 8 idiomas, cada um com uma prévia real gerada.",
        "intro": "Cada prompt abaixo foi executado num modelo real, e o resultado aparece logo ao lado. Copie o prompt no seu idioma e cole no Nano Banana, GPT Image, Gemini, Midjourney, Seedream, Flux ou qualquer outro gerador de imagens.",
        "gallery": "Galeria", "contents": "Sumário",
        "model": "Modelo", "ratio": "Proporção",
        "note": "As imagens de prévia foram geradas com o prompt em inglês. Os modelos multilíngues atuais dão resultados muito parecidos com os prompts traduzidos.",
        "api": "Gerar via API",
        "api_desc": "Todas as prévias foram geradas com o [RouterBase](https://routerbase.com), uma API compatível com OpenAI para Nano Banana, GPT Image, Gemini, Seedream e outros:",
        "tips": "Dicas para escrever prompts",
        "tips_list": [
            "**Assunto primeiro**: diga claramente o que a imagem mostra e depois acrescente detalhes.",
            "**Nomeie a técnica**: foto, aquarela, render 3D, ukiyo-e, pôster…",
            "**Descreva a luz**: hora dourada, iluminação Rembrandt, neon, céu nublado.",
            "**Use termos de câmera** em fotos: lente (35 mm, 85 mm), abertura (f/1.4), ângulo.",
            "**Coloque o texto entre aspas**: os modelos desenham `\"JAZZ NIGHTS\"` com muito mais precisão.",
        ],
        "contrib": "Contribuindo",
        "contrib_desc": "PRs são bem-vindos! Adicione uma entrada em `prompts.json` (nos 8 idiomas ou só nos que você domina) e rode `python3 scripts/generate.py` e `python3 scripts/build_readme.py`.",
        "license": "Licença",
        "license_desc": "Prompts e imagens são publicados sob [CC0 1.0](LICENSE): use para qualquer finalidade, sem necessidade de atribuição.",
        "star": "Se esta coleção te ajudou, deixe uma ⭐ estrela!",
    },
}

API_SNIPPET = """```bash
curl https://routerbase.com/v1/images/generations \\
  -H "Authorization: Bearer $ROUTERBASE_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"model": "google/gemini-nano-banana-2.1-t2i", "prompt": "…", "aspect_ratio": "16:9"}'
```"""


MODEL_PAGES = {
    "google/gemini-nano-banana-2.1-t2i": "nano-banana-2",
    "google/gemini-3-pro-image-t2i": "nano-banana-pro",
    "openai/gpt-image-2.5-flare-t2i": "gpt-image-2-5",
}

TOOL_PAGES = ["background-remover", "remove-object", "change-background-color",
              "image-to-image", "gif-maker", "compress-image"]

UTM = "utm_source=github&utm_medium=readme&utm_campaign=awesome-ai-image-prompts"


def site(lang, path=""):
    parts = [x for x in ("" if lang == "en" else lang, path) if x]
    return f"https://aiimage.com/{'/'.join(parts)}?{UTM}"


def readme_name(lang):
    return "README.md" if lang == "en" else f"README_{lang}.md"


def build(lang, data):
    t = UI[lang]
    cats = data["categories"]
    prompts = data["prompts"]
    out = []

    switcher = " | ".join(
        f"**{LANG_NAMES[l]}**" if l == lang else f"[{LANG_NAMES[l]}]({readme_name(l)})"
        for l in data["languages"])

    out += [
        '<div align="center">',
        "",
        "# Awesome AI Image Prompts",
        "",
        f"[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        f"[![Prompts](https://img.shields.io/badge/prompts-{len(prompts)}-blue)](#{cats[0]['id']})",
        f"[![Languages](https://img.shields.io/badge/languages-{len(data['languages'])}-green)](#)",
        f"[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-lightgrey)](LICENSE)",
        f"[![GitHub stars](https://img.shields.io/github/stars/{REPO}?style=social)](https://github.com/{REPO})",
        "",
        switcher,
        "",
        t["tagline"],
        "",
        f'<a href="{site(lang)}"><img src="https://img.shields.io/badge/'
        f'%F0%9F%8E%A8%20{t["try"].replace(" ", "%20")}-AIImage.com-ff5a5f?style=for-the-badge" '
        f'alt="{t["try"]}"></a>',
        "",
        "</div>",
        "",
        t["intro"],
        "",
        f"> {t['note']}",
        "",
        f"### 🎨 {t['promo_title']}",
        "",
        t["promo_desc"].format(home=site(lang)),
        "",
    ]

    # Gallery: 4-column thumbnail grid linking to each entry
    out += [f"## {t['gallery']}", "", "<table>"]
    for i in range(0, len(prompts), 4):
        out.append("<tr>")
        for p in prompts[i:i + 4]:
            out.append(f'<td align="center" width="25%"><a href="#{p["id"]}">'
                       f'<img src="images/{p["id"]}.webp" alt="{p["title"][lang]}"><br>'
                       f'<sub>{p["title"][lang]}</sub></a></td>')
        out.append("</tr>")
    out += ["</table>", ""]

    out += [f"## {t['contents']}", ""]
    for c in cats:
        out.append(f'- [{c["title"][lang]}](#{c["id"]})')
    out += [f"- [{t['tools']}](#tools)", f"- [{t['api']}](#api)", f"- [{t['tips']}](#tips)",
            f"- [{t['contrib']}](#contributing)", ""]

    for c in cats:
        out += [f'<a id="{c["id"]}"></a>', "", f'## {c["title"][lang]}', ""]
        for p in (p for p in prompts if p["category"] == c["id"]):
            out += [
                f'<a id="{p["id"]}"></a>',
                "",
                f'### {p["title"][lang]}',
                "",
                f'<img src="images/{p["id"]}.webp" width="560" alt="{p["title"][lang]}">',
                "",
                "```text",
                p["prompt"][lang],
                "```",
                "",
                f'**{t["model"]}:** {MODEL_NAMES.get(p["model"], p["model"])} · '
                f'**{t["ratio"]}:** `{p["aspect_ratio"]}` · '
                f'[**▶ {t["try"]}**]({site(lang, MODEL_PAGES[p["model"]])})',
                "",
            ]
            if lang != "en":
                out += ["<details><summary>English</summary>", "", "```text",
                        p["prompt"]["en"], "```", "", "</details>", ""]

    out += ['<a id="tools"></a>', "", f"## {t['tools']}", "", t["tools_desc"], ""]
    out += [f"- [{name}]({site(lang, path)})" for name, path in zip(t["tool_names"], TOOL_PAGES)]
    out += [f"- [{t['tools']} →]({site(lang, 'tools')})", ""]
    out += ['<a id="api"></a>', "", f"## {t['api']}", "", t["api_desc"], "", API_SNIPPET, ""]
    out += ['<a id="tips"></a>', "", f"## {t['tips']}", ""]
    out += [f"{i}. {tip}" for i, tip in enumerate(t["tips_list"], 1)]
    out += ["", '<a id="contributing"></a>', "", f"## {t['contrib']}", "", t["contrib_desc"], ""]
    out += [f"## {t['license']}", "", t["license_desc"], "", "---", "",
            f'<div align="center">{t["star"]}</div>', ""]
    return "\n".join(out)


def main():
    data = json.loads((ROOT / "prompts.json").read_text())
    for lang in data["languages"]:
        (ROOT / readme_name(lang)).write_text(build(lang, data))
        print(f"wrote {readme_name(lang)}")


if __name__ == "__main__":
    main()
