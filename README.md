# 🚀 Sistema RAG Profissional Notecraft

**Sistema RAG (Retrieval-Augmented Generation) completo com múltiplas estratégias, avaliação científica e interface moderna.**

## ✨ Características Principais

### 🏗️ Arquitetura Completa
- **Frontend Moderno**: Interface web responsiva com design profissional
- **Backend RAG**: Motor Python completo com múltiplas estratégias
- **Avaliação Científica**: Sistema LLM-as-Judge integrado
- **Configuração Flexível**: YAML configurável para todos os parâmetros

### 🔧 Componentes Principais

#### 📄 **Document Processor**
- Suporte a múltiplos formatos: PDF, DOCX, TXT, MD, RTF
- Extração inteligente com preservação de metadados
- Validação automática de arquivos

#### ⚙️ **Chunking Engine**
- **Chunking Recursivo**: Preserva estrutura natural do texto
- **Chunking por Tokens**: Controle preciso baseado em tokens
- **Chunking Semântico**: Divisão baseada em significado
- **Chunking por Páginas**: Detecta marcadores de página
- Métricas detalhadas para cada estratégia

#### 🔗 **Embedding Generator**  
- **Múltiplos Provedores**: OpenAI, Hugging Face, Modelos Locais
- **Cache Inteligente**: Otimização de performance
- **Fallback Automático**: Sistema determinístico para demos
- Análise de similaridade e estatísticas

#### 📊 **Evaluation System**
- **LLM-as-Judge**: Avaliação automática usando LLMs
- **Métricas Quantitativas**: Retrieval, relevância, completude
- **Comparação de Estratégias**: A/B testing integrado
- **Relatórios Detalhados**: Performance e otimização

#### 🤖 **RAG Agent**
- **Chat Interativo**: Interface de linha de comando
- **Múltiplas Estratégias**: Configuráveis em tempo real
- **Histórico Completo**: Rastreamento de conversas
- **Métricas em Tempo Real**: Performance e confiança

## 🚀 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/Froggerr10/professional-rag-system.git
cd professional-rag-system
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente (Opcional)
```bash
# Crie um arquivo .env na raiz do projeto
echo "OPENAI_API_KEY=sua_api_key_aqui" > .env
echo "GEMINI_API_KEY=sua_api_key_aqui" >> .env
```

### 4. Execute o Teste Completo
```bash
python test_complete_system.py
```

## 🎯 Como Usar

### 💻 Interface de Linha de Comando
```bash
# Iniciar chat interativo
python rag_agent.py

# Comandos disponíveis no chat:
# - Digite qualquer pergunta
# - 'metrics' - Ver estatísticas
# - 'ajuda' - Ver comandos
# - 'sair' - Encerrar
```

### 🌐 Interface Web
1. Abra o arquivo `interface-demo.html` no navegador
2. Teste a interface visual com chat simulado
3. Visualize a paleta de cores em `paleta-cores.html`

### ⚙️ Configuração Personalizada
Edite o arquivo `config.yaml` para:
- Ajustar estratégias de chunking
- Configurar provedores de LLM
- Definir métricas de avaliação
- Personalizar interface

## 📁 Estrutura do Projeto

```
professional-rag-system/
├── 🎨 Frontend/
│   ├── interface-demo.html      # Interface principal
│   ├── paleta-cores.html        # Demonstração de cores
│   └── notecraft-colors.css     # Paleta de cores
├── 🔧 Backend/
│   ├── rag_agent.py            # Agente principal
│   ├── document_processor.py    # Processamento de documentos
│   ├── chunking_engine.py      # Motor de chunking
│   ├── embedding_generator.py  # Geração de embeddings
│   └── evaluation_system.py    # Sistema de avaliação
├── ⚙️ Configuração/
│   ├── config.yaml             # Configuração principal
│   ├── requirements.txt        # Dependências Python
│   └── .env.example           # Exemplo de variáveis
├── 🧪 Testes/
│   └── test_complete_system.py # Teste completo
└── 📚 Documentação/
    ├── README.md              # Este arquivo
    └── docs/                  # Documentação adicional
```

## 🔬 Funcionalidades Avançadas

### 📊 Sistema de Avaliação
- **LLM-as-Judge**: Avaliação automática de qualidade
- **Métricas Científicas**: Precisão, relevância, completude
- **Comparação A/B**: Entre diferentes estratégias
- **Relatórios Detalhados**: Performance histórica

### 🎯 Múltiplas Estratégias
```yaml
# Exemplo de configuração em config.yaml
chunking_strategies:
  recursive_500_100:
    type: "recursive"
    chunk_size: 500
    chunk_overlap: 100
    
  semantic_auto:
    type: "semantic"
    max_chunk_size: 1000
    min_chunk_size: 200
```

### 🔗 Provedores Flexíveis
- **OpenAI**: GPT-3.5/4 + text-embedding-ada-002
- **Hugging Face**: Sentence Transformers
- **Local**: Modelos locais sem API
- **Fallback**: Sistema determinístico para demos

## 📈 Métricas e Monitoramento

