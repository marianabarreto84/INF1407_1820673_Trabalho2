# INF1407_1820673_Trabalho2

INF1407 - Programação para Web
Nome: Mariana Porto Barreto
Matrícula: 1820673

## Tema do Trabalho: Catálogo Online de Jogos de Tabuleiro (tabulando.herokuapp.com)

O objetivo do site é que o usuário consiga criar e manter um catálogo online de seus jogos de tabuleiro. Jogar jogos de tabuleiro normalmente não são uma atividade de lazer tão popular quanto séries, livros, filmes e até videogames. De qualquer forma, é um nicho que anda crescendo no Brasil e contém muitos colecionadores, com alguns até chegando a comprar os jogos para revender posteriormente. Como esse nicho não é tão conhecido assim, a internet carece de ferramentas parecidas, principalmente em português. Por isso, como projeto da disciplina, seria uma ideia interessante. A ideia é que o usuário comum consiga inserir/atualizar/deletar/consultar seus jogos de tabuleiro e ver diferentes estatísticas sobre eles, assim como classificá-los de acordo com o número de jogadores máximo e mínimo, idade mínima, etc.

## Requisitos do trabalho e implementação

O site é implementado em Python, utilizando o framework Django.

## Banco

O SGDB utilizado foi o SQLite, que é padrão do Django. Como não havia nenhuma manipulação muito intensa do banco, foi mantida essa opção. Pro deploy, o Heroku utiliza o PostgreSQL.
O banco não é muito extenso e precisa apenas de duas tabelas além das criadas automaticamente pelo Django. Como a ideia é que os jogos não sejam inseridos pelos usuários, existe a tabela "Jogo" e a tabela "Catálogo". A tabela catálogo tem uma FK para a tabela de usuários e outra para a tabela de jogos. Ou seja, um usuário pode catalogar 0 ou mais jogos. Para adicionar um registro em seu catálogo de um jogo que ainda não está presente na tabela de jogos, é preciso cadastrar esse jogo antes e aí sim adicionar o registro.
A chave primária de Jogo é "Codigo" e a de catálogo. O "Nome" do jogo e ["ID_Usuário", "Nome_Jogo"] do catálogo poderiam ser PKs de suas tabelas, mas foram utilizadas chaves artificiais por preferência ao utilizar Django. Porém, foi implementado que não podem ser cadastrados dois jogos com o mesmo nome. 


### HTML, CSS e Javascript

Para criar as páginas do site, foi utilizado HTML, CSS e Javascript. Para uma visualização um pouco mais "user-friendly" foi utilizado também o Bootstrap 5.
As especificações CSS estão nos arquivos estáticos, em tabulando/css/style.css. O style.css engloba todos os estilos do site. Ele foi bastante utilizado pois o padrão do site tem cores em tons marrons e o padrão do Bootstrap é branco, azul ou preto. Dessa forma, várias classes foram criadas para implementar tal palheta. Além disso, foi utilizado para espaçamento e posicionamento também.
Já o javascript teve usos específicos, como para implementar o AJAX, os gráficos da página de estatísticas e a tabela para o CRUD. Para a página de estatísticas, o Plotly JS foi escolhido para os gráficos e para a tabela, o DataTable. Para essa última funcionalidade, também foi necessário utilizar o jQuery. 


## Referências
1. Material disponibilizado da disciplina INF1407, ministrada pelo professor Alexandre Meslin.

2. Tutorial Django Parte 8: Autenticação de usuário e permissões
https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django/Authentication

3. How to Send Emails in Django?
https://data-flair.training/blogs/django-send-email/

4. How to perform join operations in django ORM?
https://books.agiliq.com/projects/django-orm-cookbook/en/latest/join.html

5. How to rename items in values() in Django?
https://stackoverflow.com/questions/10598940/how-to-rename-items-in-values-in-django

6. Passing value to Bootstrap modal in Django?
https://stackoverflow.com/questions/13168606/passing-value-to-bootstrap-modal-in-django

7. Page/Paging number color style
https://datatables.net/forums/discussion/51763/page-paging-number-color-styles