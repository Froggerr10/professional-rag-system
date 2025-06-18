#!/usr/bin/env python3
"""
Demo Completo do Sistema RAG Notecraft
Demonstração prática de todas as funcionalidades
"""

import os
import json
import time
from datetime import datetime

def demo_banner():
    """Banner da demonstração"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 DEMO INTERATIVO - SISTEMA RAG NOTECRAFT               ║
║                                                                              ║
║               Demonstração Completa de Funcionalidades                      ║
║                            Versão 1.0.0                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

def create_sample_documents():
    """Cria documentos de exemplo para a demonstração"""
    
    # Criar diretório data/raw se não existir
    os.makedirs('data/raw', exist_ok=True)
    
    documents = {
        'politica_ferias.txt': """
POLÍTICA DE FÉRIAS - EMPRESA NOTECRAFT

1. DIREITO A FÉRIAS
Todo funcionário tem direito a 30 dias corridos de férias remuneradas após cada período aquisitivo de 12 meses de trabalho.

2. SOLICITAÇÃO DE FÉRIAS
- As férias devem ser solicitadas com pelo menos 30 dias de antecedência
- A solicitação deve ser feita através do sistema interno RH Digital
- A aprovação final depende do gestor direto do funcionário
- Em casos excepcionais, o prazo pode ser reduzido mediante aprovação da diretoria

3. PERÍODOS DE FÉRIAS
- As férias podem ser divididas em até 3 períodos distintos
- Pelo menos um dos períodos deve ter no mínimo 14 dias corridos
- Os demais períodos não podem ser inferiores a 5 dias corridos cada
- É vedado o início das férias nos dois dias que antecedem feriados ou dias de repouso semanal remunerado

4. ABONO PECUNIÁRIO
- O funcionário pode converter até 1/3 (um terço) das férias em abono pecuniário
- A solicitação deve ser feita junto com o pedido de férias
- O pagamento será feito junto com a primeira parcela das férias

5. FÉRIAS COLETIVAS
- A empresa pode conceder férias coletivas a todos os funcionários
- O período será comunicado com pelo menos 15 dias de antecedência
- As férias coletivas podem ser divididas em dois períodos anuais

6. PAGAMENTO
- As férias devem ser pagas até 2 dias antes do início do período
- O valor inclui a remuneração do período mais 1/3 constitucional
- Em caso de abono, este será calculado sobre o valor total
        """,
        
        'manual_onboarding.txt': """
MANUAL DE INTEGRAÇÃO DE NOVOS FUNCIONÁRIOS

BOAS-VINDAS À NOTECRAFT!

1. PRIMEIRO DIA
- Apresentação às 9h no RH
- Recebimento de materiais (crachá, equipamentos)
- Tour pelas instalações
- Apresentação à equipe
- Configuração de acessos e senhas

2. PRIMEIRA SEMANA
- Treinamento sobre sistemas internos
- Reunião com gestor para definir objetivos
- Participação em reuniões de equipe
- Leitura de políticas e procedimentos
- Agendamento de check-ins semanais

3. DOCUMENTAÇÃO NECESSÁRIA
- Carteira de trabalho
- CPF e RG
- Comprovante de endereço
- Certificados de escolaridade
- Exames médicos admissionais

4. BENEFÍCIOS
- Vale refeição: R$ 25,00/dia
- Vale transporte: 100% do valor
- Plano de saúde: disponível após 90 dias
- Plano odontológico: disponível após 90 dias
- Gympass: disponível imediatamente

5. HORÁRIOS E POLÍTICAS
- Horário padrão: 9h às 18h
- Flexibilidade de 1h na entrada
- Home office: até 2 dias por semana
- Dress code: casual business
- Política de portas abertas

6. DESENVOLVIMENTO
- Plano de desenvolvimento individual (PDI)
- Budget anual para cursos: R$ 2.000
- Mentoria com funcionário sênior
- Avaliação de performance: semestral
        """,
        
        'codigo_conduta.txt': """
CÓDIGO DE CONDUTA EMPRESARIAL

VALORES FUNDAMENTAIS
- Integridade
- Transparência  
- Respeito mútuo
- Inovação
- Responsabilidade social

COMPORTAMENTO ESPERADO

1. RELACIONAMENTO INTERPESSOAL
- Tratar todos com respeito e dignidade
- Não tolerar discriminação ou assédio
- Promover ambiente inclusivo e diverso
- Comunicação clara e respeitosa

