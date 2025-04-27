# 📖 To Do List - Simples com Flask

### 📌 Descrição
Um site **To Do List** simples para criação de tarefas com uma interface simples.

**Funcionalidades**:  
- **Usuários:** `Login` `Logout` `Registrar-se` `Editar conta` `Excluir conta`
- **Tarefas** `Vizualizar tarefas` `Criar tarefas` `Editar tarefas` `Excluir Tarefas`
- **Segurança** `Bcrypt`

---

### ⚠ **IMPORTANTE**

**Aviso:** Utilize dados fictícios ao testar o sistema de cadastro para evitar o armazenamento de informações pessoais.

Você pode optar por utilizar a **CONTA TESTE**:
- **Email**: `teste@email.com`
- **Senha**: `teste123`

---

### ☕ Linguagens e Tecnologias
<div>
    <img style="margin-right: 10px" src="https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white">
    <img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white">
</div><br>
<div>
    <img style="margin-right: 10px" src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white">
    <img style="margin-right: 10px" src="https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white">
    <img src="https://img.shields.io/badge/CSS3-1572B6.svg?style=for-the-badge&logo=CSS3&logoColor=white">
</div><br>
<div>
    <img src="https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=MySQL&logoColor=white">
</div><br>
<div>
    <img style="margin-right: 10px" src="https://img.shields.io/badge/Jinja-B41717.svg?style=for-the-badge&logo=Jinja&logoColor=white">
    <img src="https://img.shields.io/badge/.ENV-ECD53F.svg?style=for-the-badge&logo=dotenv&logoColor=black">
</div>

---

### 📦 Instalação
1) Clone o repositório
```bash
git clone https://github.com/Leonardo2106/to-do-list-flask.git
```
2) Crie um ambiente virtual
```bash
cd to-do-list-flask
python -m venv venv
source venv/bin/activate # MacOS/Linux
venv\Scripts\activate # Windows
```
3) Instale as dependências
```bash
pip install -r requirements.txt
```
4) Configure as variáveis de ambiente
- Crie um arquivo `.env` na raiz do projeto
- Preencha o arquivo `.env` com os seguintes dados:

```python
SECRET_KEY=sua_chave_secreta    # Segurança do aplicativo Flask
DB_USER=seu_usuario_mysql       # Nome do usuário do banco de dados MySQL
DB_PASSWORD=sua_senha_mysql     # Senha do usuário MySQL
DB_HOST=localhost               # Endereço do servidor MySQL (localhost se for local)
DB_NAME=nome_do_banco           # Nome do banco de dados
SGBD=mysql+mysqlconnector       # Sistema de banco de dados
```

5) você pode aproveitar o arquivo `database.py` para gerar o banco de dados e as tabelas
```bash
cd to-do-list-flask # se ainda não tiver acessado o projeto
python database.py
```
- **Nota:** O arquivo `database.py` é utilizado para criar o banco de dados e as tabelas automaticamente. Você pode utilizar para gerar as tabelas e o banco após configurar as variáveis de ambiente no arquivo `.env`.

6) Execute o projeto
```bash
cd to-do-list-flask # se ainda não tiver acessado o projeto
python run.py
```
- No seu terminal aparecerá uma mensagem semelhante a essa:
```bash
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000 # <-- Link
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```
- Clique no link `http://127.0.0.1:5000` para acessar o site

---
