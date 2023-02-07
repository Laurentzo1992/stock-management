from . import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
from gestion.models import ProducStoct, Product, Unite, Direction, Services, FriendWork
from .forms import ProductForm, StockForm
from django.forms import formset_factory
from  django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, FileResponse
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A3, A5, A4, A6, A7, A8, B5, B1, B2, B3, B4, B6, B7
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from io import BytesIO
import io, csv
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.views.generic import ListView



def index(request):
    sortiies = ProducStoct.objects.filter(mouvement__contains='Sortie', create_at__year=2023).count()
    entrees = ProducStoct.objects.filter(mouvement__contains='Entre', create_at__year=2023).count()
    products = Product.objects.all().count()
    products_arletes = Product.objects.all()
    paginator = Paginator(products_arletes, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"products":products, "page_obj":page_obj, "sortiies":sortiies, "entrees":entrees}
    return render(request, 'gestion/index.html', context)


def login_user(request):
    #crée une instance du formulaire
    form = forms.LoginForm()
    #definir une variable message pour informer le user si ses identifiant sont iccorecte
    message = ''
    #Test l'action si post (envoi de donnée)
    if request.method == 'POST':
        # On recupère les données dans l'instance du formulaire
        form = forms.LoginForm(request.POST)
        #Verifie si le formulaire est valide
        if form.is_valid():
            #On authentifie l'instance du user avec la methode authenticate
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            #Test si le usernme  envoyé du fomrulair ,'est pas null
            if user is not None:
                #Etablie une connection de lutilisateur
                login(request, user)
                #On le redirige vers une page ici c'est index.html
                return redirect('index')
            #si le formulaire n'est pas correct e.i si des les données dont incorrecte informé le user
        message = 'Invalides veuillez verifiez votre nom d\'utilisateur ou votre mot de passe'
    return render(request, 'gestion/login_user.html', context={'form': form, 'message': message})



def logout_user(request):
    #deconnection du user avec la methode logout 
    logout(request)
    return redirect('login_user')


