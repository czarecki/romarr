# BlueRoms magnet resolution

BlueRoms changed its download page from an anchor containing a literal magnet
URI to a button whose `data-link` attribute contains the magnet encoded as
Base64. Prowlarr 2.5.2 still expects the old anchor and returns HTTP 500 when
its proxied download URL is fetched.

ROMarr will resolve only BlueRoms results while processing Prowlarr search
responses. It will fetch the result's direct BlueRoms `guid`, accept only the
official HTTPS host and `/download/` path, parse the `magnet-button`, decode
`data-link`, and replace the unusable proxied URL with the literal magnet.
Failures remain isolated to that release and retain the normal Prowlarr
fallback. No other indexer or download client behavior changes.

The change is covered by a regression test using the current BlueRoms HTML
shape and by safety tests for malformed data and untrusted URLs. Deployment
uses a local Docker image patch and keeps the existing UI correction.
