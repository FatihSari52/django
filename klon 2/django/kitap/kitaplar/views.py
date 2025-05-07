from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Kitap
from django.db.models import Q
from datetime import datetime

def kitap_listesi(request):
    # Filtreleme parametrelerini al
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    # Temel sorgu
    kitaplar = Kitap.objects.all()
    
    # Arama filtresi
    if search_query:
        kitaplar = kitaplar.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Fiyat filtresi
    if min_price:
        kitaplar = kitaplar.filter(price__gte=min_price)
    if max_price:
        kitaplar = kitaplar.filter(price__lte=max_price)
    
    # Tarih filtresi
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            kitaplar = kitaplar.filter(published_time__gte=start_date)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            kitaplar = kitaplar.filter(published_time__lte=end_date)
        except ValueError:
            pass
    
    # Filtreleme formu için context
    context = {
        'kitaplar': kitaplar,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'kitaplar/kitap_listesi.html', context)

def kitap_detay(request, pk):
    kitap = get_object_or_404(Kitap, pk=pk)
    return render(request, 'kitaplar/kitap_detay.html', {'kitap': kitap})

def kitap_ekle(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        published_time = request.POST.get('published_time')
        price = request.POST.get('price')
        
        if title and content:
            Kitap.objects.create(
                title=title,
                content=content,
                published_time=published_time if published_time else None,
                price=price if price else None
            )
            messages.success(request, 'Kitap başarıyla eklendi.')
            return redirect('kitap_listesi')
        else:
            messages.error(request, 'Lütfen gerekli alanları doldurun.')
    
    return render(request, 'kitaplar/kitap_form.html')

def kitap_duzenle(request, pk):
    kitap = get_object_or_404(Kitap, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        published_time = request.POST.get('published_time')
        price = request.POST.get('price')
        
        if title and content:
            kitap.title = title
            kitap.content = content
            kitap.published_time = published_time if published_time else None
            kitap.price = price if price else None
            kitap.save()
            messages.success(request, 'Kitap başarıyla güncellendi.')
            return redirect('kitap_listesi')
        else:
            messages.error(request, 'Lütfen gerekli alanları doldurun.')
    
    return render(request, 'kitaplar/kitap_form.html', {'kitap': kitap})

def kitap_sil(request, pk):
    kitap = get_object_or_404(Kitap, pk=pk)
    if request.method == 'POST':
        kitap.delete()
        messages.success(request, 'Kitap başarıyla silindi.')
        return redirect('kitap_listesi')
    return render(request, 'kitaplar/kitap_sil.html', {'kitap': kitap})
