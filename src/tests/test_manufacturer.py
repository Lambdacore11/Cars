# pylint: disable=redefined-outer-name
import pytest
from httpx import AsyncClient


@pytest.fixture
def sample_manufacturer():
    return {'name': 'testmanufacturer'}

@pytest.fixture
def sample_manufacturer2():
    return {'name': 'testmanufacturertwo'}


class TestManufacturerCreate:
    @pytest.mark.asyncio
    async def test_create_manufacturer(
        self,
        client: AsyncClient,
        sample_manufacturer: dict[str, str]
    ):
        response = await client.post('/manufacturers', json=sample_manufacturer)
        data = response.json()
        assert response.status_code == 201
        assert data['name'] == sample_manufacturer['name']
        assert 'id' in data

    @pytest.mark.asyncio
    async def test_create_manufacturer_uppercase_conversion(
        self,
        client: AsyncClient,
        sample_manufacturer: dict[str, str]
    ):
        response = await client.post(
            '/manufacturers',
            json={'name':sample_manufacturer['name'].upper()}
        )
        data = response.json()
        assert response.status_code == 201
        assert data['name'] == sample_manufacturer['name']
        assert 'id' in data

    @pytest.mark.asyncio
    async def test_create_manufacturer_invalid_name(self, client: AsyncClient):
        response = await client.post('/manufacturers', json={'name':'123456789'})
        data = response.json()
        assert response.status_code == 422
        assert data['detail'][0]['msg'] == "String should match pattern '^[a-zA-Z\\-]+$'"

    @pytest.mark.asyncio
    async def test_create_manufacturer_duplicate(
        self,
        client:AsyncClient,
        sample_manufacturer: dict[str, str]
    ):
        await client.post('/manufacturers', json=sample_manufacturer)
        response = await client.post(
            '/manufacturers',
            json={'name':sample_manufacturer['name'].upper()}
        )
        data = response.json()
        assert response.status_code == 400
        assert data['detail'] == 'Manufacturer with that name already exists'


class TestManufacturerGet:
    @pytest.mark.asyncio
    async def test_get_single_manufacturer(
        self,
        client: AsyncClient,
        sample_manufacturer: dict[str, str]
    ):
        post_response = await client.post('/manufacturers', json=sample_manufacturer)
        post_data = post_response.json()
        manufacturer_id = post_data['id']

        get_response = await client.get(f'/manufacturers/{manufacturer_id}')
        get_data = get_response.json()
        assert get_response.status_code == 200
        assert get_data['name'] == sample_manufacturer['name']

    @pytest.mark.asyncio
    async def test_get_single_manufacturer_not_found(self, client: AsyncClient):
        response = await client.get('/manufacturers/1')
        data = response.json()
        assert response.status_code == 404
        assert data['detail'] == 'Manufacturer not found'

    @pytest.mark.asyncio
    async def test_get_multiple_manufacturer(
        self,
        client: AsyncClient,
        sample_manufacturer: dict[str, str],
        sample_manufacturer2: dict[str, str]
    ):
        await client.post('/manufacturers', json=sample_manufacturer)
        await client.post('/manufacturers', json=sample_manufacturer2)

        response = await client.get('/manufacturers')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2


class TestManufacturerUpdate:
    @pytest.mark.asyncio
    async def test_update_manufacturer(
        self,
        client:AsyncClient,
        sample_manufacturer,
        sample_manufacturer2
    ):
        post_response = await client.post('/manufacturers', json=sample_manufacturer)
        post_data = post_response.json()
        manufacturer_id = post_data['id']
        put_response = await client.put(
            f'/manufacturers/{manufacturer_id}',
            json=sample_manufacturer2
        )
        put_data = put_response.json()
        assert put_response.status_code == 200
        assert put_data['id'] == manufacturer_id
        assert put_data['name'] == sample_manufacturer2['name']


class TestManufacturerDelete:
    @pytest.mark.asyncio
    async def test_update_manufacturer(
        self,
        client: AsyncClient,
        sample_manufacturer: dict[str, str]
    ):
        post_response = await client.post('/manufacturers', json=sample_manufacturer)
        post_data = post_response.json()
        manufacturer_id = post_data['id']

        delete_response = await client.delete(f'/manufacturers/{manufacturer_id}')
        delete_data = delete_response.json()
        assert delete_response.status_code == 200
        assert delete_data['message'] == 'deleted'

        get_response = await client.get(f'/manufacturers/{manufacturer_id}')
        get_data = get_response.json()
        assert get_response.status_code == 404
        assert get_data['detail'] == 'Manufacturer not found'
