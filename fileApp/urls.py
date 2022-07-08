
from django.urls import path
from .views import *

urlpatterns = [   
    path('',home,name=''),

    path('file/<int:file_id>',viewFile,name='file'),
    path('approve/<int:f_id>',approve,name='approve'),
    path('reject/<int:fl_id>',reject,name='reject'),

    path('addfile',addfile,name='addfile'),
    path('yourfiles',yourfiles,name='yourfiles'),    
    path('allocate/<int:fid>',allocate,name='allocate'),   
    path('detail/<int:data>',detail,name='detail'),   

    path('delete/<int:did>',delete,name='delete'),    

    path('login/',login,name='login'),
    path('regs/',regs,name='regs'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),

    # path('test/',test,name='test'),

]
