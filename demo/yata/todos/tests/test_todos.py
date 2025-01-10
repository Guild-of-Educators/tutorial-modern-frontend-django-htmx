"""
Why pytest 
liveserver fixture
page fixture

pytest 
pytest --headed 
pytest --headed --slowmo=2000 
pytest --headed --slowmo=1000 --browser firefox
pytest --headed --slowmo=1000 --browser firefox --browser chromium

pytest --tracing=on --browser firefox --browser chromium
playwright show-trace test-results/todos-tests-test-todos-py-test-create-todo-item-gets-rid-of-nothing-to-see-chromium/trace.zip

vscode debugging
breakpoint()

playwright codegen http://127.0.0.1:8181/
pytest  todo/tests/test_todos.py -k test_form_clears_upon_submission
hx-on::after-request="this.reset()" 

playwright --help 
"""

from playwright.sync_api import Page, expect
from django.urls import reverse
from todos import models
import pytest


def test_display_empty_list_on_first_load(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)

    page.wait_for_selector("text=Nothing to see")


def reverse_url(
    live_server, viewname, urlconf=None, args=None, kwargs=None, current_app=None
):
    end = reverse(viewname, urlconf, args, kwargs, current_app)
    return f"{live_server.url}{end}"


def test_create_todo_item_gets_rid_of_nothing_to_see(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.get_by_label("Title:").click()
    page.get_by_label("Title:").fill("foo")
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Nothing to see here...")).to_be_hidden()


def test_create_todo_item_shows_new_item(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.get_by_label("Title:").click()
    page.get_by_label("Title:").fill("foo")
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("text=foo")


def test_display_one_item_on_first_load(live_server, page: Page):
    models.TodoItem.objects.create(title="Test item")
    page.goto(reverse_url(live_server, "index"))
    page.wait_for_selector("text=Test item")  # select dom elements
    expect(page.get_by_text("Nothing to see here...")).to_be_hidden()


def test_checkbox(live_server, page: Page):
    items = [models.TodoItem.objects.create(title=f"Test item {i}") for i in range(3)]
    page.goto(reverse_url(live_server, "index"))

    middle_item = items[1]
    middle_id = f"toggle_item_{middle_item.id}"
    page.get_by_test_id(middle_id).check()
    expect(page.get_by_test_id(middle_id)).to_be_checked()

    middle_item.refresh_from_db()
    assert middle_item.completed is True

    items[0].refresh_from_db()
    assert items[0].completed is False

    items[2].refresh_from_db()
    assert items[2].completed is False


def test_checkbox_loads_correctly(live_server, page: Page):
    item = models.TodoItem.objects.create(title="Test item", completed=True)
    page.goto(reverse_url(live_server, "index"))
    checkbox_id = f"toggle_item_{item.id}"
    expect(page.get_by_test_id(checkbox_id)).to_be_checked()


def test_delete_item(live_server, page: Page):
    item = models.TodoItem.objects.create(title="Test item", completed=True)
    page.goto(reverse_url(live_server, "index"))

    delete_id = f"delete_item_{item.id}"
    page.get_by_test_id(delete_id).click()

    expect(page.get_by_test_id("todo_items")).not_to_contain_text("Test item")

    with pytest.raises(models.TodoItem.DoesNotExist):
        models.TodoItem.objects.get(id=item.id)
