from sentence_transformers import SentenceTransformer
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from openrouter_client import ChatOpenRouter
from get_response import get_response
import iris
import pandas as pd


class RAGService:
    def __init__(self, ):
        # Initialize IRIS connection
        hostname = 'localhost'
        username="demo"
        password="demo"
        namespace="USER"
        port='1972'
        CONNECTION_STRING = f"{hostname}:{port}/{namespace}"
        self.conn = iris.connect(CONNECTION_STRING, username, password)
        self.cursor = self.conn.cursor()
        self.table_name = f"Hospital.QuestionAnswer"
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.initialize_database()
        self.initialise_docs()
        
    def initialize_database(self):
        """Initialize the IRIS database table."""
        table_definition = """(
            hospital VARCHAR(255), 
            title VARCHAR(255), 
            question VARCHAR(2000), 
            answer VARCHAR(2000), 
            combined_text VARCHAR(2000), 
            vector VECTOR(DOUBLE, 384)
        )"""
        
        try:
            self.cursor.execute(f"DROP TABLE {self.table_name}")
        except:
            pass
            
        self.cursor.execute(f"CREATE TABLE {self.table_name} {table_definition}")
        
    def add_documents(self, documents):
        """Add documents to the IRIS database."""
        # Convert documents to dataframe-like structure
        for doc in documents:
            combined_text = f"{doc.metadata.get('hospital', '')} {doc.metadata.get('title', '')} {doc.page_content}"
            vector = self.embedding_model.encode(combined_text, normalize_embeddings=True).tolist()
            
            sql = f"""
                INSERT INTO {self.table_name} 
                (hospital, title, question, answer, combined_text, vector) 
                VALUES (?, ?, ?, ?, ?, TO_VECTOR(?))
            """
            
            data = (
                doc.metadata.get('hospital', ''),
                doc.metadata.get('title', ''),
                doc.metadata.get('question', ''),
                doc.metadata.get('answer', doc.page_content),
                combined_text,
                str(vector)
            )
            
            self.cursor.execute(sql, data)
        
        self.conn.commit()
        
    def initialise_docs(self):
            # Load documents from Excel file
        dataframe = pd.read_excel('data/questionandanswers.xlsx')
        dataframe['Combined Text'] = dataframe[['Hospital', 'Title', 'Question', 'Answer']].apply(lambda x: ' '.join(x), axis=1)
        documents = [
            Document(
                page_content=row['Combined Text'],
                metadata={
                    'hospital': row['Hospital'],
                    'title': row['Title'],
                    'question': row['Question'],
                    'answer': row['Answer']
                }
            )
            for _, row in dataframe.iterrows()
        ]

        # Add documents to the RAG service
        self.add_documents(documents)
        
    
    def get_relevant_context(self, query: str, k: int = 3) -> list:
        """Retrieve relevant context from IRIS database."""
        query_vector = self.embedding_model.encode(query, normalize_embeddings=True).tolist()
        
        sql = f"""
            SELECT TOP ? hospital, title, question, answer, combined_text
            FROM {self.table_name}
            ORDER BY VECTOR_DOT_PRODUCT(vector, TO_VECTOR(?)) DESC
        """
        
        self.cursor.execute(sql, [k, str(query_vector)])
        results = self.cursor.fetchall()
        return results
    
    def query(self, question: str) -> str:
        """Query the RAG system with a question."""
        # Get relevant context
        context = self.get_relevant_context(question)
        # Format context for the prompt
        formatted_context = "\n\n".join([
            f"Hospital: {row[0]}\nTitle: {row[1]}\nQ: {row[2]}\nA: {row[3]}"
            for row in context
        ])
        # Create prompt
        prompt = f"""Answer the question based on the following context. If you cannot find
        the answer in the context, say "I don't have enough information to answer that question."
        Context:
        {formatted_context}
        Question: {question}
        Answer:"""
        print(prompt)
        # Use the common get_response function
        response = get_response(prompt)
        return response

    def rag_tool_function(self, query: str) -> str:
        """Function to be used as a tool in the unified agent."""
        print(f"RAG Tool Input: {query}")  # Log the input
        try:
            response = self.query(query)
            print(f"RAG Tool Output: {response}")  # Log the output
            return response
        except Exception as e:
            print(f"RAG Tool Error: {str(e)}")  # Log the error
            return f"Error processing RAG query: {str(e)}"

    def __del__(self):
        """Clean up database connections."""
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
# Initialize the RAG service and load documents
        
if __name__ == "__main__":
    # Example usage
    rag_service = RAGService()
    question = "What is the hotline for referral??"
    response = rag_service.query(question)
    print(response)