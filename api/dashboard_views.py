from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Expense, Income, Savings, UserProfile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = None
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username', ''),
                            password=request.POST.get('password', ''))
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', '/dashboard/'))
        error = 'Invalid credentials or insufficient permissions.'
    return render(request, 'dashboard/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


def _base_context(request):
    return {'admin_user': request.user.username}


@login_required(login_url='/login/')
def dashboard(request):
    total_users   = User.objects.count()
    total_expense = sum(e.amount for e in Expense.objects.all())
    total_income  = sum(i.amount for i in Income.objects.all())
    total_savings = sum(s.current_balance for s in Savings.objects.all())

    recent = Expense.objects.select_related('user').order_by('-created_at')[:8]

    today = timezone.now().date()
    days_labels   = []
    days_school   = []
    days_personal = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        days_labels.append(f'"{day.strftime("%a")}"')
        school_amt   = sum(e.amount for e in Expense.objects.filter(date=day, category='school'))
        personal_amt = sum(e.amount for e in Expense.objects.filter(date=day, category='personal'))
        days_school.append(float(school_amt))
        days_personal.append(float(personal_amt))

    school_total   = float(sum(e.amount for e in Expense.objects.filter(category='school')))
    personal_total = float(sum(e.amount for e in Expense.objects.filter(category='personal')))
    other_total    = float(sum(e.amount for e in Expense.objects.filter(category='other')))
    grand_total    = school_total + personal_total + other_total or 1

    context = {
        **_base_context(request),
        'total_users':    total_users,
        'total_expense':  total_expense,
        'total_income':   total_income,
        'total_savings':  total_savings,
        'balance':        total_income - total_expense,
        'recent':         recent,
        'days_labels':    '[' + ','.join(days_labels) + ']',
        'days_school':    days_school,
        'days_personal':  days_personal,
        'school_total':   school_total,
        'personal_total': personal_total,
        'other_total':    other_total,
        'school_pct':     round(school_total   / grand_total * 100, 1),
        'personal_pct':   round(personal_total / grand_total * 100, 1),
        'other_pct':      round(other_total    / grand_total * 100, 1),
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='/login/')
def reports(request):
    expenses = Expense.objects.select_related('user').order_by('-date', '-created_at')
    total_school   = float(sum(e.amount for e in expenses if e.category == 'school'))
    total_personal = float(sum(e.amount for e in expenses if e.category == 'personal'))
    total_other    = float(sum(e.amount for e in expenses if e.category == 'other'))
    grand_total    = total_school + total_personal + total_other

    context = {
        **_base_context(request),
        'expenses':       expenses,
        'total_school':   total_school,
        'total_personal': total_personal,
        'total_other':    total_other,
        'grand_total':    grand_total,
    }
    return render(request, 'dashboard/reports.html', context)


@login_required(login_url='/login/')
def notifications(request):
    recent_expenses = Expense.objects.select_related('user').order_by('-created_at')[:20]
    recent_incomes  = Income.objects.select_related('user').order_by('-id')[:10]
    context = {
        **_base_context(request),
        'recent_expenses': recent_expenses,
        'recent_incomes':  recent_incomes,
    }
    return render(request, 'dashboard/notifications.html', context)


@login_required(login_url='/login/')
def settings_view(request):
    total_users    = User.objects.count()
    total_expenses = Expense.objects.count()
    total_incomes  = Income.objects.count()
    total_savings  = Savings.objects.count()
    context = {
        **_base_context(request),
        'total_users':    total_users,
        'total_expenses': total_expenses,
        'total_incomes':  total_incomes,
        'total_savings':  total_savings,
    }
    return render(request, 'dashboard/settings.html', context)


@login_required(login_url='/login/')
def profile_view(request):
    raw_users = User.objects.select_related('profile').order_by('-date_joined')
    users = []
    for u in raw_users:
        try:
            gender = u.profile.gender or '—'
        except Exception:
            gender = '—'
        users.append({
            'username':    u.username,
            'email':       u.email or '—',
            'gender':      gender,
            'date_joined': u.date_joined,
            'is_superuser': u.is_superuser,
            'initials':    u.username[:2].upper(),
        })
    context = {
        **_base_context(request),
        'users':      users,
        'admin_info': request.user,
    }
    return render(request, 'dashboard/profile.html', context)


@login_required(login_url='/login/')
def savings_view(request):
    savings = Savings.objects.select_related('user').order_by('-id')
    total_target  = float(sum(s.target          for s in savings))
    total_balance = float(sum(s.current_balance for s in savings))
    total_monthly = float(sum(s.monthly_plan    for s in savings))

    context = {
        **_base_context(request),
        'savings':       savings,
        'total_target':  total_target,
        'total_balance': total_balance,
        'total_monthly': total_monthly,
    }
    return render(request, 'dashboard/savings.html', context)
