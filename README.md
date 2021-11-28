# INF1407_1820673_Trabalho2

INF1407 - Programação para Web
Nome: Mariana Porto Barreto
Matrícula: 1820673

## Tema do Trabalho: Catálogo Online de Jogos de Tabuleiro (tabulando.herokuapp.com)

O objetivo do site é que o usuário consiga criar e manter um catálogo online de seus jogos de tabuleiro. Jogar jogos de tabuleiro normalmente não são uma atividade de lazer tão popular quanto séries, livros, filmes e até videogames. De qualquer forma, é um nicho que anda crescendo no Brasil e contém muitos colecionadores, com alguns até chegando a comprar os jogos para revender posteriormente. Como esse nicho não é tão conhecido assim, a internet carece de ferramentas parecidas, principalmente em português. Por isso, como projeto da disciplina, seria uma ideia interessante. A ideia é que o usuário comum consiga inserir/atualizar/deletar/consultar seus jogos de tabuleiro e ver diferentes estatísticas sobre eles, assim como classificá-los de acordo com o número de jogadores máximo e mínimo, idade mínima, etc.

## Requisitos do trabalho e implementação

O site é implementado em Python, utilizando o framework Django e foi colocado em produção por meio do Heroku.

### Banco

O SGDB utilizado foi o SQLite, que é padrão do Django. Como não havia nenhuma manipulação muito intensa do banco, foi mantida essa opção. Pro deploy, o Heroku utiliza o PostgreSQL.
O banco não é muito extenso e precisa apenas de duas tabelas além das criadas automaticamente pelo Django. Como a ideia é que os jogos não sejam inseridos pelos usuários, existe a tabela "Jogo" e a tabela "Catálogo". A tabela catálogo tem uma FK para a tabela de usuários e outra para a tabela de jogos. Ou seja, um usuário pode catalogar 0 ou mais jogos. Para adicionar um registro em seu catálogo de um jogo que ainda não está presente na tabela de jogos, é preciso cadastrar esse jogo antes e aí sim adicionar o registro.
A chave primária de Jogo é "Codigo" e a de catálogo. O "Nome" do jogo e ["ID_Usuário", "Nome_Jogo"] do catálogo poderiam ser PKs de suas tabelas, mas foram utilizadas chaves artificiais por preferência ao utilizar Django. Porém, foi implementado que não podem ser cadastrados dois jogos com o mesmo nome. 
Além disso, essas condições foram reforçadas no banco, colocando o nome do jogo como unique = True na classe Jogo e colocando um "unique_together" entre o id do usuário e o código do jogo na classe Catalogo do models.py. 

### Login e acesso dos usuários

Foram implementadas as páginas de cadastro de um usuário, login e logout, além da parte de "Esqueci minha senha". Na parte de esquecer a senha, o usuário insere o e-mail associado a sua conta e depois recebe um e-mail da conta "tabulandosite@gmail.com". Normalmente está chegando na caixa de spam, mas isso também é alertado para o usuário. Não é feito um controle que informa ao usuário se o e-mail que ele inseriu não está associado a nenhum usuário, mas o próprio Django não manda e-mail para o e-mail errado caso esse seja o caso. Isso também foi testado e de fato o Django não manda o e-mail.

Poderia ter sido utilizado AJAX para essa parte do e-mail, para avisar para o usuário que o e-mail certamente está errado, mas eu considero que isso seria um pouco de vazamento de informação, pois dessa forma o usuário poderia descobrir e-mails que estão cadastrados ou não. Por isso, achei o melhor caminho a forma que foi implementada.

Não foi implementada a parte de alterar a senha (password_change), mas caso o usuário queira trocar sua senha ele pode fazer o processo de password_reset que está disponível na página do perfil do usuário como "Alterar a minha senha". É mais chato porque o usuário tem que fazer o processo de receber o e-mail para trocar, mas não foi um incômodo grande o bastante para deixar de utilizar essa alternativa.

Os usuários não cadastrados tem uma visão diferente do site do que os que estão autenticados. Além disso, os usuários podem obter status "Premium" (grupo de autenticação do Django) que pode permitir que ele acesse a página de "Estatísticas". Para se tornar premium, como informado pela FAQ, ele precisa enviar um e-mail para o site do Tabulando e aí a equipe decide se ele pode se tornar premium ou não. Essa ideia foi pensada na concepção de que o site será pequeno, para o projeto da disciplina. No entanto, essa parte poderia ser melhorada caso houvesse algum desejo de tornar o projeto maior.

Caso um usuário não autenticado tente entrar em qualquer uma das páginas que exige autenticação (isso só pode ser feito digitando a url), ele será direcionado para a página de login. Caso um usuário não-premium tente entrar na página de Estatísticas, aparece uma mensagem explicando que ele não tem permissão e, caso queira, tem que mandar um e-mail para o Tabulando.

