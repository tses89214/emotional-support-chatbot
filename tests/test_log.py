from src.models.log import Log

def test_log():
    log = Log(
        user_id = 'test_id',
        prompt = 'test_prompt',
        input_ = 'test_input',
        output = 'test_output',
        timestamp = 12345
        )
        
    assert log.user_id == 'test_id'
    assert log.prompt == 'test_prompt'
    assert log.input_ == 'test_input'
    assert log.output == 'test_output'
    assert log.timestamp == 12345
    
    
    assert log.to_item() == {
    'user_id':'test_id',
     'prompt':'test_prompt',
     'input':'test_input',
     'output':'test_output',
     'timestamp':12345
    }