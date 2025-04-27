from django.shortcuts import render, redirect
from . import models
# Create your views here.


def user_list(request):
    queryset = models.User.objects.all()
    context = {"queryset": queryset,}
    return render(request, 'user_list.html', context)


def user_add(request):
    if request.method == "GET":
        return render(request, 'user_add.html')
    form = {
        'account': request.POST.get('account'),
        'name': request.POST.get('name'),
        'gender': request.POST.get('gender'),
        'email': request.POST.get('email'),
        'password': request.POST.get('password'),
    }
    result = models.User.objects.filter(account=form['account'])
    if result:
        form['tip'] = '该账号已存在。'
        return render(request, 'user_add.html', form)
    models.User.objects.create(**form)
    return redirect('/app01/login/')


def user_delete(request, id_):
    models.User.objects.filter(id=id_).delete()
    return redirect('/app01/user/list/')


def user_edit(request, id_):
    user = models.User.objects.filter(id=id_).first()
    form = {
        'name': user.name,
        'email': user.email,
        'password': user.password,
    }
    if request.method == "GET":
        return render(request, 'user_edit.html', form)
    form = {
        'name': request.POST.get('name'),
        'gender': request.POST.get('gender'),
        'email': request.POST.get('email'),
        'password': request.POST.get('password'),
    }
    models.User.objects.filter(id=user.id).update(**form)
    return redirect('/app01/user/list/')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    form = {}
    form['account'] = request.POST['username']
    form['password'] = request.POST['password']
    obj = models.User.objects.filter(**form)
    if len(obj) == 0:
        form['tip'] = '账号或密码错误'
        return render(request, 'login.html', form)
    request.session['info'] = {
        'id': obj.first().id,
        'account': obj.first().account,
    }
    return redirect('/ys/home/')


def logout(request):
    request.session.clear()
    return redirect('/app01/login/')
