from resemble import Resemble
Resemble.api_key('UssJh4dZSplnDL9lCnQUeQtt')

# Get your default Resemble project.
project_uuid = Resemble.v2.projects.all(1, 10)['items'][0]['uuid']

# Get your Voice uuid. In this example, we'll obtain the first.
voice_uuid = Resemble.v2.voices.all(1, 10)['items'][0]['uuid']

# Let's create a clip!
body = 'This is a test'
response = Resemble.v2.clips.create_sync(project_uuid,
                                         voice_uuid,
                                         body,
                                         title=None,
                                         sample_rate=None,
                                         output_format=None,
                                         precision=None,
                                         include_timestamps=None,
                                         is_archived=None,
                                         raw=None)

print(clip['audio_src'])