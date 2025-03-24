from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI

from src.config import OPENAI_API_KEY
from src.llms.prompts import system_prompt
from src.llms.prompts.vi_prompt import extract_mood_prompt_template_vi
from src.llms.schema import ExtractTextModel
from src.utils import latency

import pandas as pd
from tqdm import tqdm


class SeoAssistant:
    def __init__(self):
        self.model = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o-mini",
            temperature=0.0
        )
        self._setup_chains()

    def _setup_chains(self):
        self._setup_extract_text_chain()

    def _setup_extract_text_chain(self):
        output_parser = PydanticOutputParser(pydantic_object=ExtractTextModel)
        chat_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(
                template=extract_mood_prompt_template_vi,
                input_variables=["user_answering"],
                partial_variables={"format_instructions": output_parser.get_format_instructions()}
            )
        ])
        self.extract_mood_chain = chat_template | self.model | output_parser

    @latency("Extract mood")
    def extract_mood(self, answering: str = "") -> ExtractTextModel:
        response = self.extract_mood_chain.invoke({"user_answering": answering})
        print(response)
        print(response.reasoning)
        return response

    def process_xlsx_file(self, file_path: str, column_name: str = "user_answering", chunk_size: int = 100):
        # Load the Excel file
        df = pd.read_excel(file_path)

        df = df[df['user_answering'].notna()]

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in Excel file.")

        # Prepare results
        all_results = []

        # Optional: Chunking for huge files
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

        print(f"🔍 Processing {len(chunks)} chunks of size {chunk_size}...")

        for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
            for index, row in chunk.iterrows():
                user_text = str(row[column_name])
                try:
                    result = self.extract_mood_chain.invoke({"user_answering": user_text})
                    all_results.append({
                        "original": user_text,
                        "parsed": result.dict()  # If it's a Pydantic object
                    })
                except Exception as e:
                    all_results.append({
                        "original": user_text,
                        "error": str(e)
                    })
                break
            break

        return all_results


if __name__ == '__main__':
    assistant = SeoAssistant()
    results = assistant.process_xlsx_file(
        file_path="/home/juan/Documents/oneiroposlos/oneir-seo/src/llms/keywords_seo_test.xlsx")
    print(results)
