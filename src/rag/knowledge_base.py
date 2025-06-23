import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class KnowledgeBase:
    """
    管理知识库的创建和加载
    """
    def __init__(self, file_path: str, vector_store_path: str = "faiss_index"):
        self.file_path = file_path
        self.vector_store_path = vector_store_path
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = self._load_or_create_vector_store()

    def _create_vector_store(self):
        """从文档创建新的向量存储"""
        loader = TextLoader(self.file_path, encoding='utf-8')
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        print("Creating new vector store...")
        db = FAISS.from_documents(docs, self.embeddings)
        db.save_local(self.vector_store_path)
        print("Vector store created and saved.")
        return db

    def _load_or_create_vector_store(self):
        """加载或创建向量存储"""
        if os.path.exists(self.vector_store_path):
            print("Loading existing vector store...")
            return FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            return self._create_vector_store()

    def as_retriever(self, k: int = 4):
        """将向量存储作为检索器返回"""
        return self.vector_store.as_retriever(search_kwargs={"k": k})

if __name__ == '__main__':
    # 使用示例文件进行测试
    sample_file = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'sample_features.txt')
    kb = KnowledgeBase(file_path=sample_file)
    retriever = kb.as_retriever()
    
    query = "用户登录功能"
    results = retriever.get_relevant_documents(query)
    
    print(f"\nQuery: {query}")
    print("\nResults:")
    for doc in results:
        print(f"- {doc.page_content[:100]}...") 