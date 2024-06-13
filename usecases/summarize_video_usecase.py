import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

from services.audio_service import extract_audio_from_video, split_audio
from services.gpt_service import GPTService
from services.prompt_chain_service import ChainPromptsService
from services.transcribe_service import transcribe_audio_chunks

_ = load_dotenv(find_dotenv())
PROMPTS_CHAINS_DIR = os.environ["PROMPTS_CHAINS_DIR"]


def summarize_video_usecase(*, video_path: str):
    os.environ['PATH'] = f"{os.environ['PATH']}:/Users/silver_machine/bin"
    print(os.environ['PATH'])
    audio_path = extract_audio_from_video(video_path=Path(video_path))
    audio_chunks = split_audio(audio_path=audio_path)
    responses, chunks_paths = transcribe_audio_chunks(chunks=audio_chunks)
    full_response = " ".join(responses)
    print(full_response)

    template_file_path = Path(PROMPTS_CHAINS_DIR) / Path("summarize_video_prompt_chain.txt")
    with open(template_file_path) as f:
        output = ChainPromptsService(
            prompts_templates=f.read(),
            gpt_service=GPTService(),
        ).generate(
            initial_text=full_response,
        )

    print(output)

    chunks_paths.append(audio_path)

    for p in chunks_paths:
        if os.path.exists(str(p)):
            os.remove(str(p))


