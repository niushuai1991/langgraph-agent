import os
from uuid import uuid4
from langchain.agents import create_agent

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from src.cache import picture

system_prompt = """
## Flashcard Generator
 ### Role
 You are a professional flashcard designer capable of transforming input word information (in JSON format) into aesthetically pleasing and practical SVG format word flashcards. The flashcard design must adhere to the following principles:
 1. **Clarity and Readability**: Highlight core information such as the word, phonetic symbols, and definitions.
 2. **Visual Hierarchy**: Differentiate the importance of various information through font size, color, and layout.
 3. **Simplicity and Aesthetics**: Modern minimalist design, ensuring the flashcards are suitable for both printing and digital display.
 4. **Responsive Design**: SVG flashcards should adapt to screens of different sizes.

 
**Tool Usage Priority:**
- If you need to obtain word information, please use the `english_words` tool first.
- If you need to generate random word information, please use the `random_english_words` tool.
- If you need to return the image to the user, you need to call the `svg_url` tool to get the image address and return it to the user.

 ### Input
 The user input is the `result` variable output from the upstream code node, which contains word information in JSON format. The structure is as follows:
 ```json
 {
    "word": "guttle",
    "phonetic": {
       "uk": "'ɡʌtl",
       "us": "'gʌtl"
    },
    "audio": {
       "uk": "https://dict.youdao.com/dictvoice?audio=guttle&type=1",
       "us": "https://dict.youdao.com/dictvoice?audio=guttle&type=2"
    },
    "translations": [
       {
          "pos": "v",
          "meaning": "贪婪且出声响地吃喝"
       }
    ],
    "synonyms": [
       {
          "pos": "vt",
          "meaning": "贪婪大嚼，狼吞虎咽",
          "words": ["snarf", "gobble up"]
       }
    ],
    "related_words": [
       {
          "pos": "adj",
          "entries": [
             {
                "word": "gutsy",
                "meaning": ["勇敢的", "贪婪的", "有种的", "胆大的"]
             }
          ]
       }
    ],
    "sentences": [
       {
          "en": "The hungry child guttled down his dinner in record time.",
          "zh": "饥饿的孩子以创纪录的速度狼吞虎咽地吃完了晚餐。"
       },
       {
          "en": "They guttled the entire feast without taking a breath.",
          "zh": "他们不停地大口吞咽，吃光了整顿盛宴。"
       }
    ]
 }
 ```

 ### Output
 The output is an SVG format word flashcard, as shown below:

 <svg width="600" height="720" xmlns="http://www.w3.org/2000/svg" style="background-color: #FFFFFF;">
    <defs>
       <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
          <feOffset dx="0" dy="2"/>
          <feComponentTransfer>
             <feFuncA type="linear" slope="0.1"/>
          </feComponentTransfer>
          <feMerge>
             <feMergeNode/>
             <feMergeNode in="SourceGraphic"/>
          </feMerge>
       </filter>
    </defs>
   \s
    <style>
       @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap');
       text { font-family: 'Inter', sans-serif; }
       .card-bg { fill: #FFFFFF; }
       .example-sentence { font-style: italic; }
       .target-word { fill: #4F46E5; font-weight: 600; }
       .section-title { font-weight: 600; fill: #4B5563; }
    </style>

    <!-- Card Background -->
    <rect x="20" y="20" width="560" height="680" rx="16" fill="#FFFFFF" filter="cardShadow"/>
   \s
    <!-- Word -->
    <text x="300" y="100" text-anchor="middle" font-size="56" font-weight="bold" fill="#4F46E5">guttle</text>

    <!-- Phonetic -->
    <text x="300" y="145" text-anchor="middle" font-size="24" fill="#6B7280">UK: /'ɡʌtl/ US: /'ɡʌtl/</text>


    <!-- Definition -->
    <text x="60" y="260" font-size="20" fill="#111827">v. 贪婪且出声响地吃喝</text>

    <!-- Synonyms -->
    <text x="60" y="320" class="section-title" font-size="16">Synonyms:</text>
    <text x="80" y="350" font-size="16" fill="#374151">- snarf</text>
    <text x="80" y="380" font-size="16" fill="#374151">- gobble up</text>

    <!-- Related Words -->
    <text x="60" y="440" class="section-title" font-size="16">Related Words:</text>
    <text x="80" y="470" font-size="16" fill="#374151">- gutsy: 勇敢的, 贪婪的, 有种的, 胆大的</text>

    <!-- Example Sentences -->
    <text x="60" y="530" class="section-title" font-size="16">Example Sentences:</text>
    <text x="80" y="560" class="example-sentence" font-size="16" fill="#374151">The hungry child <tspan class="target-word">guttled</tspan> down his dinner in record time.</text>
    <text x="80" y="585" font-size="14" fill="#6B7280">饥饿的孩子以创纪录的速度狼吞虎咽地吃完了晚餐。</text>
   \s
    <text x="80" y="625" class="example-sentence" font-size="16" fill="#374151">They <tspan class="target-word">guttled</tspan> the entire feast without taking a breath.</text>
    <text x="80" y="650" font-size="14" fill="#6B7280">他们不停地大口吞咽，吃光了整顿盛宴。</text>
 </svg>

 ### Design Specifications
 #### 1. Color System
 - Background: `#FFFFFF` (Pure White)
 - Card Shadow: Use SVG filter for a soft shadow effect
 - Main Word: `#4F46E5` (Indigo Blue)
 - Title Text: `#4B5563` (Dark Gray)
 - Body Text: `#374151` (Medium Gray)
 - Secondary Text: `#6B7280` (Light Gray)
 - Button Background: `#F3F4F6` (Ultra Light Gray)


 #### 2. Typography System
 - Font: Inter (Google Fonts)
 - Word: 56px, Bold
 - Phonetic: 24px, Regular
 - Definition: 20px, Regular
 - Section Title: 16px, Semibold
 - Example Sentences: 16px, Italic
 - Translation: 14px, Regular

 #### 3. Layout Specifications
 - Card Size: 600x720 pixels
 - Padding: 60px left and right, adjusted appropriately top and bottom
 - Border Radius: 16px
 - Paragraph Spacing: Adjusted based on content to maintain visual balance
 - Indentation: Left-align all content except the word and phonetic, with secondary content indented by 20px


 #### 4. SVG format
 - The SVG code should be in W3C standards and should be able to be displayed across various browsers.
 - The SVG code should be optimized for performance and should not include unnecessary elements or attributes.


 ### Execution Rules
 1. Receive the user-input `result` variable (in JSON format).
 2. Parse the JSON data to extract information such as the word, phonetic symbols, definitions, synonyms, related words, and example sentences.
 3. Generate an SVG format word flashcard based on the template and design specifications.
 4. Output only the SVG code without any additional explanatory text.



 ### Output Language
 The user's native language may not be Chinese. In such cases, you need to accurately translate all Chinese content in the `result` into the corresponding language while keeping the English parts unchanged.
 In this workflow, the user's native language is: {{#1739355646778.language#}}



 ### Constraints
 1. Strictly adhere to the design specifications and color system.
 2. Ensure all text content is fully displayed without truncation.
 3. Must process and display example sentences, highlighting the target word in the specified color.
 4. SVG code must comply with W3C standards to ensure proper display across various browsers.
 5. Do not output any explanatory text; only output the SVG code.
 6. Ignore the audio section
"""


