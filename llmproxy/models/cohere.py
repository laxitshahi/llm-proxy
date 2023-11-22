import cohere
from llmproxy.models.base import BaseModel, CompletionResponse
from llmproxy.utils.enums import BaseEnum
from llmproxy.utils.log import logger

cohere_price_data_summarize_generate_chat = {
    "max-output-tokens": 50,
    "model-costs": {
        "prompt": 1.50 / 1_000_000,
        "completion": 2.00 / 1_000_000,
    },
}


# These are the "Models" only for chat/command
class CohereModel(str, BaseEnum):
    COMMAND = "command"
    COMMAND_LIGHT = "command-light"
    COMMAND_NIGHTLY = "command-nightly"
    COMMAND_LIGHT_NIGHTLY = "command-light-nightly"


class Cohere(BaseModel):
    def __init__(
        self,
        prompt: str = "",
        model: CohereModel = CohereModel.COMMAND.value,
        temperature: float = 0.0,
        api_key: str = "",
        max_output_tokens: int = None,
    ) -> None:
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.api_key = api_key
        self.max_output_tokens = max_output_tokens
        self.co = None
        try:
            self.co = cohere.Client(self.api_key)
        except cohere.CohereError as e:
            raise CohereException(exception=e, error_type=ValueError)

    def get_completion(self, prompt: str = "") -> CompletionResponse:
        if self.model not in CohereModel:
            raise CohereException(
                exception=f"Model not supported. Please use one of the following models: {', '.join(CohereModel.list_values())}",
                error_type=ValueError,
            )
        if self.co is None:
            raise self.error_response
        try:
            response = self.co.chat(
                max_tokens=self.max_output_tokens,
                message=prompt or self.prompt,
                model=self.model,
                temperature=self.temperature,
            )
            return CompletionResponse(
                payload=response.text,
                message="OK",
                err="",
            )
        except cohere.CohereError as e:
            return CohereException(exception=e.message, error_type=e.http_status)
        except Exception as e:
            raise Exception("Unknown Cohere error when making API call")

    def get_estimated_max_cost(self, prompt: str = "") -> float:
        if not self.prompt and not prompt:
            logger.info("No prompt provided.")
            raise ValueError("No prompt provided.")

        # Assumption, model exists (check should be done at yml load level)
        logger.info(f"Tokenizing model: {self.model}")

        prompt_cost_per_token = cohere_price_data_summarize_generate_chat[
            "model-costs"
        ]["prompt"]
        logger.info(f"Prompt Cost per token: {prompt_cost_per_token}")

        completion_cost_per_token = cohere_price_data_summarize_generate_chat[
            "model-costs"
        ]["completion"]
        logger.info(f"Output cost per token: {completion_cost_per_token}")

        tokens = self.co.tokenize(text=prompt or self.prompt).tokens

        logger.info(f"Number of input tokens found: {len(tokens)}")

        logger.info(
            f"Final calculation using {len(tokens)} input tokens and {cohere_price_data_summarize_generate_chat['max-output-tokens']} output tokens"
        )

        cost = round(
            prompt_cost_per_token * len(tokens)
            + completion_cost_per_token
            * cohere_price_data_summarize_generate_chat["max-output-tokens"],
            8,
        )

        logger.info(f"Calculated Cost: {cost}")

        return cost


class CohereException(Exception):
    def __init__(self, exception: str, error_type: str) -> None:
        super().__init__(f"Cohere Error: {exception}, Type: {error_type}")
