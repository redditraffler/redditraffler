from app.db.models import Raffle
from app.util import reddit
from app.util.raffle_form_validator import RaffleFormValidator
import pytest


@pytest.fixture
def base_form():
    return dict.fromkeys(RaffleFormValidator.REQUIRED_KEYS, '')


@pytest.fixture
def form_valid_ints():
    return dict.fromkeys(RaffleFormValidator.INT_KEYS, 1)


def test_run_valid(base_form, mocker):
    class_path = 'app.util.raffle_form_validator.RaffleFormValidator'
    mocker.patch(class_path + '._validate_required_keys')
    mocker.patch(class_path + '._validate_int_values')
    mocker.patch(class_path + '._validate_submission_url')
    mocker.patch(class_path + '._validate_raffle_not_exists')
    mocker.patch(class_path + '._validate_ignored_users_list')
    v = RaffleFormValidator(base_form)
    assert v.run()


def test_run_invalid(client, base_form, mocker):
    mock = mocker.patch('app.util.raffle_form_validator.RaffleFormValidator'
                        '._validate_required_keys')
    mock.side_effect = ValueError
    v = RaffleFormValidator(base_form)
    assert not v.run()


def test_validate_required_keys_valid(base_form):
    v = RaffleFormValidator(base_form)
    v._validate_required_keys()


def test_validate_required_keys_invalid(base_form):
    base_form.pop('submissionUrl')
    v = RaffleFormValidator(base_form)
    with pytest.raises(KeyError):
        v._validate_required_keys()


def test_validate_int_values_valid_ints(form_valid_ints):
    form = form_valid_ints
    v = RaffleFormValidator(form)
    v._validate_int_values()


def test_validate_int_values_negative_ints(form_valid_ints):
    form = form_valid_ints
    for key in form.keys():
        form[key] = -1
    v = RaffleFormValidator(form)
    with pytest.raises(ValueError):
        v._validate_int_values()


def test_validate_int_values_valid_strings(form_valid_ints):
    form = form_valid_ints
    for key in form.keys():
        form[key] = '1'
    v = RaffleFormValidator(form)
    v._validate_int_values()


def test_validate_int_values_invalid_types(form_valid_ints):
    form = form_valid_ints
    for key in form.keys():
        form[key] = 'this_cannot_be_cast_to_int'
    v = RaffleFormValidator(form)
    with pytest.raises(TypeError):
        v._validate_int_values()


def test_validate_submission_url_valid_url_valid_submission(base_form, mocker):
    mocker.patch('app.util.reddit.get_submission').return_value = True
    v = RaffleFormValidator(base_form)
    v._validate_submission_url()


def test_validate_submission_url_valid_url_invalid_submission(base_form,
                                                              mocker):
    mocker.patch('app.util.reddit.get_submission').return_value = False
    v = RaffleFormValidator(base_form)
    with pytest.raises(ValueError):
        v._validate_submission_url()


def test_validate_submission_url_not_string(base_form):
    form = base_form
    form.update({'submissionUrl': 123})
    v = RaffleFormValidator(form)
    with pytest.raises(TypeError):
        v._validate_submission_url()


def test_validate_raffle_not_exists_success(base_form, mocker, db_session):
    mocker.patch('app.util.reddit.submission_id_from_url').return_value = 'x'
    v = RaffleFormValidator(base_form)
    v._validate_raffle_not_exists()


def test_validate_raffle_not_exists_fail(base_form, mocker, raffle):
    sub_id = raffle.submission_id
    mocker.patch('app.util.reddit.submission_id_from_url') \
          .return_value = sub_id
    v = RaffleFormValidator(base_form)
    with pytest.raises(ValueError):
        v._validate_raffle_not_exists()


def test_validate_ignored_users_list_not_list(base_form):
    v = RaffleFormValidator(base_form)
    with pytest.raises(TypeError):
        v._validate_ignored_users_list()


def test_validate_ignored_users_list_valid_string(base_form):
    base_form.update({'ignoredUsers': '["SomeUser"]'})
    v = RaffleFormValidator(base_form)
    v._validate_ignored_users_list()


def test_validate_ignored_users_list_invalid_username(base_form):
    base_form.update({'ignoredUsers': '["X"]'})
    v = RaffleFormValidator(base_form)
    with pytest.raises(ValueError):
        v._validate_ignored_users_list()
