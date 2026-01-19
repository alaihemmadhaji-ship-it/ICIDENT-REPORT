from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.views.decorators.cache import never_cache
#from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username, password=password)
            request.session["user_id"] = user.id
            return redirect("dashboard")   # ← this sends them to THEIR dashboard
        except User.DoesNotExist:
            return render(request, "pages-login.html", {"error": "Wrong login details"})

    return render(request, "pages-login.html")


# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']
#         profile = request.POST['profile']
#         data_user = User(username=username, email=email, password=password, profile=profile)
#         if (username and password and email):
#             data_user.save()
#             messages.success(request, "Sign up was successful. Please log in")
#             return redirect("login")
#     else:
#         data_user = User()
#     return render(request, 'pages-register.html')
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        profile = request.FILES.get("profile")

        if username and password and email:
            user = User(
                username=username,
                email=email,
                password=password,
                profile=profile
            )
            user.save()

            messages.success(request, "Sign up was successful. Please log in")
            return redirect("login")

    return render(request, "pages-register.html")

# @login_required(login_url='login')

@never_cache
def dashboard(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])
    incidents = Incident.objects.filter(user_id=user)

    return render(request, "dashboard.html", {
        "user": user,
        "incidents": incidents
    })


# def add_incident(request):
#     if not request.session.get("user_id"):
#         return redirect("login")
#
#     if request.method == "POST":
#         user = User.objects.get(id=request.session["user_id"])
#
#         Incident.objects.create(
#             user_id=user,
#             title=request.POST["title"],
#             description=request.POST["description"],
#             file = request.FILES.get('file'),
#             severity=request.POST["severity"],
#         )
#         return redirect("dashboard")
#
#     return render(request, "add_incident.html")
# def add_incident(request):
#     if not request.session.get("user_id"):
#         return redirect("login")
#
#     if request.method == "POST":
#         user = User.objects.get(id=request.session.get("user_id"))
#
#         Incident.objects.create(
#             user=user,
#             title=request.POST.get("title"),
#             description=request.POST.get("description"),
#             severity=request.POST.get("severity"),
#             file=request.FILES.get("file"),
#         )
#
#
#         IncidentHistory.objects.create(
#             incident=incident,
#             action_type="created",
#             performed_by=user
#         )
#
#         return redirect("dashboard")
#
#     return render(request, "add_incident.html")


@never_cache
def edit_incident(request, id):
    if not request.session.get("user_id"):
        return redirect("login")

    incident = get_object_or_404(Incident, id=id)

    if request.method == "POST":
        incident.title = request.POST["title"]
        incident.description = request.POST["description"]
        incident.severity = request.POST["severity"]
        incident.save()

        user = User.objects.get(id=request.session.get("user_id"))
        IncidentHistory.objects.create(
            incident=incident,
            action_type="edited",
            performed_by=user
        )

        return redirect("dashboard")

    return render(request, "edit_incident.html", {"incident": incident})

@never_cache
def add_incident(request):
    if not request.session.get("user_id"):
        return redirect("login")

    if request.method == "POST":
        user = User.objects.get(id=request.session.get("user_id"))


        incident = Incident.objects.create(
            user=user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            severity=request.POST.get("severity"),
            file=request.FILES.get("file"),
        )


        IncidentHistory.objects.create(
            incident=incident,
            action_type="created",
            performed_by=user
        )

        return redirect("dashboard")

    return render(request, "add_incident.html")



@never_cache
def delete_incident(request, id):
    if not request.session.get("user_id"):
        return redirect("login")

    incident = get_object_or_404(Incident, id=id)

    if request.method == "POST":
        incident.delete()
        messages.success(request, "Incident has been deleted successfully.")
        return redirect("dashboard")

    return render(request, "confirm_delete.html", {"incident": incident})






@never_cache
def report_list(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session.get("user_id")

    reports = IncidentReport.objects.select_related("incident").filter(
        incident__user_id=user_id
    )

    return render(request, "report.html", {"reports": reports})


@never_cache
def report_details(request, incident_id):
    report = get_object_or_404(
        IncidentReport,
        incident_id=incident_id
    )
    return render(request, "report_details.html", {"report": report})

@never_cache
def incident_history(request):
    if not request.session.get("user_id"):
        return redirect("login")

    print(request.session.get("user_id"))

    user = User.objects.get(id=request.session.get("user_id"))

    history = IncidentHistory.objects.filter(incident__user=user).order_by('-timestamp')

    return render(request, "incident_history.html", {"history": history})


def logout(request):
    request.session.flush()
    return redirect("index")

# Create your views here.
