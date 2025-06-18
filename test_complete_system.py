#!/usr/bin/env python3
"""
Script de Teste Completo do Sistema RAG Notecraft
Executa todos os componentes e demonstra funcionalidades
"""

import os
import sys
import time
import json
from datetime import datetime

def print_banner():
    """Exibe banner do sistema"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🚀 SISTEMA RAG NOTECRAFT - TESTE COMPLETO                ║
║                                                                              ║
║  Sistema RAG Profissional com Múltiplas Estratégias e Avaliação Científica  ║
║                              Versão 1.0.0                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def test_imports():
    """Testa importação de todos os módulos"""
    print("\n🔍 TESTE 1: Verificando Módulos do Sistema")
    print("-" * 60)
    
    modules = [
        ('rag_agent', 'RAGAgent'),
        ('document_processor', 'DocumentProcessor'),
        ('chunking_engine', 'ChunkingEngine'),
        ('embedding_generator', 'EmbeddingGenerator'),
        ('evaluation_system', 'EvaluationSystem')
    ]
    
    results = {}
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            results[module_name] = {'status': '✅', 'class': cls}
            print(f"✅ {module_name}.{class_name} - OK")
        except ImportError as e:
            results[module_name] = {'status': '❌', 'error': str(e)}
            print(f"❌ {module_name} - ERRO: {e}")
        except AttributeError as e:
            results[module_name] = {'status': '⚠️', 'error': str(e)}
            print(f"⚠️ {module_name} - CLASSE NÃO ENCONTRADA: {e}")
    
    return results

def test_document_processing():
    """Testa processamento de documentos"""
    print("\n📄 TESTE 2: Processamento de Documentos")
    print("-" * 60)
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # Criar documento de teste
        test_content = """
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
        
        # Criar arquivo temporário
        temp_file = "temp_test_doc.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Testar extração
        result = processor.extract_text(temp_file)
        
        print(f"✅ Arquivo processado: {result['file_name']}")
        print(f"📊 Caracteres extraídos: {len(result['content'])}")
        print(f"🔧 Formato: {result['format']}")
        
        # Limpar arquivo temporário
        os.remove(temp_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de processamento: {e}")
        return False

def test_chunking_strategies():
    """Testa estratégias de chunking"""
    print("\n🔧 TESTE 3: Estratégias de Chunking")
    print("-" * 60)
    
    try:
        from chunking_engine import ChunkingEngine
        
        # Configuração de teste
        config = {
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
            }
        }
        
        engine = ChunkingEngine(config)
        
        # Texto de teste
        test_text = """
        A inteligência artificial está revolucionando diversos setores da economia.
        
        No setor financeiro, algoritmos de machine learning estão sendo usados para detectar fraudes.
        
        Na medicina, sistemas de IA auxiliam no diagnóstico precoce de doenças.
        
        No varejo, chatbots automatizados melhoram o atendimento ao cliente.
        
        A automação de processos está aumentando a eficiência operacional.
        """
        
        strategies = ['recursive_500_100', 'semantic_auto']
        
        for strategy in strategies:
            chunks = engine.create_chunks(test_text, strategy)
            print(f"✅ {strategy}: {len(chunks)} chunks criados")
            
            if chunks:
                avg_size = sum(len(chunk['text']) for chunk in chunks) / len(chunks)
                print(f"   📊 Tamanho médio: {avg_size:.0f} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de chunking: {e}")
        return False