### 📊 Métricas Disponíveis
- **Response Quality**: Precisão, relevância, clareza
- **Retrieval Quality**: Cobertura, diversidade
- **Performance**: Tempo de resposta, taxa de sucesso
- **Confidence Scores**: Nível de confiança das respostas

### 📋 Relatórios
```bash
# No chat interativo, digite:
metrics  # Ver estatísticas em tempo real

# Ou programe avaliações automáticas
python -c "
from evaluation_system import EvaluationSystem
evaluator = EvaluationSystem()
report = evaluator.generate_performance_report()
print(report)
"
```

## 🛠️ Desenvolvimento e Customização

### 🔧 Adicionar Nova Estratégia de Chunking
```python
# Em chunking_engine.py
def _custom_chunking(self, text: str, config: Dict) -> List[str]:
    # Implementar lógica personalizada
    return chunks
```

### 🤖 Integrar Novo LLM
```python
# Em rag_agent.py
def _setup_custom_llm(self):
    # Configurar novo provedor
    pass
```

### 📊 Adicionar Nova Métrica
```python
# Em evaluation_system.py
def _evaluate_custom_metric(self, question: str, answer: str) -> Dict:
    # Implementar métrica personalizada
    return metrics
```

## 🎨 Interface e Design

### 🌈 Paleta de Cores Notecraft
- **Primary**: `#4bffa5` (Verde vibrante)
- **Secondary**: `#101010` (Preto profundo)
- **Success**: `#22c55e` (Verde sucesso)
- **Warning**: `#f59e0b` (Laranja aviso)
- **Error**: `#ef4444` (Vermelho erro)

### 💡 Características da Interface
- **Design Responsivo**: Mobile-first
- **Modo Escuro/Claro**: Configurável
- **Animações Suaves**: Micro-interações
- **Acessibilidade**: WCAG 2.1 compatível

## 🚨 Solução de Problemas

### ❓ Problemas Comuns

**❌ Erro: "No module named 'openai'"**
```bash
pip install openai
```

**❌ Erro: "API key not found"**
```bash
# Configure no .env ou como variável de ambiente
export OPENAI_API_KEY="sua_key_aqui"
```

**❌ Erro: "tiktoken not found"**
```bash
pip install tiktoken
```

### 🔍 Diagnóstico
```bash
# Execute o teste completo para diagnosticar
python test_complete_system.py

# Verifique logs detalhados
tail -f logs/rag_system.log
```

## 🤝 Contribuição

### 📋 Como Contribuir
1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### 🎯 Áreas de Contribuição
- **Novos Provedores**: Integração com novos LLMs
- **Estratégias de Chunking**: Algoritmos inovadores
- **Métricas de Avaliação**: Novas formas de medir qualidade
- **Interface**: Melhorias de UX/UI
- **Documentação**: Tutoriais e exemplos

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **OpenAI**: Pelos modelos GPT e embeddings
- **Hugging Face**: Pela biblioteca Sentence Transformers
- **LangChain**: Pela inspiração na arquitetura RAG
- **Comunidade Python**: Pelas excelentes bibliotecas

## 📞 Suporte e Contato

- **Issues**: [GitHub Issues](https://github.com/Froggerr10/professional-rag-system/issues)
- **Discussões**: [GitHub Discussions](https://github.com/Froggerr10/professional-rag-system/discussions)
- **Email**: [contato@notecraft.com](mailto:contato@notecraft.com)

---

**⭐ Se este projeto foi útil, dê uma estrela no GitHub!**

## 🚀 Roadmap

### 📅 Versão 1.1 (Em Desenvolvimento)
- [ ] Interface Web Completa com Backend Flask
- [ ] Suporte a mais formatos de documento
- [ ] Integração com bases de dados vetoriais externas
- [ ] API REST completa

### 📅 Versão 1.2 (Planejado)
- [ ] Suporte a documentos com imagens
- [ ] Análise semântica avançada
- [ ] Dashboard de métricas em tempo real
- [ ] Deploy automatizado com Docker

### 📅 Versão 2.0 (Futuro)
- [ ] Sistema multimodal (texto + imagens)
- [ ] Agentes autônomos
- [ ] Integração com ferramentas empresariais
- [ ] Marketplace de estratégias customizadas

## 🔥 Funcionalidades Destacadas

### 💡 **Inovações Técnicas**
1. **Chunking Híbrido**: Combina múltiplas estratégias automaticamente
2. **LLM-as-Judge**: Avaliação científica automática
3. **Cache Inteligente**: Otimização de performance sem perda de qualidade
4. **Fallback Determinístico**: Funciona mesmo sem APIs externas

### 🎯 **Cases de Uso**
- **Empresas**: Knowledge base inteligente
- **Educação**: Assistente de pesquisa acadêmica
- **Jurídico**: Análise de documentos legais
- **Saúde**: Suporte a decisões médicas
- **Pesquisa**: Análise de literatura científica

### 📊 **Diferenciais Competitivos**
- **Avaliação Científica**: Métricas rigorosas de qualidade
- **Múltiplas Estratégias**: Configuráveis por caso de uso
- **Interface Profissional**: Design moderno e intuitivo
- **Código Aberto**: Totalmente customizável

---

*Desenvolvido com ❤️ para democratizar o acesso a sistemas RAG profissionais.*