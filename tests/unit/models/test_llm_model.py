from langchain.chat_models import ChatOpenAI

from docucite.models.llm_model import LLMModel


class TestLLMModel:
    def test_get_llm_chatopenai(self, mocker):
        mocker.patch("langchain.chat_models.ChatOpenAI")
        llm = LLMModel(llm_name="cool_model", llm_temperature=0)
        llm._get_llm()
        assert isinstance(llm.llm, ChatOpenAI)
