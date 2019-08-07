from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from upload.forms import UploadFileForm
from upload.models import UploadFileModel
from .models import category,brand_for_category
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


#category_id -> 브랜드 선택 , product_id -> 상품 선택, sale_id -> 판매 타입 선택
#값이 99999면 선택되지 않은 default 상태임을 의미한다.
class main:
    @csrf_exempt
    def home( request, category_id=99999 , product_id=99999,sale_id=99999):
        print('####  START  ####')
        print(category_id ,product_id,sale_id)

        #여기서부터 시작
        ufl = UploadFileModel.objects.all()


        if request.method == 'POST':
            select_brand = request.POST['brand']
            select_sale = request.POST['saletype']

            if select_brand != 'all':
                ufl = ufl.filter(pbrand=select_brand)

                if select_sale != 'all':
                    ufl = ufl.filter(saletype=select_sale)

                    
            

        if category_id != 99999:   #브랜드가 선택된다면             
            selectedcategory = get_object_or_404(brand_for_category,pk=category_id)
            ufl = UploadFileModel.objects.filter(pbrand = selectedcategory.brandname)
        else:   #브랜드 선택안됨,
            selectedcategory = None
        
        

        if sale_id != 99999: #판매방식 선택됨
            pass
        else:
            pass

        if product_id != 99999:       #상품의 detail을 보려고 한다면,
            details = get_object_or_404(UploadFileModel, pk=product_id)  
        else:
            details = None


        brand_for_categorys = brand_for_category.objects

        #정렬부분
        #sort = request.GET.get('sort','')
        #if sort == 'lowprice':
        #    ufl = ufl.order_by('lowerlimit')
        #elif sort == 'date':
        #    ufl = UploadFileModel.objects.all().order_by('pub_date')
        #elif sort == 'highprice':
        #    ufl = UploadFileModel.objects.all().order_by('-lowerlimit')
        #else:
        #    ufl =  ufl

    
        paginator = Paginator(ufl, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
  
        return render(request, 'home.html',{'selectedcategory':selectedcategory, 'posts':posts,'brand_for_categorys':brand_for_categorys,'details':details})



@csrf_exempt
@login_required
def auction(request,product_id):

    details = UploadFileModel.objects.get( pk=product_id)

    ufl = UploadFileModel.objects
    brand_for_categorys = brand_for_category.objects
    sort = request.GET.get('sort','')

    if sort == 'lowprice':
        ufl = UploadFileModel.objects.all().order_by('lowerlimit')
    elif sort == 'date':
        ufl = UploadFileModel.objects.all().order_by('pub_date')
    elif sort == 'highprice':
        ufl = UploadFileModel.objects.all().order_by('-lowerlimit')
    else:
        ufl =  ufl = UploadFileModel.objects.all()

    product_list = ufl
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    bidprice = request.POST.get('bidprice', '오류')
    if int(bidprice) < details.lowerlimit and int(bidprice)<= details.bidprice:
        print('하한가, 현재입찰가보다 낮은 가격으로 입찰할 수 없음  이라는 메시지 띄워야함')
        return render(request,'home.html',{'ufl':ufl, 'posts':posts,'brand_for_categorys':brand_for_categorys,'details':details})
    else:
        details.bidprice = bidprice
        details.biduser = request.user.username
        details.save()
    return render(request,'home.html',{'ufl':ufl, 'posts':posts,'brand_for_categorys':brand_for_categorys,'details':details})



@login_required
def mypage(request):
    ufl = UploadFileModel.objects.filter(user_id = request.user.username)
    return render(request, 'mypage.html',{'ufl':ufl})

@login_required
def buy(request, product_id):
    productbuy = get_object_or_404(UploadFileModel ,pk=product_id)
    return render(request,'buy.html',{'productbuy':productbuy})
    
@login_required
def pay(request, product_id):
    productpay = get_object_or_404(UploadFileModel ,pk=product_id)
    return render(request,'pay.html',{'productpay':productpay})