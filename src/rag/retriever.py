from .knowledge_base import KnowledgeBase
import os

class Retriever:
    """
    从知识库中检索相关文档
    """
    def __init__(self, file_path=None):
        if file_path is None:
            # 默认使用 faiss_index 目录
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'faiss_index')
        self.knowledge_base = KnowledgeBase(file_path=file_path)
        self.retriever = self.knowledge_base.as_retriever()

    def query(self, query_text: str) -> str:
        """
        根据查询文本检索相关文档，并格式化为字符串
        """
        docs = self.retriever.invoke(query_text)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

if __name__ == '__main__':
    retriever = Retriever()
    context = retriever.query("如何测试用户登录？")
    print("----- Retrieved Context -----")
    print(context)
    print("-----------------------------") 