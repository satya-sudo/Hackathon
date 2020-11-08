from django.core.management.base import BaseCommand 

from JobsForALL.models import  User,UserProfile,Gig

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        count = 0
        x = Gig.objects.all().filter(active=True)
        y = UserProfile.objects.all().filter(usertype='employee')
        for i in x:
            for j in y:
                if i.location == j.location and i.gig_type == j.service_type and i.assign == None:
                    i.assign = j.user
                    count += 1
                    i.save()
                    break
        print('jobs assigned :',count)        