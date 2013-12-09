import gettext
import googkit.lib.path


_ = gettext.translation(
    domain='googkit',
    localedir=googkit.lib.path.locale(),
    fallback=True).gettext
