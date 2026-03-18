# Arquivo que define como os dados da loja são organizados e salvos no banco de dados
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Regra que garante que produtos invisíveis/desativados nunca apareçam para os clientes
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

# Representa uma categoria da loja, como "Eletrônicos" ou "Roupas"
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)      # Nome da categoria
    slug = models.SlugField(max_length=255, unique=True)        # Texto que aparece na URL, ex: /eletronicos

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name

