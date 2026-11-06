# 🍃 MongoDB + Python — Laboratório Prático

## 📁 Estrutura de Arquivos

```text
ultimo projeto/
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
├── conexao.py
└── p01_alunos/
    ├── __init__.py
    └── main.py
```

## 🚀 Como Executar

1. **Instalar dependências** (com o ambiente virtual ativado):
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Testar a conexão com o MongoDB**:
   ```bash
   python -c "from conexao import banco; print('Conectado a:', banco.name)"
   ```

3. **Executar o Projeto 01 (Cadastro de Alunos)**:
   ```bash
   python -m p01_alunos.main
   ```

