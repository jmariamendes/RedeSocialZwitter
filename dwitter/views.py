# dwitter/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Q
from django.db.models import F
from django.db.models.functions import Now
from django.core.mail import send_mail
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .forms import DweetForm, CustomUserCreationForm, ConviteAmigoForm
from .models import Dweet, Profile, Convites, Mensagens, ControleMsgs

from .serializers import UserSerializer

''' View da tela inicial/dashboard:
    - Exibe todas as nsgs. dos usuários seguidos pelo usuário atual
    - Cria botão para exibir todos os usuários
    - Cria botão para exibir o perfil do usuário atual
    - Habilita a tela para publicar uma nova msg do usuário atual
    - Template - dashboard.html'''


def dashboard(request):
    if request.user.is_authenticated:
        if not hasattr(request.user, 'profile'):
            missing_profile = Profile(user=request.user)
            missing_profile.save()
        profile = Profile.objects.get(pk=request.user.profile.id)
        existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0

    form = DweetForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":  # grava a mensagem
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.user = request.user
                dweet.save()
                return redirect("dwitter:dashboard")
        followed_dweets = Dweet.objects.filter(
            user__profile__in=request.user.profile.follows.all()
        ).order_by("-created_at")

        return render(request, "dwitter/dashboard.html", {"form": form,
                                                          "dweets": followed_dweets,
                                                          "existe_convite": request.user.profile.existe_convite,
                                                          "existe_mensagem": request.user.profile.existe_mensagem,
                                                          'existeMsgNaoLida': existeMsgNaoLida
                                                          }
                      )
    else:
        return redirect("dwitter:login")


''' View da tela para a exibição de todos os usuários cadastrados
    - A tela é chamada à partir do botão Todos Usuários, na tela dashboard
    - Template - profile_list.html'''


def profile_list(request):
    if request.user.is_authenticated:
        if not hasattr(request.user, 'profile'):
            missing_profile = Profile(user=request.user)
            missing_profile.save()
        profile = Profile.objects.get(pk=request.user.profile.id)
        existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0

    # profiles = Profile.objects.exclude(user=request.user) # não exibe o usuário atual
    profiles = Profile.objects.all()  # exibe todos os usuários
    return render(request, "dwitter/profile_list.html", {"profiles": profiles,
                                                         "existe_convite": request.user.profile.existe_convite,
                                                         "existe_mensagem": request.user.profile.existe_mensagem,
                                                         'existeMsgNaoLida': existeMsgNaoLida
                                                         }
                  )


''' View da tela para a exibição de um usuário específico
    - Exibe nome e msgs deste usuário
    - Habilita botões de Seguir/Parar deste usuário para o usuário atual
    - Exibe os usuários sendo seguidos por este usuário
    - Exibe os usuários que seguem este usuário
    - Habilita botão para voltar à tela de todos os usuários
    - Template - profile.html'''


def profile(request, pk):
    resp = ""
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0
    profile = Profile.objects.get(pk=pk)
    current_user_profile = request.user.profile
    if request.method == "POST":  # Trata botões Seguir/Parar (follow/unfollow)
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            # current_user_profile.follows.add(profile)
            convite = Convites(user=profile.user, solicitante=request.user, solicitante_id=request.user.profile.id)
            convite.save()
            profile.existe_convite = True
            profile.save()
            resp = f"Solicitação enviada para {request.user.profile.user}"
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    else:
        resp = ""

    convidado = True
    # verifica se o usuário atual já solicitou convite para este usuário
    try:
        convite = Convites.objects.get(user=profile.user_id, solicitante_id=request.user.profile.id)
    except Convites.DoesNotExist:
        convidado = False

    return render(request, "dwitter/profile.html", {"profile": profile,
                                                    "convidado": convidado,
                                                    "resp": resp,
                                                    "existe_convite": request.user.profile.existe_convite,
                                                    "existe_mensagem": request.user.profile.existe_mensagem,
                                                    "existeMsgNaoLida": existeMsgNaoLida
                                                    }
                  )


''' View da tela para a inclusão de novos usuários
    - Utiliza o form da inclusão de usuários do Admin
'''


def register(request):
    if request.method == "GET":
        return render(request, "dwitter/register.html", {"form": CustomUserCreationForm, "msg": ""})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # form.full_clean()
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect("dwitter:dashboard")
        else:
            return render(request, "dwitter/register.html", {"form": form,

                                                             "msg": ""})


''' View da tela para a exibição de todos os convites para o usuário atual
    - Template - convites.html'''


def convites(request):
    if request.user.is_authenticated:
        if not hasattr(request.user, 'profile'):
            missing_profile = Profile(user=request.user)
            missing_profile.save()
        profile = Profile.objects.get(pk=request.user.profile.id)
        existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0

    convites = Convites.objects.filter(user=request.user)  # exibe todos os convites do usuário atual
    return render(request, "dwitter/convites.html", {"convites": convites,
                                                     "existe_convite": request.user.profile.existe_convite,
                                                     "existe_mensagem": request.user.profile.existe_mensagem,
                                                     'existeMsgNaoLida': existeMsgNaoLida
                                                     }
                  )


