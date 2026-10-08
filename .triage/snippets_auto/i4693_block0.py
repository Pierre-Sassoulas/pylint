    result = handler.check_callback(result.url, parse_args(result.url), {})
    assert isinstance(result, disposition.Verified)
    assert result.identity == 'https://mastodon.example/@moo'
    assert result.redir == 'qwerpoiu'
    assert result.profile == { 
        'name': 'moo friend',
        'bio': 'a cow',
        'avatar': 'https://placekitten.com/1280/1024',
        'homepage': 'https://moo.example',
        'pronouns': 'moo/moo'
    }

