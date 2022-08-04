# RedeSocialZwitter

  Implementação de uma rede social, utilizando Python/Django/DjangoRESTFramework
  
Desenvolvi este projeto com o objetivo de aprimorar meus conhecimentos de Python para aplicações Web, utilizando Django. Ele está baseado no Tutorial Build a Social Network With Django, do site Real Python (https://realpython.com/django-social-network-1/). Aliás, recomendo fortemente este site para o aprendizado de Python. Muito bom !!!

O objetivo inicial do Tutorial era construir uma pequena rede social, que permitisse aos usuários postar pequenas mensagens de texto. Os usuários podem seguir outros usuários, para compartilhar suas mensagems, ou parar de seguir a qualquer momento. 

O Tutorial é bem simples e cumpre perfeitamente o objetivo de ensinar Python e Django. Mas como eu pretendia me aprofundar mais nesta matéria, fiz diversas implementações novas, as quais listo abaixo as principais:

  1. Mudança na parte visual e funcional das telas, principalmente no HTML principal (base.html), fazendo diversas alterações, com aprendizado do Bulma CSS
  2. Utilização de banco de dados Postgre ao invés de SQLite, com o desenvolvimento de novas tabelas, para controle de mensagens e convites.
  3. Implementação da tela de Login, acrescentando também a opção de cadastrar novos usuários.
  4. Implementações na funcionalidade de Seguir um usuário (follow/unfollow), fazendo com que o usuário a ser seguido aprove as solicitações, através de uma sinalização  de Convite no HTML principal (base.html) e implementando rotinas novas para que o usuário faça a aprovação do convite. Após a aprovação, uma mensagem é enviada para o usuário solicitante.
  5. Implementação da funcionalidade de troca de mensagens InBox entre usuários, sinalizando a existencias de mensagens novas no HTML principal (base.html) e implementando rotinas novas para exibir e escrever mensagens.
  6. Implementação da funcionalidade Convide Um Amigo, para que os usuários possam convidar amigos para participarem da Rede. O convite é feito através de envio de e-mail.
  7. Deployment do projeto, utilizando a plataforma Heroku
  8. Liberação para utilização publica.
  
O endereço para a utilização da # RedeSocialZwitter é http://zewitter.herokuapp.com/. Faça uma visita, para verificar as suas funcionalidades. O meu usuario na Zwitter é josemaria, e terei imenso prazer em trocar algumas mensagens com você.




