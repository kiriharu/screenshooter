from contextlib import suppress
from ipaddress import ip_address

from fastapi import Header
from pydantic import HttpUrl

from screenshooter.config import RESTRICTED_HOSTS, ACCESS_TOKEN
from screenshooter.errors import RestrictedAddressException, InvalidTokenException


def check_restricted_urls(url: HttpUrl):
    # local ips
    with suppress(ValueError):
        ip_addr = ip_address(url.host)
        if any(
            [
                ip_addr.is_loopback,
                ip_addr.is_private,
                ip_addr.is_multicast,
                ip_addr.is_link_local,
                ip_addr.is_unspecified,
                not ip_addr.is_global,
            ]
        ):
            raise RestrictedAddressException()
    # restricted hosts
    if url.host in RESTRICTED_HOSTS:
        raise RestrictedAddressException()
    return url


def verify_token(x_token: str = Header(...)):
    if x_token != ACCESS_TOKEN:
        raise InvalidTokenException
