from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    model = Post

    def report_count(self, obj):
        return Report.objects.filter(post=obj).count()

    report_count.short_description = "Report Count"

    list_display = ['id', 'title', 'content', 'date_posted', 'author', 'attachment', 'report_count']


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ['post', 'user', 'type']


class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = ['post', 'reason', 'date_reported',
                    'investigated', 'removed']


admin.site.register(Report, ReportAdmin)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
admin.site.register(Vote, VoteAdmin)


class PostTagAdmin(admin.ModelAdmin):
    model = PostTag
    list_display = ['id', 'post', 'topic', ]


admin.site.register(PostTag, PostTagAdmin)
