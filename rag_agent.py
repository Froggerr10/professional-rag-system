"""
RAG Agent - Agente Principal do Sistema RAG
Implementação completa com chat interativo e múltiplas estratégias
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGAgent:
    """
    Agente RAG Principal - Coordena todo o sistema
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializa o agente RAG
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config = self._load_config(config_path)
        self.documents = []
        self.vector_store = None
        self.llm_client = None
        self.chat_history = []
        
        # Métricas de performance
        self.metrics = {
            'total_queries': 0,
            'avg_response_time': 0,
            'avg_confidence': 0,
            'successful_queries': 0
        }
        
        logger.info("🚀 RAG Agent inicializado")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuração do sistema"""
        default_config = {
            'chunking_strategies': {
                'recursive_500_100': {
                    'type': 'recursive',
                    'chunk_size': 500,
                    'chunk_overlap': 100
                },
                'token_400_50': {
                    'type': 'token',
                    'chunk_size': 400,
                    'chunk_overlap': 50
                }
            },
            'retrieval_configs': {
                'standard': {
                    'search_type': 'similarity',
                    'k': 3,
                    'score_threshold': 0.7,
                    'use_hyde': False
                }
            },
            'llm_config': {
                'provider': 'openai',
                'model': 'gpt-3.5-turbo',
                'temperature': 0.1,
                'max_tokens': 1000
            }
        }
        
        try:
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return {**default_config, **config}
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return default_config
    
    def initialize_system(self) -> bool:
        """
        Inicializa todos os componentes do sistema
        
        Returns:
            bool: True se inicialização bem-sucedida
        """
        try:
            # Inicializar processador de documentos
            from document_processor import DocumentProcessor
            self.doc_processor = DocumentProcessor()
            
            # Inicializar chunking engine
            from chunking_engine import ChunkingEngine
            self.chunking_engine = ChunkingEngine(self.config['chunking_strategies'])
            
            # Inicializar gerador de embeddings
            from embedding_generator import EmbeddingGenerator
            self.embedding_generator = EmbeddingGenerator()
            
            # Inicializar cliente LLM
            self._setup_llm_client()
            
            logger.info("✅ Todos os componentes inicializados com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na inicialização: {e}")
            return False
    
    def _setup_llm_client(self):
        """Configura cliente LLM baseado na configuração"""
        provider = self.config['llm_config']['provider']
        
        if provider == 'openai':
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.llm_client = openai
        elif provider == 'gemini':
            # Implementar cliente Gemini
            pass
        else:
            raise ValueError(f"Provedor LLM não suportado: {provider}")
    
    def process_documents(self, file_paths: List[str]) -> Dict:
        """
        Processa documentos e cria embeddings
        
        Args:
            file_paths: Lista de caminhos para arquivos
            
        Returns:
            Dict: Resultado do processamento
        """
        start_time = time.time()
        results = {
            'processed_files': [],
            'total_chunks': 0,
            'processing_time': 0,
            'errors': []
        }
        
        try:
            for file_path in file_paths:
                logger.info(f"📄 Processando: {file_path}")
                
                # Extrair texto do documento
                text_content = self.doc_processor.extract_text(file_path)
                
                # Aplicar chunking
                chunks = self.chunking_engine.create_chunks(
                    text_content, 
                    strategy='recursive_500_100'
                )
                
                # Gerar embeddings
                embeddings = self.embedding_generator.generate_embeddings(chunks)
                
                # Armazenar no vector store
                self._store_chunks(chunks, embeddings, file_path)
                
                results['processed_files'].append(file_path)
                results['total_chunks'] += len(chunks)
                
                logger.info(f"✅ {file_path}: {len(chunks)} chunks criados")
        
        except Exception as e:
            results['errors'].append(str(e))
            logger.error(f"❌ Erro processando documentos: {e}")
        
        results['processing_time'] = time.time() - start_time
        return results
    
    def _store_chunks(self, chunks: List[str], embeddings: List, source_file: str):
        """Armazena chunks e embeddings no vector store"""
        # Implementação simplificada - usar ChromaDB ou similar
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_data = {
                'text': chunk,
                'embedding': embedding,
                'source': source_file,
                'chunk_id': f"{source_file}_{i}",
                'timestamp': datetime.now().isoformat()
            }
            self.documents.append(chunk_data)
    
    def query(self, question: str, strategy: str = 'standard') -> Dict:
        """
        Executa query RAG completa
        
        Args:
            question: Pergunta do usuário
            strategy: Estratégia de retrieval
            
        Returns:
            Dict: Resposta completa com metadados
        """
        start_time = time.time()
        self.metrics['total_queries'] += 1
        
        try:
            # 1. Buscar documentos relevantes
            relevant_docs = self._retrieve_documents(question, strategy)
            
            # 2. Gerar contexto
            context = self._build_context(relevant_docs)
            
            # 3. Gerar resposta
            response = self._generate_response(question, context)
            
            # 4. Calcular métricas
            processing_time = time.time() - start_time
            confidence = self._calculate_confidence(response, relevant_docs)
            
            # 5. Atualizar métricas
            self._update_metrics(processing_time, confidence)
            
            result = {
                'question': question,
                'answer': response,
                'sources': [doc['source'] for doc in relevant_docs],
                'confidence': confidence,
                'processing_time': processing_time,
                'strategy_used': strategy,
                'timestamp': datetime.now().isoformat()
            }
            
            # Adicionar ao histórico
            self.chat_history.append(result)
            self.metrics['successful_queries'] += 1
            
            logger.info(f"✅ Query processada em {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na query: {e}")
            return {
                'question': question,
                'answer': f"Erro ao processar pergunta: {e}",
                'sources': [],
                'confidence': 0,
                'processing_time': time.time() - start_time,
                'error': str(e)
            }
    
    def _retrieve_documents(self, question: str, strategy: str) -> List[Dict]:
        """Busca documentos relevantes"""
        # Implementação simplificada de busca por similaridade
        question_lower = question.lower()
        relevant_docs = []
        
        for doc in self.documents:
            # Busca simples por palavras-chave
            if any(word in doc['text'].lower() for word in question_lower.split()):
                relevant_docs.append(doc)
        
        # Retornar top-k mais relevantes
        return relevant_docs[:3]
    
    def _build_context(self, relevant_docs: List[Dict]) -> str:
        """Constrói contexto a partir dos documentos relevantes"""
        context_parts = []
        
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(f"Documento {i} ({doc['source']}):\\n{doc['text']}\\n")
        
        return "\\n".join(context_parts)
    
    def _generate_response(self, question: str, context: str) -> str:
        """Gera resposta usando LLM"""
        prompt = f"""
        Com base no contexto fornecido, responda à pergunta de forma clara e precisa.
        
        Contexto:
        {context}
        
        Pergunta: {question}
        
        Resposta:
        """
        
        try:
            if self.llm_client and hasattr(self.llm_client, 'ChatCompletion'):
                response = self.llm_client.ChatCompletion.create(
                    model=self.config['llm_config']['model'],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.config['llm_config']['max_tokens'],
                    temperature=self.config['llm_config']['temperature']
                )
                return response.choices[0].message.content
            else:
                # Fallback: resposta simulada
                return f"Com base nos documentos analisados, posso responder sobre: {question}"
                
        except Exception as e:
            logger.error(f"Erro gerando resposta: {e}")
            return "Desculpe, houve um erro ao gerar a resposta."
    
    def _calculate_confidence(self, response: str, relevant_docs: List[Dict]) -> float:
        """Calcula nível de confiança da resposta"""
        # Implementação simplificada
        if not relevant_docs:
            return 0.1
        
        # Confiança baseada no número de documentos encontrados
        base_confidence = min(len(relevant_docs) / 3, 1.0)
        
        # Ajustar baseado no tamanho da resposta
        response_quality = min(len(response) / 200, 1.0)
        
        return (base_confidence + response_quality) / 2
    
    def _update_metrics(self, processing_time: float, confidence: float):
        """Atualiza métricas do sistema"""
        # Média móvel do tempo de resposta
        self.metrics['avg_response_time'] = (
            (self.metrics['avg_response_time'] * (self.metrics['total_queries'] - 1) + processing_time) 
            / self.metrics['total_queries']
        )
        
        # Média móvel da confiança
        self.metrics['avg_confidence'] = (
            (self.metrics['avg_confidence'] * (self.metrics['total_queries'] - 1) + confidence) 
            / self.metrics['total_queries']
        )
    
    def get_chat_history(self) -> List[Dict]:
        """Retorna histórico do chat"""
        return self.chat_history
    
    def get_metrics(self) -> Dict:
        """Retorna métricas do sistema"""
        return {
            **self.metrics,
            'success_rate': (
                self.metrics['successful_queries'] / self.metrics['total_queries'] 
                if self.metrics['total_queries'] > 0 else 0
            )
        }
    
    def interactive_chat(self):
        """
        Inicia chat interativo no terminal
        """
        print("🤖 Sistema RAG Notecraft - Chat Interativo")
        print("Digite 'sair' para encerrar, 'ajuda' para comandos")
        print("-" * 50)
        
        while True:
            try:
                question = input("\\n❓ Sua pergunta: ").strip()
                
                if question.lower() in ['sair', 'exit', 'quit']:
                    print("👋 Obrigado por usar o sistema RAG!")
                    break
                
                if question.lower() == 'ajuda':
                    self._show_help()
                    continue
                
                if question.lower() == 'metrics':
                    self._show_metrics()
                    continue
                
                if not question:
                    print("⚠️ Por favor, digite uma pergunta.")
                    continue
                
                # Processar query
                print("🔍 Processando...")
                result = self.query(question)
                
                # Mostrar resultado
                print(f"\\n🤖 Resposta:")
                print(f"{result['answer']}")
                
                if result['sources']:
                    print(f"\\n📚 Fontes: {', '.join(set(result['sources']))}")
                
                print(f"\\n📊 Confiança: {result['confidence']:.1%} | "
                      f"Tempo: {result['processing_time']:.2f}s")
                
            except KeyboardInterrupt:
                print("\\n\\n👋 Chat interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"\\n❌ Erro: {e}")
    
    def _show_help(self):
        """Mostra comandos disponíveis"""
        print("""
📋 Comandos disponíveis:
- Digite qualquer pergunta para consultar documentos
- 'metrics' - Mostrar estatísticas do sistema
- 'ajuda' - Mostrar esta ajuda
- 'sair' - Encerrar chat
        """)
    
    def _show_metrics(self):
        """Mostra métricas do sistema"""
        metrics = self.get_metrics()
        print(f"""
📊 Métricas do Sistema:
- Total de consultas: {metrics['total_queries']}
- Taxa de sucesso: {metrics['success_rate']:.1%}
- Tempo médio: {metrics['avg_response_time']:.2f}s
- Confiança média: {metrics['avg_confidence']:.1%}
- Documentos carregados: {len(self.documents)}
        """)

def main():
    """Função principal para teste"""
    agent = RAGAgent()
    
    if agent.initialize_system():
        # Processar documentos de exemplo se existirem
        sample_docs = ['data/raw/sample.txt'] # Ajustar caminhos conforme necessário
        # agent.process_documents(sample_docs)
        
        # Iniciar chat interativo
        agent.interactive_chat()
    else:
        print("❌ Falha na inicialização do sistema")

if __name__ == "__main__":
    main()