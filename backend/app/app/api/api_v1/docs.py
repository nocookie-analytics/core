from fastapi import APIRouter
from starlette.responses import HTMLResponse

docs_router = APIRouter()

description = """
## Javascript snippet

Integrate No Cookie Analytics on your website with a simple snippet. Add this script tag on your page and you're good to go:

```javascript
 <script async defer src="https://nocookieanalytics.com/latest.js"></script>
```

That's it! You can now track your visitors on your website.

Notes:

* Make sure you add a domain to your profile in the No Cookie Analytics dashboard.
* This snippet tracks your website visitors. Also across page navigations in Single Page Applications (SPA) and web apps.
* Want to track custom events? Read on ahead.

### Custom events

Use the `nca_event` function to track custom events. It's injected by the Javascript snippet into the global context.

```javascript
 // Track a custom event
 nca_track('order_placed'); // Defaults to a numeric value of 1

 nca_track('order_value', 19.25);

 ```


 ## OpenAPI schema

 The OpenAPI schema for No Cookie Analytics is available at [this URL](/api/v1/openapi.json)


 ## Custom backend integrations

You can use No Cookie Analytics to integrate with your own services using this API documentation.
"""


@docs_router.get(
    "/docs",
    include_in_schema=False,
)
async def get_documentation():
    return HTMLResponse(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>No Cookie Analytics - Documentation</title>
            <!-- Embed elements Elements via Web Component -->
            <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
            <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
          </head>
          <body>

            <elements-api
              apiDescriptionUrl="/api/v1/openapi.json"
              router="hash"
              layout="sidebar"
              logo="/img/logo.png"
            />

          </body>
          <script type="text/javascript">

          function replaceDomain() {
            var reportServer = window.location.hostname;
            var elm = document.querySelector('.sl-code-viewer');
            if (elm) {
                elm.innerHTML = elm.innerHTML.replace('nocookieanalytics.com', reportServer);
            } else {
                setTimeout(replaceDomain, 500);
            }
          }

          document.addEventListener('DOMContentLoaded', replaceDomain);
            </script>

          <script async defer src="/latest.js"></script>
        </html>
    """
    )
