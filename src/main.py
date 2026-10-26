import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class NutritionReview(BaseModel):
    estimated_calories: int = Field(description="預估攝取的總熱量 (kcal)")
    protein_level: str = Field(description="蛋白質評級：充足 / 勉強合格 / 嚴重缺乏")
    roast_comment: str = Field(description="毒舌嚴厲、反向激勵的專業教練點評")
    action_item: str = Field(description="具體且可執行的飲食改善建議")


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "ollama"),
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
)


def analyze_meal(meal_log: str) -> NutritionReview:
    prompt = f"""
    你是一位極度嚴格、毒舌但專業的健身健美教練。
    請分析學員今日的飲食紀錄，指出營養問題並給予毒舌評價。

    學員打卡紀錄：
    {meal_log}
    """

    response = client.beta.chat.completions.parse(
        model=os.getenv("LLM_MODEL", "llama3.1"),
        messages=[
            {
                "role": "system",
                "content": "你是一位專業且講話一針見血的毒舌健身教練。",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=NutritionReview,
    )

    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise RuntimeError("LLM 未回傳符合 NutritionReview 的結構化結果")
    return parsed


if __name__ == "__main__":
    sample_input = (
        "早餐：一杯大冰奶、鮪魚蛋餅。午餐：炸排骨便當（白飯吃光）。"
        "下午：喝了一杯微糖珍珠鮮奶茶。"
    )
    print("正在由教練分析飲食紀錄...\n")
    result = analyze_meal(sample_input)

    print("=== 飲食分析結果 (結構化 JSON) ===")
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
