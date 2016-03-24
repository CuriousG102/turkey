from django.db import models
from django.utils.translation import ugettext_lazy as _

# register and build your auditor models here
from .models import Auditor, AuditorData


# Some inspiration: http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf
NAME_TO_AUDITOR = {
    'before_typing_delay': 'AuditorBeforeTypingDelay',
    'clicks_total': 'AuditorClicksTotal',
    'clicks_specific': 'AuditorClicksSpecific',
    'focus_changes': 'AuditorFocusChanges',  # timestamped
    # There are fields total tabs, total
    # backspaces, and count of unique characters
    # in the paper above, but these can
    # be extracted from aggregations on
    # keypresses_specific
    'keypresses_total': 'AuditorKeypressesTotal',
    'keypresses_specific': 'AuditorKeypressesSpecific',
    'mouse_movement_total': 'AuditorMouseMovementTotal',
    'mouse_movement_specific': 'AuditorMouseMovementSpecific',
    'on_focus_time': 'AuditorOnFocusTime',
    'pastes_total': 'AuditorPastesTotal',
    'pastes_specific': 'AuditorPastesSpecific',
    'recorded_time_disparity': 'AuditorRecordedTimeDisparity',
    'scrolled_pixels_total': 'AuditorScrolledPixelsTotal', 
    'scrolled_pixels_specific': 'AuditorScrolledPixelsSpecific',
    'within_typing_delay': 'AuditorWithinTypingDelay',
    'total_task_time': 'AuditorTotalTaskTime',
}

#before_typing_delay
class AuditorBeforeTypingDelayData(AuditorData):
    general_model = models.ForeignKey('AuditorBeforeTypingDelay')
    milliseconds = models.IntegerField(
        verbose_name=_('total task time'),
        help_text=_('total time in milliseconds that the user'
                    'took before typing'),
        null=True  # can be null because user might never type
    )

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorBeforeTypingDelay(Auditor):
    script_location = 'survey/js/auditors/before_typing_delay.js'
    data_model = AuditorBeforeTypingDelayData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Before Typing Delay')
        verbose_name_plural = _('Auditors: Before Typing Delay')


#clicks_total
class AuditorClicksTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorClicksTotal')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorClicksTotal(Auditor):
    script_location = 'survey/js/auditors/clicks_total.js'
    data_model = AuditorClicksTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Clicks Total')
        verbose_name_plural = _('Auditors: Clicks Total')


#clicks_specific
class AuditorClicksSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorClicksSpecific')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorClicksSpecific(Auditor):
    script_location = 'survey/js/auditors/clicks_specific.js'
    data_model = AuditorClicksSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Clicks Specific')
        verbose_name_plural = _('Auditors: Clicks Specific')


#focus_changes
class AuditorFocusChangesData(AuditorData):
    general_model = models.ForeignKey('AuditorFocusChanges')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorFocusChanges(Auditor):
    script_location = 'survey/js/auditors/focus_changes.js'
    data_model = AuditorFocusChangesData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Focus Changes')
        verbose_name_plural = _('Auditors: Focus Changes')


#keypresses_total
class AuditorKeypressesTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorKeypressesTotal')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorKeypressesTotal(Auditor):
    script_location = 'survey/js/auditors/keypresses_total.js'
    data_model = AuditorKeypressesTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Keypresses Total')
        verbose_name_plural = _('Auditors: Keypresses Total')


#keypresses_specific
class AuditorKeypressesSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorKeypressesSpecific')

    class Meta(AuditorData.Meta):
        abstract = False

class Auditor_(Auditor):
    script_location = 'survey/js/auditors/keypresses_specific.js'
    data_model = AuditorKeypressesSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Keypresses Specific')
        verbose_name_plural = _('Auditors: Keypresses Specific')


