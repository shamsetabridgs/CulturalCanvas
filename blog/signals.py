from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from .models import Blog,Comment,Reply
from user_profile.models import Follow,User
from notification.models import Notification
from .views import add_reply


@receiver(post_save, sender = Blog)
def send_notification_to_followers_when_blog_created(instance, created, *args, **kwargs):
    if created:
        followers = instance.user.followers.all()

        for data in followers:
            follower = data.followed_by

            if not data.muted:
                Notification.objects.create(
                    content_object = instance,
                    user = follower,
                    text = f"{instance.user.username} posted a new blog",
                    notification_types= "Blog"
                )



@receiver(post_save, sender = Follow)
def send_notification_to_user_when_someone_followed(instance, created, *args, **kwargs):
    if created:
        followed = instance.followed

        if not instance.muted:
                Notification.objects.create(
                    content_object = instance,
                    user = followed,
                    text = f"{instance.followed_by.username} started following you",
                    notification_types= "Follow"
                )


@receiver(m2m_changed, sender = Blog.likes.through)
def send_notification_when_someone_likes_blog(instance, pk_set, action, *args, **kwargs):
     pk = list(pk_set)[0]
     user = User.objects.get(pk=pk)

     if action == "post_add":
          Notification.objects.create(
               content_object = instance,
               user = instance.user,
               text = f"{user.username} liked your blog",
               notification_types = "Like"
          )


@receiver(post_save, sender=Comment)  # Add this line for the comment signal
def send_notification_when_commented(instance, created, *args, **kwargs):
    if created:
        blog_owner = instance.blog.user

        if blog_owner != instance.user:  # Avoid sending notification if the commenter is also the blog owner
            Notification.objects.create(
                content_object=instance,
                user=blog_owner,
                text=f"{instance.user.username} commented on your blog",
                notification_types="Comment"
            )

@receiver(post_save, sender=Reply)  # Add this line for the reply signal
def send_notification_when_replied(instance, created, *args, **kwargs):
    if created:
        comment_owner = instance.comment.user

        if comment_owner != instance.user:  # Avoid sending notification if the replier is also the comment owner
            Notification.objects.create(
                content_object=instance,
                user=comment_owner,
                text=f"{instance.user.username} replied to your comment",
                notification_types="Reply"
            )
"""@receiver(post_save, sender=Reply)
def send_notification_when_replied(instance, created, *args, **kwargs):
     if created:
          comment_owner = instance.comment.user

          if comment_owner != instance.user:
               Notification.objects.create(
                    content_object = instance,
                    user = comment_owner,
                    text = f"{instance.user.username} replied on your comment",
                    notification_types = "Reply"
               )

@receiver(post_save, sender = Comment)
def send_notification_when_someone_commented(instance, created, *args, **kwargs):
     if created:
           if instance.user.id != instance.blog.user.id: #send notification to author 
               noti_to_author = Notification.objects.create(
                    duplicate_value="author",
                    blog=instance.blog,
                    blogcomment=instance,
                    sender=instance.user,
                    receiver=instance.blog.user,
                    text_preview=f"Recived new comment from {instance.user}",
                    notification_types = "Comment"
                    )
           if instance.parent and instance.parent.user.id != instance.user.id:  
               noti_to_commenter = Notification.objects.create(
                    duplicate_value="commenter",
                    blog=instance.blog,
                    blogcomment=instance,
                    sender=instance.user,
                    receiver=instance.parent.user,
                    text_preview=f"{instance.user} replied on your comment",
                    notification_types = "Reply"
                ) 
                        
        #Notify to parent commenter. This will prevent to create notification if parent owner add reply on his own parent commnet.  
          
          
          
              

           if action == "post_add":
               Notification.objects.create(
               content_object = instance,
               user = instance.user,
               text = f"{user.username} commented your blog",
               notification_types = "Comment"
          )"""