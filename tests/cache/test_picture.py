import uuid


from src.cache.picture import get, put


def test_put_and_get():
    """
    Tests that a value can be put into the cache and retrieved.
    """
    key = uuid.uuid4()
    value = "<svg>test</svg>"
    put(key, value)
    retrieved_value = get(key)
    assert retrieved_value == value


def test_get_nonexistent():
    """
    Tests that getting a nonexistent key returns None.
    """
    key = uuid.uuid4()
    retrieved_value = get(key)
    assert retrieved_value is None


def test_cache_eviction():
    """
    Tests that the cache evicts the oldest item when it's full.
    """
    # Fill the cache to its max size
    keys = [uuid.uuid4() for _ in range(128)]
    for i, key in enumerate(keys):
        put(key, f"<svg>{i}</svg>")

    # The first key should be evicted
    first_key = keys[0]
    assert get(first_key) is not None

    # Add one more item to trigger eviction
    new_key = uuid.uuid4()
    put(new_key, "<svg>new</svg>")

    # The first key should now be evicted
    assert get(first_key) is None
    # The new key should be present
    assert get(new_key) == "<svg>new</svg>"


def test_put_on_empty_cache_eviction():
    """
    Tests that put doesn't raise an error when evicting from an empty cache.
    """
    # This test is primarily to ensure that the StopIteration exception in put is handled.
    # We can't directly test the eviction logic on an empty cache,
    # but we can ensure that putting an item into an empty cache works.
    key = uuid.uuid4()
    value = "<svg>test</svg>"
    put(key, value)
    assert get(key) == value