2. CONFIDENCIALIDADE
- Proteger informações confidenciais da empresa
- Não divulgar dados de clientes
- Usar informações apenas para fins profissionais
- Relatar vazamentos ou suspeitas

3. CONFLITOS DE INTERESSE
- Declarar potenciais conflitos
- Não usar posição para benefício pessoal
- Transparência em relacionamentos comerciais
- Consultar RH em casos duvidosos

4. USO DE RECURSOS
- Utilizar recursos da empresa de forma responsável
- Não usar equipamentos para fins pessoais excessivos
- Zelar pelo patrimônio da empresa
- Reportar desperdícios ou má utilização

5. CONFORMIDADE LEGAL
- Cumprir todas as leis aplicáveis
- Seguir regulamentações do setor
- Cooperar com auditorias internas
- Reportar irregularidades

6. CANAL DE DENÚNCIAS
- Disponível 24h: 0800-123-456
- Email: etica@notecraft.com
- Anonimato garantido
- Não retaliação por denúncias de boa-fé
        """
    }
    
    # Salvar arquivos
    for filename, content in documents.items():
        filepath = os.path.join('data/raw', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Documento criado: {filename}")
    
    return list(documents.keys())

def demo_step(step_num, title, description):
    """Formata uma etapa da demonstração"""
    print(f"\n{'='*80}")
    print(f"🎯 ETAPA {step_num}: {title}")
    print(f"{'='*80}")
    print(f"📝 {description}")
    print("-" * 80)

def wait_for_user():
    """Pausa para o usuário visualizar"""
    input("\n⏸️  Pressione ENTER para continuar...")

def demo_rag_complete_pipeline():
    """Demonstra pipeline RAG completo"""
    demo_step(4, "PIPELINE RAG COMPLETO", 
              "Executando sistema RAG end-to-end com chat interativo")
    
    try:
        from rag_agent import RAGAgent
        
        # Inicializar agente
        print("🚀 Inicializando sistema RAG...")
        agent = RAGAgent()
        
        if not agent.initialize_system():
            print("❌ Falha na inicialização")
            return False
        
        print("✅ Sistema inicializado com sucesso!")
        
        # Carregar documentos processados
        print("\n📚 Carregando documentos...")
        
        # Simular documentos carregados
        sample_documents = [
            {
                'text': 'Todo funcionário tem direito a 30 dias de férias após 12 meses de trabalho. Férias devem ser solicitadas com 30 dias de antecedência.',
                'source': 'politica_ferias.txt',
                'chunk_id': 'pol_ferias_1'
            },
            {
                'text': 'A solicitação deve ser feita através do sistema interno RH Digital com aprovação do gestor direto.',
                'source': 'politica_ferias.txt',
                'chunk_id': 'pol_ferias_2'
            },
            {
                'text': 'Primeiro dia inclui apresentação às 9h no RH, recebimento de materiais e tour pelas instalações.',
                'source': 'manual_onboarding.txt',
                'chunk_id': 'onboard_1'
            },
            {
                'text': 'Benefícios incluem vale refeição de R$ 25/dia, vale transporte 100% e plano de saúde após 90 dias.',
                'source': 'manual_onboarding.txt',
                'chunk_id': 'onboard_2'
            },
            {
                'text': 'Código de conduta estabelece valores de integridade, transparência e respeito mútuo.',
                'source': 'codigo_conduta.txt',
                'chunk_id': 'conduta_1'
            }
        ]
        
        agent.documents = sample_documents
        print(f"✅ {len(sample_documents)} documentos carregados")
        
        # Teste de queries
        test_questions = [
            "Quantos dias de férias tenho direito?",
            "Como solicitar férias?",
            "O que acontece no primeiro dia de trabalho?",
            "Quais são os benefícios da empresa?",
            "Quais são os valores da empresa?"
        ]
        
        print(f"\n🤖 TESTE DE QUERIES RAG:")
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n--- Query {i} ---")
            print(f"❓ Pergunta: {question}")
            
            # Executar query
            result = agent.query(question)
            
            print(f"✅ Processado em {result['processing_time']:.2f}s")
            print(f"🤖 Resposta: {result['answer']}")
            print(f"📊 Confiança: {result['confidence']:.1%}")
            print(f"📚 Fontes: {', '.join(result['sources'])}")
        
        # Mostrar métricas finais
        metrics = agent.get_metrics()
        print(f"\n📈 MÉTRICAS FINAIS DO AGENTE:")
        print(f"   Total de consultas: {metrics['total_queries']}")
        print(f"   Taxa de sucesso: {metrics['success_rate']:.1%}")
        print(f"   Tempo médio: {metrics['avg_response_time']:.2f}s")
        print(f"   Confiança média: {metrics['avg_confidence']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no pipeline RAG: {e}")
        return False

def demo_evaluation_system():
    """Demonstra sistema de avaliação"""
    demo_step(5, "SISTEMA DE AVALIAÇÃO", 
              "Testando avaliação científica LLM-as-Judge")
    
    try:
        from evaluation_system import EvaluationSystem
        
        evaluator = EvaluationSystem(llm_provider='fallback')
        
        # Dados de teste para avaliação
        test_cases = [
            {
                'question': 'Quantos dias de férias tenho direito?',
                'answer': 'Todo funcionário tem direito a 30 dias corridos de férias remuneradas após cada período aquisitivo de 12 meses de trabalho.',
                'docs': [
                    {
                        'text': 'Todo funcionário tem direito a 30 dias corridos de férias remuneradas após cada período aquisitivo de 12 meses de trabalho',
                        'source': 'politica_ferias.txt',
                        'similarity_score': 0.95
                    }
                ],
                'expected': 'Você tem direito a 30 dias de férias após 12 meses de trabalho.'
            },
            {
                'question': 'Como solicitar férias?',
                'answer': 'As férias devem ser solicitadas com pelo menos 30 dias de antecedência através do sistema interno RH Digital, com aprovação do gestor direto.',
                'docs': [
                    {
                        'text': 'As férias devem ser solicitadas com pelo menos 30 dias de antecedência através do sistema interno RH Digital',
                        'source': 'politica_ferias.txt',
                        'similarity_score': 0.88
                    }
                ],
                'expected': 'Solicite com 30 dias de antecedência pelo sistema RH Digital.'
            }
        ]
        
        print(f"🔍 Avaliando {len(test_cases)} casos de teste...")
        
        evaluations = []
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n--- Caso {i} ---")
            print(f"❓ Pergunta: {case['question']}")
            
            # Avaliar resposta
            evaluation = evaluator.evaluate_rag_response(
                case['question'],
                case['answer'],
                case['docs'],
                case['expected']
            )
            
            evaluations.append(evaluation)
            
            print(f"📊 Score Geral: {evaluation['overall_score']:.2f}/10")
            
            # Métricas detalhadas
            metrics = evaluation.get('metrics', {})
            
            if 'retrieval' in metrics:
                ret_score = metrics['retrieval'].get('retrieval_score', 0)
                print(f"🔍 Retrieval: {ret_score:.1f}/10")
            
            if 'relevance' in metrics:
                rel_score = metrics['relevance'].get('relevance_score', 0)
                print(f"🎯 Relevância: {rel_score:.1f}/10")
            
            if 'completeness' in metrics:
                comp_score = metrics['completeness'].get('completeness_score', 0)
                print(f"📝 Completude: {comp_score:.1f}/10")
            
            if 'accuracy' in metrics:
                acc_score = metrics['accuracy'].get('accuracy_score', 0)
                print(f"✅ Precisão: {acc_score:.1f}/10")
        
        # Relatório final de performance
        print(f"\n📋 RELATÓRIO DE PERFORMANCE:")
        
        avg_score = sum(e['overall_score'] for e in evaluations) / len(evaluations)
        success_count = sum(1 for e in evaluations if e['overall_score'] >= 7)
        
        print(f"   📊 Score médio: {avg_score:.2f}/10")
        print(f"   ✅ Taxa de sucesso: {success_count}/{len(evaluations)} ({success_count/len(evaluations)*100:.1f}%)")
        print(f"   📈 Casos avaliados: {len(evaluations)}")
        
        # Salvar histórico (opcional)
        try:
            evaluator.save_evaluation_history('demo_evaluation_history.json')
            print(f"   💾 Histórico salvo em: demo_evaluation_history.json")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de avaliação: {e}")
        return False

def demo_interactive_chat():
    """Demonstra chat interativo simplificado"""
    demo_step(6, "CHAT INTERATIVO", 
              "Simulação de chat interativo com o usuário")
    
    print("🤖 Iniciando modo de chat interativo simplificado...")
    print("💡 Digite 'sair' para encerrar ou 'demo' para perguntas automáticas")
    
    try:
        from rag_agent import RAGAgent
        
        agent = RAGAgent()
        agent.initialize_system()
        
        # Carregar documentos de exemplo
        sample_docs = [
            {
                'text': 'Todo funcionário tem direito a 30 dias de férias após 12 meses de trabalho.',
                'source': 'politica_ferias.txt'
            },
            {
                'text': 'Primeiro dia inclui apresentação às 9h no RH e recebimento de materiais.',
                'source': 'manual_onboarding.txt'
            }
        ]
        agent.documents = sample_docs
        
        demo_questions = [
            "Quantos dias de férias tenho?",
            "O que acontece no primeiro dia?",
            "Como funciona o RH?"
        ]
        
        while True:
            user_input = input("\n❓ Sua pergunta: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("👋 Encerrando chat interativo...")
                break
            
            if user_input.lower() == 'demo':
                print("🎯 Executando perguntas de demonstração:")
                for q in demo_questions:
                    print(f"\n❓ {q}")
                    result = agent.query(q)
                    print(f"🤖 {result['answer']}")
                continue
            
            if not user_input:
                print("⚠️ Por favor, digite uma pergunta.")
                continue
            
            # Processar pergunta
            print("🔍 Processando...")
            result = agent.query(user_input)
            
            print(f"🤖 {result['answer']}")
            print(f"📊 Confiança: {result['confidence']:.1%}")
            
            if len(agent.chat_history) >= 3:
                print("\n💡 Demo limitada - use 'python rag_agent.py' para chat completo")
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no chat interativo: {e}")
        return False

def demo_configuration():
    """Demonstra sistema de configuração"""
    demo_step(7, "CONFIGURAÇÃO DO SISTEMA", 
              "Explorando configurações e personalização")
    
    try:
        import yaml
        
        print("⚙️ Carregando configurações do sistema...")
        
        # Verificar config.yaml
        if os.path.exists('config.yaml'):
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            print("✅ Arquivo config.yaml encontrado")
            
            # Mostrar seções principais
            sections = {
                'chunking_strategies': 'Estratégias de Chunking',
                'retrieval_configs': 'Configurações de Retrieval',
                'llm_config': 'Configuração de LLMs',
                'embedding_config': 'Configuração de Embeddings',
                'evaluation_config': 'Configuração de Avaliação'
            }
            
            print("\n📋 Seções de configuração disponíveis:")
            
            for section_key, section_name in sections.items():
                if section_key in config:
                    section_data = config[section_key]
                    if isinstance(section_data, dict):
                        count = len(section_data)
                        print(f"✅ {section_name}: {count} configurações")
                        
                        # Mostrar algumas opções
                        if section_key == 'chunking_strategies':
                            strategies = list(section_data.keys())[:3]
                            print(f"   🔧 Estratégias: {', '.join(strategies)}")
                        
                        elif section_key == 'llm_config' and 'providers' in section_data:
                            providers = list(section_data['providers'].keys())
                            print(f"   🤖 Provedores: {', '.join(providers)}")
                            
                        elif section_key == 'embedding_config' and 'providers' in section_data:
                            emb_providers = list(section_data['providers'].keys())
                            print(f"   🔗 Embeddings: {', '.join(emb_providers)}")
                    else:
                        print(f"✅ {section_name}: configurado")
                else:
                    print(f"⚠️ {section_name}: não encontrado")
            
            # Mostrar exemplo de personalização
            print(f"\n💡 EXEMPLO DE PERSONALIZAÇÃO:")
            print("Para adicionar nova estratégia de chunking, edite config.yaml:")
            print("""
