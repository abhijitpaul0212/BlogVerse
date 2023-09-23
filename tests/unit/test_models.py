from project.app import User, password_hashing


def test_add_new_user(app, client):
    user = User(
                username="digiscotch1",
                first_name="digiscotch1",
                last_name="",
                email='digiscotch1@gmail.com',
                password=password_hashing('Qwerty@123'),
            )
    user.save()

    assert user.email == "digiscotch1@gmail.com"
    assert user.password != 'Qwerty@123'
    assert user.first_name == "digiscotch1"
    
    user.delete()
    assert user.email not in [all_user.email for all_user in User.objects.all()]