def add_product(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method=="POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pro_code = form.cleaned_data.get('code')
            nom_pro = form.cleaned_data.get('name')
            messages.success(request, f"L'élément {nom_pro} code {pro_code}  ajouté avec succes !")
            return HttpResponseRedirect('add_product')
        else:
            return render(request, 'gestion/add_product.html', {"form":form, "page_obj":page_obj})
    else:
        form = ProductForm()
        return render(request, 'gestion/add_product.html', {"form":form, "page_obj":page_obj})
    

def vue(request, pk):
    product_arlet = Product.objects.get(pk=pk)
    return render(request, 'gestion/vue.html', {"product_arlet":product_arlet})


def operation(request):
    Operations = ProducStoct.objects.filter(mouvement__contains='Sortie').order_by('-id')
    paginator = Paginator(Operations, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request, 'gestion/operation.html', context)


def product_plus_stock(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        mouvement = request.POST['mouvement']
        if quantity >= 1:
            product.stock += quantity
            messages.success(request, f'{quantity} {product.name} ajouté avec succès')
        else:
            messages.error(request, 'Veuillez verifiez la quantité sasie')
        product.save()
        ProducStoct.objects.create(product=product, quantity=quantity, mouvement=mouvement)
        return redirect('add_product')
    return render(request, 'gestion/product_detail.html')



def product_minus_stock(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        mouvement = request.POST['mouvement']
        demandeur = request.POST['demandeur']
        service = request.POST['service']
        if quantity >= 1 and product.stock >= quantity:
            product.stock -= quantity
            messages.success(request, f'{quantity} {product.name} retiré')
        else:
            messages.error(request, 'Veuillez verifiez la quantité sasie et votre stock!')
        product.save()
        ProducStoct.objects.create(product=product, quantity=quantity, mouvement=mouvement, demandeur_id=demandeur, service_id=service)
        return redirect('add_product')
    return render(request, 'gestion/product_detail2.html')




def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    demandeurs = FriendWork.objects.all()
    services = Services.objects.all()
    return render(request, 'gestion/product_detail.html', {'product': product, "demandeurs":demandeurs, "services":services})

def product_detail2(request, pk):
    product = Product.objects.get(pk=pk)
    demandeurs = FriendWork.objects.all()
    services = Services.objects.all()
    return render(request, 'gestion/product_detail2.html', {'product': product, "demandeurs":demandeurs, "services":services})



def entree(request):
    demandeurs= FriendWork.objects.all()
    services = Services.objects.all()
    products = Product.objects.all()
    StockFormset = formset_factory(forms.StockForm, extra=1)
    formset = StockFormset()
    if request.method == 'POST':
        # formset = StockForm(request.POST, request.FILES)
        # mouvement = formset.cleaned_data.get('mouvement')
        # quantity = formset.cleaned_data.get('quantity')
        product = request.POST.get('product')
        formset = StockForm(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    product.stock += form.cleaned_data['quantity']
                    product.save(commit=False)
                    form.save()
                    quant = form.cleaned_data.get('quantity')
                    nom_pro = form.cleaned_data.get('product')
            messages.success(request, f"Vous avez ajouté {quant} à l'artile {nom_pro} avec succes !")
            return HttpResponseRedirect('add_product')
    return render(request, 'gestion/entree.html', {"formset":formset, "demandeurs":demandeurs, "services":services, "products":products})



def sorti(request):
    demandeurs= FriendWork.objects.all()
    services = Services.objects.all()
    products = Product.objects.all()
    StockFormset = formset_factory(forms.StockForm, extra=1)
    formset = StockFormset()
    if request.method == 'POST':
        # formset = StockForm(request.POST, request.FILES)
        # mouvement = formset.cleaned_data.get('mouvement')
        # quantity = formset.cleaned_data.get('quantity')
        product = request.POST.get('product')
        formset = StockForm(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    product.stock += form.cleaned_data['quantity']
                    product.save(commit=False)
                    form.save()
                    quant = form.cleaned_data.get('quantity')
                    nom_pro = form.cleaned_data.get('product')
            messages.success(request, f"Vous avez retiré {quant} à l'artile {nom_pro} avec succes !")
            return HttpResponseRedirect('add_product')
    return render(request, 'gestion/sorti.html', {"formset":formset, "demandeurs":demandeurs, "services":services, "products":products})



def pdf_view(request, pk):
     
    #create a byttestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=B7, bottomup=0)
    #create text oject
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 10)
   
    operation = ProducStoct.objects.get(pk=pk)
    Prenom = request.user.first_name
    Nom = request.user.last_name
    
    textob.textLine("Code article ===> " + operation.product.code)
    textob.textLine(" ")
    textob.textLine("Nom de l'artile ===> " +operation.product.name)
    textob.textLine(" ")
    textob.textLine("Type de mouvement ===> " + operation.mouvement)
    textob.textLine(" ")
    textob.textLine("Quantité demandé ===> " + str(operation.quantity))
    textob.textLine(" ")
    textob.textLine("Services receveur ===> " + str(operation.service.direction.sigle))
    textob.textLine(" ")
    textob.textLine("---------------------------------------")
    #textob.textLine("Responsable : " + operation.demandeur.nom_prenom + "               " + "Operateur : " + Prenom + " " + Nom)
    textob.textLine("Responsable : " + operation.demandeur.nom_prenom)
    textob.textLine(" ")
    textob.textLine(" ")
    textob.textLine(" ")
    textob.textLine(" ")
    textob.textLine(" ")
    textob.textLine("Operateur : " + Prenom + " " + Nom)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    #return something
    return FileResponse(buf, as_attachment=False, filename='bon.pdf')



def approvisionement(request, pk):
    article = Product.objects.get(pk=pk)
    template_path = 'gestion/approvisionement.html'
    context = {'article':article}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if you want to dowload
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if you want to display only
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def liste(request):
    articles = Product.objects.all()
    template_path = 'gestion/articles.html'
    context = {'articles':articles}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if you want to dowload
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if you want to display only
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



