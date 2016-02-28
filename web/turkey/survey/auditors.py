# register and build your auditor models here
from django.db import models
from .models import Auditor, AuditorDataModel
from django.utils.translation import ugettext_lazy as _

# Some inspiration: http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf
NAME_TO_AUDITOR = {
    'total_task_time': 'AuditorTotalTaskTime',
    'before_typing_delay': 'AuditorBeforeTypingDelay',
    'on_focus_time': '',
    'within_typing_delay': '',
    'recorded_time_disparity': '',
    'clicks_total': '',
    'clicks_specific': '',  # specific positions and (hopefully) elements clicked inside of
    'keypresses_total': '',
    # There are fields total tabs, total
    # backspaces, and count of unique characters
    # in the paper above, but these can
    # be extracted from aggregations on
    # keypresses_specific
    'keypresses_specific': '',
    'mouse_movement_total': '',
    'mouse_movement_specific': '',
    'pastes_total': '',
    'pastes_specific': '',
    'scrolled_vertical_pixels_total': '',  # total of position changes via scroll (absolute values)
    'scrolled_horizontal_pixels_total': '',
    'scrolled_vertical_pixels_specific': '',  # breakdown of specific_scrolled_pixels in time intervals
    'scrolled_horizontal_pixels_specific': '',
    'focus_changes': '',  # timestamped
}


class AuditorTotalTaskTimeData(AuditorDataModel):
    general_model = models.ForeignKey('AuditorTotalTaskTime')
    milliseconds = models.IntegerField(
        verbose_name=_('total task time'),
        help_text=_('total time in milliseconds that the user'
                    'spent on the task page')
    )


class AuditorTotalTaskTime(Auditor):
    template_code = 'survey/auditors/total_task_time.html'
    data_model = AuditorTotalTaskTimeData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Total Task Time')
        verbose_name_plural = _('Auditors: Total Task Time')


class AuditorBeforeTypingDelayData(AuditorDataModel):
    general_model = models.ForeignKey('AuditorBeforeTypingDelay')
    milliseconds = models.IntegerField(
        verbose_name=_('total task time'),
        help_text=_('total time in milliseconds that the user'
                    'took before typing'),
        null=True  # can be null because user might never type
    )


class AuditorBeforeTypingDelay(Auditor):
    template_code = 'survey/auditors/before_typing_delay.html'
    data_model = AuditorBeforeTypingDelayData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Before Typing Delay')
        verbose_name_plural = _('Auditors: Before Typing Delay')
