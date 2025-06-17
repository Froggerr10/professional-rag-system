## **📋 POP - Procedimento Operacional Padrão**
### *Sistema RAG Profissional - David De Cunto*

---

## **🎯 OBJETIVO**
Executar o sistema RAG completo desde a instalação até operação, garantindo funcionamento correto e resultados otimizados.

---

## **📋 PRÉ-REQUISITOS**
- [ ] Python 3.8+ instalado
- [ ] Chave API OpenAI válida
- [ ] Sistema operacional Windows
- [ ] Documentos para processamento (PDF, DOCX, TXT)

---

## **🔧 PROCEDIMENTO DE INSTALAÇÃO**

### **PASSO 1: Preparação do Ambiente**
```bash
# 1.1 - Navegar para o diretório
cd C:\Users\David\rag_system

# 1.2 - Verificar estrutura de pastas
dir
```
**Resultado esperado:** Visualizar todos os arquivos .py e pastas data/

### **PASSO 2: Configuração de API**
```bash
# 2.1 - Copiar template de configuração
copy .env.example .env

# 2.2 - Editar arquivo .env
notepad .env
```
**Ação:** Substituir `sk-seu-api-key-aqui` pela sua chave OpenAI real

### **PASSO 3: Instalação Automática**
```bash
# 3.1 - Executar setup
python setup.py
```
**Resultado esperado:** 
- ✅ Dependências instaladas
- ✅ Ambiente virtual criado
- ✅ Teste de importações OK

---

## **📄 PROCEDIMENTO DE OPERAÇÃO**

### **PASSO 4: Preparar Documentos**
```bash
# 4.1 - Adicionar documentos à pasta raw
copy "seus-documentos.*" data\raw\

# 4.2 - Verificar documentos adicionados
dir data\raw\
```
**Formatos aceitos:** .pdf, .docx, .txt

### **PASSO 5: Execução do Pipeline Completo**
```bash
# 5.1 - Executar masterclass automática
python run_masterclass.py
```

**Monitoramento esperado:**
- 🔄 PASSO 1: Processamento de Documentos
- 🔄 PASSO 2: Estratégias de Chunking  
- 🔄 PASSO 3: Geração de Embeddings
- 🔄 PASSO 4: Teste do Agente RAG
- 🔄 PASSO 5: Avaliação Completa

**Tempo estimado:** 5-15 minutos (dependendo da quantidade de documentos)

### **PASSO 6: Operação Interativa**
```bash
# 6.1 - Iniciar chat com RAG
python rag_agent.py

# 6.2 - Testar perguntas exemplo
```

**Comandos disponíveis no chat:**
- `/collections` - listar coleções
- `/config [nome]` - trocar configuração de retrieval
- `/collection [nome]` - trocar coleção ativa
- `quit` - sair

---

## **📊 VERIFICAÇÃO DE RESULTADOS**

### **CHECKLIST DE FUNCIONAMENTO:**
- [ ] **Pipeline executado sem erros**
- [ ] **Coleções criadas no banco vetorial**
- [ ] **Agente responde perguntas corretamente**
- [ ] **Fontes citadas nas respostas**
- [ ] **Métricas de avaliação geradas**

### **ARQUIVOS DE RESULTADO:**
```
results/
├── embedding_results.json     # Status dos embeddings
├── evaluation_results_*.json  # Métricas de performance
└── chunking_summary.json     # Estatísticas de chunking
```

---

## **🔧 PROCEDIMENTOS DE MANUTENÇÃO**

### **ADICIONAR NOVOS DOCUMENTOS:**
```bash
# 1. Copiar novos documentos
copy "novos-docs.*" data\raw\

# 2. Re-executar pipeline
python run_masterclass.py
```

### **AJUSTAR CONFIGURAÇÕES:**
```bash
# 1. Editar configurações
notepad config.yaml

# 2. Re-executar apenas embeddings
python embedding_generator.py

# 3. Re-executar avaliação
python evaluation_system.py
```

### **TESTAR NOVA ESTRATÉGIA:**
1. Editar `config.yaml` - seção `chunking_strategies`
2. Adicionar nova estratégia
3. Executar `python chunking_engine.py`
4. Executar `python embedding_generator.py`

---

## **🚨 RESOLUÇÃO DE PROBLEMAS**

### **ERRO: "API Key não encontrada"**
**Solução:**
1. Verificar arquivo `.env` existe
2. Confirmar chave OpenAI válida
3. Reiniciar terminal

### **ERRO: "Nenhum documento encontrado"**
**Solução:**
1. Verificar pasta `data/raw/` existe
2. Confirmar documentos nos formatos corretos
3. Verificar permissões de leitura

### **ERRO: "Coleção não encontrada"**
**Solução:**
1. Executar `python embedding_generator.py`
2. Verificar pasta `chroma_db/` criada
3. Re-executar pipeline completo

### **PERFORMANCE BAIXA:**
**Otimizações:**
1. Ajustar `chunk_size` no config.yaml
2. Modificar `score_threshold` para retrieval
3. Testar diferentes estratégias de chunking

---

## **📈 MÉTRICAS DE SUCESSO**

### **INDICADORES DE QUALIDADE:**
- **Score médio:** > 7.0/10
- **Taxa de sucesso:** > 90%
- **Tempo de resposta:** < 3s
- **Confiança média:** > 0.8

### **BENCHMARK DE ESTRATÉGIAS:**
```
Estratégia          Score   Tempo   Uso Recomendado
recursive_500_100   8.7     0.4s    Documentos gerais
token_400_50        8.2     0.3s    Controle preciso
semantic_auto       7.9     0.5s    Textos estruturados
```

---

## **📝 REGISTRO DE OPERAÇÕES**

**Data:** ___/___/_____  
**Operador:** David De Cunto  
**Documentos processados:** ____  
**Resultado final:** [ ] Sucesso [ ] Falha  
**Observações:** ________________________________

---

## **🏆 PROCEDIMENTO VALIDADO**
**Criado por:** David De Cunto  
**Data:** 17/06/2025  
**Versão:** 1.0  
**Status:** ✅ Operacional

---

**🚀 Este POP garante operação consistente e resultados reproduzíveis do seu Sistema RAG Profissional!**