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

# Representa um produto da loja com todas as suas informações
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)         # Categoria à qual o produto pertence
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')   # Usuário administrador que cadastrou o produto
    title = models.CharField(max_length=255)                       # Nome do produto
    author = models.CharField(max_length=255, default='admin')     # Responsável pelo cadastro
    description = models.TextField(blank=True)                     # Descrição detalhada do produto
    image = models.ImageField(upload_to='images/')                 # Foto do produto
    slug = models.SlugField(max_length=255)                        # Texto que aparece na URL, ex: /tenis-nike
    price = models.DecimalField(max_digits=9, decimal_places=2)    # Preço do produto, ex: 99.90
    in_stock = models.BooleanField(default=True)                   # Se o produto está disponível no estoque
    is_active = models.BooleanField(default=True)                  # Se o produto está visível na loja
    created = models.DateTimeField(auto_now_add=True)              # Data em que o produto foi cadastrado
    updated = models.DateTimeField(auto_now=True)                  # Data da última atualização do produto
    objects = models.Manager()
    products = ProductManager()                                    # Busca apenas produtos ativos/visíveis

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)                                   # Produtos mais recentes aparecem primeiro

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title