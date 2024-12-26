from django.shortcuts import render,redirect,get_object_or_404
from .models import Employe,Service
from .forms import EmployeForm
from django.contrib import messages
from django.db.models import Q


# Create your views here.

def afficherEmploye(request):
    employe= Employe.objects.all()
    return render(request,'testdjango.html',{'Employe':employe})



def ajouterEmploye(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            form = EmployeForm()  # Réinitialiser le formulaire
            mssg = "Commande envoyée, vous pouvez saisir une autre."
            # return render(request, 'testaddemp.html', {'formEmp': form, 'messgEmp': mssg})
            return redirect('empList')
        else:
            mssg = "Erreur : Veuillez corriger les erreurs dans le formulaire."
            return render(request, 'testaddemp.html', {'formEmp': form, 'messgEmp': mssg})
    else:
        form = EmployeForm()
        mssg = "Veuillez remplir les champs."
        return render(request, 'testaddemp.html', {'formEmp': form, 'messgEmp': mssg})

# methode supprimer Employe 
def supprimerEmploye(request, pk):
    employe = Employe.objects.get(id=pk)
    if request.method== 'POST':
        try:
            employe.delete()
            messages.success(request, "L'employé a été supprimé avec succès.")
            return redirect('empList')
        except Employe.DoesNotExist:
            messages.error(request, "L'employé n'a pas été trouvé.")
            return redirect('empList')
    
    return render(request,'testsuppemp.html',{'emp':employe})

# def supprimerEmploye(request, pk):
#     # importe l'objet employe , ou raise a 404 error si non trouvé
#     employe = get_object_or_404(Employe, id=pk)
#     if request.method == 'POST':
#         employe.delete()
#         messages.success(request, "L'employé a été supprimé avec succès.")
#         return redirect('empList')
#     else:
#         messages.error(request, "L'employé n'est pas valide pour suppression.")
#         return redirect('empList')
#     # si le request method est GET, allez the confirmation page
#     return render(request, 'testsuppemp.html', {'emp': employe})

def recherchreEmploye(request):
    if request.method == 'GET':
        query = request.GET.get('search').strip()
        # eliminer les espaces de debut et la fin de text 
        if query:
           
            employes = Employe.objects.filter(
                Q(nom__icontains=query) |
                Q(prenom__icontains=query) |
                Q(id__icontains=query) |
                Q(adresse__icontains=query) |
                Q(date_naissance__icontains=query) |
                Q(date_embauche__icontains=query)
            )

            if employes.exists(): 
                return render(request, 'testsearch.html', {'employe': employes})

            return render(request, 'testsearch.html', {'message': 'Aucun employé trouvé pour cette recherche.'})
        
        return render(request, 'testsearch.html', {'message': 'Veuillez entrer un terme de recherche.'})
    
    return render(request, 'testsearch.html', {'message': 'Utilisez la méthode GET pour effectuer une recherche.'})



# def supprimerEmploye(request, pk):
#     # importe l'objet employe , ou raise a 404 error si non trouvé
#     employe = get_object_or_404(Employe, id=pk)
#     if request.method == 'POST':
#         employe.delete()
#         messages.success(request, "L'employé a été supprimé avec succès.")
#         return redirect('empList')
#     else:
#         messages.error(request, "L'employé n'est pas valide pour suppression.")
#         return redirect('empList')

#     # si le request method est GET, allez the confirmation page
#     return render(request, 'testsuppemp.html', {'emp': employe})


def modifierEmploye(request,pk):
    emp=Employe.objects.get(id=pk)
    if request.method=='POST':
        formEmp=EmployeForm(request.POST,instance=emp)
        if formEmp.is_valid():
            formEmp.save()
            return redirect("empList")
        else:
            return render(request, 'empEdit.html', {"form": formEmp})
    else:
        formEmp=EmployeForm(instance=emp)
        return render(request,'empEdit.html',{"form":formEmp})

    
# def afficherServices(request):
#     Services=