''' View da tela para tratar o convite espefíco de um usuário para o usuário atual
    - Se o convite for aceito, adiciona o usuário à lista de seguidores do usuário atual
    - Deleta a solicitação de convite
    - Se não existir mais convite para o usuário atual, reseta a flag na tabela Profile
    - Template - trata_convite.html'''


def trata_convite(request, pk):
    profile = Profile.objects.get(pk=pk)
    current_user_profile = request.user.profile
    existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0
    if request.method == "GET":
        return render(request, "dwitter/trata_convite.html", {"profile": profile,
                                                              "existe_convite": request.user.profile.existe_convite,
                                                              "existe_mensagem": request.user.profile.existe_mensagem,
                                                              'existeMsgNaoLida': existeMsgNaoLida
                                                              }
                      )
    elif request.method == "POST":  # Trata botões Aceitar/Ignorar
        data = request.POST
        action = data.get("convite")
        if action == "aceitar":
            profile.follows.add(current_user_profile)
            profile.sequencia_msg += 1
            mensagem = Mensagens(destino_id=profile.user,  # envia mensagem de aceite do convite
                                 origem_nome=request.user,
                                 origem_id=request.user.profile.id,
                                 sequencia=profile.sequencia_msg,
                                 texto=request.user.username + " aceitou seu convite"
                                 )
            # atualiza tabela de controle de mensagens

            try:
                controleMsg = ControleMsgs.objects.get(destino=profile.user,
                                                       origem_id=request.user.profile.id
                                                       )
            except ControleMsgs.DoesNotExist:
                controleMsg = ControleMsgs(destino=profile.user,
                                           origem_nome=request.user,
                                           origem_id=request.user.profile.id
                                           )
            controleMsg.created_at = Now()
            profile.existe_mensagem = True
            controleMsg.save()
            profile.save()
            mensagem.save()

        convite = Convites.objects.get(user=request.user.profile.id, solicitante_id=profile.user_id)
        convite.delete()
        try:
            convite = Convites.objects.get(user=request.user.profile.id)
        except Convites.DoesNotExist:
            request.user.profile.existe_convite = False
        except Convites.MultipleObjectsReturned:
            request.user.profile.existe_convite = True
        request.user.profile.save()
    return redirect("dwitter:dashboard")


def password_change_done(request):
    return render(request, "dwitter/password_change_done.html")


''' View da tela para a exibição de todos os usuários que enviaram mensagens para o usuário atual
    - Template - mensagens.html'''


def mensagens(request):
    if request.user.is_authenticated:
        if not hasattr(request.user, 'profile'):
            missing_profile = Profile(user=request.user)
            missing_profile.save()
        profile = Profile.objects.get(pk=request.user.profile.id)
        existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0

    # exibe todas as mensagens para o usuário atual

    todas_msgs = ControleMsgs.objects.filter(destino_id=request.user).order_by('-created_at')
    return render(request, "dwitter/mensagens.html", {"todas_msgs": todas_msgs,
                                                      "existe_convite": request.user.profile.existe_convite,
                                                      "existe_mensagem": request.user.profile.existe_mensagem,
                                                      'existeMsgNaoLida': existeMsgNaoLida
                                                      }
                  )


def trata_msg_user(request, pk):
    profile = Profile.objects.get(pk=pk)
    current_user_profile = request.user.profile
    existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0

    todas_msgs = ControleMsgs.objects.filter(destino=request.user).order_by('-created_at')

    msg_user = Mensagens.objects.filter(Q(origem_id=pk, destino_id=request.user.profile.id, msg_ativa=True) |
                                        Q(origem_id=request.user.profile.id, destino_id=pk, msg_ativa=True)
                                        ).order_by('-created_at')

    if request.method == "GET":
        controleMsg = ControleMsgs.objects.get(destino=request.user.profile.id,
                                               origem_id=pk
                                               )
        controleMsg.exibida_at = Now()
        controleMsg.save()
        return render(request, "dwitter/trata_msg_user.html", {"msg_user": msg_user,
                                                               "todas_msgs": todas_msgs,
                                                               "profile": profile,
                                                               "existe_convite": request.user.profile.existe_convite,
                                                               "existe_mensagem": request.user.profile.existe_mensagem,
                                                               'existeMsgNaoLida': existeMsgNaoLida
                                                               }
                      )
    elif request.method == "POST":
        data = request.POST
        texto_msg = data.get("texto")
        request.user.profile.sequencia_msg += 1
        mensagem = Mensagens(destino_id=profile.user,
                             origem_nome=request.user,
                             origem_id=request.user.profile.id,
                             sequencia=request.user.profile.sequencia_msg,
                             texto=texto_msg)
        # atualiza tabela de controle de mensagens

        try:

            controleMsg = ControleMsgs.objects.get(destino=profile.user,
                                                   origem_id=request.user.profile.id
                                                   )
        except ControleMsgs.DoesNotExist:
            controleMsg = ControleMsgs(destino=profile.user,
                                       origem_nome=request.user,
                                       origem_id=request.user.profile.id
                                       )
        controleMsg.created_at = Now()
        profile.existe_mensagem = True
        request.user.profile.save()
        controleMsg.save()
        profile.save()
        mensagem.save()

    return render(request, "dwitter/trata_msg_user.html", {"msg_user": msg_user,
                                                           "todas_msgs": todas_msgs,
                                                           "profile": profile,
                                                           "existe_convite": request.user.profile.existe_convite,
                                                           "existe_mensagem": request.user.profile.existe_mensagem,
                                                           'existeMsgNaoLida': existeMsgNaoLida
                                                           }
                  )


