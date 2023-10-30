from django.contrib.auth.models import User, Group

from organizations.models import Company


def setUp_for_tests():
    company = Company.objects.create(name="test", email_domain="test.com")
    user_owner = User.objects.create(username="test_user1", email="test_user1@test.com")
    user_owner.set_password("password")
    user_owner.save()
    user_owner.groups.add(Group.objects.get(name="Owner"))
    user_candidate = User.objects.create(username="test_user2", email="test_user2@candidate.com")
    user_candidate.set_password("password")
    user_candidate.save()
    user_candidate.groups.add(Group.objects.get(name="Candidate"))
    return user_owner, user_candidate
