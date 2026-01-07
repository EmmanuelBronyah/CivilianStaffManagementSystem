from rest_framework import generics
import logging
from . import serializers
from . import models
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from . import utils

logger = logging.getLogger(__name__)

# TODO: Ensure all perform update functions include the updated by key


# * TERMINATION OF APPOINTMENT
class CreateTerminationOfAppointmentAPIView(generics.CreateAPIView):
    serializer_class = serializers.TerminationOfAppointmentSerializer
    queryset = models.TerminationOfAppointment.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_create(self, serializer):
        termination_of_appointment = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(
            f"Termination Of Appointment({termination_of_appointment}) created."
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Termination Of Appointment: '{termination_of_appointment.employee.service_id} — {termination_of_appointment.cause}'",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Termination Of Appointment: '{termination_of_appointment.employee.service_id} — {termination_of_appointment.cause}') created."
        )


class EditTerminationOfAppointmentAPIView(generics.UpdateAPIView):
    queryset = models.TerminationOfAppointment.objects.all()
    serializer_class = serializers.TerminationOfAppointmentSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_update(self, serializer):
        previous_termination_of_appointment = self.get_object()
        termination_of_appointment_update = serializer.save()
        logger.debug(
            f"Termination Of Appointment({previous_termination_of_appointment}) updated."
        )

        changes = utils.termination_of_appointment_changes(
            previous_termination_of_appointment, termination_of_appointment_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Termination Of Appointment '{previous_termination_of_appointment.employee.service_id} — {previous_termination_of_appointment.cause}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Termination Of Appointment '{previous_termination_of_appointment.employee.service_id} — {previous_termination_of_appointment.cause}': {changes}) created."
            )


class ListEmployeeTerminationOfAppointmentAPIView(generics.ListAPIView):
    queryset = models.TerminationOfAppointment.objects.all()
    serializer_class = serializers.TerminationOfAppointmentSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        termination_of_appointment = employee.termination_of_appointment.all()
        return termination_of_appointment


class RetrieveTerminationOfAppointmentAPIView(generics.RetrieveAPIView):
    queryset = models.TerminationOfAppointment.objects.all()
    serializer_class = serializers.TerminationOfAppointmentSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteTerminationOfAppointmentAPIView(generics.DestroyAPIView):
    queryset = models.TerminationOfAppointment.objects.all()
    serializer_class = serializers.TerminationOfAppointmentSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Termination Of Appointment({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Termination Of Appointment '{instance.employee.service_id} — {instance.cause}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Termination Of Appointment '{instance.employee.service_id} — {instance.cause}' was deleted by {self.request.user}) created."
        )


# * CAUSES OF TERMINATION
class CreateCausesOfTerminationAPIView(generics.CreateAPIView):
    serializer_class = serializers.CausesOfTerminationSerializer
    queryset = models.CausesOfTermination.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        causes_of_termination = serializer.save()
        logger.debug(f"Causes Of Termination({causes_of_termination}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Causes Of Termination: '{causes_of_termination.termination_cause}'",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Causes Of Termination: '{causes_of_termination.termination_cause}') created."
        )


class EditCausesOfTerminationAPIView(generics.UpdateAPIView):
    queryset = models.CausesOfTermination.objects.all()
    serializer_class = serializers.CausesOfTerminationSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        previous_causes_of_termination = self.get_object()
        causes_of_termination_update = serializer.save()
        logger.debug(
            f"Causes Of Termination({previous_causes_of_termination}) updated."
        )

        changes = utils.causes_of_termination_changes(
            previous_causes_of_termination, causes_of_termination_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Causes Of Termination '{previous_causes_of_termination.termination_cause}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Causes Of Termination '{previous_causes_of_termination.termination_cause}': {changes}) created."
            )


class ListCausesOfTerminationAPIView(generics.ListAPIView):
    queryset = models.CausesOfTermination.objects.all()
    serializer_class = serializers.CausesOfTerminationSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class RetrieveCausesOfTerminationAPIView(generics.RetrieveAPIView):
    queryset = models.CausesOfTermination.objects.all()
    serializer_class = serializers.CausesOfTerminationSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteCausesOfTerminationAPIView(generics.DestroyAPIView):
    queryset = models.CausesOfTermination.objects.all()
    serializer_class = serializers.CausesOfTerminationSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Causes Of Termination({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Causes Of Termination '{instance.termination_cause}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Causes Of Termination '{instance.termination_cause}' was deleted by {self.request.user}) created."
        )


# * TERMINATION STATUS
class CreateTerminationStatusAPIView(generics.CreateAPIView):
    serializer_class = serializers.TerminationStatusSerializer
    queryset = models.TerminationStatus.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        termination_status = serializer.save()
        logger.debug(f"Termination Status({termination_status}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Termination Status: '{termination_status.termination_status}'",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Termination Status: '{termination_status.termination_status}') created."
        )


class EditTerminationStatusAPIView(generics.UpdateAPIView):
    queryset = models.TerminationStatus.objects.all()
    serializer_class = serializers.TerminationStatusSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        previous_termination_status = self.get_object()
        termination_status_update = serializer.save()
        logger.debug(f"Termination Status({previous_termination_status}) updated.")

        changes = utils.termination_status_changes(
            previous_termination_status, termination_status_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Termination Status '{previous_termination_status.termination_status}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Termination Status '{previous_termination_status.termination_status}': {changes}) created."
            )


class ListTerminationStatusAPIView(generics.ListAPIView):
    queryset = models.TerminationStatus.objects.all()
    serializer_class = serializers.TerminationStatusSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class RetrieveTerminationStatusAPIView(generics.RetrieveAPIView):
    queryset = models.TerminationStatus.objects.all()
    serializer_class = serializers.TerminationStatusSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteTerminationStatusAPIView(generics.DestroyAPIView):
    queryset = models.TerminationStatus.objects.all()
    serializer_class = serializers.TerminationStatusSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Termination(Status {instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Termination Status '{instance.termination_status}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Termination Status '{instance.termination_status}' was deleted by {self.request.user}) created."
        )
