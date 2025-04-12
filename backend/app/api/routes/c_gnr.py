from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import CodeGeneratorOutput, CodeGeneratorInput

from transformers import GPT2LMHeadModel, GPT2Tokenizer

router = APIRouter()

# Load the fine-tuned model and tokenizer
model_name = "app/api/fine_tuned_code_completion_model"  # Replace with the path to your fine-tuned model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

@router.post("/")
def get_response(
    *, session: SessionDep, current_user: CurrentUser, item_in: CodeGeneratorInput
) -> Any:
    # Set the model to evaluation mode
    model.eval()

    # Generate sample text
    prompt = item_in.input
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Adjust the max length of the generated sequence as needed
    max_length = 100

    # Generate the sample
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)

    # Decode the generated output
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    print("Generated Code:")
    print(generated_text)

    return generated_text