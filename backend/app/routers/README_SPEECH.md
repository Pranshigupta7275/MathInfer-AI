# Speech-to-Text API Documentation

## Overview

The Speech-to-Text API endpoint allows the AI Math Chatbot to convert audio recordings into text using the Hugging Face Whisper API. This enables users to ask math questions verbally instead of typing them.

## Endpoint

```
POST /stt
```

## Request Format

The request should be a multipart/form-data request with an audio file attached.

### Parameters

- `audio`: The audio file to transcribe (required)

### Supported Audio Formats

- WAV (`audio/wav`)
- MP3 (`audio/mpeg`)
- WebM (`audio/webm`)
- OGG (`audio/ogg`)
- M4A (`audio/x-m4a`)

### Size Limits

The maximum audio file size is 10MB by default. This can be configured using the `MAX_AUDIO_SIZE` environment variable.

## Response Format

### Success Response (200 OK)

```json
{
  "text": "The transcribed text from the audio file."
}
```

### Error Responses

- **415 Unsupported Media Type**: The audio file format is not supported.
- **413 Request Entity Too Large**: The audio file exceeds the maximum allowed size.
- **500 Internal Server Error**: Error with the Whisper API or server-side processing.
- **503 Service Unavailable**: Network error connecting to the Whisper API.

## Example Usage

### cURL

```bash
curl -X POST \
  -F "audio=@recording.mp3" \
  http://localhost:8000/stt
```

### JavaScript (Frontend)

```javascript
async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');
  
  try {
    const response = await fetch('http://localhost:8000/stt', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.text;
  } catch (error) {
    console.error('Error transcribing audio:', error);
    throw error;
  }
}
```

## Configuration

The Speech-to-Text functionality requires a Hugging Face API token to be set in the environment variables:

```
HUGGINGFACE_API_TOKEN=your_api_token_here
```

You can also configure the following optional settings:

```
AUDIO_DIR=/path/to/temporary/audio/storage
MAX_AUDIO_SIZE=10485760  # 10MB in bytes
```

## Notes

- Audio files are temporarily stored on the server during processing and then deleted.
- The transcription quality depends on the Whisper model and the clarity of the audio.
- For best results, ensure the audio has minimal background noise and clear speech.