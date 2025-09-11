import os
import shutil

from django.contrib.contenttypes.models import ContentType

from common.models import Attachment, attachment_upload_to


def move_attachment_file(attachment):
    # Get the current file path
    old_path = attachment.file.path
    # Generate the new path based on the model
    new_path = attachment_upload_to(attachment, os.path.basename(old_path))

    # Ensure the directory exists
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    # Move the file
    shutil.move(old_path, new_path)

    # Update the file field and save the model
    attachment.file.name = new_path
    attachment.save()


def attach_file_to_object(instance, uploaded_file):
    """
    A utility function to attach a file to a model instance.

    Args:
        instance: The model instance to which the file should be attached.
        uploaded_file: The file object to attach.

    Returns:
        Attachment instance.
    """
    # Get the content type for the model instance
    content_type = ContentType.objects.get_for_model(instance.__class__)

    # Create an attachment linked to the instance
    attachment = Attachment.objects.create(
        content_type=content_type,
        object_id=instance.id,
        file=uploaded_file
    )
    return attachment


def get_attachments_by_object(object_instance):
    """
    Get all attachment objects linked to a specific object instance.

    Args:
        object_instance: The instance of the model to get attachments for.

    Returns:
        Queryset of Attachment objects.
    """
    # Get the content type for the related object model
    content_type = ContentType.objects.get_for_model(object_instance.__class__)

    # Query the Attachment model using object_id and content_type
    attachments = Attachment.objects.filter(
        content_type=content_type,
        object_id=object_instance.id
    )

    return attachments