### HTML, CSS e Javascript

Para criar as páginas do site, foi utilizado HTML, CSS e Javascript. Para uma visualização um pouco mais "user-friendly" foi utilizado também o Bootstrap 5.

#### CSS

As especificações CSS estão nos arquivos estáticos, em tabulando/css/style.css. O style.css engloba todos os estilos do site. Ele foi bastante utilizado pois o padrão do site tem cores em tons marrons e o padrão do Bootstrap é branco, azul ou preto. Dessa forma, várias classes foram criadas para implementar tal palheta. Além disso, foi utilizado para espaçamento e posicionamento também.

#### Javascript e AJAX

Os códigos em javascript podem ser localizados em "templates/javascript". Eles estão em .html pois cada um deles contém um script. Essa solução foi adotada pois tentei tratá-los como arquivos estáticos mas pessoalmente não gostei da solução. Acho que dentro do código também fica muita informação, e violaria o MVC. Essa solução por mais que tenha uma extensão diferente me pareceu mais razoável.
O primeiro arquivo, chamado "graficos.html", contém todos os gráficos da página de "Estatísticas" e é utilizada a biblioteca Plotly JS para tal. 
O segundo arquivo, chamado "tabela.html", contém as funcionalidades da tabela do CRUD presente em "Catálogo de Jogos". Para isso, é utilizado jQuery e DataTable.
Por fim, o terceiro arquivo, chamado de "verifica_cadastro_jogo.html", verifica algumas informações do formulário para cadastrar um jogo. É nela que contém a parte especifica pelo projeto de utilizar AJAX. Nesse caso, foi escolhido o nome do jogo (diferente do nome de usuário, que foi utilizado durante a disciplina). É verificado, então, se o nome do jogo que está sendo digitado já existe no banco. Se sim, ele avisa com uma mensagem erro. Caso o usuário ainda aperte em enviar, o Django sim faz esse controle.
Além disso, sem utilizar AJAX, também é verificado se o número mínimo de jogadores digitado é menor ou igual ao número máximo. É necessário lembrar que é possível que os dois sejam iguais, pois um número pode ter um número exato de jogadores. Esse controle é feito nos campos tanto de número máximo quanto de número mínimo, pois é possível que a pessoa digite o número máximo antes do número mínimo. 

### CRUD

As 4 operações do CRUD foram implementadas na página de "Catálogo", na qual o usuário pode adicionar um registro, deletar um registro, ver todos o seus registros e atualizar um registro. Para editar e deletar um registro, essas informações ficam nas linhas da tabelas, com um símbolo de lápis (edição) e símbolo de lixeira (supressão). Ambos foram testados e funcionam. Como os atributos da tabela de catálogo são o código do jogo, o id do usuário, a data de inserção e o status, o único que realmente seria legal de editar é o status. Por isso ele é direcionado a uma página que lhe permite alterar essa informação. Para a supressão de qualquer um dos registros, foi inserido um modal perguntando se essa operação deve mesmo ser feita. Isso é sempre bom caso o usuário apenas tenha esbarrado no mouse e clicado sem querer.

A parte de "DataTable" foi inserida justamente aqui, para a parte de consulta do CRUD. Houve uma questão importante sobre essa parte que gerou alterações. Anteriormente, a parte de editar o status era inserida com um modal. Ele ainda está presente no código por motivos didáticos, caso alguém encontre o mesmo problema. Só que quando foi adicionado o datatable, o filtro do datatable também pegava o texto do modal. Então não só todas as opções disponibilizadas no status eram reconhecidas no filtro como também o texto da pergunta ("Deseja alterar o status?"). Isso tornava o filtro ruim principlamente porque você não conseguia filtrar os status direito. Como solução, o ícone de edição agora redireciona para uma página diferente que possibilita alterar o status. Dessa forma, funciona, mas fica mais chato para o usuário. Como a parte de filtros foi julgada como mais importante do que a incoveniência do usuário de ser redirecionado para uma página diferente, tal solução foi implementada. 
Note que essa não foi a mesma decisão tomada para o modal de confirmação de remoção. Isso acontece porque ela não contém muito texto e os textos não estão diretamente vinculados a nenhum campo (como  era o caso do status). Essa questão seria uma inconveniência para os casos em que o usuário quisesse filtrar o nome do jogo com algo como "Confirmar", "Voltar" ou "Você", já que os nomes dos jogos e da editora e do status começam com letra maiúscula necessariamente. Claro que nesse caso se perde a consulta de "nomes de jogos, editoras ou status que começam com C ou V" mas isso é bastante específico e o filtro foi mais utilizado para pesquisar exatamente o nome do jogo ou exatamente o nome da editora. 

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

8. Django - Reset Password
https://dev.to/earthcomfy/django-reset-password-3k0l