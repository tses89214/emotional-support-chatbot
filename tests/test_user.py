from src.models.user import User

def test_user():
    user = User(
        user_id = 'test_id',
        prompt = 'test_prompt'
        )
        
    assert user.user_id == 'test_id'
    assert user.prompt == 'test_prompt'
    assert user.to_item() == {
        'user_id': 'test_id',
        'prompt': 'test_prompt'
    }

    user.set_prompt = 'test_prompt2'
    assert user.prompt == 'test_prompt2'