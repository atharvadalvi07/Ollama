import unittest
from unittest.mock import patch, Mock
import feedback


class TestFeedbackGenerator(unittest.TestCase):
    def test_build_review_prompt_contains_rules_and_code(self):
        code = "print('hello')"
        prompt = feedback.build_review_prompt(code, language="Python")

        # Basic checks: the prompt contains key instructions and the student's code
        self.assertIn("Do NOT include any code", prompt)
        self.assertIn("Here is the student's code", prompt)
        self.assertIn(code, prompt)
        self.assertIn("```Python", prompt)

    @patch("feedback.requests.post")
    def test_ask_ollama_parses_response(self, mock_post):
        # Mock the HTTP response from Ollama
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"response": "Some feedback text"}
        mock_post.return_value = mock_response

        out = feedback.ask_ollama("test prompt", model="dummy-model")
        self.assertEqual(out, "Some feedback text")

        # Verify request was made with expected endpoint and JSON payload keys
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], feedback.OLLAMA_URL)
        self.assertIn("json", kwargs)
        self.assertEqual(kwargs["json"]["prompt"], "test prompt")
        self.assertEqual(kwargs["json"]["model"], "dummy-model")
        self.assertFalse(kwargs["json"]["stream"])


if __name__ == "__main__":
    unittest.main()
