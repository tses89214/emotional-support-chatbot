from src.models.user import User


def test_user():
    user = User(
        user_id='test_id',
        create_at=12345,
        status='test_status'
    )

    assert user.user_id == 'test_id'
    assert user.create_at == 12345
    assert user.status == 'test_status'
    assert user.to_item() == {
        'user_id': 'test_id',
        'create_at': 12345,
        'status': 'test_status'
    }
