from dataclasses import dataclass, field

from openai import OpenAI
import logging.config
from src.config import *
from src.llms.prompts import prompts_tpl

logger = logging.getLogger(__name__)


@dataclass
class LLMClient:
    _client: OpenAI = field(init=False)
    API_KEY: str = OPENAI_API_KEY
    BASE_URL: str = DEEPSEEK_BASE_URL

    def __post_init__(self):
        self._client = self.llm_client()

    def llm_client(self):
        if self.API_KEY is None:
            raise ValueError("API_KEY is not set")

        return OpenAI(api_key=self.API_KEY)

    def llm_text(self, prompt, model="gpt-4o-mini", response_format=None):
        max_tokens = 10000
        temperature = 0.0

        if response_format == "json":
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt}
                        ],
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
        else:
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt}
                        ],
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
        return response.choices[0].message.content

    def llm_image(self, prompt, img_base64, model="gpt-4o-mini", response_format="json"):
        max_tokens = 2048
        temperature = 0.0

        if isinstance(img_base64, str):
            img_base64 = [img_base64]
        content = [{"type": "text", "text": prompt}]
        for img_b64 in img_base64:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_b64}",
                },
            })

        if response_format == "json":
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
        else:
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
        return response.choices[0].message.content


if __name__ == '__main__':
    llm_client = LLMClient()
    convo = """
    User: "Tôi cô đơn kể từ khi chuyển thành phố. Có mẹo nào để gặp gỡ mọi người không?"
    Assistant: "Làm tình nguyện hoặc tham gia câu lạc bộ có thể giúp ích. Bạn muốn gợi ý sự kiện địa phương không?"
    """
    prompt = prompts_tpl.get_template('extract_mood.jinja').render(
        user_answering="Tôi cảm thấy thật là vui vẻ ngày hôm nay")
    # prompt = prompts_tpl.get_template('suggest_keywords.jinja').render(conversation_history=convo)
    print(llm_client.llm_text(prompt, model="gpt-4o-mini"))
