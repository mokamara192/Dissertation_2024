from django.urls import path, include
# from voting import views
from . import views
#from users import views

urlpatterns = [
    path('',views.index, name='index'),
    path("vote/<int:pk>/", views.votedash, name='votedash'),
    path("vote/<int:candidate_id>/<int:voting_session_id>/", views.vote, name='vote'),
    path('vote/', views.dashboard, name='dashboard'),
    path('results/', views.results_dashboard, name='results_dashboard'),
    path('results/<int:pk>/', views.results_detail, name='results_detail'),
    path('adminpage',views.adminpage, name="adminpage"),
    path('logout',views.logout, name='logout'),

    path('Add_candidate',views.add_candidate, name="Add_candidate"),
    path('Add_position',views.add_position, name="Add_position"),
    path('Add_voter',views.add_voter, name="Add_voter"),
    path('Create_report',views.Create_report, name="Create_report"),

    path('View_candidate/',views.View_candidate, name="View_candidate"),
    path('View_votedUsers/',views.voted_users_list, name="View_votedUsers"),
    path('View_position',views.View_position, name="View_position"),
    path('View_voter',views.View_voter, name="View_voter"),
    path('View_result',views.View_result, name="View_result"),

    
    path('print/', views.print_page, name='print_page'),
   
#                       DELETE AND UPDATE
    path('delete/<int:id>/', views.delete_candidate, name='candidate_del'),
    path('update_candidate/<int:id>/', views.update_candidate, name='update_candidate'),

    path('dele/<int:id>/', views.delete_position, name='posi_del'),    
    path('update_position/<int:id>/', views.update_position, name='update_position'),

    path('del/<int:id>/', views.delete_voter, name='voter_dele'),
    path('update_voter/<int:id>/', views.update_voter, name='update_voter'),

    
  
    
]