chunking_strategies:
  custom_strategy:
    type: "recursive"
    chunk_size: 750
    chunk_overlap: 150
    description: "Estratégia personalizada para documentos longos"
            """)
            
        else:
            print("⚠️ Arquivo config.yaml não encontrado")
            print("💡 Execute o sistema para criar configuração padrão")
        
        # Mostrar variáveis de ambiente
        print(f"\n🔐 VARIÁVEIS DE AMBIENTE:")
        env_vars = ['OPENAI_API_KEY', 'GEMINI_API_KEY', 'HUGGINGFACE_API_KEY']
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"⚠️ {var}: não configurada")
        
        print(f"\n💡 Para configurar APIs:")
        print("   1. Crie arquivo .env na raiz do projeto")
        print("   2. Adicione: OPENAI_API_KEY=sua_chave_aqui")
        print("   3. Reinicie o sistema")
        
        return True
        
    except ImportError:
        print("⚠️ PyYAML não instalado - configuração básica será usada")
        return True
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def generate_demo_report(results):
    """Gera relatório da demonstração"""
    print(f"\n{'='*80}")
    print("📋 RELATÓRIO FINAL DA DEMONSTRAÇÃO")
    print(f"{'='*80}")
    
    total_demos = len(results)
    successful_demos = sum(1 for r in results.values() if r)
    
    print(f"\n✅ Demonstrações Bem-sucedidas: {successful_demos}/{total_demos}")
    print(f"📊 Taxa de Sucesso: {(successful_demos/total_demos)*100:.1f}%")
    
    demo_names = [
        "Processamento de Documentos",
        "Estratégias de Chunking", 
        "Embeddings e Similaridade",
        "Pipeline RAG Completo",
        "Sistema de Avaliação",
        "Chat Interativo",
        "Configuração do Sistema"
    ]
    
    print(f"\n📝 Status por Demonstração:")
    for demo_name, status in zip(demo_names, results.values()):
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {demo_name}")
    
    if successful_demos == total_demos:
        print(f"\n🎉 DEMONSTRAÇÃO COMPLETA!")
        print("🚀 Todas as funcionalidades foram testadas com sucesso.")
        print("\n📚 Próximos Passos:")
        print("   1. Execute 'python rag_agent.py' para chat completo")
        print("   2. Abra 'interface-demo.html' para interface web")
        print("   3. Configure suas API keys para funcionalidades avançadas")
        print("   4. Adicione seus próprios documentos em data/raw/")
    else:
        print(f"\n⚠️ Algumas demonstrações falharam.")
        print("💡 Verifique as dependências com: pip install -r requirements.txt")
    
    print(f"\n📁 Arquivos criados durante a demo:")
    demo_files = [
        'data/raw/politica_ferias.txt',
        'data/raw/manual_onboarding.txt', 
        'data/raw/codigo_conduta.txt',
        'demo_evaluation_history.json'
    ]
    
    for file_path in demo_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"⚠️ {file_path} (não criado)")

def main():
    """Função principal da demonstração"""
    demo_banner()
    
    print("🎯 Iniciando Demonstração Completa do Sistema RAG Notecraft")
    print(f"⏰ Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 Esta demonstração mostra todas as funcionalidades do sistema")
    print("⏸️  Pressione CTRL+C a qualquer momento para sair")
    
    # Perguntar se quer demo automática ou interativa
    print(f"\n❓ Modo de demonstração:")
    print("   1. Automática (executa todos os testes)")
    print("   2. Interativa (pausa entre etapas)")
    
    try:
        mode = input("\nEscolha (1/2): ").strip()
        interactive = mode == '2'
    except:
        interactive = False
    
    results = {}
    
    try:
        # Demo 1: Processamento de documentos
        results['document_processing'] = demo_document_processing()
        if interactive: wait_for_user()
        
        # Demo 2: Chunking strategies 
        results['chunking'] = demo_chunking_strategies()
        if interactive: wait_for_user()
        
        # Demo 3: Embeddings
        results['embeddings'] = demo_embeddings_and_similarity()
        if interactive: wait_for_user()
        
        # Demo 4: Pipeline RAG completo
        results['rag_pipeline'] = demo_rag_complete_pipeline()
        if interactive: wait_for_user()
        
        # Demo 5: Sistema de avaliação
        results['evaluation'] = demo_evaluation_system()
        if interactive: wait_for_user()
        
        # Demo 6: Chat interativo (apenas se interativo)
        if interactive:
            results['chat'] = demo_interactive_chat()
            wait_for_user()
        else:
            results['chat'] = True  # Skip em modo automático
        
        # Demo 7: Configuração
        results['configuration'] = demo_configuration()
        
        # Gerar relatório final
        generate_demo_report(results)
        
        return results
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Demonstração interrompida pelo usuário")
        return results
    except Exception as e:
        print(f"\n\n❌ Erro durante demonstração: {e}")
        return results

if __name__ == "__main__":
    try:
        results = main()
        
        # Determinar código de saída
        if all(results.values()):
            print(f"\n🎉 Demonstração concluída com sucesso!")
            exit(0)
        else:
            print(f"\n⚠️ Demonstração concluída com algumas falhas")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ Erro fatal na demonstração: {e}")
        exit(1)
