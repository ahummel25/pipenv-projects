#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3

from sys import argv
import click
from click_aliases import ClickAliasedGroup
import json
import requests
import socket
import soco
import sys
import time
import xml.dom.minidom

usage_text = """\
commands:
    list [<interface address>]
    pair <left/master> <right/slave>
    unpair <left/master>\
"""

request_address_format = "http://{}:1400/DeviceProperties/Control"

pair_payload_format = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
    "<s:Body>"
    '<u:AddBondedZones xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1">'
    "<ChannelMapSet>{}:LF,LF;{}:RF,RF</ChannelMapSet>"
    "</u:AddBondedZones>"
    "</s:Body>"
    "</s:Envelope>"
)

unpair_payload_format = (
    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
    "<s:Body>"
    '<u:RemoveBondedZones xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1">'
    "<ChannelMapSet></ChannelMapSet>"
    "</u:RemoveBondedZones>"
    "</s:Body>"
    "</s:Envelope>"
)

pair_soap_action = "urn:schemas-upnp-org:service:DeviceProperties:1#AddBondedZones"
unpair_soap_action = "urn:schemas-upnp-org:service:DeviceProperties:1#RemoveBondedZones"

def prettify_xml(xml_string) -> str:
    """Prettify XML"""
    dom = xml.dom.minidom.parseString(xml_string)
    return dom.toprettyxml()

@click.group(
    cls=ClickAliasedGroup, context_settings=dict(help_option_names=["-h", "--help"])
)
def main_cli() -> None:
    """A CLI tool to pair and unpair Sonos devices"""
    pass


def get_ni_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    return s.getsockname()[0]


@main_cli.command(aliases=["list", "ls"])
def list_socos(interface_addr=None) -> None:
    """List Sonos devices on the network"""
    start_time = time.perf_counter()
    if interface_addr is None:
        try:
            interface_addr = get_ni_ip()
            click.secho(
                f"\nFetched Network Interface IP: {interface_addr}\n", fg="cyan"
            )
        except:
            pass
    devs = soco.discover(interface_addr=interface_addr)
    for dev in devs:
        d = dev.ip_address
        ip = dev.ip_address
        name = dev.player_name
        household_id = dev.household_id
        click.secho(f"IP: {ip}, Name: {name}, Household ID {household_id}\n", fg="cyan")
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(f"Finished {sys._getframe().f_code.co_name} in {run_time:.4f} secs")


@main_cli.command(name="pair")
@click.argument("master_ip")
@click.argument("slave_ip")
def pair_socos(master_ip, slave_ip) -> None:
    """
    Arguments to pass: - MASTER_IP, SLAVE_IP
    """
    l_soco = soco.SoCo(master_ip)
    r_soco = soco.SoCo(slave_ip)

    l_uid = l_soco.uid
    r_uid = r_soco.uid

    req_addr = request_address_format.format(master_ip)
    req_headers = {
        "Content-Type": "application/xml",
        "SOAPAction": pair_soap_action,
    }
    req_payload = pair_payload_format.format(l_uid, r_uid)
    response = requests.post(req_addr, data=req_payload, headers=req_headers)

    if response.status_code != 200:
        click.secho("Failed to pair", fg="red")
        xml_string = prettify_xml(response.text)
        click.secho(xml_string, fg="red")


@main_cli.command(name="unpair")
@click.argument("master_ip")
def unpair_socos(master_ip) -> None:
    """
    Arguments to pass: - MASTER_IP
    """
    req_addr = request_address_format.format(master_ip)
    req_headers = {
        "Content-Type": "application/xml",
        "SOAPAction": unpair_soap_action,
    }
    req_payload = unpair_payload_format

    response = requests.post(req_addr, data=req_payload, headers=req_headers)

    if response.status_code != 200:
        click.secho("Failed to unpair", fg="red")
        xml_string = prettify_xml(response.text)
        click.secho(xml_string, fg="red")


if __name__ == "__main__":
    main_cli()
