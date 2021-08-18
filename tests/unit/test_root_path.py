import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastapi_versioning import VersionedFastAPI


@pytest.mark.parametrize("root_path", ["/custom/root", "/custom/root/"])
def test_root_path(root_path) -> None:
    parent_app = FastAPI(root_path=root_path)

    @parent_app.get("/greet")
    def noop() -> None:
        ...

    versioned_app = VersionedFastAPI(app=parent_app)
    test_client = TestClient(versioned_app)

    # currently passes with:
    # assert test_client.get("/v1_0/greet").status_code == 200
    # I believe the issue is that the route_path is being set on a mounted app
    # and not on the version route where the app is mounted

    assert test_client.get("/custom/root/v1_0/greet").status_code == 200
