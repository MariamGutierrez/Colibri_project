# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AvistamientosAvistamiento(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_creacion = models.DateTimeField()
    publicado = models.BooleanField()
    estado_conservacion = models.CharField(max_length=15)
    tipo_especie = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'avistamientos_avistamiento'


class AvistamientosImagenavistamiento(models.Model):
    imagen = models.CharField(max_length=100)
    avistamiento = models.ForeignKey(AvistamientosAvistamiento, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'avistamientos_imagenavistamiento'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EducacionAmbientalArticulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.CharField(max_length=50)
    fecha_publicacion = models.DateTimeField()
    publish = models.BooleanField()
    imagen_principal = models.ForeignKey('EducacionAmbientalImagenarticulo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'educacion_ambiental_articulo'


class EducacionAmbientalImagenarticulo(models.Model):
    imagen = models.CharField(max_length=100)
    articulo = models.ForeignKey(EducacionAmbientalArticulo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'educacion_ambiental_imagenarticulo'


class EducacionAmbientalVideoarticulo(models.Model):
    video = models.CharField(max_length=100)
    articulo = models.ForeignKey(EducacionAmbientalArticulo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'educacion_ambiental_videoarticulo'


class MaltratoAnimalEvidencia(models.Model):
    reporte = models.ForeignKey('MaltratoAnimalReportemaltrato', models.DO_NOTHING)
    imagen = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'maltrato_animal_evidencia'


class MaltratoAnimalReportemaltrato(models.Model):
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_creacion = models.DateTimeField()
    nombre = models.CharField(max_length=255, blank=True, null=True)
    publicado = models.BooleanField()
    tipo_especie = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    estado_conservacion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'maltrato_animal_reportemaltrato'


class UsersAnimal(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users_animal'
