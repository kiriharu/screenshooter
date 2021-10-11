# Screenshooter - site screenshoter as service 

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
* Token auth (set in .env)

## Endpoints:
Screenshooter has a single POST endpoint - /screenshot.  
You need to pass `url` in query and `x-token` header to make screenshot.  
For other values you can set `DOCS_URL=/docs` to .env and get docs in /docs endpoint

Default response looks like:
```json
{
  "url": "data/-2881154151398968169.jpeg",
  "ttl": 99
}
```

## Install
1. Clone repo:  
`git clone https://github.com/kiriharu/screenshooter`
2. Copy .env.example to .env and edit
3. Up and build with docker-compose:  
`docker-compose up -d --build`