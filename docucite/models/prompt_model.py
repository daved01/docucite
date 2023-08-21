class PromptGenerator:
    def get_prompt(self, question: str, context_str: str) -> str:
        """Returns a prompt from the question given a set of source documents."""

        return f"""Use the following pieces of context, provided in the tripple backticks,
        to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        If you have the information available from the metadata of the context under the field "page",
        cite your answers with page numbers in square brackets after each sentence or paragraph.
        Context: ```{context_str}```
        Question: ```{question}```
        Helpful Answer:"""
