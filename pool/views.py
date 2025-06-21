from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PoolSerializer,PoolJoinSerializer
from .models import Pool
from children.models import Children
from .models import Pool, PoolMember
class PoolView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        user = request.user
        if pk:
            try:
                # Use select_related for ForeignKey
                pool = Pool.objects.select_related('vehicle').get(pk=pk)
                serializer = PoolSerializer(pool)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Pool.DoesNotExist:
                return Response({"status": "error", "message": "Pool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Use select_related for all pools
        pools = Pool.objects.select_related('vehicle').filter(user=user)
        serializer = PoolSerializer(pools, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user  # Authenticated user object
        data = request.data.copy()  # Create a mutable copy of request.data
        data['user'] = user.id  # Assign the user ID (primary key) instead of the object
        serializer = PoolSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"status": "error", "message": "pool ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pool = Pool.objects.get(pk=pk)
        except Pool.DoesNotExist:
            return Response({"status": "error", "message": "pool not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PoolSerializer(pool, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            children = Pool.objects.get(pk=pk)
            children.delete()
            return Response({"status": "success", "message": "pool deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Pool.DoesNotExist:
            return Response({"status": "error", "message": "pool not found"}, status=status.HTTP_404_NOT_FOUND)
        



class PoolJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        """
        Join a pool
        """
        try:
            pool = Pool.objects.get(pk=pk)
            user = request.user
            children_ids = request.data.get('children', '')
            pickup_location = request.data.get('pickup_location', '')
            if pickup_location =='' or children_ids =='':
                return Response({"status": "error", "message": "children and location both field are required."}, status=status.HTTP_404_NOT_FOUND)
            children = Children.objects.filter(id__in=children_ids, user=user)
            try:
                check_pool = PoolMember.objects.get(pool=pool,user=user)
                if check_pool:
                    return Response({"status": "error", "message": "You have already join this pool"}, status=status.HTTP_404_NOT_FOUND)
            except:
                pool_member, created = PoolMember.objects.get_or_create(
                    pool=pool,
                    user=user,
                    pickup_location=pickup_location,
                    defaults={
                        'role': 'Member',
                        'status': 'Pending',
                    }
                )
                pool_member.children.set(children)
                pool_member.save()

                serializer = PoolJoinSerializer(pool_member)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Pool.DoesNotExist:
            return Response({"status": "error", "message": "Pool not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        """
        Get all pool members
        """
        try:
            pool = Pool.objects.get(pk=pk)
            members = pool.members.select_related('user').prefetch_related('children')
            serializer = PoolJoinSerializer(members, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Pool.DoesNotExist:
            return Response({"status": "error", "message": "Pool not found"}, status=status.HTTP_404_NOT_FOUND)

class PoolMemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Get a single pool member
        """
        try:
            pool_member = PoolMember.objects.select_related('user', 'pool').prefetch_related('children').get(pk=pk)
            serializer = PoolJoinSerializer(pool_member)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except PoolMember.DoesNotExist:
            return Response({"status": "error", "message": "Pool member not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        """
        Leave a pool
        """

        try:
            pool_member = PoolMember.objects.get(pool=pk, user=request.user).delete()
            return Response({"status": "success", "message": "Left the pool successfully"}, status=status.HTTP_204_NO_CONTENT)
        except PoolMember.DoesNotExist:
            return Response({"status": "error", "message": "Pool member not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

class BecomeDriverView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        """
        Become a driver in a pool
        """
        try:
            pool_member = PoolMember.objects.get(user=request.user)
            pool_member.role = 'Driver'
            pool_member.status = 'Approved'
            pool_member.save()
            return Response({"status": "success", "message": "You are now a driver for this pool"}, status=status.HTTP_200_OK)
        except PoolMember.DoesNotExist:
            return Response({"status": "error", "message": "Pool member not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)