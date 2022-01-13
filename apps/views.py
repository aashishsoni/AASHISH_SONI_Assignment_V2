from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import F
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate, logout
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.models import UserProfile, Sale_Statistics, Country, Country_City

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """ new user creation function """
    first_isalpha = request.data['password'][0].isalpha()
    if len(request.data['password']) < 8:
        return Response({'status': 'fail', 'message': 'The password must be at least 8 characters long!'})
    if all(c.isalpha() == first_isalpha for c in request.data['password']):
        return Response({'status': 'fail', 'message': 'The Password must be a combination of characters with numbers or special characters!'})
    if not User.objects.filter(email=request.data['email']).exists():
        User.objects.create_user(
            email=request.data['email'], password=request.data['password'],
            first_name=request.data['first_name'], last_name=request.data['last_name'])
        return Response({'status': 'success', "message": "user create successfully"})
    return Response({'status': 'fail', "message": "this email is already register"})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """ for user login """

    if not User.objects.filter(email=request.data['email']).exists():
        return Response({'status': 'fail', "message": "this email not register"})
    user = User.objects.get(email=request.data['email'])
    if user.is_active:
        authenticate(email=request.data['email'],
                     password=request.data['password'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 'success', 'message': 'User loggedIn', 'token': token.key, 'user_id': user.id})
    return Response({'status': 'fail', 'message': 'this user is not active'})


@api_view(['POST'])
def user_logout(request):
    """ This function used for logout."""
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return Response(status=status.HTTP_200_OK)


class user_details(GenericAPIView):
    """ This Api used for get and upadte user profile. """

    def get(self, request, id):
        """ This function used for get user details. """
        all_user_data = UserProfile.objects.filter(user_id=id).values(
            'user_id', 'user__first_name', 'user__last_name', 'user__email', 'gender', 'age', 'country', 'city').annotate(user_first_name=F('user__first_name'))
        return Response({'status': 'success', 'message': 'User details.', 'data': all_user_data})

    def patch(self, request, id):
        """ This function used for update user profile details. """
        try:
            if User.objects.get(id=id).email == request.data['email'] or not User.objects.filter(email=request.data['email']).exists():
                User.objects.filter(id=id).update(
                    first_name=request.data['first_name'], last_name=request.data['last_name'], email=request.data['email'])
                UserProfile.objects.filter(user_id=id).update(
                    gender=request.data['gender'], age=request.data['age'], country=request.data['country'], city=request.data['city'])
                all_user_data = UserProfile.objects.get(
                    user=User.objects.get(id=id))
                all_data = [{'id': all_user_data.user.id, 'first_name': all_user_data.user.first_name, 'last_name': all_user_data.user.last_name,
                             'email': all_user_data.user.email, 'gender': all_user_data.gender, 'age': all_user_data.age, 'country': all_user_data.country.id, 'city': all_user_data.city.id}]
                return Response({'status': 'success', 'message': 'user details updated successfully..!', 'data': all_data})
            return Response({'status': 'fail', 'message': 'user email already exists..!'}, status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response({'status': 'fail', 'message': 'This User data id not available..!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def countries(request):
    """ This function used for get all city details according to country. """
    rwc_data = []
    for country_data in Country.objects.all():
        all_data = {'id': country_data.id, 'name': country_data.country_name,
                    'cities': Country_City.objects.filter(country_id=country_data.id).values()}
        rwc_data.append(all_data)
    return Response({'status': 'success', 'message': "user data get successfully",
                    'data': rwc_data}, status=status.HTTP_200_OK)


class sales_data(GenericAPIView):
    """ This api used for sels curd operatin. """

    def get(self, request):
        """ Thisfunction used for get all sales data according to user. """
        try:
            all_sales_data = Sale_Statistics.objects.filter(
                user=request.user).values()
        except Exception:
            return Response({'status': 'fail', 'message': "Sales data not available."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'success', 'message': "Sales data get successfully.", 'data': all_sales_data})

    def post(self, request):
        """ This function used for save sales data according to user. """
        try:
            sale_statistics_data = Sale_Statistics.objects.create(user=request.user, date=request.data['date'], product=request.data['product'],
                                                                  sales_number=request.data['sales_number'], revenue=request.data['revenue'])
            data = {'sale_statistics_data': sale_statistics_data.date, "product": sale_statistics_data.product,
                    "sales_number": sale_statistics_data.sales_number, "revenue": sale_statistics_data.revenue}
        except Exception:
            return Response({'status': 'fail', 'message': "data not found", }, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'success', 'message': "user data get successfully", 'data': data}, status=status.HTTP_201_CREATED)

    def patch(self, request, **kwargs):
        """ This function used for upadre sales data according to user. """
        if 'date' in request.data:
            Sale_Statistics.objects.filter(id=self.kwargs['id']).update(
                date=request.data['date'])
        if 'product' in request.data:
            Sale_Statistics.objects.filter(id=self.kwargs['id']).update(
                product=request.data['product'])
        if 'sales_number' in request.data:
            Sale_Statistics.objects.filter(id=self.kwargs['id']).update(
                sales_number=request.data['sales_number'])
        if 'revenue' in request.data:
            Sale_Statistics.objects.filter(id=self.kwargs['id']).update(
                revenue=request.data['revenue'])
        sale_statistics_data = Sale_Statistics.objects.get(
            id=self.kwargs['id'])
        data = {"date": sale_statistics_data.date, "product": sale_statistics_data.product,
                "sales_number": sale_statistics_data.sales_number, "revenue": sale_statistics_data.revenue}
        return Response({'status': 'success', 'message': "user data get successfully", 'data': data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        """ This function used for upadre sales data according to user. """
        try:
            Sale_Statistics.objects.filter(id=id).update(date=request.data['date'], product=request.data['product'],
                                                         sales_number=request.data['sales_number'], revenue=request.data['revenue'])
            sale_statistics_data = Sale_Statistics.objects.get(id=id)
            data = {'sale_statistics_data': sale_statistics_data.date, "product": sale_statistics_data.product,
                    "sales_number": sale_statistics_data.sales_number, "revenue": sale_statistics_data.revenue}
        except Exception:
            return Response({'status': 'fail', 'message': "Sales data id not available."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'success', 'message': "user data get successfully", 'data': data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """ This function used for delete sales data according to his id. """
        try:
            Sale_Statistics.objects.get(id=id).delete()
        except Exception:
            return Response({'status': 'fail', 'message': "This Sales data id not available."}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'success', 'message': "Sales data deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def StatisticsAverageData(request):
    """ This function used for get averge data accorning to user. """
    sale_statistics_data = Sale_Statistics.objects.filter(
        user=request.user).values()
    average_data = 0
    for statistics_data in sale_statistics_data:
        average_data = average_data + statistics_data['revenue']
    average_sales_for_current_user = average_data / len(sale_statistics_data)
    return Response({'status': 'success', 'message': "user data get successfully", 'average_sales_for_current_user': average_sales_for_current_user})
