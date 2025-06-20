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
        if pk:
            try:
                # Use select_related for ForeignKey
                pool = Pool.objects.select_related('vehicle').get(pk=pk)
                serializer = PoolSerializer(pool)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Pool.DoesNotExist:
                return Response({"status": "error", "message": "Pool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Use select_related for all pools
        pools = Pool.objects.select_related('vehicle').all()
        serializer = PoolSerializer(pools, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PoolSerializer(data=request.data)
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
            children_ids = request.data.get('children', [])
            driving_days = request.data.get('driving_days', [])
            children = Children.objects.filter(id__in=children_ids, user=user)

            pool_member, created = PoolMember.objects.get_or_create(
                pool=pool,
                user=user,
                driving_days=driving_days,
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
            pool_member = PoolMember.objects.get(pk=pk, user=request.user)
            pool_member.status ='Leave'
            pool_member.save()
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