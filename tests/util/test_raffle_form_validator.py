import pytest

from app.db.models.raffle import Raffle
from app.util.raffle_form_validator import RaffleFormValidator
from tests.factories import RaffleFactory


@pytest.fixture
def base_form():
    return dict.fromkeys(RaffleFormValidator.REQUIRED_KEYS, "")


@pytest.fixture
def form_valid_ints():
    return dict.fromkeys(RaffleFormValidator.INT_KEYS, 1)


@pytest.fixture
def unsanitized_form():
    return {
        "submissionUrl": "redd.it/57xvjb",
        "winnerCount": "1",
        "minAge": "0",
        "minComment": "0",
        "minLink": "0",
        "ignoredUsers": "[]",
    }


@pytest.fixture
def raffle():
    return RaffleFactory()


def test_run_valid(base_form, mocker):
    class_path = "app.util.raffle_form_validator.RaffleFormValidator"
    mocker.patch(class_path + "._validate_required_keys")
    mocker.patch(class_path + "._validate_karma_keys")
    mocker.patch(class_path + "._validate_int_values")
    mocker.patch(class_path + "._validate_submission_url")
    mocker.patch(class_path + "._validate_raffle_not_exists")
    mocker.patch(class_path + "._validate_ignored_users_list")
    v = RaffleFormValidator(base_form)
    assert v.run()


def test_run_invalid(app, base_form, mocker):
    mock = mocker.patch(
        "app.util.raffle_form_validator.RaffleFormValidator" "._validate_required_keys"
    )
    mock.side_effect = ValueError
    v = RaffleFormValidator(base_form)
    assert not v.run()


def test_validate_required_keys_valid(base_form):
    v = RaffleFormValidator(base_form)
    v._validate_required_keys()


def test_validate_required_keys_invalid(base_form):
    base_form.pop("submissionUrl")
    v = RaffleFormValidator(base_form)
    with pytest.raises(KeyError):
        v._validate_required_keys()


class TestValidateKarmaKeys:
    @pytest.fixture
    def valid_form(self, base_form):
        base_form.update({"minCombined": 0})
        yield base_form

    @pytest.fixture
    def invalid_form_missing_keys(self, base_form):
        yield base_form

    @pytest.fixture
    def invalid_form_both_keys(self, base_form):
        base_form.update({"minCombined": 0, "minLink": 0, "minComment": 0})
        yield base_form

    def test_valid_form(self, valid_form):
        v = RaffleFormValidator(valid_form)
        v._validate_karma_keys()

    def test_invalid_form_missing_keys(self, invalid_form_missing_keys):
        v = RaffleFormValidator(invalid_form_missing_keys)
        with pytest.raises(KeyError):
            v._validate_karma_keys()

    def test_invalid_form_both_keys_present(self, invalid_form_both_keys):
        v = RaffleFormValidator(invalid_form_both_keys)
        with pytest.raises(KeyError):
            v._validate_karma_keys()


class TestValidateIntValues:
    class TestValidValues:
        def test_winner_count_within_range(self, form_valid_ints):
            form = form_valid_ints
            form["winnerCount"] = 70
            v = RaffleFormValidator(form)
            v._validate_int_values()

        def test_string_ints(self, form_valid_ints):
            form = form_valid_ints
            for key in form.keys():
                form[key] = "1"
            v = RaffleFormValidator(form)
            v._validate_int_values()

    class TestInvalidValues:
        def test_invalid_types(self, form_valid_ints):
            form = form_valid_ints
            for key in form.keys():
                form[key] = "this_cannot_be_cast_to_int"
            v = RaffleFormValidator(form)
            with pytest.raises(TypeError):
                v._validate_int_values()

        def test_negative_ints(self, form_valid_ints):
            form = form_valid_ints
            for key in form.keys():
                form[key] = -1
            v = RaffleFormValidator(form)
            with pytest.raises(ValueError):
                v._validate_int_values()

        def test_valid_ints_but_invalid_winner_count(self, form_valid_ints):
            form = form_valid_ints
            form["winnerCount"] = Raffle.MAX_WINNER_COUNT + 1
            v = RaffleFormValidator(form)
            with pytest.raises(ValueError):
                v._validate_int_values()


def test_validate_submission_url_valid_url_valid_submission(base_form, mocker):
    mocker.patch("app.services.reddit_service.get_submission_by_url").return_value = {
        "some": "submission"
    }
    v = RaffleFormValidator(base_form)
    v._validate_submission_url()


def test_validate_submission_url_valid_url_invalid_submission(base_form, mocker):
    mocker.patch(
        "app.services.reddit_service.get_submission_by_url"
    ).return_value = None
    v = RaffleFormValidator(base_form)
    with pytest.raises(ValueError):
        v._validate_submission_url()


def test_validate_submission_url_not_string(base_form):
    form = base_form
    form.update({"submissionUrl": 123})
    v = RaffleFormValidator(form)
    with pytest.raises(TypeError):
        v._validate_submission_url()


def test_validate_raffle_not_exists_success(base_form, mocker, db_session):
    mocker.patch("app.services.reddit_service.get_submission_by_url").return_value = {
        "id": "some-id-not-in-db"
    }
    v = RaffleFormValidator(base_form)
    v._validate_raffle_not_exists()


def test_validate_raffle_not_exists_fail(base_form, mocker, raffle):
    mocker.patch("app.services.reddit_service.get_submission_by_url").return_value = {
        "id": raffle.submission_id
    }
    v = RaffleFormValidator(base_form)
    with pytest.raises(ValueError):
        v._validate_raffle_not_exists()


def test_validate_ignored_users_list_not_list(base_form):
    v = RaffleFormValidator(base_form)
    with pytest.raises(TypeError):
        v._validate_ignored_users_list()


def test_validate_ignored_users_list_valid_string(base_form):
    form = base_form
    form.update({"ignoredUsers": '["SomeUser"]'})
    v = RaffleFormValidator(form)
    v._validate_ignored_users_list()


def test_validate_ignored_users_list_invalid_username(base_form):
    form = base_form
    form.update({"ignoredUsers": '["X"]'})
    v = RaffleFormValidator(form)
    with pytest.raises(ValueError):
        v._validate_ignored_users_list()


def test_get_sanitized_form(unsanitized_form):
    v = RaffleFormValidator(unsanitized_form)
    form = v.get_sanitized_form()
    assert form["submissionUrl"].startswith("https")
    assert isinstance(form["ignoredUsers"], list)
    for key in RaffleFormValidator.INT_KEYS:
        if key in form:
            assert isinstance(form[key], int)
