"""Basic tests. Run with:  python -m unittest -v
They use mock mode, so no API key is needed."""
import os
import unittest

os.environ["USE_MOCK"] = "1"

import llm


class TestClean(unittest.TestCase):
    def test_good_answer_passes(self):
        out = llm.clean({"score": 3, "strengths": ["a"], "gaps": ["b"], "next_step": "c"})
        self.assertEqual(out["score"], 3)

    def test_score_out_of_range_is_rejected(self):
        with self.assertRaises(ValueError):
            llm.clean({"score": 9, "strengths": [], "gaps": [], "next_step": "x"})

    def test_missing_field_is_rejected(self):
        with self.assertRaises(KeyError):
            llm.clean({"score": 3, "strengths": [], "gaps": []})


class TestGetFeedback(unittest.TestCase):
    def test_returns_expected_keys(self):
        out = llm.get_feedback("Title: Test\n\nA Python project with 90% accuracy on GitHub.")
        self.assertEqual(set(out), {"score", "strengths", "gaps", "next_step", "truncated"})

    def test_same_input_gives_same_score_in_mock_mode(self):
        text = "Title: X\n\nSome project text " * 5
        scores = {llm.get_feedback(text)["score"] for _ in range(5)}
        self.assertEqual(len(scores), 1)

    def test_long_input_is_marked_truncated(self):
        out = llm.get_feedback("word " * (llm.MAX_CHARS))
        self.assertTrue(out["truncated"])

    def test_short_input_is_not_truncated(self):
        self.assertFalse(llm.get_feedback("short text")["truncated"])


if __name__ == "__main__":
    unittest.main()
