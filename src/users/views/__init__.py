# authorization

from users.views.authorization.login import UserLoginView
from users.views.authorization.register import RegisterView
from users.views.authorization.logout import UserLogoutView

# other

from .dashboard import DashboardView
from .profile import ProfileDetailView, UserProfileUpdateView

# password

from users.views.password_reset.password_reset import UserPasswordResetView
from users.views.password_reset.password_reset_done import UserPasswordResetDoneView
from users.views.password_reset.password_reset_confirm import UserPasswordResetConfirmView
from users.views.password_reset.password_reset_complete import UserPasswordResetCompleteView