def convidar_amigo(request):
    endereco_email = []
    existeMsgNaoLida = ControleMsgs.objects.filter(destino=request.user, created_at__gt=F('exibida_at')).count() > 0
    if request.method == "GET":
        return render(request, "dwitter/convite_amigo.html", {"form": ConviteAmigoForm,
                                                              "existe_convite": request.user.profile.existe_convite,
                                                              "existe_mensagem": request.user.profile.existe_mensagem,
                                                              'existeMsgNaoLida': existeMsgNaoLida
                                                              }
                      )
    elif request.method == "POST":
        form = ConviteAmigoForm(request.POST)
        if form.is_valid():
            nome_amigo = form.cleaned_data['nome']
            endereco_email.append(form.cleaned_data['email'])
            mensagem = f"Olá {nome_amigo}, \n       você foi convidado por {request.user.username}" \
                       f" para participar da rede social Zwitter. \n\n" \
                       f"       Venha fazer parte desta rede onde todos são membros da família.\n\n" \
                       f"       Acesse o link http://zewitter.herokuapp.com/. \n\n" \
                       f"       Esperamos você lá !!!!\n\n" \
                       f"       Abraços\n" \
                       f"Zwitter - a rede social do Zé Maria"

            send_mail("Zwitter - a rede social do Zé Maria",
                      mensagem,
                      "jmariamendes@uol.com.br",
                      endereco_email)
            return redirect("dwitter:convite_enviado")


def convite_enviado(request):
    return render(request, "dwitter/convite_enviado.html")


'''********************************************************************************************************************
   *  
   *                                REST API´s
   *        - get usuários - retorna todos usuários, ou um específico dependendo do parâmetro recebido na URL
   *        - post usuário - inclui um novo uisuário(não implementado)
   *        - get usuario/<pk> - retorna um usuário específico, através do Id
   *        - get usuario/<user> - retorna um usuário específico, através do Username
   *        - put usuario/<pk> - altera os dados de um usuário
   *        - get follows - retorna os seguidores e os seguidos de um usuário
   *
   *
   *********************************************************************************************************************
   '''


@api_view(['GET'])
# pesquisa genérica dos usuários (GET). Se não for passado nenhum parametro, pesquisa todos usuários. Caso contrario,
# pesquisa pelo nome ou pelo id
def get_usuarios(request):
    if request.method == 'GET':
        username = request.query_params.get('username')
        userId = request.query_params.get('id')
        if username is not None:
            try:
                users = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(users)
        elif userId is not None:
            try:
                users = User.objects.get(id=userId)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(users)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
# retorna um usuário específico, através do username (GET)
# altera um usuário (PUT)
def get_update_usuarios(request, user):
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# retorna um usuário específico, através do user-id (GET)
def get_usuario(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['GET'])
# retorna os seguidores e os seguidos de um usuário/profile (GET)
def get_follows (request, user):
    resposta = {}
    seguindo = []
    seguidores = []

    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    profile = Profile.objects.get(id=user.id)

    ''' Nesta API não foi utilizado serializer, porque eu queria retornar os nomes dos usuários
        seguidores e seguidos, e no Profile tem só o Id. Como não consegui achar uma forma de serializar, decidi 
        montar a resposta diretamente, montando o JSON via dicionário'''

    resposta['username'] = user.username
    for usuario in profile.follows.all():
        user = User.objects.get(id=usuario.id)
        seguindo.append(user.username)
    # seguindo = profile.follows
    resposta['seguindo'] = seguindo
    for usuario in profile.followed_by.all():
        user = User.objects.get(id=usuario.id)
        seguidores.append(user.username)
    # seguidores = profile.followed_by
    resposta['seguidores'] = seguidores

    if request.method == 'GET':
        #serializer = ProfileSerializer(resposta)
        return Response(resposta)
