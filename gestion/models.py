from django.db import models

class Unite(models.Model):
    unit = models.CharField(max_length=200)
    libelle = models.CharField(max_length=200)
    create_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.libelle

class Direction(models.Model):
    sigle = models.CharField(max_length=10, null=True, blank=True)
    libelle = models.CharField(max_length=200)
    create_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.libelle
    
    
class Services(models.Model):
    libelle = models.CharField(max_length=200)
    direction = models.ForeignKey(Direction, verbose_name='Direction', on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.libelle

class FriendWork(models.Model):
    nom_prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)
    service = models.ForeignKey(Services, verbose_name='Service', on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.nom_prenom)
    
    
class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    alerte_stock = models.PositiveIntegerField()
    sec_stock = models.PositiveIntegerField()
    create_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    
    class Meta:
       ordering = ['code']
    
    def __str__(self):
        return self.name
    
class ProducStoct(models.Model):

    product = models.ForeignKey(Product, verbose_name='produit', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    mouvement = models.CharField(max_length=5, null=True, blank=True)
    service = models.ForeignKey(Services, verbose_name='Services', on_delete=models.CASCADE, null=True, blank=True)
    demandeur = models.ForeignKey(FriendWork, verbose_name='Demandeurs', on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
    

    
    