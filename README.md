# 暴躁教練健身飲食打卡分析器

使用 OpenAI 相容 API 與 Pydantic Structured Output，將每日飲食打卡轉成固定格式的熱量、蛋白質評級、毒舌點評與改善行動。

## 使用 uv 執行

```powershell
uv sync
Copy-Item .env.example .env
uv run python src/main.py
```

啟動後，程式會提示你輸入今天吃了什麼，例如：

```text
請輸入今天吃了什麼（例如：早餐...；午餐...）：早餐：蛋餅和無糖豆漿；午餐：雞腿便當
```

預設連線到本地 Ollama 的 `http://localhost:11434/v1`，也可以在 `.env` 中改成其他 OpenAI 相容服務。

> `.env` 只供本機使用，已被 `.gitignore` 排除，請勿提交 API 金鑰。