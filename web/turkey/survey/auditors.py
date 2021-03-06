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
    'total_task_time': 'AuditorTotalTaskTime',
    'within_typing_delay': 'AuditorWithinTypingDelay',
    'url': 'AuditorURL',
    'user_agent': 'AuditorUserAgent'
}


# before_typing_delay
class AuditorBeforeTypingDelayData(AuditorData):
    general_model = models.ForeignKey('AuditorBeforeTypingDelay')
    milliseconds = models.IntegerField(
        verbose_name=_('before typing delay'),
        help_text=_('total time in milliseconds that the user took before typing'),
        null=True,  # can be null because user might never type
        blank=True
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorBeforeTypingDelay(Auditor):
    script_location = 'survey/js/auditors/before_typing_delay.js'
    data_model = AuditorBeforeTypingDelayData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Before Typing Delay Auditor')
        verbose_name_plural = _('Before Typing Delay Auditors')


# clicks_total
class AuditorClicksTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorClicksTotal')
    count = models.IntegerField(
        verbose_name=_('clicks total'),
        help_text=_('total number of times a user clicked')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorClicksTotal(Auditor):
    script_location = 'survey/js/auditors/clicks_total.js'
    data_model = AuditorClicksTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Clicks Total Auditor')
        verbose_name_plural = _('Clicks Total Auditors')


# clicks_specific
class AuditorClicksSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorClicksSpecific')
    dom_type = models.TextField(
        verbose_name=_('clicks specific type'),
        help_text=_('DOM type of element that was clicked')
    )
    dom_id = models.TextField(
        verbose_name=_('clicks specific id'),
        help_text=_('DOM ID of element that was clicked'),
        null=True,
        blank=True
    )
    dom_class = models.TextField(
        verbose_name=_('clicks specific id'),
        help_text=_('DOM class of element that was clicked'),
        null=True,
        blank=True
    )
    dom_name = models.TextField(
        verbose_name=_('clicks specific id'),
        help_text=_('DOM name of element that was clicked'),
        null=True,
        blank=True
    )
    time = models.IntegerField(
        verbose_name=('clicks specific timestamp'),
        help_text=_('timestamp of this click event')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorClicksSpecific(Auditor):
    script_location = 'survey/js/auditors/clicks_specific.js'
    data_model = AuditorClicksSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Clicks Specific Auditor')
        verbose_name_plural = _('Clicks Specific Auditors')


# focus_changes
class AuditorFocusChangesData(AuditorData):
    general_model = models.ForeignKey('AuditorFocusChanges')
    time = models.IntegerField(
        verbose_name=_('focus changes times'),
        help_text=_('timestamps of whenever the user switches out of focus')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorFocusChanges(Auditor):
    script_location = 'survey/js/auditors/focus_changes.js'
    data_model = AuditorFocusChangesData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Focus Changes Auditor')
        verbose_name_plural = _('Focus Changes Auditors')


# keypresses_total
class AuditorKeypressesTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorKeypressesTotal')
    count = models.IntegerField(
        verbose_name=_('keypresses total'),
        help_text=_('total number of times a user pressed a key')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorKeypressesTotal(Auditor):
    script_location = 'survey/js/auditors/keypresses_total.js'
    data_model = AuditorKeypressesTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Keypresses Total Auditor')
        verbose_name_plural = _('Keypresses Total Auditors')


# keypresses_specific
class AuditorKeypressesSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorKeypressesSpecific')
    key = models.TextField(
        verbose_name=_('keypresses specific'),
        help_text=_('specific keys pressed by the user')
    )
    time = models.IntegerField(
        verbose_name=('keypresses specific timestamp'),
        help_text=_('timestamp of this keypress event')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorKeypressesSpecific(Auditor):
    script_location = 'survey/js/auditors/keypresses_specific.js'
    data_model = AuditorKeypressesSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Keypresses Specific Auditor')
        verbose_name_plural = _('Keypresses Specific Auditors')


# mouse_movement_total
class AuditorMouseMovementTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorMouseMovementTotal')
    amount = models.IntegerField(
        verbose_name=_('mouse movement total'),
        help_text=_('total number of pixels traversed by the cursor due to user moving mouse')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorMouseMovementTotal(Auditor):
    script_location = 'survey/js/auditors/mouse_movement_total.js'
    data_model = AuditorMouseMovementTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Mouse Movement Total Auditor')
        verbose_name_plural = _('Mouse Movement Total Auditors')


# mouse_movement_specific
class AuditorMouseMovementSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorMouseMovementSpecific')
    x = models.IntegerField(
        verbose_name=_('mouse movement x coordinate'),
        help_text=_('ending x coordinate of mouse whenever user moves mouse')
    )
    y = models.IntegerField(
        verbose_name=_('mouse movement y coordinate'),
        help_text=_('ending y coordinate of mouse whenever user moves mouse')
    )
    time = models.IntegerField(
        verbose_name=('mouse movement timestamp'),
        help_text=_('timestamp of this mouse movement')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorMouseMovementSpecific(Auditor):
    script_location = 'survey/js/auditors/mouse_movement_specific.js'
    data_model = AuditorMouseMovementSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Mouse Movement Specific Auditor')
        verbose_name_plural = _('Mouse Movement Specific Auditors')


# on_focus_time
class AuditorOnFocusTimeData(AuditorData):
    general_model = models.ForeignKey('AuditorOnFocusTime')
    milliseconds = models.IntegerField(
        verbose_name=_('on focus time'),
        help_text=_('total time in milliseconds that the user spent on focus'),
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorOnFocusTime(Auditor):
    script_location = 'survey/js/auditors/on_focus_time.js'
    data_model = AuditorOnFocusTimeData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('On Focus Time Auditor')
        verbose_name_plural = _('On Focus Time Auditors')


# pastes_total
class AuditorPastesTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorPastesTotal')
    count = models.IntegerField(
        verbose_name=_('pastes total'),
        help_text=_('number of times a user pastes something (^V)')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorPastesTotal(Auditor):
    script_location = 'survey/js/auditors/pastes_total.js'
    data_model = AuditorPastesTotalData

    class Meta(AuditorData.Meta):
        abstract = False
        verbose_name = _('Pastes Total Auditor')
        verbose_name_plural = _('Pastes Total Auditors')


# pastes_specific
class AuditorPastesSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorPastesSpecific')
    data = models.TextField(
        verbose_name=_('pastes specific'),
        help_text=_('specific content pasted by the user')
    )
    time = models.IntegerField(
        verbose_name=('pastes specific timestamp'),
        help_text=_('timestamp of this paste event')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorPastesSpecific(Auditor):
    script_location = 'survey/js/auditors/pastes_specific.js'
    data_model = AuditorPastesSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Pastes Specific Auditor')
        verbose_name_plural = _('Pastes Specific Auditors')


# recorded_time_disparity
class AuditorRecordedTimeDisparityData(AuditorData):
    general_model = models.ForeignKey('AuditorRecordedTimeDisparity')
    milliseconds = models.IntegerField(
        verbose_name=_('recorded time disparity'),
        help_text=_('total time in milliseconds that the user spent off focus'),
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorRecordedTimeDisparity(Auditor):
    script_location = 'survey/js/auditors/recorded_time_disparity.js'
    data_model = AuditorRecordedTimeDisparityData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Recorded Time Disparity Auditor')
        verbose_name_plural = _('Recorded Time Disparity Auditors')


# scrolled_pixels_total
class AuditorScrolledPixelsTotalData(AuditorData):
    general_model = models.ForeignKey('AuditorScrolledPixelsTotal')
    horizontal = models.IntegerField(
        verbose_name=_('scrolled horizontal pixels total'),
        help_text=_('total number of pixels scrolled horizontally by the user')
    )
    vertical = models.IntegerField(
        verbose_name=_('scrolled vertical pixels total'),
        help_text=_('total number of pixels scrolled vertically by the user')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorScrolledPixelsTotal(Auditor):
    script_location = 'survey/js/auditors/scrolled_pixels_total.js'
    data_model = AuditorScrolledPixelsTotalData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Scrolled Pixels Total Auditor')
        verbose_name_plural = _('Scrolled Pixels Total Auditors')


# scrolled_pixels_specific
class AuditorScrolledPixelsSpecificData(AuditorData):
    general_model = models.ForeignKey('AuditorScrolledPixelsSpecific')
    horizontal_position = models.IntegerField(
        verbose_name=_('horizontal scrolled pixels position'),
        help_text=_('horizontal position on page after scrolling')
    )
    horizontal_change = models.IntegerField(
        verbose_name=_('horizontal scrolled pixels change'),
        help_text=_('horizontal change in position on page after scrolling')
    )
    vertical_position = models.IntegerField(
        verbose_name=_('vertical scrolled pixels position'),
        help_text=_('vertical position on page after scrolling')
    )
    vertical_change = models.IntegerField(
        verbose_name=_('vertical scrolled pixels change'),
        help_text=_('vertical change in position on page after scrolling')
    )
    time = models.IntegerField(
        verbose_name=('scrolled pixels specific timestamp'),
        help_text=_('timestamp of this scroll event')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorScrolledPixelsSpecific(Auditor):
    script_location = 'survey/js/auditors/scrolled_pixels_specific.js'
    data_model = AuditorScrolledPixelsSpecificData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Scrolled Pixels Specific Auditor')
        verbose_name_plural = _('Scrolled Pixels Specific Auditors')


# total_task_time
class AuditorTotalTaskTimeData(AuditorData):
    general_model = models.ForeignKey('AuditorTotalTaskTime')
    milliseconds = models.IntegerField(
        verbose_name=_('total task time'),
        help_text=_('total time in milliseconds that the user spent on the task page')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorTotalTaskTime(Auditor):
    script_location = 'survey/js/auditors/total_task_time.js'
    data_model = AuditorTotalTaskTimeData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Total Task Time Auditor')
        verbose_name_plural = _('Total Task Time Auditors')


# user_agent
class AuditorUserAgentData(AuditorData):
    general_model = models.ForeignKey('AuditorUserAgent')
    user_agent = models.TextField(
        verbose_name=_('User Agent'),
        help_text=_('User Agent of the browser being used')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorUserAgent(Auditor):
    script_location = 'survey/js/auditors/user_agent.js'
    data_model = AuditorUserAgentData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('User Agent Auditor')
        verbose_name_plural = _('User Agent Auditors')


# within_typing_delay
class AuditorWithinTypingDelayData(AuditorData):
    general_model = models.ForeignKey('AuditorWithinTypingDelay')
    within_delay = models.TextField(
        verbose_name=_('within typing delay'),
        help_text=_('whether the user typed within the delay period'),
        null=True,
        blank=True
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorWithinTypingDelay(Auditor):
    script_location = 'survey/js/auditors/within_typing_delay.js'
    data_model = AuditorWithinTypingDelayData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('Within Typing Delay Auditor')
        verbose_name_plural = _('Within Typing Delay Auditors')


class AuditorURLData(AuditorData):
    general_model = models.ForeignKey('AuditorURL')
    url = models.TextField(
        verbose_name=_('URL'),
        help_text=_('URL of the current task')
    )

    class Meta(AuditorData.Meta):
        abstract = False


class AuditorURL(Auditor):
    script_location = 'survey/js/auditors/url.js'
    data_model = AuditorURLData

    class Meta(Auditor.Meta):
        abstract = False
        verbose_name = _('URL Auditor')
        verbose_name_plural = _('URL Auditors')
