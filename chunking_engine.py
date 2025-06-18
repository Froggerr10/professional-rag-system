"""
Chunking Engine - Motor de Segmentação
Implementa múltiplas estratégias de chunking com métricas
"""

import re
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChunkMetrics:
    """Métricas de um chunk"""
    chunk_id: str
    size: int
    token_count: int
    overlap_with_previous: int
    semantic_score: float = 0.0

class ChunkingEngine:
    """
    Motor de chunking com múltiplas estratégias
    Suporta chunking recursivo, por tokens, semântico e por páginas
    """
    
    def __init__(self, strategies_config: Dict = None):
        """Inicializa o motor de chunking"""
        self.strategies_config = strategies_config or self._get_default_config()
        self.tokenizer = None
        self._initialize_tokenizer()
        logger.info("🔧 Chunking Engine inicializado")
    
    def _get_default_config(self) -> Dict:
        """Configuração padrão de estratégias"""
        return {
            'recursive_500_100': {
                'type': 'recursive',
                'chunk_size': 500,
                'chunk_overlap': 100
            },
            'token_400_50': {
                'type': 'token',
                'chunk_size': 400,
                'chunk_overlap': 50
            },
            'semantic_auto': {
                'type': 'semantic',
                'max_chunk_size': 1000,
                'min_chunk_size': 200
            },
            'page_based': {
                'type': 'page',
                'chunk_size': 2000
            }
        }
    
    def _initialize_tokenizer(self):
        """Inicializa tokenizer para contagem de tokens"""
        try:
            import tiktoken
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            logger.warning(f"⚠️ Erro inicializando tokenizer: {e}")
    
    def create_chunks(self, text: str, strategy: str = 'recursive_500_100') -> List[Dict]:
        """
        Cria chunks usando estratégia especificada
        
        Args:
            text: Texto para segmentar
            strategy: Nome da estratégia
            
        Returns:
            List[Dict]: Lista de chunks com metadados
        """
        if strategy not in self.strategies_config:
            logger.warning(f"⚠️ Estratégia {strategy} não encontrada, usando padrão")
            strategy = 'recursive_500_100'
        
        config = self.strategies_config.get(strategy)
        
        logger.info(f"📝 Criando chunks com estratégia: {strategy}")
        
        chunk_type = config['type']
        
        if chunk_type == 'recursive':
            chunks = self._recursive_chunking(text, config)
        elif chunk_type == 'token':
            chunks = self._token_chunking(text, config)
        elif chunk_type == 'semantic':
            chunks = self._semantic_chunking(text, config)
        elif chunk_type == 'page':
            chunks = self._page_chunking(text, config)
        else:
            raise ValueError(f"Tipo de chunking não suportado: {chunk_type}")
        
        # Adicionar métricas
        chunks_with_metrics = self._calculate_metrics(chunks, strategy)
        
        logger.info(f"✅ Criados {len(chunks_with_metrics)} chunks")
        return chunks_with_metrics
    
    def _recursive_chunking(self, text: str, config: Dict) -> List[str]:
        """Chunking recursivo que preserva estrutura natural"""
        chunk_size = config.get('chunk_size', 500)
        chunk_overlap = config.get('chunk_overlap', 100)
        
        # Separadores em ordem de prioridade
        separators = ['\n\n', '\n', '. ', ' ', '']
        
        chunks = []
        current_chunk = ""
        
        # Dividir texto por parágrafos primeiro
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            # Se parágrafo cabe no chunk atual
            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                # Salvar chunk atual se não estiver vazio
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # Se parágrafo é muito grande, dividir recursivamente
                if len(paragraph) > chunk_size:
                    sub_chunks = self._split_text_recursively(
                        paragraph, chunk_size, separators
                    )
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                else:
                    current_chunk = paragraph + '\n\n'
        
        # Adicionar último chunk se não estiver vazio
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Aplicar overlap
        if chunk_overlap > 0:
            chunks = self._apply_overlap(chunks, chunk_overlap)
        
        return chunks
    
    def _split_text_recursively(self, text: str, chunk_size: int, separators: List[str]) -> List[str]:
        """Divide texto recursivamente usando separadores"""
        if len(text) <= chunk_size:
            return [text]
        
        # Tentar cada separador
        for separator in separators:
            if separator in text:
                parts = text.split(separator)
                
                chunks = []
                current_chunk = ""
                
                for part in parts:
                    if len(current_chunk) + len(part) + len(separator) <= chunk_size:
                        current_chunk += part + separator
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.rstrip(separator))
                        
                        if len(part) > chunk_size:
                            # Recursão para partes muito grandes
                            sub_chunks = self._split_text_recursively(
                                part, chunk_size, separators[1:]
                            )
                            chunks.extend(sub_chunks)
                            current_chunk = ""
                        else:
                            current_chunk = part + separator
                
                if current_chunk:
                    chunks.append(current_chunk.rstrip(separator))
                
                return [chunk for chunk in chunks if chunk.strip()]
        
        # Se nenhum separador funcionar, dividir por caracteres
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    def _token_chunking(self, text: str, config: Dict) -> List[str]:
        """Chunking baseado em contagem de tokens"""
        chunk_size = config.get('chunk_size', 400)
        chunk_overlap = config.get('chunk_overlap', 50)
        
        if not self.tokenizer:
            logger.warning("⚠️ Tokenizer não disponível, usando chunking por caracteres")
            return self._character_chunking(text, chunk_size * 4, chunk_overlap * 4)
        
        # Tokenizar texto completo
        tokens = self.tokenizer.encode(text)
        
        chunks = []
        start_idx = 0
        
        while start_idx < len(tokens):
            end_idx = min(start_idx + chunk_size, len(tokens))
            
            # Extrair tokens do chunk
            chunk_tokens = tokens[start_idx:end_idx]
            
            # Decodificar de volta para texto
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Aplicar overlap
            start_idx = end_idx - chunk_overlap
            
            if start_idx >= end_idx:
                break
        
        return chunks
    
    def _semantic_chunking(self, text: str, config: Dict) -> List[str]:
        """Chunking semântico baseado em significado"""
        # Implementação simplificada - dividir por tópicos/seções
        
        # Detectar cabeçalhos e seções
        lines = text.split('\n')
        chunks = []
        current_chunk = ""
        
        for line in lines:
            # Detectar início de nova seção
            if self._is_section_header(line):
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
                
                # Verificar se chunk está muito grande
                max_size = config.get('max_chunk_size', 1000)
                if len(current_chunk) > max_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _page_chunking(self, text: str, config: Dict) -> List[str]:
        """Chunking por páginas (detecta marcadores de página)"""
        # Detectar marcadores de página
        page_markers = [
            r'--- Página \d+ ---',
            r'\[Página \d+\]',
            r'Page \d+',
            r'\f'  # Form feed
        ]
        
        chunks = []
        
        # Tentar detectar páginas
        for marker_pattern in page_markers:
            if re.search(marker_pattern, text):
                pages = re.split(marker_pattern, text)
                chunks = [page.strip() for page in pages if page.strip()]
                break
        
        # Se não encontrar marcadores, dividir por tamanho
        if not chunks:
            chunk_size = config.get('chunk_size', 2000)
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        return chunks
    
    def _character_chunking(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Chunking simples por caracteres"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
            
            if start >= end:
                break
        
        return chunks
    
    def _apply_overlap(self, chunks: List[str], overlap_size: int) -> List[str]:
        """Aplica overlap entre chunks"""
        if len(chunks) <= 1 or overlap_size <= 0:
            return chunks
        
        overlapped_chunks = [chunks[0]]
        
        for i in range(1, len(chunks)):
            prev_chunk = chunks[i-1]
            current_chunk = chunks[i]
            
            # Pegar final do chunk anterior
            overlap_text = prev_chunk[-overlap_size:] if len(prev_chunk) > overlap_size else prev_chunk
            
            # Combinar com início do chunk atual
            combined_chunk = overlap_text + ' ' + current_chunk
            overlapped_chunks.append(combined_chunk)
        
        return overlapped_chunks
    
    def _is_section_header(self, line: str) -> bool:
        """Detecta se linha é cabeçalho de seção"""
        line = line.strip()
        
        # Padrões de cabeçalho
        header_patterns = [
            r'^#{1,6}\s+',  # Markdown headers
            r'^\d+\.\s+[A-Z]',  # Numbered sections
            r'^[A-Z][A-Z\s]+:$',  # All caps headers
            r'^SEÇÃO\s+\d+',  # Section markers
            r'^CAPÍTULO\s+\d+',  # Chapter markers
        ]
        
        for pattern in header_patterns:
            if re.match(pattern, line):
                return True
        
        # Verificar se linha é muito curta e em maiúsculas
        if len(line) < 50 and line.isupper() and len(line) > 5:
            return True
        
        return False
    
    def _calculate_metrics(self, chunks: List[str], strategy: str) -> List[Dict]:
        """Calcula métricas para os chunks"""
        chunks_with_metrics = []
        
        for i, chunk in enumerate(chunks):
            # Contagem de tokens
            token_count = 0
            if self.tokenizer:
                try:
                    token_count = len(self.tokenizer.encode(chunk))
                except:
                    token_count = len(chunk.split())  # Fallback
            else:
                token_count = len(chunk.split())
            
            # Overlap com chunk anterior
            overlap = 0
            if i > 0:
                prev_chunk = chunks[i-1]
                overlap = self._calculate_overlap(prev_chunk, chunk)
            
            chunk_data = {
                'text': chunk,
                'chunk_id': f"{strategy}_{i}",
                'size': len(chunk),
                'token_count': token_count,
                'overlap_with_previous': overlap,
                'strategy': strategy,
                'position': i
            }
            
            chunks_with_metrics.append(chunk_data)
        
        return chunks_with_metrics
    
    def _calculate_overlap(self, chunk1: str, chunk2: str) -> int:
        """Calcula overlap entre dois chunks"""
        # Implementação simples - buscar substring comum no final/início
        min_length = min(len(chunk1), len(chunk2)) // 2
        
        for length in range(min_length, 0, -1):
            if chunk1[-length:] in chunk2[:length*2]:
                return length
        
        return 0
    
    def evaluate_chunking_strategy(self, text: str, strategy: str) -> Dict:
        """Avalia qualidade de uma estratégia de chunking"""
        chunks = self.create_chunks(text, strategy)
        
        if not chunks:
            return {'error': 'Nenhum chunk criado'}
        
        # Métricas de avaliação
        sizes = [chunk['size'] for chunk in chunks]
        token_counts = [chunk['token_count'] for chunk in chunks]
        
        metrics = {
            'strategy': strategy,
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(sizes) / len(sizes),
            'min_chunk_size': min(sizes),
            'max_chunk_size': max(sizes),
            'avg_token_count': sum(token_counts) / len(token_counts),
            'total_tokens': sum(token_counts),
            'size_variance': self._calculate_variance(sizes),
            'coverage': sum(sizes) / len(text),  # Quanto do texto original está coberto
        }
        
        return metrics
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calcula variância dos valores"""
        if len(values) <= 1:
            return 0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance

def main():
    """Função de teste"""
    engine = ChunkingEngine()
    
    # Texto de teste
    sample_text = """
    POLÍTICA DE FÉRIAS - EMPRESA TESTE

    1. DIREITO A FÉRIAS
    Todo funcionário tem direito a 30 dias de férias após 12 meses de trabalho.

    2. SOLICITAÇÃO
    - Férias devem ser solicitadas com 30 dias de antecedência
    - Solicitação deve ser feita através do sistema interno
    - Aprovação depende do gestor direto

    3. PERÍODOS
    - Férias podem ser divididas em até 3 períodos
    - Pelo menos um período deve ter no mínimo 14 dias
    """
    
    # Testar estratégias
    strategies = ['recursive_500_100', 'token_400_50', 'semantic_auto']
    
    for strategy in strategies:
        print(f"\n=== Testando {strategy} ===")
        chunks = engine.create_chunks(sample_text, strategy)
        print(f"Chunks criados: {len(chunks)}")
        
        for i, chunk in enumerate(chunks[:2]):  # Mostrar apenas primeiros 2
            print(f"Chunk {i}: {len(chunk['text'])} chars")

if __name__ == "__main__":
    main()