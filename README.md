## Grupo 1 - CP901TAN1

- Diogo Confortini De Oliveira - 211898  
- Edgar Moiti Inoki Yabiku - 212176  
- Graziano Aparecido Gonçalves Rodrigues - 211971  
- João Henrique Coelho Nascimento - 222228  
- João Pedro Rodrigues Pinto - 211313  
- Larissa Naomy Otsu - 223382  
- Luís Teixeira de Oliveira Alves - 223624  
- Mayara Lima - 211918  
- Vítor Floriano Shinoda - 222293  
- Gustavo Costa Gomes - 151281  

## Tema - Foods&Restaurants
### Empresa
- FoodHunter

### Dataset (Fonte)
- https://www.kaggle.com/code/ritesaluja/food-restaurants/input?select=food_coded.csv

### Project Owner
- Edgar Moiti Inoki Yabiku

## Sprint 1 - Definição do Produto

### 1. Definição da Empresa Fictícia
- **Nome:** FoodHunter (ou Food Hunt)
- **Missão:** Ajudar pessoas a decidir rapidamente onde comer usando IA personalizada e contextual.
- **Visão:** Ser a IA referência em recomendações gastronômicas locais.
- **Diferencial:** Não é apenas um buscador padrão. É uma IA conversacional que entende preferências implícitas e sugere opções sob medida, integrando dados comportamentais.

### 2. Definição do Problema de Negócio
- **Problema:** Escolher onde comer é um processo frequentemente demorado e confuso, agravado pelo excesso de opções e pela falta de personalização nos aplicativos tradicionais de delivery e mapas.
- **Dores do Usuário:**
  - Indecisão constante ("O que vamos comer hoje?").
  - Falta de recomendações realmente relevantes ao contexto (clima, humor, restrições).
  - Filtros engessados (apenas por "tipo de cozinha" ou "distância").
  - Tempo perdido comparando opções em múltiplos apps.
- **Solução Proposta:** Uma plataforma baseada em IA que entende linguagem natural, considera o contexto do usuário (localização, horário, perfil comportamental) e realiza recomendações diretas, interativas e inteligentes.

### 3. Levantamento de Requisitos
**Requisitos Funcionais:**
- [RF01] O sistema deve receber perguntas em linguagem natural via chat.
- [RF02] O sistema deve processar a intenção do usuário utilizando NLP/LLM.
- [RF03] O sistema deve classificar o perfil gastronômico do usuário com base em um modelo de Machine Learning treinado.
- [RF04] O sistema deve buscar restaurantes cruzando a localização do usuário com APIs externas.
- [RF05] O sistema deve manter um histórico/banco de preferências do usuário.

**Requisitos Não Funcionais:**
- [RNF01] Tempo de resposta conversacional rápido (idealmente < 2 segundos).
- [RNF02] Alta disponibilidade da API e do modelo de IA.
- [RNF03] Privacidade e segurança dos dados e histórico de preferências do usuário.
- [RNF04] Escalabilidade para suportar múltiplos usuários simultâneos.

### 4. Definição dos Papéis Scrum
- **Product Owner (PO):** Edgar Moiti Inoki Yabiku
- **Scrum Master (SM):** Luís Teixeira
- **Development Team (Time de Engenharia de Dados e Backend):** Graziano, João Henrique, João Pedro, Larissa.
- **Development Team (Time de Ciência de Dados e IA):** Diogo Confortini De Oliveira, Mayara, Vítor, Gustavo.

---

### 📦 ENTREGÁVEL: Product Backlog Inicial

Abaixo estão as épicas e histórias de usuário (User Stories) priorizadas para a construção do FoodHunter:

**Épico 1: Infraestrutura e Arquitetura de Dados (Sprint 2 & 3)**
- **US01:** Como engenheiro de dados, quero subir um ambiente Docker com MinIO e PostgreSQL para armazenar os dados brutos e relacionais.
- **US02:** Como engenheiro de dados, quero criar uma arquitetura Medallion (Bronze, Silver, Gold) no MinIO para garantir a governança do dataset `food_coded.csv`.

**Épico 2: Motor de Recomendação (Machine Learning) (Sprint 4)**
- **US03:** Como cientista de dados, quero limpar e processar o dataset `food_coded.csv` para utilizá-lo em treinamento.
- **US04:** Como cientista de dados, quero treinar um modelo de classificação que preveja o tipo de "comfort food" do usuário com base em suas características.
- **US05:** Como cientista de dados, quero rastrear os experimentos de treinamento do modelo utilizando o MLflow.

**Épico 3: IA Conversacional e Backend (Sprint Final)**
- **US06:** Como desenvolvedor backend, quero criar uma API em FastAPI que receba a mensagem do usuário e consulte o serviço de localização.
- **US07:** Como engenheiro de IA, quero integrar um LLM (ex: Ollama) que utilize o perfil predito do usuário e o contexto da busca para formular a resposta final.
- **US08:** Como desenvolvedor frontend/UX, quero criar uma interface de chat (via Gradio ou Streamlit) para que o usuário possa interagir com o FoodHunter.
