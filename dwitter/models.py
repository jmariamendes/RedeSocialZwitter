# dwitter/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

''' O sistema utiliza o esquema de usuários do Django,  principalmente a tabela User
    A tabela Profile é uma extensão de User, um-para-um, onde existe o relacionamento com os seguidores,
    na tabela follows'''


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    existe_convite = models.BooleanField(default=False)
    existe_mensagem = models.BooleanField(default=False)
    sequencia_msg = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #user_profile.follows.set([instance.profile.id])
        user_profile.follows.add(user_profile)
        user_profile.save()


''' Tabela dos Zweets postadas pelos usuários'''


class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )

# Create a Profile for each new user. ---> trocado pelo decorator @receiver
# post_save.connect(create_profile, sender=User)


''' Tabela para controle de convites para seguir um usuário '''


class Convites(models.Model):
    user = models.ForeignKey(
        User, related_name="convite", on_delete=models.CASCADE
    )
    solicitante_id = models.IntegerField()
    solicitante = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.solicitante}"
        )


''' Tabela para troca de mensagens inBox entre os uusários '''


class Mensagens(models.Model):
    destino_id = models.ForeignKey(
        User, related_name="mensagem", on_delete=models.CASCADE
    )
    origem_id = models.IntegerField()
    origem_nome = models.CharField(max_length=150)
    texto = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    sequencia = models.IntegerField(default=0)
    msg_ativa = models.BooleanField(default=True)
    status_msg = models.IntegerField(default=0) # lida/respondida/...
    def __str__(self):
        return (
            f"{self.destino_id} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.origem_nome}"
        )


''' Tabela para controle de exibição de mesagens recebidas '''


class ControleMsgs(models.Model):
    destino = models.ForeignKey(
        User, related_name="controle", on_delete=models.CASCADE
    )
    origem_id = models.IntegerField()
    origem_nome = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    exibida_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.destino} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.origem_nome}"
        )