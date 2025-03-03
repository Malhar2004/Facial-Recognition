from django.shortcuts import render
from django.http import JsonResponse
import cv2
import face_recognition, numpy as np
from .models import Person, Detected_person
import base64
from django.db.models import Q
from datetime import date







def recognition(input_person_encoding):
    known_pictures_encodings = []
    known_pictures_Name = []
    know_persons = Person.objects.all()

    for known_person in know_persons:
        encoding = np.fromstring(known_person.Name_encoding[1:-1], sep=' ')
        known_pictures_encodings.append(encoding)
        known_pictures_Name.append(known_person.Name)
            
    # camparing the input image with image and getting the results in the form of list (eg. [true, false, false....])
    matches = face_recognition.compare_faces(known_pictures_encodings, input_person_encoding, tolerance=0.48)
    # print(matches)
    print(matches)
    # calculating the distance of input image with each every know image and the least one get extracted by using (argmin) function
    # which extracts the index os least value
    face_distance = face_recognition.face_distance(known_pictures_encodings, input_person_encoding)
    print(face_distance)
    if len(face_distance) > 0:
        best_match_index = np.argmin(face_distance)
        
        if matches[best_match_index]:
            name = known_pictures_Name[best_match_index]
            return name







def decode_image(image):
    img_str = image.split(';base64,')[1]   # data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA.. 
    decoded_image = np.frombuffer(base64.b64decode(img_str), np.uint8)
    frame = cv2.imdecode(decoded_image, cv2.IMREAD_COLOR)
    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return RGB_frame






# Create your views here.

def get_Detected_Person(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    TotalRecord = 0
    FilteredRecord = 0
    data = []

    # total record count (person)
    TotalRecord = Detected_person.objects.count()

    # search opreation
    if search_value:
        Detected_person_queryset = Detected_person.objects.filter(Q(Name__icontains = search_value)|Q(Date_icontains = search_value)|Q(Time_icontains = search_value))

    else:
        Detected_person_queryset = Detected_person.objects.all()

    
    # filteres record count
    FilteredRecord = Detected_person_queryset.count()

    # sorting 

    column_index = int(request.GET.get('order[0][column]', 1))
    direction = request.GET.get('order[0][dir]', 'asc')

    print(column_index)

    column_name = ['Name', 'Date','Time'] [column_index]
    print(column_name)

    if direction == 'desc':
        column_name = f'-{column_name}'
    
    Detected_person_queryset = Detected_person_queryset.order_by(column_name)
    print(Detected_person)

    # pagination

    Detected_person_queryset = Detected_person_queryset[start:start+length]

    for person in Detected_person_queryset:
        formated_date = person.Date.strftime("%d-%m-%y")
        formated_time  = person.Time.strftime("%I:%M %p")
        data.append([person.Name, formated_date, formated_time])

    
    response = {
        'draw' : draw,
        'recordsTotal' : TotalRecord,
        'recordsFiltered' : FilteredRecord,
        'data' : data
    }

    return JsonResponse(response)

    



def index(request):
    return render(request , "index.html")




def process_frame(request):

    if request.method == "POST":
        imgdata = request.POST.get('imagedata')
        decoded_img = decode_image(imgdata)

        # encoding the input frame (webcame image)
        face_encodings = face_recognition.face_encodings(decoded_img)
        
        for face_encoding in face_encodings:
            name = recognition(face_encoding)
            if name :
                if not Detected_person.objects.filter(Q(Name=name)&Q(Date=date.today())).exists():
                    print("Inside")
                    Detected_person.objects.create(Name=name)

                    response_data = {
                        'status' : "success"
                    }

                    return JsonResponse(response_data)
            
                return JsonResponse({'status': "unchanged"})
                
    return JsonResponse({"error" : "Something went wrong"})





def registration(request):
    return render(request, "registration.html")





def person_registration(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Image = request.POST.get('image')

        decoded_image = decode_image(Image)

        # face_location = face_recognition.face_locations(loaded_image, model='cnn')
        encoded_image = face_recognition.face_encodings(decoded_image)

        if Person.objects.filter(Name=Name).exists():
            return JsonResponse({"status": "already Registered"})

        if len(encoded_image) > 1:
            return JsonResponse({"status":"Multiple faces Detected"})

        if encoded_image:
            encoded_image = encoded_image[0]
            name = recognition(encoded_image)
            if name :
                return JsonResponse({"status":"400", "name":name})
            
            encoding_str = np.array2string(encoded_image)

            p = Person.objects.create(Name_encoding = encoding_str, Name=Name)

    
            response_data = {
                    'name' : p.Name,
                    'status' : "success"
            }
            return JsonResponse(response_data)




