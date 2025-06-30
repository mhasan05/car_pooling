from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PoolSerializer,PoolJoinSerializer
from .models import Pool
from children.models import Children
from .models import Pool, PoolMember
from accounts.models import UserPickupLocation
from children.serializers import ChildrenSerializer
from accounts.serializers import pickupLocationSerializer


class PoolView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        user = request.user
        if pk:
            try:
                # Use select_related for ForeignKey
                pool = Pool.objects.select_related('vehicle').get(pk=pk,user=user)
                serializer = PoolSerializer(pool)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Pool.DoesNotExist:
                return Response({"status": "error", "message": "Pool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Use select_related for all pools
        pools = Pool.objects.select_related('vehicle').exclude(user=user)
        serializer = PoolSerializer(pools, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user  # Authenticated user object
        data = request.data.copy()  # Create a mutable copy of request.data
        data['user'] = user.id  # Assign the user ID (primary key) instead of the object
        serializer = PoolSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        user = request.user
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
        user = request.user
        try:
            pool = Pool.objects.get(pk=pk,user=user)
            pool.delete()
            return Response({"status": "success", "message": "pool deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Pool.DoesNotExist:
            return Response({"status": "error", "message": "pool not found"}, status=status.HTTP_404_NOT_FOUND)

class MyPoolView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        user = request.user
        if pk:
            try:
                # Use select_related for ForeignKey
                pool = Pool.objects.select_related('vehicle').get(pk=pk,user=user)
                serializer = PoolSerializer(pool)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Pool.DoesNotExist:
                return Response({"status": "error", "message": "Pool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Use select_related for all pools
        pools = Pool.objects.select_related('vehicle').filter(user=user)
        serializer = PoolSerializer(pools, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

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
            pickup_location_lat = request.data.get('pickup_location_lat', '')
            pickup_location_lng = request.data.get('pickup_location_lng', '')
            if pickup_location_lng =='' or children_ids =='':
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
                    pickup_location_lat=pickup_location_lat,
                    pickup_location_lng=pickup_location_lng,
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
            pool = Pool.objects.get(pk=pk,user=request.user)
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
        
    def post(self, request, pk=None):
        """
        Approve a pool member request
        """
        apply_status = request.data.get('apply_status',None)
        if not apply_status:
            return Response({"status": "error", "message": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pool_member = PoolMember.objects.get(pk=pk)
            if apply_status == 'Approve':
                pool_member.status = 'Approve'
                pool_member.save()
            elif apply_status == 'Decline':
                pool_member.status = 'Decline'
                pool_member.save()
            return Response({"status": "success", "message": "Successfully approved member"}, status=status.HTTP_200_OK)
        except PoolMember.DoesNotExist:
            return Response({"status": "error", "message": "Pool member not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        """
        Leave a pool
        """
        try:
            pool_member = PoolMember.objects.get(pk=pk, user=request.user).delete()
            return Response({"status": "success", "message": "Left the pool successfully"}, status=status.HTTP_204_NO_CONTENT)
        except PoolMember.DoesNotExist:
            return Response({"status": "error", "message": "Pool member not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

class BecomeDriverView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        """
        Become a driver in a pool
        """
        driving_days = request.data.get('driving_days', None)
        try:
            pool_member = PoolMember.objects.get(pk=pk,user=request.user)
            pool = pool_member.pool
            driver_check = PoolMember.objects.filter(pool=pool, role='Driver').exists()
            if pool_member.role == 'Driver':
                return Response({"status": "error", "message": "You are already a driver for this pool"}, status=status.HTTP_400_BAD_REQUEST)
            if driver_check:
                return Response({"status": "error", "message": "This pool already has a driver"}, status=status.HTTP_400_BAD_REQUEST)
            if pool_member.status == 'Approve':
                pool_member.role = 'Driver'
                pool_member.driving_days = driving_days
                pool_member.save()
                return Response({"status": "success", "message": "You are now a driver for this pool"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "You must be an approved member to become a driver"}, status=status.HTTP_400_BAD_REQUEST)
        except PoolMember.DoesNotExist:
            return Response({"status": "error", "message": "Pool member not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

class PendingMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Get pending pool members who joined pools created by the authenticated user
        """
        user = request.user
        # Filter PoolMember for pending status and pools created by the authenticated user
        pool_members = PoolMember.objects.filter(status='Pending', pool__user=user)
        
        if not pool_members.exists():
            return Response(
                {"status": "error", "message": "No pending pool members found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PoolJoinSerializer(pool_members, many=True)  # Serialize the filtered queryset
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class JoinedPoolsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get the list of pools the authenticated user has joined
        """
        user = request.user
        # Filter for pools the user has joined
        joined_pools = PoolMember.objects.filter(user=user, status='Approve').select_related('pool')

        if not joined_pools.exists():
            return Response(
                {"status": "error", "message": "You have not joined any pools"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the joined pools
        serializer = PoolJoinSerializer(joined_pools, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ChildrenAndLocationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        children = Children.objects.filter(user=user)
        children_serializer = ChildrenSerializer(children, many=True)
        location = UserPickupLocation.objects.filter(user=user)
        location_serializer = pickupLocationSerializer(location, many=True)
        return Response({
            "status": "success",
            "data": {
                "children": children_serializer.data,
                "location": location_serializer.data
            }
        }, status=status.HTTP_200_OK)
    

class DriverPoolsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter pools where the user is a driver
        driver_pools = Pool.objects.filter(members__user=request.user, members__role='Driver')

        # Serialize the filtered pools
        serializer = PoolSerializer(driver_pools, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