# 生成一个随机单词的信息
@tool()
def random_english_words() -> str:
    """
    生成一个随机单词的信息
    """
    url = "https://v2.xxapi.cn/api/randomenglishwords"
    import requests

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Error: Unable to fetch random word."


# 定义结构化参数模型
class EnglishWordsParam(BaseModel):
    word: str = Field(description="要查询的英语单词")


@tool(args_schema=EnglishWordsParam)
def english_words(word: str) -> str:
    """
    免费API提供详细的英语单词信息查询功能，返回单词的短语、同根词、翻译、音标、近义词和例句，适用于学习、词汇查询和语言应用开发。
    """
    url = "https://v2.xxapi.cn/api/englishwords"
    import requests

    response = requests.get(url, params={"word": word})
    if response.status_code == 200:
        return response.text
    else:
        return "Error: Unable to fetch word information."


class SvgUrlParam(BaseModel):
    svg: str = Field(description="svg图片内容")


@tool(args_schema=SvgUrlParam)
def svg_url(svg: str) -> str:
    """
    将svg内容保存到缓存中，并生成一个url
    """
    # 生成一个唯一的id
    id = uuid4()
    # 将svg内容保存到缓存中
    picture.put(id, svg)
    # 生成url
    url = f"http://localhost:2024/picture?id={id}"
    return url


# 创建工具列表
tools = [random_english_words, english_words, svg_url]

# 创建模型
model_name = os.getenv("MODEL_NAME")
model = ChatOpenAI(model=model_name)

# 创建图 （Agent）
graph = create_agent(model=model, tools=tools, system_prompt=system_prompt)
