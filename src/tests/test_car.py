# # pylint: disable=redefined-outer-name
from typing import TypedDict
import pytest
from httpx import AsyncClient


class CarDict(TypedDict):
    name: str
    color: str
    price: str
    manufacturer_name: str

@pytest.fixture
def sample_car():
    return {
        'name': 'test-car',
        'color': 'red',
        'price': '3000.00',
        'manufacturer_name': 'test-manufacturer'
    }

@pytest.fixture
def sample_car2():
    return {
        'name': 'test-car-2',
        'color': 'blue', 
        'price': '4000.00',
        'manufacturer_name': 'test-manufacturer-two'
    }


class TestCarCreate:
    @pytest.mark.asyncio
    async def test_create_car(
        self,
        client : AsyncClient,
        sample_car: CarDict
    ):
        response = await client.post('/cars', json=sample_car)
        data = response.json()
        assert response.status_code == 201
        assert data['name'] == sample_car['name']
        assert data['color'] == sample_car['color']
        assert data['price'] == sample_car['price']
        assert data['manufacturer_name'] == sample_car['manufacturer_name']
        assert 'id' in data


    @pytest.mark.asyncio
    async def test_create_car_uppercase_conversion(self, client: AsyncClient):
        car_data = {
            'name': 'TEST-CAR',
            'color': 'RED',
            'price': '35000.00',
            'manufacturer_name': 'TEST-MANUFACTURER'
        }
        response = await client.post('/cars', json=car_data)
        data = response.json()
        assert response.status_code == 201
        assert data['name'] == "test-car"
        assert data['color'] == "red"
        assert data['manufacturer_name'] == 'test-manufacturer'

        car_id = data['id']
        get_response = await client.get(f'/cars/{car_id}')
        get_data = get_response.json()
        assert get_response.status_code == 200
        assert get_data['name'] == "test-car"
        assert get_data['color'] == "red"
        assert get_data['manufacturer_name'] == 'test-manufacturer'

    @pytest.mark.asyncio
    async def test_create_car_with_new_manufacturer(self, client: AsyncClient, sample_car: CarDict):
        post_response = await client.post('/cars', json=sample_car)
        post_data = post_response.json()
        manufacturer_id = post_data['manufacturer_id']

        get_response = await client.get(f'/manufacturers/{manufacturer_id}')
        get_data = get_response.json()
        assert get_response.status_code == 200
        assert get_data['name'] == sample_car['manufacturer_name']

    @pytest.mark.asyncio
    async def test_create_car_with_existing_manufacturer(
        self,
        client: AsyncClient,
        sample_car: CarDict,
        sample_car2: CarDict
    ):
        sample_car2['manufacturer_name'] = sample_car['manufacturer_name']
        await client.post('/cars', json=sample_car)
        post_response = await client.post('/cars', json=sample_car2)
        post_data = post_response.json()
        manufacturer_id = post_data['manufacturer_id']

        get_response = await client.get(f'/manufacturers/{manufacturer_id}')
        get_data = get_response.json()
        assert get_response.status_code == 200
        assert get_data['name'] == sample_car['manufacturer_name']


    @pytest.mark.asyncio
    async def test_create_car_invalid_name(self, client: AsyncClient):
        car_data = {
            'name': 'test@car',
            'color': 'red',
            'price': '30000.00',
            'manufacturer_name': 'test-manufacturer'
        }
        response = await client.post('/cars', json=car_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_car_invalid_color(self, client: AsyncClient):
        car_data = {
            'name': 'test-car',
            'color': 'red123',
            'price': '30000.00', 
            'manufacturer_name': 'test-manufacturer'
        }
        response = await client.post('/cars', json=car_data)
        assert response.status_code == 422


class TestCarRead:
    @pytest.mark.asyncio
    async def test_get_single_car(self, client: AsyncClient, sample_car: CarDict):
        post_response = await client.post('/cars', json=sample_car)
        car_id = post_response.json()['id']

        get_response = await client.get(f'/cars/{car_id}')
        data = get_response.json()
        assert get_response.status_code == 200
        assert data['id'] == car_id
        assert data['name'] == sample_car['name']
        assert data['manufacturer_name'] == sample_car['manufacturer_name']

    @pytest.mark.asyncio
    async def test_get_car_not_found(self, client: AsyncClient):
        response = await client.get('/cars/9999')
        data = response.json()
        assert response.status_code == 404
        assert data['detail'] == 'Car not found'

    @pytest.mark.asyncio
    async def test_get_all_cars(
        self,
        client: AsyncClient,
        sample_car: CarDict,
        sample_car2: CarDict
    ):
        await client.post('/cars', json=sample_car)
        await client.post('/cars', json=sample_car2)

        response = await client.get('/cars')
        data = response.json()
        print(f"All cars: {data}")
        assert response.status_code == 200
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_get_cars_filter_by_name(
        self,
        client: AsyncClient,
        sample_car: CarDict,
        sample_car2: CarDict
    ):
        await client.post('/cars', json=sample_car)
        await client.post('/cars', json=sample_car2)

        response = await client.get('/cars', params={'name': 'test-car'})
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == 'test-car'

    @pytest.mark.asyncio
    async def test_get_cars_filter_by_color(
        self,
        client: AsyncClient,
        sample_car: CarDict,
        sample_car2: CarDict
    ):
        await client.post('/cars', json=sample_car)
        await client.post('/cars', json=sample_car2)

        response = await client.get('/cars', params={'color': 'blue'})
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['color'] == 'blue'

    @pytest.mark.asyncio
    async def test_get_cars_filter_by_manufacturer(
        self,
        client: AsyncClient,
        sample_car: CarDict,
        sample_car2: CarDict
    ):
        await client.post('/cars', json=sample_car)
        await client.post('/cars', json=sample_car2)

        response = await client.get('/cars', params={'manufacturer': 'test-manufacturer'})
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['manufacturer_name'] == 'test-manufacturer'

    @pytest.mark.asyncio
    async def test_get_cars_multiple_filters(self, client: AsyncClient, sample_car: CarDict):
        await client.post('/cars', json=sample_car)

        response = await client.get('/cars', params={
            'name': 'test-car',
            'color': 'red',
            'manufacturer': 'test-manufacturer'
        })
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == 'test-car'
        assert data[0]['color'] == 'red'
        assert data[0]['manufacturer_name'] == 'test-manufacturer'


class TestCarUpdate:
    @pytest.mark.asyncio
    async def test_update_car(self, client: AsyncClient, sample_car: CarDict):
        post_response = await client.post('/cars', json=sample_car)
        car_id = post_response.json()['id']

        update_data = {
            'name': 'updated-car',
            'color': 'green',
            'price': '35000.00'
        }
        response = await client.put(f'/cars/{car_id}', json=update_data)
        data = response.json()
        assert response.status_code == 200
        assert data['id'] == car_id
        assert data['name'] == 'updated-car'
        assert data['color'] == 'green'
        assert data['price'] == '35000.00'

    @pytest.mark.asyncio
    async def test_update_car_manufacturer(self, client: AsyncClient, sample_car: CarDict):
        post_response = await client.post('/cars', json=sample_car)
        car_id = post_response.json()['id']

        update_data = {
            'manufacturer_name': 'new-manufacturer'
        }
        response = await client.put(f'/cars/{car_id}', json=update_data)
        data = response.json()
        assert response.status_code == 200
        assert data['manufacturer_name'] == 'new-manufacturer'

    @pytest.mark.asyncio
    async def test_update_car_partial(self, client: AsyncClient, sample_car: CarDict):
        post_response = await client.post('/cars', json=sample_car)
        car_id = post_response.json()['id']

        update_data = {
            "color": "black"
        }
        response = await client.put(f'/cars/{car_id}', json=update_data)
        data = response.json()
        assert response.status_code == 200
        assert data['color'] == 'black'
        assert data['name'] == sample_car['name']

    @pytest.mark.asyncio
    async def test_update_car_not_found(self, client: AsyncClient):
        update_data = {'name': 'updated'}
        response = await client.put('/cars/9999', json=update_data)
        data = response.json()
        assert response.status_code == 404
        assert data['detail'] == 'Car not found'


class TestCarDelete:
    @pytest.mark.asyncio
    async def test_delete_car(self, client: AsyncClient, sample_car: CarDict):
        post_response = await client.post('/cars', json=sample_car)
        car_id = post_response.json()['id']

        delete_response = await client.delete(f'/cars/{car_id}')
        delete_data = delete_response.json()
        assert delete_response.status_code == 200
        assert delete_data['message'] == 'deleted'

        get_response = await client.get(f'/cars/{car_id}')
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_car_not_found(self, client: AsyncClient):
        response = await client.delete('/cars/9999')
        data = response.json()
        assert response.status_code == 404
        assert data['detail'] == 'Car not found'
