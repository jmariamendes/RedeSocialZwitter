# dwitter/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Q
from django.db.models import F
from django.db.models.functions import Now
from .forms import DweetForm, CustomUserCreationForm
from .models import Dweet, Profile, Convites, Mensagens, ControleMsgs

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
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    convidado = True
    # verifica se o usuário atual já solicitou convite para este usuário
    try:
        convite = Convites.objects.get(user=profile.user_id, solicitante_id=request.user.profile.id)
    except Convites.DoesNotExist:
        convidado = False

    '''existeConvitePendente = True
    # verifica se este usuário possui algum convite pendente
    try:
        convite = Convites.objects.get(user=pk)
    except Convites.DoesNotExist:
        existeConvitePendente = False'''
    return render(request, "dwitter/profile.html", {"profile": profile,
                                                    "convidado": convidado,
                                                    "existe_convite": request.user.profile.existe_convite,
                                                    "existe_mensagem": request.user.profile.existe_mensagem,
                                                    'existeMsgNaoLida': existeMsgNaoLida
                                                    }
                  )

    # return render(request, "dwitter/profile.html", {"profile": profile})


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
            mensagem = Mensagens(destino_id=profile.user, # envia mensagem de aceite do convite
                                 origem_nome=request.user,
                                 origem_id=request.user.profile.id,
                                 sequencia=profile.sequencia_msg,
                                 texto=request.user.username + " aceitou seu convite"
                                 )
            # atualiza tabela de controle de mensagens

            try:
                controleMsg = ControleMsgs.objects.get (destino=profile.user,
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
        controleMsg = ControleMsgs.objects.get (destino=request.user.profile.id,
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

            controleMsg = ControleMsgs.objects.get (destino=profile.user,
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
    #return redirect("dwitter:dashboard")