# tap-syncro Configuration

This document describes the configuration options for the tap-syncro Singer tap, which extracts data from the Syncro MSP API.

## Config Options

### Authentication

#### `auth_token` (string, required)
The API token used to authenticate against the Syncro API. This value is treated as secret and should not be logged or exposed.
- **Example**: `"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

#### `subdomain` (string, optional)
Your Syncro account subdomain. Used to build the API base URL: `https://{subdomain}.syncromsp.com/api/v1`.
- **Default**: `"demo"`
- **Example**: `"your-subdomain"` or `"acme-msp"`

### API Configuration

#### `page_size` (number, optional)
Number of records to request per page for paginated API calls. When omitted, the API uses its default page size. On gateway timeouts (504), the tap may automatically reduce this value and retry.
- **Example**: `100` or `50`

#### `user_agent` (string, optional)
Custom User-Agent string sent in HTTP requests to Syncro. Syncro may require a identifiable user agent.
- **Default**: `"hotglue (support@hotglue.xyz)"`
- **Example**: `"tap-syncro/1.0.0"` or `"my-org-syncro-tap/1.0"`

---

## Example: Minimal config

Only required options (auth_token). Other options use defaults.

```json
{
  "auth_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

---

## Example: Complete config

All supported options with sample values.

```json
{
  "auth_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subdomain": "your-subdomain",
  "page_size": 100,
  "user_agent": "tap-syncro/1.0.0"
}
```
