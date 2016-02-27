# register and build your step models here
from .models import Auditor

# Some inspiration: http://jeffrz.com/wp-content/uploads/2010/08/fp359-rzeszotarski.pdf
NAME_TO_AUDITOR = {
    'total_task_time': '',
    'before_typing_delay': '',
    'on_focus_time': '',
    'within_typing_delay': '',
    'recorded_time_disparity': '',
    'clicks_total': '',
    'clicks_specific': '',      # specific positions and (hopefully) elements clicked inside of
    'keypresses_total': '',
    'keypresses_specific': '',  # There are fields total tabs, total
                                # backspaces, and count of unique characters
                                # in the paper above, but these can
                                # be extracted from aggregations on
                                # keypresses_specific
    'mouse_movement_total': '',
    'mouse_movement_specific': '',
    'pastes_total': '',
    'pastes_specific': '',
    'scrolled_vertical_pixels_total': '', # total of position changes via scroll (absolute values)
    'scrolled_horizontal_pixels_total': '',
    'scrolled_vertical_pixels_specific': '',        # breakdown of specific_scrolled_pixels in time intervals
    'scrolled_horizontal_pixels_specific': '',
    'focus_changes': '',        # timestamped
}
