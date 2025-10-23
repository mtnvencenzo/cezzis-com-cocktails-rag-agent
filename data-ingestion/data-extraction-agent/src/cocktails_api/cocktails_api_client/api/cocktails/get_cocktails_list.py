from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...models.cocktail_data_include_model import CocktailDataIncludeModel
from ...models.cocktails_list_rs import CocktailsListRs
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    free_text: Union[Unset, str] = UNSET,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    m: Union[Unset, list[str]] = UNSET,
    match_exclusive: Union[Unset, bool] = False,
    inc: Union[Unset, list[CocktailDataIncludeModel]] = UNSET,
    sf: Union[Unset, list[str]] = UNSET,
    x_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_key, Unset):
        headers["X-Key"] = x_key

    params: dict[str, Any] = {}

    params["freeText"] = free_text

    params["skip"] = skip

    params["take"] = take

    json_m: Union[Unset, list[str]] = UNSET
    if not isinstance(m, Unset):
        json_m = m

    params["m"] = json_m

    params["match-exclusive"] = match_exclusive

    json_inc: Union[Unset, list[str]] = UNSET
    if not isinstance(inc, Unset):
        json_inc = []
        for inc_item_data in inc:
            inc_item = inc_item_data.value
            json_inc.append(inc_item)

    params["inc"] = json_inc

    json_sf: Union[Unset, list[str]] = UNSET
    if not isinstance(sf, Unset):
        json_sf = sf

    params["sf"] = json_sf

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/cocktails",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CocktailsListRs, ProblemDetails]:
    if response.status_code == 200:
        response_200 = CocktailsListRs.from_dict(response.json())

        return response_200

    response_default = ProblemDetails.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CocktailsListRs, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    free_text: Union[Unset, str] = UNSET,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    m: Union[Unset, list[str]] = UNSET,
    match_exclusive: Union[Unset, bool] = False,
    inc: Union[Unset, list[CocktailDataIncludeModel]] = UNSET,
    sf: Union[Unset, list[str]] = UNSET,
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[CocktailsListRs, ProblemDetails]]:
    """Search the cocktail recipes

    Args:
        free_text (Union[Unset, str]):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        m (Union[Unset, list[str]]):
        match_exclusive (Union[Unset, bool]):  Default: False.
        inc (Union[Unset, list[CocktailDataIncludeModel]]):
        sf (Union[Unset, list[str]]):
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CocktailsListRs, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        free_text=free_text,
        skip=skip,
        take=take,
        m=m,
        match_exclusive=match_exclusive,
        inc=inc,
        sf=sf,
        x_key=x_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    free_text: Union[Unset, str] = UNSET,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    m: Union[Unset, list[str]] = UNSET,
    match_exclusive: Union[Unset, bool] = False,
    inc: Union[Unset, list[CocktailDataIncludeModel]] = UNSET,
    sf: Union[Unset, list[str]] = UNSET,
    x_key: Union[Unset, str] = UNSET,
) -> Optional[Union[CocktailsListRs, ProblemDetails]]:
    """Search the cocktail recipes

    Args:
        free_text (Union[Unset, str]):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        m (Union[Unset, list[str]]):
        match_exclusive (Union[Unset, bool]):  Default: False.
        inc (Union[Unset, list[CocktailDataIncludeModel]]):
        sf (Union[Unset, list[str]]):
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CocktailsListRs, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        free_text=free_text,
        skip=skip,
        take=take,
        m=m,
        match_exclusive=match_exclusive,
        inc=inc,
        sf=sf,
        x_key=x_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    free_text: Union[Unset, str] = UNSET,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    m: Union[Unset, list[str]] = UNSET,
    match_exclusive: Union[Unset, bool] = False,
    inc: Union[Unset, list[CocktailDataIncludeModel]] = UNSET,
    sf: Union[Unset, list[str]] = UNSET,
    x_key: Union[Unset, str] = UNSET,
) -> Response[Union[CocktailsListRs, ProblemDetails]]:
    """Search the cocktail recipes

    Args:
        free_text (Union[Unset, str]):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        m (Union[Unset, list[str]]):
        match_exclusive (Union[Unset, bool]):  Default: False.
        inc (Union[Unset, list[CocktailDataIncludeModel]]):
        sf (Union[Unset, list[str]]):
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CocktailsListRs, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        free_text=free_text,
        skip=skip,
        take=take,
        m=m,
        match_exclusive=match_exclusive,
        inc=inc,
        sf=sf,
        x_key=x_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    free_text: Union[Unset, str] = UNSET,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    m: Union[Unset, list[str]] = UNSET,
    match_exclusive: Union[Unset, bool] = False,
    inc: Union[Unset, list[CocktailDataIncludeModel]] = UNSET,
    sf: Union[Unset, list[str]] = UNSET,
    x_key: Union[Unset, str] = UNSET,
) -> Optional[Union[CocktailsListRs, ProblemDetails]]:
    """Search the cocktail recipes

    Args:
        free_text (Union[Unset, str]):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        m (Union[Unset, list[str]]):
        match_exclusive (Union[Unset, bool]):  Default: False.
        inc (Union[Unset, list[CocktailDataIncludeModel]]):
        sf (Union[Unset, list[str]]):
        x_key (Union[Unset, str]):  Example: 1234567890-0000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CocktailsListRs, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            free_text=free_text,
            skip=skip,
            take=take,
            m=m,
            match_exclusive=match_exclusive,
            inc=inc,
            sf=sf,
            x_key=x_key,
        )
    ).parsed
