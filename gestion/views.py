from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
User = get_user_model()
from gestion.models import ProducStoct, Product, Unite, Direction, Services, FriendWork
from .forms import ProductForm, StockForm
from django.forms import formset_factory
from  django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, FileResponse, JsonResponse
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A3, A5, A4, A6, A7, A8, B5, B1, B2, B3, B4, B6, B7
from io import BytesIO
import io, csv
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count, Sum



def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(code__icontains=query)
    data = []
    for result in results:
        data.append({
            'code': result.code,
            'url': result.get_absolute_url(),
        })
    return JsonResponse({'data': data})


@login_required
def index(request):
    sortiies = ProducStoct.objects.filter(mouvement__contains='Sortie', create_at__year=2023).count()
    entrees = ProducStoct.objects.filter(mouvement__contains='Entre', create_at__year=2023).count()
    products = Product.objects.filter(stock__gt = 0).count()
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



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot à été changé avec succès')
            return redirect('index')
        else:
            messages.error(request, 'Erreur veuillez verifiez vos identifiants antérieurs')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'gestion/change_password.html', {
        'form': form
    })
    
    
    

@login_required
def add_product(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 8)
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
            messages.error(request, "Veuillez verifiez svp l'article existe déja!!")
            return render(request, 'gestion/add_product.html', {"form":form, "page_obj":page_obj})
    else:
        form = ProductForm()
        return render(request, 'gestion/add_product.html', {"form":form, "page_obj":page_obj})
    
@login_required
def vue(request, pk):
    product_arlet = Product.objects.get(pk=pk)
    return render(request, 'gestion/vue.html', {"product_arlet":product_arlet})

@login_required
def operation(request):
    Operations = ProducStoct.objects.filter(mouvement__contains='Sortie').order_by('-id')
    paginator = Paginator(Operations, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request, 'gestion/operation.html', context)

@login_required
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


@login_required
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



@login_required
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    demandeurs = FriendWork.objects.all()
    services = Services.objects.all()
    return render(request, 'gestion/product_detail.html', {'product': product, "demandeurs":demandeurs, "services":services})


@login_required
def product_detail2(request, pk):
    product = Product.objects.get(pk=pk)
    demandeurs = FriendWork.objects.all()
    services = Services.objects.all()
    return render(request, 'gestion/product_detail2.html', {'product': product, "demandeurs":demandeurs, "services":services})


@login_required
def entree(request):
    demandeurs= FriendWork.objects.all()
    services = Services.objects.all()
    products = Product.objects.all()
    StockFormset = formset_factory(forms.StockForm, extra=1)
    formset = StockFormset()
    return render(request, 'gestion/entree.html', {"formset":formset, "demandeurs":demandeurs, "services":services, "products":products})


@login_required
def sorti(request):
    demandeurs= FriendWork.objects.all()
    services = Services.objects.all()
    products = Product.objects.all()
    StockFormset = formset_factory(forms.StockForm, extra=1)
    formset = StockFormset()
    return render(request, 'gestion/sorti.html', {"formset":formset, "demandeurs":demandeurs, "services":services, "products":products})


@login_required
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


@login_required
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


@login_required
def liste(request):
    articles = Product.objects.all()
    template_path = 'gestion/articles.html'
    context = {'articles':articles}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if you want to dowload
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
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


@login_required
def etat(request):
    Operations = ProducStoct.objects.filter(mouvement__contains='Sortie').order_by('-id')
    paginator = Paginator(Operations, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    etats = ProducStoct.objects.filter(mouvement__contains='Sortie').values('product__name', 'service__libelle').annotate(total=Count('product'), quantite=Sum('quantity'))
    grouped_etats = {}
    for etat in etats:
        service__libelle = etat['service__libelle']
        if service__libelle not in grouped_etats:
            grouped_etats[service__libelle] = []
        grouped_etats[service__libelle].append({
        'product__name': etat['product__name'],
        'total': etat['total'],
        'quantite': etat['quantite']
    })
    context={"page_obj":page_obj, "grouped_etats":grouped_etats}
    return render(request, 'gestion/etat.html', context)



@login_required
def statistique(request):
    etats = ProducStoct.objects.filter(mouvement__contains='Sortie').values('product__name', 'service__libelle').annotate(total=Count('product'), quantite=Sum('quantity'))
    barres = etats.count()
    grouped_etats = {}
    for etat in etats:
        service__libelle = etat['service__libelle']
        if service__libelle not in grouped_etats:
            grouped_etats[service__libelle] = []
        grouped_etats[service__libelle].append({
        'product__name': etat['product__name'],
        'total': etat['total'],
        'quantite': etat['quantite']
    })
    context={"etats":etats, "grouped_etats":grouped_etats, "barres":barres}
    return render(request, 'gestion/statistique.html', context)



