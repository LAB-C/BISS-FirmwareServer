import os, sys, json
import pytest
from server import create_app
import logging

LOGGER = logging.getLogger(__name__)
def custom_log(text):
    LOGGER.info('-' * 20 + ' {} '.format(text) + '-' * 20)

@pytest.yield_fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))

async def test_fixture_get_devices(test_cli):
    ##### get devices #####
    custom_log('GET DEVICES')
    resp = await test_cli.get('/app/devices')
    devices = await resp.json()
    print(devices)
    assert type(devices) == list
    return devices

async def test_fixture_devices(test_cli):
    wallet = '0x75a59b94889a05c03c66c3c84e9d2f8308ca4abd'

    ##### register device #####
    custom_log('REGISTER DEVICE')
    resp = await test_cli.post('/app/register',
        headers = {
            'content-type': 'application/json'
        }, json={
            'name': 'TEST-0',
            'wallet': wallet
        })
    assert resp.status == 200

    ##### get device #####
    custom_log('GET DEVICE')
    resp = await test_cli.get('/app/devices/{}'.format(wallet))
    device = await resp.json()
    print(device)
    assert type(device) == dict

    devices = await test_fixture_get_devices(test_cli)
    assert device in devices
    
    ##### delete device #####
    custom_log('DELETE DEVICE')
    resp = await test_cli.delete('/app/devices/{}'.format(wallet))
    assert resp.status == 200

    devices = await test_fixture_get_devices(test_cli)
    assert device not in devices
