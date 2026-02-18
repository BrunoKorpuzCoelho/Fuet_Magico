from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import AuditLog, ActivityLog, ActivityWorkflow
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=instance if not created else None,
        action=action,
        model_name=sender.__name__,
        object_id=str(instance.pk),
        details={
            'username': instance.username,
            'email': instance.email,
            'role': instance.role,
        }
    )


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=None,
        action='DELETE',
        model_name=sender.__name__,
        object_id=str(instance.pk),
        details={
            'username': instance.username,
            'email': instance.email,
        }
    )


# ============================================================================
# ACTIVITY WORKFLOW AUTOMATION
# ============================================================================

@receiver(post_save, sender=ActivityLog)
def trigger_activity_workflows(sender, instance, created, **kwargs):
    """
    Triggers workflows when an ActivityLog is marked as done.

    Na nova arquitectura, ActivityLog regista o resultado de cada passo
    de uma cadeia (ActivityChainStep) aplicada a um registo (ex: Lead).

    Chaining modes:
    - TRIGGER: Creates next activity automatically
    - SUGGEST: Prepares suggestion (shown in modal - handled in views)

    Args:
        sender: ActivityLog model class
        instance: ActivityLog instance
        created: Boolean indicating if this is a new record
        **kwargs: Additional signal arguments
    """
    # Skip if activity log is not marked done
    if not instance.is_done:
        return

    # Skip if created already done (data import scenario)
    if created and instance.is_done:
        logger.debug(
            f"Skipping workflow trigger for ActivityLog {instance.id} "
            f"(created already done - likely data import)"
        )
        return

    # Skip if no result is set
    if not instance.result:
        logger.warning(
            f"ActivityLog {instance.id} marked as done but has no result. "
            f"Skipping workflow execution."
        )
        return

    # Resolve activity_type from step → blueprint
    try:
        activity_type = instance.step.activity.activity_type
    except Exception:
        logger.warning(f"ActivityLog {instance.id}: could not resolve activity_type. Skipping.")
        return

    # Resolve content_type from chain_instance
    content_type = None
    if instance.chain_instance:
        content_type = instance.chain_instance.content_type

    logger.info(
        f"ActivityLog done: {activity_type.name if hasattr(activity_type, 'name') else activity_type} "
        f"(result: {instance.result}, id: {instance.id})"
    )

    # Find applicable workflows based on activity_type, result and content_type
    workflow_qs = ActivityWorkflow.objects.filter(
        trigger_activity_type=activity_type,
        is_active=True,
    ).select_related('next_activity_template').order_by('sequence')

    if content_type:
        workflow_qs = workflow_qs.filter(model=content_type)

    # Filter by trigger_result (None = any result)
    matching_workflows = [
        wf for wf in workflow_qs
        if not wf.trigger_result or wf.trigger_result == instance.result
    ]
    
    if not matching_workflows:
        logger.debug(
            f"No matching workflows found for {activity_type} "
            f"with result {instance.result}"
        )
        return

    logger.info(
        f"Found {len(matching_workflows)} matching workflow(s) "
        f"for ActivityLog {instance.id}"
    )

    # Execute each matching workflow
    executed_count = 0
    suggested_count = 0

    for workflow in matching_workflows:
        try:
            # Check chaining mode
            if workflow.chaining_mode == 'SUGGEST':
                logger.info(
                    f"Workflow '{workflow.name}' (id: {workflow.id}) "
                    f"suggests creating: {workflow.next_activity_template.name}"
                )
                suggested_count += 1
                continue

            # TRIGGER mode - execute automatically
            with transaction.atomic():
                next_activity = workflow.execute(
                    activity_log=instance,
                    user=instance.assigned_to or instance.logged_by
                )

                if next_activity:
                    logger.info(
                        f"✓ Workflow '{workflow.name}' (id: {workflow.id}) "
                        f"created blueprint: {next_activity.activity_type} "
                        f"'{next_activity}' (id: {next_activity.id})"
                    )
                    executed_count += 1
                else:
                    logger.warning(
                        f"Workflow '{workflow.name}' (id: {workflow.id}) "
                        f"executed but did not create activity"
                    )

        except Exception as e:
            logger.error(
                f"✗ Error executing workflow '{workflow.name}' "
                f"(id: {workflow.id}): {e}",
                exc_info=True
            )

    # Summary log
    if executed_count > 0 or suggested_count > 0:
        logger.info(
            f"Workflow execution complete for ActivityLog {instance.id}: "
            f"{executed_count} created, {suggested_count} suggested"
        )
