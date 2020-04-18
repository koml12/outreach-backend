import glob, re, os
from django.dispatch import receiver
from django.db.models.signals import post_save
from api.models import Resume, Job, Event, Registered
from api.serializers import RegistrationSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tika import parser as pdf_parser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

@receiver(post_save, sender=Resume)
def save_parsed_resume(sender, instance, created=False, **kwargs):
    file_path = instance.file.path
    parent_save_dir = os.path.abspath(os.path.join(file_path,'..','..','parsed_media'))
    save_file_path = os.path.abspath(os.path.join(parent_save_dir, instance.file.name))

    resume = pdf_parser.from_file(file_path)['content']
    resume = resume.replace('\n', ' ')
    resume = resume.replace('\r', ' ')
    resume = re.sub('[^a-zA-Z\d]',' ', resume)
    resume = ' '.join(resume.split())

    if not os.path.exists(parent_save_dir):
        os.makedirs(parent_save_dir)
    f = open(save_file_path, 'w')
    f.write(resume)
    f.close()

class ranking_serializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

@api_view(['POST'])
def ranking(request):
    req_serializer = ranking_serializer(data=request.data)
    if(req_serializer.is_valid()):
        job_desc = Job.objects.filter(id=request.data["job"])[0].Description.replace('\n', ' ').replace('\r', ' ')
        job_desc = re.sub('[^a-zA-Z\d]',' ', job_desc)
        job_desc = ' '.join(job_desc.split())
        registrations = Registered.objects.filter(event=request.data["event"])

        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        job_desc_vector = tfidf_vectorizer.fit_transform([job_desc]).toarray()
        resume_ranking = []
        for registration in registrations:
            if registration.resume is not None:
                file_path = os.path.abspath(os.path.join(registration.resume.file.path,'..','..','parsed_media', registration.resume.file.name))
                f = open(file_path,mode='r')
                resume = f.read()
                f.close()
                res_vec = tfidf_vectorizer.transform([resume])
                knn_1 = NearestNeighbors(n_neighbors=1, algorithm='auto')
                knn_1.fit(res_vec)
                resume_ranking.extend(knn_1.kneighbors(job_desc_vector)[0][0].tolist())
        resume_rankings = [x for _,x in sorted(zip(resume_ranking,registrations))]
        return Response(RegistrationSerializer(resume_rankings,many=True).data)
    else:
        return Response({"Error": "Invalid job or event."})