# Screenshooter - screenshot as a service.

Screenshooter is a simple service that just makes screenshot of provided url.

Built with pyppeteer and FastAPI.

## Supports:
* All pictures will be created in data dir, you can setup reverse proxy (like nginx) to serve pics.
* Caching with ttl
* List of restricted urls
* Enable/disable javascript
* Set useragent
* Set cookies
* Jpeg/Png format
* Configure some viewport settings (width, height, isMobile, deviceScaleFactor, isLandscape)

## Endpoints:
Screenshooter has a single POST endpoint - /screenshot

## Errors:
422 http code on missing required params. Detail will show default FastAPI value_error.missing

Example:  
POST http://127.0.0.1:8000/screenshot

Response:
```json
{
  "detail": [
    {
      "loc": [
        "query",
        "url"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
TODO more errors