"""
Embedding Generator - Gerador de Embeddings
Cria embeddings para chunks de texto usando diferentes provedores
"""

import os
import logging
import numpy as np
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Gerador de embeddings com suporte a múltiplos provedores
    Suporta OpenAI, Hugging Face, e modelos locais
    """
    
    def __init__(self, provider: str = 'openai', model: str = None):
        """
        Inicializa o gerador de embeddings
        
        Args:
            provider: Provedor de embeddings ('openai', 'huggingface', 'local')
            model: Nome do modelo específico
        """
        self.provider = provider
        self.model = model or self._get_default_model(provider)
        self.client = None
        self.embedding_cache = {}
        
        self._initialize_provider()
        logger.info(f"🔗 Embedding Generator inicializado: {provider}/{self.model}")
    
    def _get_default_model(self, provider: str) -> str:
        """Retorna modelo padrão para cada provedor"""
        defaults = {
            'openai': 'text-embedding-ada-002',
            'huggingface': 'sentence-transformers/all-MiniLM-L6-v2',
            'local': 'all-MiniLM-L6-v2'
        }
        return defaults.get(provider, 'text-embedding-ada-002')
    
    def _initialize_provider(self):
        """Inicializa o provedor de embeddings"""
        try:
            if self.provider == 'openai':
                self._setup_openai()
            elif self.provider == 'huggingface':
                self._setup_huggingface()
            elif self.provider == 'local':
                self._setup_local()
            else:
                raise ValueError(f"Provedor não suportado: {self.provider}")
                
        except Exception as e:
            logger.error(f"❌ Erro inicializando {self.provider}: {e}")
            self._setup_fallback()
    
    def _setup_openai(self):
        """Configura cliente OpenAI"""
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY não encontrada")
            
            openai.api_key = api_key
            self.client = openai
            logger.info("✅ Cliente OpenAI configurado")
            
        except ImportError:
            logger.error("❌ openai package não instalado")
            raise
        except Exception as e:
            logger.error(f"❌ Erro configurando OpenAI: {e}")
            raise
    
    def _setup_huggingface(self):
        """Configura cliente Hugging Face"""
        try:
            from sentence_transformers import SentenceTransformer
            
            self.client = SentenceTransformer(self.model)
            logger.info("✅ Cliente Hugging Face configurado")
            
        except ImportError:
            logger.error("❌ sentence-transformers não instalado")
            raise
        except Exception as e:
            logger.error(f"❌ Erro configurando Hugging Face: {e}")
            raise
    
    def _setup_local(self):
        """Configura modelo local"""
        try:
            from sentence_transformers import SentenceTransformer
            
            # Usar modelo local ou baixar se necessário
            self.client = SentenceTransformer(self.model)
            logger.info("✅ Modelo local configurado")
            
        except ImportError:
            logger.error("❌ sentence-transformers não instalado para modelo local")
            raise
        except Exception as e:
            logger.error(f"❌ Erro configurando modelo local: {e}")
            raise
    
    def _setup_fallback(self):
        """Configura fallback simples (embeddings aleatórios para demo)"""
        logger.warning("⚠️ Usando embeddings de fallback (aleatórios)")
        self.provider = 'fallback'
        self.client = None
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Gera embeddings para lista de textos
        
        Args:
            texts: Lista de textos para embedding
            
        Returns:
            List[List[float]]: Lista de embeddings
        """
        if not texts:
            return []
        
        logger.info(f"🔄 Gerando embeddings para {len(texts)} textos")
        
        embeddings = []
        
        for i, text in enumerate(texts):
            # Verificar cache primeiro
            cache_key = self._get_cache_key(text)
            if cache_key in self.embedding_cache:
                embeddings.append(self.embedding_cache[cache_key])
                continue
            
            # Gerar embedding
            try:
                embedding = self._generate_single_embedding(text)
                embeddings.append(embedding)
                
                # Adicionar ao cache
                self.embedding_cache[cache_key] = embedding
                
                if (i + 1) % 10 == 0:
                    logger.info(f"📊 Processados {i + 1}/{len(texts)} embeddings")
                    
            except Exception as e:
                logger.error(f"❌ Erro gerando embedding para texto {i}: {e}")
                # Usar embedding de fallback
                embeddings.append(self._generate_fallback_embedding(text))
        
        logger.info(f"✅ {len(embeddings)} embeddings gerados")
        return embeddings
    
    def _generate_single_embedding(self, text: str) -> List[float]:
        """Gera embedding para um texto único"""
        if self.provider == 'openai':
            return self._generate_openai_embedding(text)
        elif self.provider in ['huggingface', 'local']:
            return self._generate_transformer_embedding(text)
        else:
            return self._generate_fallback_embedding(text)
    
    def _generate_openai_embedding(self, text: str) -> List[float]:
        """Gera embedding usando OpenAI"""
        try:
            response = self.client.Embedding.create(
                input=text,
                model=self.model
            )
            return response['data'][0]['embedding']
            
        except Exception as e:
            logger.error(f"❌ Erro OpenAI embedding: {e}")
            return self._generate_fallback_embedding(text)
    
    def _generate_transformer_embedding(self, text: str) -> List[float]:
        """Gera embedding usando Sentence Transformers"""
        try:
            embedding = self.client.encode(text)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"❌ Erro transformer embedding: {e}")
            return self._generate_fallback_embedding(text)
    
    def _generate_fallback_embedding(self, text: str) -> List[float]:
        """Gera embedding de fallback (baseado em hash do texto)"""
        # Usar hash do texto para gerar embedding determinístico
        import hashlib
        
        # Criar seed baseado no texto
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        np.random.seed(seed)
        
        # Gerar embedding de dimensão fixa
        embedding_dim = 384  # Dimensão padrão
        embedding = np.random.normal(0, 1, embedding_dim)
        
        # Normalizar
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding.tolist()
    
    def _get_cache_key(self, text: str) -> str:
        """Gera chave de cache para o texto"""
        import hashlib
        return hashlib.md5(f"{self.provider}_{self.model}_{text}".encode()).hexdigest()
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calcula similaridade de cosseno entre dois embeddings
        
        Args:
            embedding1: Primeiro embedding
            embedding2: Segundo embedding
            
        Returns:
            float: Similaridade de cosseno (-1 a 1)
        """
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calcular produto escalar
            dot_product = np.dot(vec1, vec2)
            
            # Calcular normas
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            # Evitar divisão por zero
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Similaridade de cosseno
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"❌ Erro calculando similaridade: {e}")
            return 0.0
    
    def find_most_similar(self, query_embedding: List[float], 
                         candidate_embeddings: List[List[float]], 
                         top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Encontra embeddings mais similares ao query
        
        Args:
            query_embedding: Embedding da query
            candidate_embeddings: Lista de embeddings candidatos
            top_k: Número de resultados mais similares
            
        Returns:
            List[Tuple[int, float]]: Lista de (índice, similaridade)
        """
        similarities = []
        
        for i, candidate in enumerate(candidate_embeddings):
            similarity = self.calculate_similarity(query_embedding, candidate)
            similarities.append((i, similarity))
        
        # Ordenar por similaridade (maior primeiro)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def batch_similarity_search(self, query_text: str, 
                               documents: List[Dict], 
                               top_k: int = 5) -> List[Dict]:
        """
        Busca por similaridade em lote
        
        Args:
            query_text: Texto da query
            documents: Lista de documentos com embeddings
            top_k: Número de resultados
            
        Returns:
            List[Dict]: Documentos mais similares com scores
        """
        # Gerar embedding da query
        query_embedding = self._generate_single_embedding(query_text)
        
        # Extrair embeddings dos documentos
        doc_embeddings = []
        for doc in documents:
            if 'embedding' in doc:
                doc_embeddings.append(doc['embedding'])
            else:
                # Gerar embedding se não existir
                embedding = self._generate_single_embedding(doc.get('text', ''))
                doc['embedding'] = embedding
                doc_embeddings.append(embedding)
        
        # Encontrar mais similares
        similar_indices = self.find_most_similar(
            query_embedding, doc_embeddings, top_k
        )
        
        # Retornar documentos com scores
        results = []
        for idx, score in similar_indices:
            doc = documents[idx].copy()
            doc['similarity_score'] = score
            results.append(doc)
        
        return results
    
    def get_embedding_stats(self, embeddings: List[List[float]]) -> Dict:
        """
        Calcula estatísticas dos embeddings
        
        Args:
            embeddings: Lista de embeddings
            
        Returns:
            Dict: Estatísticas
        """
        if not embeddings:
            return {}
        
        embeddings_array = np.array(embeddings)
        
        # Calcular normas
        norms = [np.linalg.norm(emb) for emb in embeddings]
        
        stats = {
            'count': len(embeddings),
            'dimensions': embeddings_array.shape[1],
            'mean_norm': np.mean(norms),
            'std_norm': np.std(norms),
            'min_norm': np.min(norms),
            'max_norm': np.max(norms),
            'mean_values': np.mean(embeddings_array, axis=0).tolist()[:5],  # Primeiros 5
            'provider': self.provider,
            'model': self.model
        }
        
        return stats

def main():
    """Função de teste"""
    # Testar com diferentes provedores
    providers = ['fallback']  # Usar fallback para demo
    
    sample_texts = [
        "Como solicitar férias na empresa?",
        "Política de férias estabelece 30 dias anuais",
        "Configuração de email corporativo"
    ]
    
    for provider in providers:
        print(f"\n=== Testando {provider} ===")
        
        try:
            generator = EmbeddingGenerator(provider=provider)
            
            # Gerar embeddings
            embeddings = generator.generate_embeddings(sample_texts)
            
            print(f"Embeddings gerados: {len(embeddings)}")
            if embeddings:
                print(f"Dimensões: {len(embeddings[0])}")
            
            # Testar similaridade
            if len(embeddings) >= 2:
                similarity = generator.calculate_similarity(embeddings[0], embeddings[1])
                print(f"Similaridade entre textos 0 e 1: {similarity:.3f}")
            
            # Estatísticas
            stats = generator.get_embedding_stats(embeddings)
            print(f"Estatísticas: {stats}")
            
        except Exception as e:
            print(f"❌ Erro testando {provider}: {e}")

if __name__ == "__main__":
    main()