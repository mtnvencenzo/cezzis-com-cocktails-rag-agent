from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    x_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_key, Unset):
        headers["X-Key"] = x_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/cocktails",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, ProblemDetails]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    response_default = ProblemDetails.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ProblemDetails]]:
    """Seeds the cocktails in the database

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        x_key=x_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    x_key: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ProblemDetails]]:
    """Seeds the cocktails in the database

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        x_key=x_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ProblemDetails]]:
    """Seeds the cocktails in the database

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        x_key=x_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    x_key: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ProblemDetails]]:
    """Seeds the cocktails in the database

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            x_key=x_key,
        )
    ).parsed
