from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI

from src.config import OPENAI_API_KEY
from src.llms.prompts import system_prompt, extract_mood_prompt_template, suggest_keywords_prompt_template
from src.llms.schema import ExtractMoodModel, SuggestKeywordsModel
from src.utils import latency


class MoodAssistant:
    def __init__(self):
        self.model = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o-mini",
            temperature=0.0
        )
        self._setup_chains()

    def _setup_chains(self):
        self._setup_extract_mood_chain()
        self._setup_suggest_keywords_chain()

    def _setup_extract_mood_chain(self):
        output_parser = PydanticOutputParser(pydantic_object=ExtractMoodModel)
        chat_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(
                template=extract_mood_prompt_template,
                input_variables=["user_answering"],
                partial_variables={"format_instructions": output_parser.get_format_instructions()}
            )
        ])
        self.extract_mood_chain = chat_template | self.model | output_parser

    def _setup_suggest_keywords_chain(self):
        output_parser = PydanticOutputParser(pydantic_object=SuggestKeywordsModel)
        chat_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(
                template=suggest_keywords_prompt_template,
                input_variables=["conversation"],
                partial_variables={"format_instructions": output_parser.get_format_instructions()}
            )
        ])
        self.suggest_keywords_chain = chat_template | self.model | output_parser

    @latency("Extract mood")
    def extract_mood(self, answering: str = "") -> ExtractMoodModel:
        response = self.extract_mood_chain.invoke({"user_answering": answering})
        print(response)
        print(response.reasoning)
        return response

    @latency("Suggest keywords")
    def suggest_keywords(self, conv: str = "") -> SuggestKeywordsModel:
        response = self.suggest_keywords_chain.invoke({"conversation": conv})
        print(response)
        return response


if __name__ == '__main__':
    assistant = MoodAssistant()
    assistant.extract_mood("Today is a great day!")
    assistant.suggest_keywords(
        """
        User: "Tôi cô đơn kể từ khi chuyển thành phố. Có mẹo nào để gặp gỡ mọi người không?"
        Assistant: "Làm tình nguyện hoặc tham gia câu lạc bộ có thể giúp ích. Bạn muốn gợi ý sự kiện địa phương không?"
        """
    )
