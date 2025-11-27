from fastapi import APIRouter, UploadFile, File, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import uuid
import httpx
import json
import logging
from ..config import get_settings
from ..utils import sanitize_filename, validate_mime_type
from .. import schemas # Ensure schemas is imported

# Set up logging
logger = logging.getLogger(__name__)

# Create a temporary directory for audio uploads if it doesn't exist
AUDIO_DIR = Path(os.getenv('AUDIO_DIR', '/tmp/ai-math-chatbot-audio'))
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Allowed audio MIME types
ALLOWED_AUDIO_TYPES = [
    'audio/wav',
    'audio/mpeg',  # mp3
    'audio/webm',
    'audio/ogg',
    'audio/x-m4a',
]

router = APIRouter(
    tags=["Speech"],
    responses={404: {"description": "Not found"}},
)

@router.post("/stt", response_model=schemas.SpeechToTextResponse, status_code=status.HTTP_200_OK)
async def speech_to_text(
    audio: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
) -> schemas.SpeechToTextResponse:
    """
    Convert speech audio to text using Whisper API.
    
    Accepts audio files, validates them, and sends to the Whisper API for transcription.
    Returns the transcribed text.
    """
    settings = get_settings()
    
    # Validate audio file type
    if not validate_mime_type(audio.content_type, ALLOWED_AUDIO_TYPES):
        logger.warning(f"Rejected audio file with unsupported type: {audio.content_type}")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Audio type {audio.content_type} not supported. Allowed types: {', '.join(ALLOWED_AUDIO_TYPES)}"
        )
    
    # Sanitize filename
    filename = sanitize_filename(audio.filename or "audio.wav")
    
    # Generate a unique file ID and save the audio file temporarily
    audio_id = str(uuid.uuid4())
    audio_path = AUDIO_DIR / f"{audio_id}.{filename.split('.')[-1]}"
    
    # Read and validate file size
    audio_size = 0
    max_audio_size = settings.max_audio_size
    with open(audio_path, "wb") as buffer:
        while chunk := await audio.read(1024 * 1024):  # 1MB chunks
            audio_size += len(chunk)
            if audio_size > max_audio_size:
                # Close and remove the partial file
                buffer.close()
                os.unlink(audio_path)
                logger.warning(f"Rejected audio file exceeding size limit: {audio_size} bytes")
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Audio file size exceeds the maximum allowed size of {max_audio_size // (1024 * 1024)}MB"
                )
            buffer.write(chunk)
    
    try:
        # Call Whisper API for transcription
        # Using Hugging Face's Whisper endpoint
        whisper_api_key = settings.whisper_api_key
        if not whisper_api_key:
            logger.error("Whisper API key not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Whisper API key not configured"
            )
        
        logger.info(f"Processing audio file {audio_id} for transcription")
        
        # Send the audio file to the Whisper API
        async with httpx.AsyncClient() as client:
            # Read the audio data from the temporarily saved file
            with open(audio_path, "rb") as f_audio:
                audio_data_for_api = f_audio.read()

            headers = {
                "Authorization": f"Bearer {whisper_api_key}",
                "Content-Type": audio.content_type # Use the content_type from the uploaded file
            }
            
            # Using Hugging Face's Whisper endpoint
            response = await client.post(
                settings.huggingface_whisper_endpoint,
                content=audio_data_for_api, # Send raw bytes using the 'content' parameter
                headers=headers,
                timeout=30.0  # Longer timeout for audio processing
            )
            
            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_json = response.json()
                    if isinstance(error_json, dict) and "error" in error_json:
                        error_detail = error_json["error"]
                except Exception:
                    error_detail = response.text
                
                logger.error(f"Whisper API error: {error_detail}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Whisper API error: {error_detail}"
                )
            
            result = response.json()
            transcription = result.get("text", "")
            logger.info(f"Successfully transcribed audio {audio_id} ({len(transcription)} characters)")
        
        # Schedule cleanup of the temporary audio file
        if background_tasks:
            background_tasks.add_task(cleanup_audio_file, audio_path)
        
        return schemas.SpeechToTextResponse(text=transcription)
    
    except httpx.RequestError as e:
        # Handle network errors
        logger.error(f"Network error connecting to Whisper API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error connecting to Whisper API: {str(e)}"
        )
    except Exception as e:
        # Handle other errors
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio: {str(e)}"
        )
    finally:
        # Ensure the file is cleaned up if not handled by background task
        if audio_path.exists() and not background_tasks:
            os.unlink(audio_path)

async def cleanup_audio_file(file_path: Path):
    """
    Delete an audio file after processing.
    """
    try:
        if file_path.exists():
            os.unlink(file_path)
            logger.info(f"Cleaned up temporary audio file: {file_path}")
    except Exception as e:
        # Log the error but don't raise it
        logger.error(f"Error cleaning up audio file {file_path}: {e}")