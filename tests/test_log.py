from src.models.log import Log


def test_log():
    log = Log(
        user_id='test_id',
        input_='test_input',
        output='test_output',
        timestamp=12345
    )

    assert log.user_id == 'test_id'
    assert log.input_ == 'test_input'
    assert log.output == 'test_output'
    assert log.timestamp == 12345

    assert log.to_item() == {
        'user_id': 'test_id',
        'input': 'test_input',
        'output': 'test_output',
        'timestamp': 12345
    }
