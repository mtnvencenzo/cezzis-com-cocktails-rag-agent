from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.account_owned_profile_rs import AccountOwnedProfileRs
from ...models.change_account_owned_email_rq import ChangeAccountOwnedEmailRq
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ChangeAccountOwnedEmailRq,
    x_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_key, Unset):
        headers["X-Key"] = x_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/accounts/owned/profile/email",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json; x-api-version=1.0"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[AccountOwnedProfileRs, ProblemDetails]:
    if response.status_code == 200:
        response_200 = AccountOwnedProfileRs.from_dict(response.json())

        return response_200

    response_default = ProblemDetails.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AccountOwnedProfileRs, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ChangeAccountOwnedEmailRq,
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[AccountOwnedProfileRs, ProblemDetails]]:
    """Updates the account profile email address for the user represented within the authenticated bearer
    token

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.
        body (ChangeAccountOwnedEmailRq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountOwnedProfileRs, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        body=body,
        x_key=x_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ChangeAccountOwnedEmailRq,
    x_key: Union[Unset, str] = UNSET,
) -> Optional[Union[AccountOwnedProfileRs, ProblemDetails]]:
    """Updates the account profile email address for the user represented within the authenticated bearer
    token

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.
        body (ChangeAccountOwnedEmailRq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountOwnedProfileRs, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        body=body,
        x_key=x_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ChangeAccountOwnedEmailRq,
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[AccountOwnedProfileRs, ProblemDetails]]:
    """Updates the account profile email address for the user represented within the authenticated bearer
    token

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.
        body (ChangeAccountOwnedEmailRq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountOwnedProfileRs, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        body=body,
        x_key=x_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ChangeAccountOwnedEmailRq,
    x_key: Union[Unset, str] = UNSET,
) -> Optional[Union[AccountOwnedProfileRs, ProblemDetails]]:
    """Updates the account profile email address for the user represented within the authenticated bearer
    token

    Args:
        x_key (Union[Unset, str]):  Example: 1234567890-0000.
        body (ChangeAccountOwnedEmailRq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountOwnedProfileRs, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_key=x_key,
        )
    ).parsed