def test_embeddings():
    """Testa geração de embeddings"""
    print("\n🔗 TESTE 4: Geração de Embeddings")
    print("-" * 60)
    
    try:
        from embedding_generator import EmbeddingGenerator
        
        # Usar fallback para demo (não requer API keys)
        generator = EmbeddingGenerator(provider='fallback')
        
        test_texts = [
            "Como solicitar férias na empresa?",
            "Política de férias estabelece 30 dias anuais",
            "Procedimento para aprovação de férias"
        ]
        
        embeddings = generator.generate_embeddings(test_texts)
        
        print(f"✅ Embeddings gerados: {len(embeddings)}")
        if embeddings:
            print(f"📊 Dimensões: {len(embeddings[0])}")
            
            # Testar similaridade
            if len(embeddings) >= 2:
                similarity = generator.calculate_similarity(embeddings[0], embeddings[1])
                print(f"🔍 Similaridade entre textos 0 e 1: {similarity:.3f}")
        
        # Estatísticas
        stats = generator.get_embedding_stats(embeddings)
        print(f"📈 Estatísticas: {stats.get('count', 0)} embeddings, provedor: {stats.get('provider', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de embeddings: {e}")
        return False

def test_evaluation():
    """Testa sistema de avaliação"""
    print("\n📊 TESTE 5: Sistema de Avaliação")
    print("-" * 60)
    
    try:
        from evaluation_system import EvaluationSystem
        
        evaluator = EvaluationSystem(llm_provider='fallback')
        
        # Dados de teste
        test_question = "Como solicitar férias?"
        test_answer = "Para solicitar férias, você deve fazer a solicitação com 30 dias de antecedência através do sistema interno, com aprovação do gestor direto."
        test_docs = [
            {
                'text': 'Férias devem ser solicitadas com 30 dias de antecedência através do sistema interno',
                'source': 'politica_ferias.txt',
                'similarity_score': 0.85
            },
            {
                'text': 'Aprovação depende do gestor direto',
                'source': 'politica_ferias.txt',
                'similarity_score': 0.78
            }
        ]
        
        # Avaliar resposta
        evaluation = evaluator.evaluate_rag_response(
            test_question, test_answer, test_docs
        )
        
        print(f"✅ Avaliação concluída")
        print(f"📊 Score Geral: {evaluation['overall_score']:.2f}/10")
        
        # Mostrar métricas principais
        metrics = evaluation.get('metrics', {})
        if 'retrieval' in metrics:
            print(f"🔍 Retrieval: {metrics['retrieval'].get('retrieval_score', 0):.1f}/10")
        if 'relevance' in metrics:
            print(f"🎯 Relevância: {metrics['relevance'].get('relevance_score', 0):.1f}/10")
        if 'completeness' in metrics:
            print(f"📝 Completude: {metrics['completeness'].get('completeness_score', 0):.1f}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de avaliação: {e}")
        return False

def test_full_rag_pipeline():
    """Testa pipeline RAG completo"""
    print("\n🚀 TESTE 6: Pipeline RAG Completo")
    print("-" * 60)
    
    try:
        from rag_agent import RAGAgent
        
        # Inicializar agente
        agent = RAGAgent()
        
        if not agent.initialize_system():
            print("❌ Falha na inicialização do sistema")
            return False
        
        print("✅ Sistema RAG inicializado com sucesso")
        
        # Criar documento de exemplo em memória
        sample_docs = [
            {
                'text': 'Todo funcionário tem direito a 30 dias de férias após 12 meses de trabalho. Férias devem ser solicitadas com 30 dias de antecedência.',
                'source': 'politica_ferias.txt',
                'chunk_id': 'doc1_chunk1'
            },
            {
                'text': 'A solicitação deve ser feita através do sistema interno com aprovação do gestor direto. Férias podem ser divididas em até 3 períodos.',
                'source': 'politica_ferias.txt', 
                'chunk_id': 'doc1_chunk2'
            }
        ]
        
        # Adicionar documentos ao agente (simular carregamento)
        agent.documents = sample_docs
        
        # Testar query
        test_question = "Quantos dias de férias tenho direito?"
        
        print(f"❓ Pergunta: {test_question}")
        
        result = agent.query(test_question)
        
        print(f"✅ Resposta gerada em {result['processing_time']:.2f}s")
        print(f"🤖 Resposta: {result['answer']}")
        print(f"📊 Confiança: {result['confidence']:.1%}")
        print(f"📚 Fontes: {', '.join(result['sources'])}")
        
        # Verificar métricas do agente
        metrics = agent.get_metrics()
        print(f"📈 Total de consultas: {metrics['total_queries']}")
        print(f"📈 Taxa de sucesso: {metrics['success_rate']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no pipeline completo: {e}")
        return False

