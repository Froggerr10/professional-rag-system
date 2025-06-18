"""
Evaluation System - Sistema de Avaliação Científica
Implementa LLM-as-Judge e métricas quantitativas para avaliar performance do RAG
"""

import json
import logging
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import statistics
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvaluationSystem:
    """
    Sistema de avaliação científica para RAG
    Implementa LLM-as-Judge, métricas de retrieval e análise de performance
    """
    
    def __init__(self, llm_provider: str = 'openai'):
        """
        Inicializa o sistema de avaliação
        
        Args:
            llm_provider: Provedor LLM para avaliação ('openai', 'local')
        """
        self.llm_provider = llm_provider
        self.llm_client = None
        self.evaluation_history = []
        
        self._setup_llm_evaluator()
        logger.info("📊 Sistema de Avaliação inicializado")
    
    def _setup_llm_evaluator(self):
        """Configura LLM para avaliação"""
        try:
            if self.llm_provider == 'openai':
                import openai
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.llm_client = openai
                logger.info("✅ Avaliador OpenAI configurado")
            else:
                logger.warning("⚠️ LLM avaliador não configurado, usando métricas básicas")
        except Exception as e:
            logger.error(f"❌ Erro configurando avaliador: {e}")
    
    def evaluate_rag_response(self, 
                            question: str, 
                            answer: str, 
                            retrieved_docs: List[Dict],
                            expected_answer: str = None) -> Dict:
        """
        Avalia uma resposta RAG completa
        
        Args:
            question: Pergunta original
            answer: Resposta gerada pelo RAG
            retrieved_docs: Documentos recuperados
            expected_answer: Resposta esperada (opcional)
            
        Returns:
            Dict: Métricas de avaliação
        """
        logger.info(f"🔍 Avaliando resposta RAG")
        
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer,
            'metrics': {}
        }
        
        # 1. Avaliação da qualidade da resposta (LLM-as-Judge)
        if self.llm_client:
            response_quality = self._evaluate_response_quality(question, answer, retrieved_docs)
            evaluation['metrics']['response_quality'] = response_quality
        
        # 2. Métricas de retrieval
        retrieval_metrics = self._evaluate_retrieval(question, retrieved_docs)
        evaluation['metrics']['retrieval'] = retrieval_metrics
        
        # 3. Métricas de relevância
        relevance_metrics = self._evaluate_relevance(question, answer, retrieved_docs)
        evaluation['metrics']['relevance'] = relevance_metrics
        
        # 4. Métricas de completude
        completeness_metrics = self._evaluate_completeness(question, answer, retrieved_docs)
        evaluation['metrics']['completeness'] = completeness_metrics
        
        # 5. Comparação com resposta esperada (se disponível)
        if expected_answer:
            accuracy_metrics = self._evaluate_accuracy(answer, expected_answer)
            evaluation['metrics']['accuracy'] = accuracy_metrics
        
        # 6. Calcular score geral
        overall_score = self._calculate_overall_score(evaluation['metrics'])
        evaluation['overall_score'] = overall_score
        
        # Adicionar ao histórico
        self.evaluation_history.append(evaluation)
        
        logger.info(f"✅ Avaliação concluída - Score: {overall_score:.2f}")
        return evaluation
    
    def _evaluate_response_quality(self, question: str, answer: str, retrieved_docs: List[Dict]) -> Dict:
        """Avalia qualidade da resposta usando LLM-as-Judge"""
        try:
            # Criar contexto dos documentos
            context = "\n".join([doc.get('text', '')[:500] for doc in retrieved_docs[:3]])
            
            prompt = f"""
            Avalie a qualidade desta resposta RAG numa escala de 0-10:

            PERGUNTA: {question}

            CONTEXTO DISPONÍVEL:
            {context}

            RESPOSTA GERADA:
            {answer}

            Critérios de avaliação:
            1. Precisão: A resposta está factualmente correta? (0-10)
            2. Relevância: A resposta responde diretamente à pergunta? (0-10) 
            3. Completude: A resposta é completa e abrangente? (0-10)
            4. Clareza: A resposta é clara e bem estruturada? (0-10)
            5. Uso do contexto: A resposta utiliza bem as informações fornecidas? (0-10)

            Responda APENAS em formato JSON:
            {{
                "precisao": <score>,
                "relevancia": <score>,
                "completude": <score>,
                "clareza": <score>,
                "uso_contexto": <score>,
                "justificativa": "<breve explicação>"
            }}
            """
            
            response = self.llm_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parsear resposta JSON
            result = json.loads(response.choices[0].message.content)
            
            # Calcular média
            scores = [result[key] for key in ['precisao', 'relevancia', 'completude', 'clareza', 'uso_contexto']]
            result['score_medio'] = sum(scores) / len(scores)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na avaliação LLM: {e}")
            return self._fallback_quality_evaluation(question, answer)
    
    def _fallback_quality_evaluation(self, question: str, answer: str) -> Dict:
        """Avaliação de qualidade usando métricas simples"""
        # Métricas básicas baseadas em heurísticas
        
        # Relevância baseada em sobreposição de palavras
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        word_overlap = len(question_words.intersection(answer_words)) / len(question_words)
        
        # Completude baseada no tamanho da resposta
        completeness = min(len(answer) / 200, 1.0)  # Resposta ideal ~200 chars
        
        # Clareza baseada na estrutura
        clarity = 0.8 if len(answer.split('.')) > 1 else 0.5  # Múltiplas frases
        
        return {
            'precisao': 7.0,  # Valor padrão
            'relevancia': word_overlap * 10,
            'completude': completeness * 10,
            'clareza': clarity * 10,
            'uso_contexto': 7.0,  # Valor padrão
            'score_medio': (7.0 + word_overlap*10 + completeness*10 + clarity*10 + 7.0) / 5,
            'justificativa': 'Avaliação automática usando métricas heurísticas'
        }
    
    def _evaluate_retrieval(self, question: str, retrieved_docs: List[Dict]) -> Dict:
        """Avalia qualidade do retrieval"""
        if not retrieved_docs:
            return {
                'num_docs': 0,
                'avg_relevance': 0,
                'coverage': 0,
                'diversity': 0
            }
        
        # Número de documentos recuperados
        num_docs = len(retrieved_docs)
        
        # Relevância média (baseada em similarity score se disponível)
        relevance_scores = []
        for doc in retrieved_docs:
            if 'similarity_score' in doc:
                relevance_scores.append(doc['similarity_score'])
            else:
                # Calcular relevância básica por sobreposição de palavras
                doc_text = doc.get('text', '').lower()
                question_words = question.lower().split()
                overlap = sum(1 for word in question_words if word in doc_text)
                relevance_scores.append(overlap / len(question_words))
        
        avg_relevance = statistics.mean(relevance_scores) if relevance_scores else 0
        
        # Cobertura (diversidade de fontes)
        sources = set()
        for doc in retrieved_docs:
            if 'source' in doc:
                sources.add(doc['source'])
        coverage = len(sources)
        
        # Diversidade de conteúdo (baseada em tamanhos diferentes)
        sizes = [len(doc.get('text', '')) for doc in retrieved_docs]
        diversity = statistics.stdev(sizes) / statistics.mean(sizes) if len(sizes) > 1 and statistics.mean(sizes) > 0 else 0
        
        return {
            'num_docs': num_docs,
            'avg_relevance': avg_relevance,
            'coverage': coverage,
            'diversity': diversity,
            'retrieval_score': (avg_relevance * 0.4 + min(coverage/3, 1) * 0.3 + min(diversity, 1) * 0.3) * 10
        }
    
    def _evaluate_relevance(self, question: str, answer: str, retrieved_docs: List[Dict]) -> Dict:
        """Avalia relevância da resposta para a pergunta"""
        # Sobreposição de palavras-chave
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        
        # Remover stop words comuns
        stop_words = {'o', 'a', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'como', 'que', 'é', 'ser'}
        question_words -= stop_words
        answer_words -= stop_words
        
        if not question_words:
            return {'keyword_overlap': 0, 'semantic_relevance': 0.5}
        
        keyword_overlap = len(question_words.intersection(answer_words)) / len(question_words)
        
        # Relevância semântica simples (baseada na presença de conceitos relacionados)
        semantic_score = 0.7  # Placeholder para análise semântica mais avançada
        
        return {
            'keyword_overlap': keyword_overlap,
            'semantic_relevance': semantic_score,
            'relevance_score': (keyword_overlap * 0.6 + semantic_score * 0.4) * 10
        }
    
    def _evaluate_completeness(self, question: str, answer: str, retrieved_docs: List[Dict]) -> Dict:
        """Avalia completude da resposta"""
        # Aspectos da pergunta que podem precisar ser abordados
        question_aspects = self._identify_question_aspects(question)
        
        # Verificar se a resposta aborda os aspectos identificados
        addressed_aspects = 0
        for aspect in question_aspects:
            if any(keyword in answer.lower() for keyword in aspect):
                addressed_aspects += 1
        
        aspect_coverage = addressed_aspects / len(question_aspects) if question_aspects else 0.5
        
        # Completude baseada na extensão da resposta vs. informação disponível
        total_context_length = sum(len(doc.get('text', '')) for doc in retrieved_docs)
        answer_length = len(answer)
        
        length_ratio = min(answer_length / max(total_context_length * 0.1, 100), 1.0)
        
        return {
            'aspect_coverage': aspect_coverage,
            'length_adequacy': length_ratio,
            'completeness_score': (aspect_coverage * 0.7 + length_ratio * 0.3) * 10
        }
    
    def _identify_question_aspects(self, question: str) -> List[List[str]]:
        """Identifica aspectos/tópicos que a pergunta está solicitando"""
        question_lower = question.lower()
        
        aspects = []
        
        # Aspectos temporais
        if any(word in question_lower for word in ['quando', 'prazo', 'tempo', 'duração']):
            aspects.append(['prazo', 'tempo', 'duração', 'dias', 'período'])
        
        # Aspectos de procedimento
        if any(word in question_lower for word in ['como', 'processo', 'procedimento', 'solicitar']):
            aspects.append(['procedimento', 'processo', 'etapas', 'passos'])
        
        # Aspectos de localização
        if any(word in question_lower for word in ['onde', 'local', 'endereço']):
            aspects.append(['local', 'endereço', 'localização'])
        
        # Aspectos de requisitos
        if any(word in question_lower for word in ['requisitos', 'necessário', 'preciso']):
            aspects.append(['requisitos', 'necessário', 'obrigatório'])
        
        # Aspectos financeiros
        if any(word in question_lower for word in ['preço', 'custo', 'valor', 'pagamento']):
            aspects.append(['preço', 'custo', 'valor', 'pagamento', 'dinheiro'])
        
        return aspects if aspects else [['informação', 'dados', 'detalhes']]
    
    def _evaluate_accuracy(self, generated_answer: str, expected_answer: str) -> Dict:
        """Compara resposta gerada com resposta esperada"""
        # Similaridade baseada em palavras
        gen_words = set(generated_answer.lower().split())
        exp_words = set(expected_answer.lower().split())
        
        if not exp_words:
            return {'word_similarity': 0, 'length_similarity': 0}
        
        word_similarity = len(gen_words.intersection(exp_words)) / len(gen_words.union(exp_words))
        
        # Similaridade de tamanho
        length_similarity = 1 - abs(len(generated_answer) - len(expected_answer)) / max(len(generated_answer), len(expected_answer))
        
        return {
            'word_similarity': word_similarity,
            'length_similarity': length_similarity,
            'accuracy_score': (word_similarity * 0.8 + length_similarity * 0.2) * 10
        }
    
    def _calculate_overall_score(self, metrics: Dict) -> float:
        """Calcula score geral baseado em todas as métricas"""
        scores = []
        weights = []
        
        # Response quality (peso maior se disponível)
        if 'response_quality' in metrics and 'score_medio' in metrics['response_quality']:
            scores.append(metrics['response_quality']['score_medio'])
            weights.append(0.4)
        
        # Retrieval quality
        if 'retrieval' in metrics and 'retrieval_score' in metrics['retrieval']:
            scores.append(metrics['retrieval']['retrieval_score'])
            weights.append(0.2)
        
        # Relevance
        if 'relevance' in metrics and 'relevance_score' in metrics['relevance']:
            scores.append(metrics['relevance']['relevance_score'])
            weights.append(0.2)
        
        # Completeness
        if 'completeness' in metrics and 'completeness_score' in metrics['completeness']:
            scores.append(metrics['completeness']['completeness_score'])
            weights.append(0.2)
        
        # Accuracy (se disponível)
        if 'accuracy' in metrics and 'accuracy_score' in metrics['accuracy']:
            scores.append(metrics['accuracy']['accuracy_score'])
            weights.append(0.1)
        
        if not scores:
            return 5.0  # Score neutro se nenhuma métrica disponível
        
        # Normalizar pesos
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # Calcular média ponderada
        weighted_score = sum(score * weight for score, weight in zip(scores, normalized_weights))
        
        return weighted_score
    
    def compare_strategies(self, evaluations: List[Dict]) -> Dict:
        """Compara múltiplas estratégias RAG"""
        if not evaluations:
            return {}
        
        # Agrupar por estratégia
        strategy_results = {}
        for eval_data in evaluations:
            strategy = eval_data.get('strategy', 'unknown')
            if strategy not in strategy_results:
                strategy_results[strategy] = []
            strategy_results[strategy].append(eval_data)
        
        # Calcular estatísticas por estratégia
        comparison = {}
        for strategy, results in strategy_results.items():
            scores = [r['overall_score'] for r in results]
            
            comparison[strategy] = {
                'total_evaluations': len(results),
                'avg_score': statistics.mean(scores),
                'median_score': statistics.median(scores),
                'std_score': statistics.stdev(scores) if len(scores) > 1 else 0,
                'min_score': min(scores),
                'max_score': max(scores),
                'success_rate': len([s for s in scores if s >= 7]) / len(scores)
            }
        
        # Ranking das estratégias
        ranked_strategies = sorted(
            comparison.items(), 
            key=lambda x: x[1]['avg_score'], 
            reverse=True
        )
        
        return {
            'strategies': comparison,
            'ranking': ranked_strategies,
            'best_strategy': ranked_strategies[0][0] if ranked_strategies else None
        }
    
    def generate_performance_report(self) -> Dict:
        """Gera relatório de performance baseado no histórico"""
        if not self.evaluation_history:
            return {'error': 'Nenhuma avaliação no histórico'}
        
        # Estatísticas gerais
        scores = [eval_data['overall_score'] for eval_data in self.evaluation_history]
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_evaluations': len(self.evaluation_history),
            'overall_stats': {
                'avg_score': statistics.mean(scores),
                'median_score': statistics.median(scores),
                'std_score': statistics.stdev(scores) if len(scores) > 1 else 0,
                'min_score': min(scores),
                'max_score': max(scores),
                'success_rate': len([s for s in scores if s >= 7]) / len(scores)
            }
        }
        
        # Análise temporal (últimas 24h vs. histórico)
        recent_evals = [
            eval_data for eval_data in self.evaluation_history 
            if datetime.fromisoformat(eval_data['timestamp']) > 
               datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ]
        
        if recent_evals:
            recent_scores = [eval_data['overall_score'] for eval_data in recent_evals]
            report['recent_performance'] = {
                'evaluations_today': len(recent_evals),
                'avg_score_today': statistics.mean(recent_scores),
                'improvement': statistics.mean(recent_scores) - statistics.mean(scores)
            }
        
        # Análise por categoria de métrica
        metric_analysis = {}
        for metric_type in ['response_quality', 'retrieval', 'relevance', 'completeness']:
            values = []
            for eval_data in self.evaluation_history:
                if metric_type in eval_data.get('metrics', {}):
                    metric_data = eval_data['metrics'][metric_type]
                    if metric_type == 'response_quality' and 'score_medio' in metric_data:
                        values.append(metric_data['score_medio'])
                    elif f'{metric_type}_score' in metric_data:
                        values.append(metric_data[f'{metric_type}_score'])
            
            if values:
                metric_analysis[metric_type] = {
                    'avg': statistics.mean(values),
                    'std': statistics.stdev(values) if len(values) > 1 else 0
                }
        
        report['metric_analysis'] = metric_analysis
        
        return report
    
    def save_evaluation_history(self, file_path: str):
        """Salva histórico de avaliações"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.evaluation_history, f, indent=2)
            logger.info(f"💾 Histórico salvo em {file_path}")
        except Exception as e:
            logger.error(f"❌ Erro salvando histórico: {e}")
    
    def load_evaluation_history(self, file_path: str):
        """Carrega histórico de avaliações"""
        try:
            with open(file_path, 'r') as f:
                self.evaluation_history = json.load(f)
            logger.info(f"📂 Histórico carregado de {file_path}")
        except Exception as e:
            logger.error(f"❌ Erro carregando histórico: {e}")

def main():
    """Função de teste"""
    evaluator = EvaluationSystem()
    
    # Teste de avaliação
    test_question = "Como solicitar férias?"
    test_answer = "Para solicitar férias, você deve fazer a solicitação com 30 dias de antecedência através do sistema interno, com aprovação do gestor direto."
    test_docs = [
        {
            'text': 'Férias devem ser solicitadas com 30 dias de antecedência através do sistema interno',
            'source': 'politica_ferias.txt',
            'similarity_score': 0.85
        }
    ]
    
    # Avaliar resposta
    evaluation = evaluator.evaluate_rag_response(
        test_question, test_answer, test_docs
    )
    
    print("=== Resultado da Avaliação ===")
    print(f"Score Geral: {evaluation['overall_score']:.2f}")
    print(f"Métricas: {json.dumps(evaluation['metrics'], indent=2)}")

if __name__ == "__main__":
    main()