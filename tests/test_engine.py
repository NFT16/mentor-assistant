from backend.engine import MentorEngine

def test_known_faq_has_source():
    result = MentorEngine().answer("What should a project README contain?")
    assert result["sources"]
    assert "README" in result["answer"]

def test_unknown_question_does_not_guess():
    result = MentorEngine().answer("What is my portal password?")
    assert "could not find" in result["answer"].lower()

def test_learning_plan_exists():
    assert MentorEngine().learning_plan("INT-002")["plan"]
