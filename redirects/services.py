database = [
    {
        "key": 1,
        "url": "1",
        "active": True,
        "created_at": "2023-12-05T18:27:23.835890Z",
        "updated_at": "2023-12-05T18:27:23.835920Z"
    },
    {
        "key": 2,
        "url": "2",
        "active": True,
        "created_at": "2023-12-05T18:30:11.082954Z",
        "updated_at": "2023-12-05T18:30:11.082987Z"
    },
    {
        "key": 3,
        "url": "3",
        "active": True,
        "created_at": "2023-12-05T18:40:59.978326Z",
        "updated_at": "2023-12-05T18:40:59.978354Z"
    },
    {
        "key": 4,
        "url": "4",
        "active": False,
        "created_at": "2023-12-05T18:46:56.042634Z",
        "updated_at": "2023-12-05T18:46:56.042652Z"
    }
]


def get_redirect_from_db(redirect_key):
    return next((item for item in database if item["key"] == redirect_key), None)