def test_configuration():
    """Testa carregamento de configuração"""
    print("\n⚙️ TESTE 7: Configuração do Sistema")
    print("-" * 60)
    
    try:
        import yaml
        
        # Verificar se config.yaml existe
        if os.path.exists('config.yaml'):
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            print("✅ Arquivo config.yaml carregado")
            
            # Verificar seções principais
            sections = ['chunking_strategies', 'retrieval_configs', 'llm_config', 'embedding_config']
            
            for section in sections:
                if section in config:
                    count = len(config[section]) if isinstance(config[section], dict) else 1
                    print(f"✅ {section}: {count} configurações")
                else:
                    print(f"⚠️ {section}: seção não encontrada")
            
            return True
        else:
            print("⚠️ Arquivo config.yaml não encontrado")
            return False
            
    except ImportError:
        print("⚠️ PyYAML não instalado - usando configurações padrão")
        return True
    except Exception as e:
        print(f"❌ Erro carregando configuração: {e}")
        return False

def generate_test_report(results):
    """Gera relatório dos testes"""
    print("\n" + "="*80)
    print("📋 RELATÓRIO FINAL DOS TESTES")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    print(f"\n✅ Testes Aprovados: {passed_tests}/{total_tests}")
    print(f"📊 Taxa de Sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📝 Detalhes por Teste:")
    test_names = [
        "Importação de Módulos",
        "Processamento de Documentos", 
        "Estratégias de Chunking",
        "Geração de Embeddings",
        "Sistema de Avaliação",
        "Pipeline RAG Completo",
        "Configuração do Sistema"
    ]
    
    for i, (test_name, status) in enumerate(zip(test_names, results.values())):
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {test_name}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 TODOS OS TESTES PASSARAM! Sistema RAG totalmente funcional.")
        print("🚀 Você pode executar o sistema com: python rag_agent.py")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} teste(s) falharam. Verifique as dependências:")
        print("   - pip install -r requirements.txt")
        print("   - Configure as variáveis de ambiente necessárias")
    
    print("\n📚 Próximos Passos:")
    print("   1. Configure suas API keys (OpenAI, etc.)")
    print("   2. Adicione seus documentos na pasta data/raw/")
    print("   3. Execute: python rag_agent.py")
    print("   4. Acesse a interface web: abra interface-demo.html")

def main():
    """Função principal do teste"""
    print_banner()
    
    print("🔍 Iniciando Testes do Sistema RAG Notecraft...")
    print(f"⏰ Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Executar todos os testes
    results = {}
    
    # Teste 1: Importações
    import_results = test_imports()
    results['imports'] = all(r.get('status') == '✅' for r in import_results.values())
    
    # Teste 2: Processamento de documentos
    results['document_processing'] = test_document_processing()
    
    # Teste 3: Chunking
    results['chunking'] = test_chunking_strategies()
    
    # Teste 4: Embeddings
    results['embeddings'] = test_embeddings()
    
    # Teste 5: Avaliação
    results['evaluation'] = test_evaluation()
    
    # Teste 6: Pipeline completo
    results['full_pipeline'] = test_full_rag_pipeline()
    
    # Teste 7: Configuração
    results['configuration'] = test_configuration()
    
    # Gerar relatório
    generate_test_report(results)
    
    return results

if __name__ == "__main__":
    try:
        results = main()
        
        # Sair com código apropriado
        if all(results.values()):
            sys.exit(0)  # Sucesso
        else:
            sys.exit(1)  # Falha
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Testes interrompidos pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro durante execução dos testes: {e}")
        sys.exit(1)
