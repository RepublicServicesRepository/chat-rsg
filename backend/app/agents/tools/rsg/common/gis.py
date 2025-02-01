import json
import requests
import os
 
#code from flsk app
def address_lookup(addressLine1,addressLine2,city,state,zipCode):

    gis_api_host = os.environ.get('GIS_API_HOST')
    gis_api_key = os.environ.get('GIS_API_KEY')
    
    if addressLine2 == '':
        url = f'{gis_api_host}/v3/address/?Data.AddressLine1={addressLine1}&Data.City={city}&Data.Zipcode={zipCode}&Data.State={state}'
    else:
        url = f'{gis_api_host}/v3/address/?Data.AddressLine1={addressLine1}&Data.AddressLine2={addressLine2}&Data.City={city}&Data.Zipcode={zipCode}&Data.State={state}'

    headers = {
        'api-key': gis_api_key
    }
    try:
        response = requests.get(url, headers = headers)
        return response.json() 
    except requests.exceptions.RequestException as e:
        print('Response type: ', type(requests.get(url, headers = headers)))
        print(f'Request failed with error: {e}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
                
## get the polygon and division info from the lat/long  
def get_gis_data(lat,long):
    gis_api_host = os.environ.get('GIS_API_HOST')
    gis_api_key = os.environ.get('GIS_API_KEY')
    headers = {
       'api-key': gis_api_key
    }
    lat_long_url = f'{gis_api_host}/v1/gis/availableservices/{lat}/{long}?caller=&geocodestatus=&matchcode=&addressdoctorhash'
    try:
        response = requests.get(lat_long_url, headers = headers, timeout=5)
        try:
            json.loads(response.text)
            return response.json()
        except json.JSONDecodeError:
            print('Response is not JSON. Error finding location.')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Request failed with error: {e}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

## get polygon information from the gis data based on lob
def resi_poly(polygon):
    data = polygon['data']
    polygon, lawson_div, infopro_div = '', '', ''
    noInfo = True
    for d in data:
        if 'Resi' in d['serviceAreaType'] and 'Trash' in d['serviceAreaType']:
            polygon, lawson_div, infopro_div = d['polygonId'], d['lawsonDiv'], d['infoproDiv']
            noInfo = False
            break
    if noInfo:
        raise ValueError('No polygon found.')
    
    return [str(polygon), str(lawson_div), str(infopro_div)]

def get_poly(address_dict,lob):   

    lobs_dict = {'residential':['Residential', resi_poly]} #add others later
    result = address_lookup(address_dict['address'],None,address_dict['city'],address_dict['state'],address_dict['zip']) 
    if 'Output' in result:
        lat = result['Output'][0]['Latitude']
        long = result['Output'][0]['Longitude']
    
        gis_data = get_gis_data(lat,long)
      
        if gis_data is None:
            raise ValueError('Error finding location.')
        else:
            ## logic to identify correct infopro/lawson division and polygon
            if lob is not None:
                poly_func = lobs_dict.get(lob)[1]
                response_list = poly_func(gis_data)
                polygon, lawsondiv, infoprodiv = response_list[0], response_list[1], response_list[2]
                ## identify prompts based on polygon and divisions
                if polygon == '':
                    raise ValueError('No polygon found.')
                return {
                    'polygonId': polygon,
                    'lawsonDivision': lawsondiv,
                    'infoproDivision': infoprodiv
                }
            else:
                lawsondiv, infoprodiv = (gis_data["data"][0]["lawsonDiv"],gis_data["data"][0]["infoproDiv"])
                return {
                    'polygonId': 'NA',
                    'lawsonDivision': lawsondiv,
                    'infoproDivision': infoprodiv
                }                       
    else:
        raise ValueError('Address not found.')
    
    