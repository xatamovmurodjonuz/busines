from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Business, Reaction, Comment
from .forms import BusinessForm, CommentForm


def home(request):
    """
    Bosh sahifa: barcha bizneslarni ko'rsatadi.
    Foydalanuvchi tizimga kirgan bo'lsa, uning har bir biznesga bergan reaksiyalarini oladi.
    """
    businesses = Business.objects.all().order_by('-created_at')

    # Har bir biznes uchun like va dislike sonini qo'shish uchun dict tayyorlash
    # Query optimallashtirish uchun (bu yerdan shablonlarda foydalanamiz)
    for business in businesses:
        business.likes_count = business.reactions.filter(value=Reaction.LIKE).count()
        business.dislikes_count = business.reactions.filter(value=Reaction.DISLIKE).count()

    user_reactions = {}
    if request.user.is_authenticated:
        reactions = Reaction.objects.filter(user=request.user)
        user_reactions = {reaction.business_id: reaction.value for reaction in reactions}

    context = {
        'businesses': businesses,
        'user_reactions': user_reactions,
    }
    return render(request, 'mainapp/home.html', context)


@login_required
def add_business(request):
    """
    Biznes qo'shish: faqat tizimga kirgan foydalanuvchilar uchun.
    Forma yuborilganda validatsiya qilinadi va saqlanadi.
    """
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            messages.success(request, "Biznes muvaffaqiyatli qo'shildi!")
            return redirect('mainapp:home')
        else:
            messages.error(request, "Formada xatolik bor, iltimos tekshiring.")
    else:
        form = BusinessForm()

    return render(request, 'mainapp/add_business.html', {'form': form})


def business_detail(request, pk):
    """
    Biznes tafsilotlari sahifasi.
    Kommentlar va foydalanuvchi reaksiyasini ko'rsatadi.
    Komment qoldirish uchun forma mavjud.
    """
    business = get_object_or_404(Business, pk=pk)
    comments = business.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Komment qoldirish uchun tizimga kiring!")
            return redirect('account_login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.business = business
            comment.user = request.user
            comment.save()
            messages.success(request, "Komment muvaffaqiyatli qoldirildi!")
            return redirect('mainapp:business_detail', pk=pk)
        else:
            messages.error(request, "Komment formasida xatolik bor.")
    else:
        form = CommentForm()

    user_reaction = 0
    if request.user.is_authenticated:
        reaction = business.reactions.filter(user=request.user).first()
        if reaction:
            user_reaction = reaction.value

    likes_count = business.reactions.filter(value=Reaction.LIKE).count()
    dislikes_count = business.reactions.filter(value=Reaction.DISLIKE).count()

    context = {
        'business': business,
        'comments': comments,
        'form': form,
        'user_reaction': user_reaction,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    }
    return render(request, 'mainapp/business_detail.html', context)


@login_required
def react_business(request, pk, reaction_type):
    """
    Biznesga like yoki dislike berish/olib tashlash funksiyasi.
    Faqat POST so'rovlarini qabul qiladi.
    """
    if request.method != 'POST':
        messages.error(request, "Noto'g'ri so'rov turi!")
        return redirect('mainapp:business_detail', pk=pk)

    business = get_object_or_404(Business, pk=pk)
    existing_reaction = business.reactions.filter(user=request.user).first()

    LIKE = Reaction.LIKE
    DISLIKE = Reaction.DISLIKE

    if reaction_type not in ['like', 'dislike']:
        messages.error(request, "Noto'g'ri reaktsiya turi!")
        return redirect('mainapp:business_detail', pk=pk)

    if existing_reaction:
        if (reaction_type == 'like' and existing_reaction.value == LIKE) or \
           (reaction_type == 'dislike' and existing_reaction.value == DISLIKE):
            existing_reaction.delete()
            messages.success(request, "Reaktsiyangiz olib tashlandi.")
        else:
            existing_reaction.value = LIKE if reaction_type == 'like' else DISLIKE
            existing_reaction.save()
            messages.success(request, "Reaktsiyangiz yangilandi.")
    else:
        value = LIKE if reaction_type == 'like' else DISLIKE
        Reaction.objects.create(business=business, user=request.user, value=value)
        messages.success(request, "Reaktsiyangiz saqlandi.")

    return redirect(request.META.get('HTTP_REFERER', 'mainapp:home'))
