from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.legal_document_rs import LegalDocumentRs
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
        "method": "get",
        "url": "/api/v1/legal/documents/terms-of-service",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[LegalDocumentRs, ProblemDetails]:
    if response.status_code == 200:
        response_200 = LegalDocumentRs.from_dict(response.json())

        return response_200

    response_default = ProblemDetails.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[LegalDocumentRs, ProblemDetails]]:
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
) -> Response[Union[LegalDocumentRs, ProblemDetails]]:
    """Gets the Cezzi's.com terms of service

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[LegalDocumentRs, ProblemDetails]]
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
) -> Optional[Union[LegalDocumentRs, ProblemDetails]]:
    """Gets the Cezzi's.com terms of service

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[LegalDocumentRs, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        x_key=x_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[LegalDocumentRs, ProblemDetails]]:
    """Gets the Cezzi's.com terms of service

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[LegalDocumentRs, ProblemDetails]]
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
) -> Optional[Union[LegalDocumentRs, ProblemDetails]]:
    """Gets the Cezzi's.com terms of service

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[LegalDocumentRs, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            x_key=x_key,
        )
    ).parsed