#mouse_movement_total
class AuditorMouseMovementTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorMouseMovementTotal')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorMouseMovementTotal(Auditor):
    script_location = 'survey/js/auditors/mouse_movement_total.js'
    data_model = AuditorMouseMovementTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Mouse Movement Total')
        verbose_name_plural = _('Auditors: Mouse Movement Total')


#mouse_movement_specific
class AuditorMouseMovementSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorMouseMovementSpecific')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorMouseMovementSpecific(Auditor):
    script_location = 'survey/js/auditors/mouse_movement_specific.js'
    data_model = AuditorMouseMovementSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Mouse Movement Specific')
        verbose_name_plural = _('Auditors: Mouse Movement Specific')


#on_focus_time
class AuditorOnFocusTimeData(AuditorData):
    general_model = models.ForeignKey('AuditorOnFocusTime')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorOnFocusTime(Auditor):
    script_location = 'survey/js/auditors/on_focus_time.js'
    data_model = AuditorOnFocusTimeData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: On Focus Time')
        verbose_name_plural = _('Auditors: On Focus Time')


#pastes_total
class AuditorPastesTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorPastesTotal')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorPastesTotal(Auditor):
    script_location = 'survey/js/auditors/pastes_total.js'
    data_model = AuditorPastesTotalData

    class Meta(AuditorData.Meta):
        abstract = False
        verbose_name = _('Auditor: Pastes Total')
        verbose_name_plural = _('Auditors: Pastes Total')


#pastes_specific
class AuditorPastesSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorPastesSpecific')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorPastesSpecific(Auditor):
    script_location = 'survey/js/auditors/pastes_specific.js'
    data_model = AuditorPastesSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Pastes Specific')
        verbose_name_plural = _('Auditors: Pastes Specific')


#recorded_time_disparity
class AuditorRecordedTimeDisparityData(AuditorData):
    general_model = models.ForeignKey('AuditorRecordedTimeDisparity')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorRecordedTimeDisparity(Auditor):
    script_location = 'survey/js/auditors/recorded_time_disparity.js'
    data_model = AuditorRecordedTimeDisparityData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Recorded Time Disparity')
        verbose_name_plural = _('Auditors: Recorded Time Disparity')


#scrolled_pixels_total
class AuditorScrolledPixelsTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorScrolledPixelsTotal')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorScrolledPixelsTotal(Auditor):
    script_location = 'survey/js/auditors/scrolled_pixels_total.js'
    data_model = AuditorScrolledPixelsTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Scrolled Pixels Total')
        verbose_name_plural = _('Auditors: Scrolled Pixels Total')


#scrolled_pixels_specific
class AuditorScrolledPixelsSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorScrolledPixelsSpecific')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorScrolledPixelsSpecific(Auditor):
    script_location = 'survey/js/auditors/scrolled_pixels_specific.js'
    data_model = AuditorScrolledPixelsSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Scrolled Pixels Specific')
        verbose_name_plural = _('Auditors: Scrolled Pixels Specific')


#within_typing_delay
class AuditorWithinTypingDelayData(AuditorData):
    general_model = models.ForeignKey('AuditorWithinTypingDelay')

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorWithinTypingDelay(Auditor):
    script_location = 'survey/js/auditors/within_typing_delay.js'
    data_model = AuditorWithinTypingDelayData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Within Typing Delay')
        verbose_name_plural = _('Auditors: Within Typing Delay')


#total_task_time
class AuditorTotalTaskTimeData(AuditorData):
    general_model = models.ForeignKey('AuditorTotalTaskTime')
    milliseconds = models.IntegerField(
        verbose_name=_('total task time'),
        help_text=_('total time in milliseconds that the user'
                    'spent on the task page')
    )

    class Meta(AuditorData.Meta):
        abstract = False

class AuditorTotalTaskTime(Auditor):
    script_location = 'survey/js/auditors/total_task_time.js'
    data_model = AuditorTotalTaskTimeData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Auditor: Total Task Time')
        verbose_name_plural = _('Auditors: Total Task Time')
