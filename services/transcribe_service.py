from pathlib import Path

from services.gpt_service import GPTService


def transcribe_audio_chunks(chunks, language="ru"):
    gpt_service = GPTService()
    responses = []
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        response = gpt_service.speech_to_text(Path(chunk_path), language=language)
        responses.append(response)
        chunk_paths.append(chunk_path)
    return responses, chunk_paths